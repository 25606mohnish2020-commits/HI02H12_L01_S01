"""[optimize] (2026-11-15) dead-code removal for the built app.js: features no data uses.

1. Slide modules: the engine (the shared Ek-aur-Anek engine) carries ~75 slide types; this card uses a handful. A module stays when
   the card has a slide of its type, or a kept module / kept alias names it (PUNCT_PICK -> PUNCT_SCENE / PUNCT_DEMO, ...). The rest
   of the SlideModules entries go, with their alias lines (SlideModules.X = SlideModules.Y for types the card does not use).
2. Top-level functions: a `function name(` whose name then appears nowhere else in app.js or index.html (no call, no reference,
   no typeof test, no string) can never run: removed, repeatedly, until nothing more goes.
Block ends are found with a JavaScript-aware scanner (strings, template literals with ${}, comments, regular expressions).
prune(js, html) -> (js, report); run alone: python -I -X utf8 js_prune.py <dist> (prints the report, writes nothing).
"""
import json, re, sys, pathlib

REGEX_PREV = set("(,=:[!&|?{};+-*%<>~^")
REGEX_KW = {"return", "typeof", "case", "do", "else", "in", "of", "void", "delete", "throw", "new", "instanceof", "yield", "await"}


def _str_end(s, i):
    q, j, n = s[i], i + 1, len(s)
    while j < n:
        c = s[j]
        if c == "\\": j += 2; continue
        if c == q: return j + 1
        if c == "\n": raise ValueError(f"newline in string at {i}")
        j += 1
    raise ValueError("unterminated string")


def _regex_end(s, i):
    j, n, cls = i + 1, len(s), False
    while j < n:
        c = s[j]
        if c == "\\": j += 2; continue
        if c == "\n": raise ValueError(f"newline in regex at {i}")
        if cls:
            if c == "]": cls = False
        elif c == "[": cls = True
        elif c == "/":
            j += 1
            while j < n and (s[j].isalnum() or s[j] == "_"): j += 1
            return j
        j += 1
    raise ValueError("unterminated regex")


def _template_end(s, i):
    j, n = i + 1, len(s)
    while j < n:
        c = s[j]
        if c == "\\": j += 2; continue
        if c == "`": return j + 1
        if c == "$" and j + 1 < n and s[j + 1] == "{":
            j = _code_end(s, j + 1)            # past the matching }
            continue
        j += 1
    raise ValueError("unterminated template")


def _code_end(s, i):
    """s[i] == '{': index just past its matching '}'"""
    assert s[i] == "{"
    depth, j, n, prev, word = 0, i, len(s), "{", ""
    while j < n:
        c = s[j]
        if c in "\"'":
            j = _str_end(s, j); prev, word = "a", ""; continue
        if c == "`":
            j = _template_end(s, j); prev, word = "a", ""; continue
        if s.startswith("//", j):
            k = s.find("\n", j); j = n if k < 0 else k; continue
        if s.startswith("/*", j):
            k = s.find("*/", j + 2); j = n if k < 0 else k + 2; continue
        if c == "/" and (prev in REGEX_PREV or word in REGEX_KW):
            j = _regex_end(s, j); prev, word = "a", ""; continue
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: return j + 1
        if c.isalnum() or c in "_$":
            word = (word + c) if (prev.isalnum() or prev in "_$") else c
            prev = c
        elif not c.isspace():
            prev, word = c, ""
        j += 1
    raise ValueError("unbalanced braces")


def _word(name):
    return re.compile(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])")


def strip_js_comments(s):
    """the code with every // and /* */ comment blanked (strings, template literals and regular expressions kept)"""
    out, j, n, prev, word, last = [], 0, len(s), "{", "", 0
    while j < n:
        c = s[j]
        if c in "\"'":
            j = _str_end(s, j); prev, word = "a", ""; continue
        if c == "`":
            j = _template_end(s, j); prev, word = "a", ""; continue
        if s.startswith("//", j):
            k = s.find("\n", j); k = n if k < 0 else k
            out.append(s[last:j]); last = k; j = k; continue
        if s.startswith("/*", j):
            k = s.find("*/", j + 2); k = n if k < 0 else k + 2
            out.append(s[last:j]); out.append(" "); last = k; j = k; continue
        if c == "/" and (prev in REGEX_PREV or word in REGEX_KW):
            j = _regex_end(s, j); prev, word = "a", ""; continue
        if c.isalnum() or c in "_$":
            word = (word + c) if (prev.isalnum() or prev in "_$") else c
            prev = c
        elif not c.isspace():
            prev, word = c, ""
        j += 1
    out.append(s[last:])
    return "".join(out)


