"""[optimize] (2026-11-15) dead-CSS removal for the built style.css, by static proof only.

A style rule is removed when EVERY one of its selectors needs a class or an id that appears nowhere in index.html (its markup
and the card data) or app.js — not as a word in any string, not behind a dynamic prefix the code builds ("thm-" + x, `pg-${x}`).
Such a rule can never match anything. Negations (:not(...)) never count as needs; :is() / :where() / :has() need at least one
possible alternative. Attribute and type selectors are always possible. Then: @keyframes no animation names, @media / @supports
blocks left empty, and custom properties (--x) defined but read nowhere (no var(--x) in CSS, no "--x" in the code) go too.
@font-face rules are kept unless their family is used nowhere.

prune(css, html, js) -> (css, report); run alone: python -I -X utf8 css_prune.py <dist> (prints the report, writes nothing).
"""
import re, sys, pathlib

WORD = r"(?<![\w-])%s(?![\w-])"


def tokenize_blocks(css: str):
    """yield (prelude, body_or_None, start, end) for each top-level statement; strings and comments respected"""
    i, n = 0, len(css)
    out = []
    while i < n:
        # skip whitespace and comments
        j = i
        while j < n:
            if css.startswith("/*", j):
                k = css.find("*/", j + 2)
                j = n if k < 0 else k + 2
            elif css[j].isspace():
                j += 1
            else:
                break
        if j >= n:
            out.append(("", None, i, n, css[i:n]))   # trailing whitespace / comments
            break
        lead = css[i:j]
        # read a prelude up to '{' or ';' at depth 0
        k, depth, q = j, 0, None
        while k < n:
            c = css[k]
            if q:
                if c == "\\": k += 2; continue
                if c == q: q = None
            elif c in "\"'": q = c
            elif css.startswith("/*", k):
                e = css.find("*/", k + 2); k = n if e < 0 else e + 2; continue
            elif c in "([": depth += 1
            elif c in ")]": depth -= 1
            elif depth == 0 and c in "{;":
                break
            k += 1
        if k >= n:
            out.append((css[j:n], None, i, n, lead)); break
        if css[k] == ";":
            out.append((css[j:k + 1], None, i, k + 1, lead)); i = k + 1; continue
        # matching '}'
        m, d, q = k + 1, 1, None
        while m < n and d:
            c = css[m]
            if q:
                if c == "\\": m += 2; continue
                if c == q: q = None
            elif c in "\"'": q = c
            elif css.startswith("/*", m):
                e = css.find("*/", m + 2); m = n if e < 0 else e + 2; continue
            elif c == "{": d += 1
            elif c == "}": d -= 1
            m += 1
        out.append((css[j:k], css[k + 1:m - 1], i, m, lead))
        i = m
    return out


def split_top(s: str, sep=","):
    parts, depth, q, cur = [], 0, None, []
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            cur.append(c)
            if c == "\\" and i + 1 < len(s): cur.append(s[i + 1]); i += 2; continue
            if c == q: q = None
        elif c in "\"'": q = c; cur.append(c)
        elif c in "([": depth += 1; cur.append(c)
        elif c in ")]": depth -= 1; cur.append(c)
        elif c == sep and depth == 0: parts.append("".join(cur)); cur = []
        else: cur.append(c)
        i += 1
    parts.append("".join(cur))
    return parts


def strip_comments(s): return re.sub(r"/\*.*?\*/", "", s, flags=re.S)


