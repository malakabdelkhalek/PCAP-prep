"""Tiny notebook builder: write content in Python, every runnable THEY ASK snippet is
executed and its real output compared with the answer written in the notebook."""
import io, contextlib, html, textwrap, sys, os, tempfile

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@font-face{font-family:Hand;src:url(%(F)s/patrick-hand-latin-400-normal.woff2)}
@font-face{font-family:Head;font-weight:bold;src:url(%(F)s/kalam-latin-700-normal.woff2)}
@font-face{font-family:Head;font-weight:normal;src:url(%(F)s/kalam-latin-400-normal.woff2)}
@font-face{font-family:Mono;src:url(%(F)s/jetbrains-mono-latin-400-normal.woff2)}
@font-face{font-family:Mono;font-weight:bold;src:url(%(F)s/jetbrains-mono-latin-700-normal.woff2)}
@page{size:A4 landscape;margin:12mm 11mm 11mm 14mm;
 background:#fffdf6 url(%(H)s/bg.svg) no-repeat;background-size:297mm 210mm;
 @bottom-right{content:"p." counter(page);font-family:Hand;color:#999;font-size:9pt}
 @bottom-left{content:"%(FOOT)s";font-family:Hand;color:#aaa;font-size:8.5pt}}
html{font-family:Hand;font-size:10.8pt;color:#1f2a5a;line-height:1.3}
body{margin:0;column-count:2;column-gap:15mm;column-fill:auto}
h1{font-family:Head;color:#d8333a;font-size:24pt;line-height:1.1;margin:0 0 3px;text-decoration:underline;text-decoration-thickness:2px;column-span:all}
.sub{column-span:all;font-family:Head;color:#1f3c9a;font-size:12pt;margin:0 0 8px}
h2{font-family:Head;color:#fff;background:#d8333a;font-size:14pt;margin:12px 0 5px;padding:1px 8px;border-radius:4px;break-after:avoid;line-height:1.25}
h3{font-family:Head;color:#1f3c9a;font-size:12.2pt;margin:8px 0 2px;break-after:avoid;text-decoration:underline;text-decoration-color:#9fb4e6}
p{margin:3px 0}
ul,ol{margin:2px 0 4px;padding-left:16px} li{margin:1px 0}
b{color:#13205a}
.y{background:#fff07a;padding:0 2px}
.r{color:#d8333a;font-weight:bold}
.g{color:#1c8a4a;font-weight:bold}
code,.c{font-family:Mono;font-size:8.6pt;background:#eef1fa;padding:0 2px;border-radius:2px;color:#1f2a5a}
pre{font-family:Mono;font-size:8.3pt;line-height:1.32;background:#f4f6fc;border-left:3px solid #8aa0d8;margin:3px 0 5px;padding:4px 7px;white-space:pre-wrap;break-inside:avoid;color:#1b244d}
pre .cm{color:#7a869f}
.box{border:1.5px solid;border-radius:6px;padding:4px 8px 5px;margin:6px 0;break-inside:avoid}
.box .t{font-family:Head;font-weight:bold;font-size:10.5pt;margin-bottom:1px}
.heart{background:#fff7c2;border-color:#e4c200}.heart .t{color:#9a7b00}
.trap{background:#ffe9dc;border-color:#ef8a4c}.trap .t{color:#c45312}
.ex{background:#e8f0ff;border-color:#7c9be0}.ex .t{color:#2a4fa8}
.ask{border:1.6px solid #d8333a;border-radius:6px;margin:7px 0;break-inside:avoid;background:#fff}
.ask .q{background:#fde6e6;padding:4px 8px;border-radius:5px 5px 0 0}
.ask .q:before{content:"THEY ASK ▸ ";font-family:Head;font-weight:bold;color:#d8333a}
.ask .a{background:#e6f6ea;padding:4px 8px;border-top:1.5px dashed #5fb47b;border-radius:0 0 5px 5px}
.ask .a:before{content:"YOU ANSWER ▸ ";font-family:Head;font-weight:bold;color:#1c8a4a}
.ask pre{margin:3px 0;background:#fff}
.out{font-family:Mono;font-size:8.4pt;background:#fff;border:1px solid #9ad3ad;padding:1px 5px;white-space:pre-wrap;display:block;margin:2px 0}
.tag{font-family:Hand;font-size:8.5pt;color:#fff;background:#7a5cc4;border-radius:3px;padding:0 4px;margin-left:4px}
table{border-collapse:collapse;width:100%%;margin:4px 0 6px;break-inside:avoid;font-size:10pt}
th{background:#1f3c9a;color:#fff;font-family:Head;font-weight:normal;padding:2px 5px;text-align:left}
td{border:1px solid #b9c5e6;padding:2px 5px;vertical-align:top;background:#fff}
.test{border:2px solid #1f3c9a;border-radius:6px;padding:4px 8px;margin:6px 0;background:#f4f7ff}
.test h3{margin-top:2px}
.test ol>li{margin:4px 0;break-inside:avoid}
.key{font-size:10pt}
.key li{margin:2px 0;break-inside:avoid}
.chapter{break-before:column}
.new{column-span:all;break-before:page}
"""

BG = """<svg xmlns="http://www.w3.org/2000/svg" width="1123" height="794" viewBox="0 0 1123 794">
<rect width="1123" height="794" fill="#fffdf6"/><g stroke="#cddbf2" stroke-width="1">%s</g>
<path d="M38 0V794" stroke="#e8888a" stroke-width="1.4"/>
<path d="M561 30V770" stroke="#d9d2c0" stroke-width="1" stroke-dasharray="3 4"/></svg>""" % "".join(
    f'<path d="M0 {y}H1123"/>' for y in range(40, 790, 22))


def run_snippet(code, files=None):
    """Run code, return printed output (+ '!ExcName' if it ends in an exception)."""
    buf = io.StringIO()
    d = tempfile.mkdtemp()
    old = os.getcwd(); os.chdir(d)
    for name, content in (files or {}).items():
        os.makedirs(os.path.dirname(os.path.join(d, name)) or d, exist_ok=True)
        open(os.path.join(d, name), "w").write(textwrap.dedent(content))
    sys.path.insert(0, d)
    g = {"__name__": "__main__"}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<snippet>", "exec"), g)
    except BaseException as e:  # noqa
        buf.write("!" + type(e).__name__)
    finally:
        os.chdir(old); sys.path.remove(d)
        for m in list(sys.modules):
            f = getattr(sys.modules[m], "__file__", None) or ""
            if f.startswith(d):
                del sys.modules[m]
    return buf.getvalue()


def norm(s):
    return "\n".join(l.rstrip() for l in s.strip().splitlines())


def hl(code):
    out = []
    for line in code.split("\n"):
        e = html.escape(line)
        if "#" in line and not line.strip().startswith(("'", '"')):
            i = e.find("#")
            e = e[:i] + '<span class="cm">' + e[i:] + "</span>"
        out.append(e)
    return "\n".join(out)


class NB:
    errors = []

    def __init__(self, num, title, sub, foot):
        self.num, self.title, self.sub, self.foot = num, title, sub, foot
        self.parts = []
        self.tests = []  # list of (section title, [(q_html, a_html)])
        self.n_ask = 0
        self.sections = []   # [{title, html:[...], asks:[...]}]

    def raw(self, s, _ask=False):
        self.parts.append(s)
        if self.sections and not _ask:
            self.sections[-1]["html"].append(s)
        return self
    def h2(self, s):
        self.parts.append(f"<h2>{s}</h2>")
        self.sections.append({"title": s, "html": [], "asks": []})
        return self
    def h3(self, s): return self.raw(f"<h3>{s}</h3>")
    def p(self, s): return self.raw(f"<p>{s}</p>")
    def ul(self, *items): return self.raw("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
    def code(self, c): return self.raw(f"<pre>{hl(textwrap.dedent(c).strip())}</pre>")
    def box(self, kind, title, body): return self.raw(f'<div class="box {kind}"><div class="t">{title}</div>{body}</div>')
    def heart(self, body): return self.box("heart", "♥ Learn by heart", body)
    def trap(self, body): return self.box("trap", "⚠ Trap", body)
    def ex(self, body, title="Example"): return self.box("ex", title, body)
    def table(self, head, rows):
        h = "".join(f"<th>{x}</th>" for x in head)
        r = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>" for row in rows)
        return self.raw(f"<table><tr>{h}</tr>{r}</table>")

    def check(self, code, expect, files=None, where=""):
        got = run_snippet(textwrap.dedent(code).strip() + "\n", files)
        if norm(got) != norm(expect):
            NB.errors.append(f"[NB{self.num} {where}]\n--- code:\n{code}\n--- expected:\n{expect}\n--- got:\n{got}")

    def ask(self, q, code=None, out=None, why="", run=True, files=None, ans=None):
        """q: question html. code: snippet. out: exact expected output (checked).
        ans: answer html when there is no output to show (MCQ/theory)."""
        self.n_ask += 1
        if code and out is not None and run:
            self.check(code, out, files, q[:50])
        s = f'<div class="ask"><div class="q">{q}'
        if code:
            s += f"<pre>{hl(textwrap.dedent(code).strip())}</pre>"
        s += '</div><div class="a">'
        if out is not None:
            o = out.strip("\n")
            shown = html.escape(o).replace("!", "→ raises ", 1) if o.startswith("!") else html.escape(o)
            if "\n!" in o:
                shown = html.escape(o[:o.index("\n!")]) + "\n→ then raises " + html.escape(o[o.index("\n!") + 2:])
            s += f'<span class="out">{shown}</span>'
        if ans:
            s += ans
        if why:
            s += f" <i>{why}</i>"
        if self.sections:
            self.sections[-1]["asks"].append({"q": q, "code": textwrap.dedent(code).strip() if code else None,
                                              "out": out.strip("\n") if out is not None else None, "ans": ans, "why": why})
        return self.raw(s + "</div></div>", _ask=True)

    def selftest(self, title, items):
        """items: list of (question_html, code_or_None, answer_html, expected_out_or_None)"""
        start = sum(len(t[1]) for t in self.tests)
        ol = []
        for i, (q, code, a, exp) in enumerate(items):
            if code and exp is not None:
                self.check(code, exp, where=f"selftest {title} #{i+1}")
            c = f"<pre>{hl(textwrap.dedent(code).strip())}</pre>" if code else ""
            ol.append(f"<li>{q}{c}</li>")
        self.tests.append((title, items))
        self.raw(_ask=True, s=f'<div class="test"><h3>✎ Self-test: {title}</h3><p><i>Cover the key at the back. Write your answer next to each one.</i></p>'
                 f'<ol start="{start+1}">' + "".join(ol) + "</ol></div>")
        return self

    def render(self, path):
        css = CSS % {"F": F, "H": HERE, "FOOT": self.foot}
        key = []
        n = 0
        for title, items in self.tests:
            key.append(f"<h3>{title}</h3><ol class='key' start='{n+1}'>")
            for (q, code, a, exp) in items:
                n += 1
                e = ""
                if exp is not None:
                    o = exp.strip("\n")
                    o = html.escape(o).replace("!", "→ raises ", 1) if o.startswith("!") else html.escape(o).replace("\n!", "\n→ then raises ")
                    e = f'<span class="out">{o}</span>'
                key.append(f"<li>{e}{a}</li>")
            key.append("</ol>")
        body = (f"<h1>PCAP Notebook {self.num} · {self.title}</h1><div class='sub'>{self.sub}</div>"
                + "".join(self.parts)
                + ("<h2 class='chapter'>✔ Answer key</h2>" + "".join(key) if key else ""))
        doc = f"<!doctype html><html><head><meta charset='utf-8'><title>PCAP {self.num} {self.title}</title><style>{css}</style></head><body>{body}</body></html>"
        open(os.path.join(HERE, "bg.svg"), "w").write(BG)
        hp = path.replace(".pdf", ".html")
        open(hp, "w").write(doc)
        import weasyprint
        weasyprint.HTML(hp, base_url=HERE).write_pdf(path)
        return path


def finish():
    if NB.errors:
        print(f"{len(NB.errors)} MISMATCHES")
        for e in NB.errors:
            print(e, "\n==========")
        sys.exit(1)
    print("all answers verified")