def remove_modules(js, html, report):
    card = json.loads(re.search(r'<script type="application/json" id="cardData">(.*?)</script>', html, re.S).group(1))
    used_types = {s["type"] for s in card["slides"]}
    m0 = re.search(r"^const SlideModules = \{\n", js, re.M)
    if not m0: raise SystemExit("[js_prune] no SlideModules object")
    obj_open = m0.end() - 2                                   # the '{'
    obj_close = _code_end(js, obj_open)                       # past its '}'
    body = js[obj_open + 1: obj_close - 1]
    entries, pos = [], 0
    for m in re.finditer(r"^  ([A-Z][A-Z0-9_]+): *\{", body, re.M):
        if m.start() < pos: continue                          # inside a previous entry
        a = m.start(); brace = m.end() - 1
        b = _code_end(body, brace)
        k = b
        while k < len(body) and body[k] in " \t": k += 1
        if k < len(body) and body[k] == ",": k += 1
        while k < len(body) and body[k] in " \t": k += 1
        if k < len(body) and body[k] == "\n": k += 1
        entries.append((m.group(1), a, k)); pos = k
    names = [e[0] for e in entries]
    text_of = {n: body[a:b] for n, a, b in entries}
    after = js[obj_close:]
    alias = re.findall(r"^SlideModules\.([A-Z][A-Z0-9_]+)\s*=\s*([^;\n]*);", after, re.M)
    keep = set(n for n in used_types if n in text_of)
    alias_keep = set(t for t, _ in alias if t in used_types)
    changed = True
    while changed:
        changed = False
        texts = [text_of[n] for n in keep] + [rhs for t, rhs in alias if t in alias_keep]
        for n in names:
            if n in keep: continue
            if any(_word(n).search(t) for t in texts):
                keep.add(n); changed = True
    keep.add("CELEBRATION") if "CELEBRATION" in text_of else None
    drop = [n for n in names if n not in keep]
    new_body, last = [], 0
    for n, a, b in entries:
        if n in drop:
            new_body.append(body[last:a]); last = b
    new_body.append(body[last:])
    js2 = js[:obj_open + 1] + "".join(new_body) + js[obj_close - 1:]
    # alias lines for types the card does not use, pointing at dropped modules
    def alias_line(m):
        t, rhs = m.group(1), m.group(2)
        if t in used_types: return m.group(0)
        refs = re.findall(r"SlideModules\.([A-Z][A-Z0-9_]+)", rhs)
        if refs and all(r in drop for r in refs): return ""
        return m.group(0)
    js2 = re.sub(r"^SlideModules\.([A-Z][A-Z0-9_]+)\s*=\s*([^;\n]*);[^\n]*\n", alias_line, js2, flags=re.M)
    report["modules_kept"] = sorted(keep)
    report["modules_removed"] = drop
    report["module_bytes_removed"] = len(js) - len(js2)
    return js2


def remove_dead_functions(js, html, report):
    removed = []
    for _ in range(30):                                       # passes: a function only a removed one called goes in the next pass
        cuts = []
        for m in re.finditer(r"^function ([A-Za-z_$][\w$]*)\s*\(", js, re.M):
            name = m.group(1)
            brace = js.find("{", m.end())
            try:
                end = _code_end(js, brace)
            except ValueError:
                continue
            if cuts and m.start() < cuts[-1][1]: continue
            rest = js[:m.start()] + js[end:]
            if _word(name).search(rest) or _word(name).search(html):
                continue
            k = end + 1 if end < len(js) and js[end] == "\n" else end
            cuts.append((m.start(), k, name))
        if not cuts: break
        for a, b, name in reversed(cuts):
            js = js[:a] + js[b:]
            removed.append((name, b - a))
    report["functions_removed"] = removed
    return js


def prune(js, html):
    report = {}
    n0 = len(js)
    js = remove_modules(js, html, report)
    js = remove_dead_functions(js, html, report)
    report["bytes_removed"] = n0 - len(js)
    return js, report


if __name__ == "__main__":
    d = pathlib.Path(sys.argv[1])
    js = (d / "app.js").read_text(encoding="utf-8")
    html = (d / "index.html").read_text(encoding="utf-8")
    new, rep = prune(js, html)
    print(f"app.js {len(js)} -> {len(new)} chars ({rep['bytes_removed']} removed)")
    print("modules kept:", rep["modules_kept"])
    print("modules removed:", len(rep["modules_removed"]), rep["modules_removed"])
    print("functions removed:", len(rep["functions_removed"]), [f for f, _ in rep["functions_removed"]][:80])