class Presence:
    def __init__(self, html: str, js: str):
        self.text = html + "\n" + js
        self.tokens = set(re.findall(r"[A-Za-z0-9_-]+", self.text))   # a class / id "appears" = it is one of these whole words
        self.cache = {}
        # classes the code builds: the last word of ANY string literal / template chunk that runs into a concatenation or a ${...}
        # is a prefix ('<div class="stp-stamp s' + k -> "s" -> s0, s1; `pg-${x}` -> "pg-"), the first word of one that follows a
        # concatenation or a ${...} a suffix (x + "-on")
        pre, suf = set(), set()
        for m in re.finditer(r'''(["'`])((?:\\.|(?!\1)[^\\\n])*)\1\s*\+''', js):
            t = re.search(r"([A-Za-z_][\w-]*)$", m.group(2))
            if t: pre.add(t.group(1))
        for m in re.finditer(r"([A-Za-z_][\w-]*)\$\{", js):
            pre.add(m.group(1))
        for m in re.finditer(r"\+\s*[\"'`]([\w-]+)", js):
            suf.add(m.group(1))
        for m in re.finditer(r"\}([\w-]+)", js):
            suf.add(m.group(1))
        # a prefix ending in - or _ protects any continuation; a bare word only a numeric one ("b" + k -> b1, b2)
        self.sep_prefixes = sorted(p for p in pre if p[-1] in "-_")
        self.word_prefixes = sorted(p for p in pre if p[-1] not in "-_")
        self.suffixes = sorted(s for s in suf if s[0] in "-_" and len(s) >= 3)

    def has(self, token: str) -> bool:
        if token in self.cache: return self.cache[token]
        ok = token in self.tokens
        if not ok: ok = any(token.startswith(p) and len(token) > len(p) for p in self.sep_prefixes)
        if not ok: ok = any(token.startswith(p) and token[len(p):].isdigit() for p in self.word_prefixes)
        if not ok: ok = any(token.endswith(s) and len(token) > len(s) for s in self.suffixes)
        self.cache[token] = ok
        return ok


PSEUDO_GROUP = re.compile(r":(not|is|where|has|matches|-webkit-any|host|host-context|nth-child|nth-last-child)\(")


def selector_possible(sel: str, P: Presence) -> bool:
    s = sel.strip()
    if not s: return True
    # resolve functional pseudo-classes, innermost first
    while True:
        m = PSEUDO_GROUP.search(s)
        if not m: break
        start = m.end()
        d, k = 1, start
        while k < len(s) and d:
            if s[k] == "(": d += 1
            elif s[k] == ")": d -= 1
            k += 1
        inner = s[start:k - 1]
        name = m.group(1)
        if name in ("not", "nth-child", "nth-last-child"):
            repl = ""                                               # never a need
        else:
            alts = split_top(inner)
            repl = "" if any(selector_possible(a, P) for a in alts) else ".__never_present__"
        s = s[:m.start()] + repl + s[k:]
    s = re.sub(r"\[[^\]]*\]", "", s)                                # attribute selectors: always possible
    s = re.sub(r"::?[\w-]+", "", s)                                 # remaining pseudo-classes / elements
    for c in re.findall(r"\.(-?[_A-Za-z][\w-]*)", s):
        if c == "__never_present__" or not P.has(c): return False
    for i in re.findall(r"#(-?[_A-Za-z][\w-]*)", s):
        if not P.has(i): return False
    return True


