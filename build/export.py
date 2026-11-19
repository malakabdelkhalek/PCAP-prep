import json, importlib, sys, re
sys.path.insert(0, '.')
import lib
out = []
for i in range(1, 7):
    m = importlib.import_module(f"nb{i}")
    nb = m.nb
    secs = []
    for s in nb.sections:
        html = "".join(h for h in s["html"] if "class='chapter'" not in h and 'class="chapter"' not in h)
        secs.append({"title": re.sub(r"<[^>]+>", "", s["title"]), "html": html, "asks": s["asks"]})
    tests = []
    for title, items in nb.tests:
        for (q, code, a, exp) in items:
            tests.append({"q": q, "code": code.strip() if code else None, "out": exp.strip("\n") if exp is not None else None, "ans": a})
    out.append({"num": i, "title": re.sub(r"&amp;", "&", nb.title), "sections": secs, "selftest": tests})
lib.finish()
json.dump(out, open("../app/notebooks.json", "w"))
for c in out:
    print(c["num"], c["title"], len(c["sections"]), sum(len(s["asks"]) for s in c["sections"]), len(c["selftest"]))