def prune(css: str, html: str, js: str):
    P = Presence(html, js)
    report = {"rules_removed": 0, "bytes_removed": 0, "examples": [], "removed_selectors": [], "keyframes_removed": [], "vars_removed": [], "fontfaces_removed": []}

    def walk(text):
        out = []
        for prelude, body, a, b, lead in tokenize_blocks(text):
            if body is None:
                out.append(text[a:b]); continue
            p = strip_comments(prelude).strip()
            pl = p.lower()
            if pl.startswith(("@media", "@supports", "@layer", "@container", "@document")):
                inner = walk(body)
                if strip_comments(inner).strip():
                    out.append(lead + prelude + "{" + inner + "}")
                else:
                    report["bytes_removed"] += b - a
                continue
            if pl.startswith("@"):
                out.append(text[a:b]); continue                     # @keyframes / @font-face / @page: decided below
            sels = split_top(p)
            if all(not selector_possible(s, P) for s in sels):
                report["rules_removed"] += 1; report["bytes_removed"] += b - a
                if len(report["examples"]) < 40: report["examples"].append(p[:120])
                report["removed_selectors"].append(" ".join(p.split()))
                out.append(lead if "/*" in lead else "")
                continue
            out.append(text[a:b])
        return "".join(out)

    css2 = walk(css)
    # @keyframes nobody animates with
    names = set(re.findall(r"@(?:-webkit-)?keyframes\s+([\w-]+)", css2))
    used_text_css = re.sub(r"@(?:-webkit-)?keyframes\s+[\w-]+", "", css2)
    for nm in sorted(names):
        if re.search(WORD % re.escape(nm), used_text_css) or re.search(WORD % re.escape(nm), js) or re.search(WORD % re.escape(nm), html):
            continue
        before = len(css2)
        css2 = _drop_at_block(css2, re.compile(r"@(?:-webkit-)?keyframes\s+" + re.escape(nm) + r"\s*\{"))
        report["keyframes_removed"].append(nm); report["bytes_removed"] += before - len(css2)
    # custom properties defined but never read
    defined = set(re.findall(r"(?<![\w-])(--[\w-]+)\s*:", css2))
    for v in sorted(defined):
        reads = len(re.findall(r"var\(\s*" + re.escape(v) + r"(?![\w-])", css2))
        if reads or re.search(WORD % re.escape(v), js) or re.search(WORD % re.escape(v), html):
            continue
        before = len(css2)
        css2 = _drop_decl(css2, v)
        report["vars_removed"].append(v); report["bytes_removed"] += before - len(css2)
    # @font-face of a family no rule or code uses
    for m in list(re.finditer(r"@font-face\s*\{", css2)):
        pass
    fams = set(m.group(1) for m in re.finditer(r"@font-face\s*\{[^}]*?font-family:\s*['\"]?([^;'\"}]+)", css2))
    rest = re.sub(r"@font-face\s*\{[^}]*\}", "", css2)
    for f in sorted(fams):
        if f in rest or f in js:
            continue
        before = len(css2)
        css2 = re.sub(r"@font-face\s*\{[^}]*font-family:\s*['\"]?" + re.escape(f) + r"['\"]?\s*;[^}]*\}", "", css2)
        report["fontfaces_removed"].append(f); report["bytes_removed"] += before - len(css2)
    return css2, report


def _drop_at_block(css, pat):
    out, pos = [], 0
    for m in list(pat.finditer(css)):
        if m.start() < pos: continue
        d, k = 1, m.end()
        while k < len(css) and d:
            if css[k] == "{": d += 1
            elif css[k] == "}": d -= 1
            k += 1
        out.append(css[pos:m.start()]); pos = k
    out.append(css[pos:])
    return "".join(out)


def _drop_decl(css, var):
    # remove `--var: value;` (value may hold parentheses / strings); keep the rest of the block
    pat = re.compile(r"(?<![\w-])" + re.escape(var) + r"\s*:")
    out, pos = [], 0
    for m in pat.finditer(css):
        if m.start() < pos: continue
        k, depth, q = m.end(), 0, None
        while k < len(css):
            c = css[k]
            if q:
                if c == q: q = None
            elif c in "\"'": q = c
            elif c == "(": depth += 1
            elif c == ")": depth -= 1
            elif depth == 0 and c in ";}":
                break
            k += 1
        end = k + 1 if k < len(css) and css[k] == ";" else k
        out.append(css[pos:m.start()]); pos = end
    out.append(css[pos:])
    return "".join(out)


if __name__ == "__main__":
    d = pathlib.Path(sys.argv[1])
    css = (d / "style.css").read_text(encoding="utf-8")
    html = (d / "index.html").read_text(encoding="utf-8")
    js = (d / "app.js").read_text(encoding="utf-8")
    new, rep = prune(css, html, js)
    print(f"style.css {len(css)} -> {len(new)} chars; rules removed {rep['rules_removed']}; keyframes {len(rep['keyframes_removed'])}; vars {len(rep['vars_removed'])}; font faces {rep['fontfaces_removed']}")
    for e in rep["examples"]: print("  rule:", e)
    print("  keyframes:", rep["keyframes_removed"][:60])
    print("  vars:", rep["vars_removed"][:60])
