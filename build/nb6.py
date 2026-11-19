from lib import NB

nb = NB(6, "New-exam extras + Mock exam", "Part A: topics only on the NEW exam PCAP-31-04 (skip if your voucher says 31-03) · Part B: 40-question mock exam (31-03 weights) for everyone",
        "PCAP Notebook 6 ~ 31-04 extras + Mock exam")

nb.box("ex", "Which exam do I have?", "Look at the exam code on your voucher / booking. <b>PCAP-31-03</b>: notebooks 1–5 + Part B. "
       "<b>PCAP-31-04</b> (42 questions, 65 min, pass 72%): notebooks 1–5 + Part A + Part B. "
       "31-04 drops <code>platform</code> functions from the list and adds everything below.")

# ================================================================ PART A
nb.h2("A1. Loops with else")
nb.ul("<code>for … else</code> / <code>while … else</code>: the <code>else</code> block runs when the loop ends <span class='y'>normally</span> (condition false / items exhausted).",
      "It does <span class='r'>NOT</span> run if the loop was left with <code>break</code>. Use: \"search, and do something if not found\".",
      "A loop that never runs at all still runs its <code>else</code>.")
nb.ask("What is printed?", "for i in range(3):\n    if i == 5:\n        break\nelse:\n    print('no break', i)\n\nwhile False:\n    pass\nelse:\n    print('while else')", "no break 2\nwhile else")
nb.ask("What is printed?", "for n in [3, 8, 11]:\n    if n % 2 == 0:\n        print('found', n)\n        break\nelse:\n    print('none even')", "found 8")

nb.h2("A2. match – case (Python 3.10+)")
nb.code("""
match command:
    case "start" | "go":          # | = several alternatives
        ...
    case ("move", x):            # pattern with capture
        ...
    case _:                      # default: matches anything
        ...
""")
nb.ul("Compares one value with patterns <b>top to bottom</b>; runs the <b>first</b> matching case only (no fall-through, no <code>break</code> needed).",
      "<code>case _:</code> is the default. Without it and with no match, nothing happens (no error).",
      "Difference from if-elif: matches on the <b>shape</b> of data (tuples, lists, captures), not only on boolean conditions.")
nb.ask("What is printed?", """
def describe(p):
    match p:
        case (0, 0):
            return "origin"
        case (0, y):
            return f"on y axis at {y}"
        case (x, y) if x == y:
            return "diagonal"
        case _:
            return "somewhere"

print(describe((0, 0)), '|', describe((0, 5)), '|', describe((3, 3)), '|', describe((1, 2)))
""", "origin | on y axis at 5 | diagonal | somewhere")
nb.ask("What is printed?", "code = 404\nmatch code:\n    case 200:\n        print('OK')\n    case 401 | 403 | 404:\n        print('client error')\n    case _:\n        print('other')", "client error")

nb.h2("A3. Set &amp; dict comprehensions, unpacking")
nb.ask("What is printed?", "print({x % 3 for x in range(10)})\nprint({c: ord(c) for c in 'ab'})", "{0, 1, 2}\n{'a': 97, 'b': 98}")
nb.ask("What is printed? (flatten with unpacking)", "a = [1, 2]\nb = [3]\nprint([*a, *b], [*'hi'])", "[1, 2, 3] ['h', 'i']")

nb.h2("A4. More OOP: getattr, super() in multiple inheritance, safe __init__")
nb.ul("<code>getattr(obj, 'name')</code> reads an attribute by its <b>string</b> name; <code>getattr(obj, 'x', default)</code> gives default instead of AttributeError.",
      "Cooperative multiple inheritance: <code>super()</code> calls the <b>next class in the MRO</b>, not necessarily the parent you think.",
      "Validate arguments inside <code>__init__</code> and <code>raise ValueError</code> / <code>TypeError</code>; use keyword arguments and sensible defaults.")
nb.trap("<b>Mutable default argument</b>: <code>def __init__(self, items=[])</code> — the same list is created <b>once</b> and shared by every object. Use <code>items=None</code> then <code>self.items = items if items is not None else []</code>.")
nb.ask("What is printed?", """
class Bag:
    def __init__(self, items=[]):
        self.items = items

a = Bag()
b = Bag()
a.items.append('pen')
print(b.items)
""", "['pen']")
nb.ask("What is printed?", """
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B" + super().hi()
class C(A):
    def hi(self): return "C" + super().hi()
class D(B, C):
    def hi(self): return "D" + super().hi()
print(D().hi())
""", "DBCA", why="MRO is D, B, C, A: B's super() goes to C, not to A.")
nb.ask("What is printed?", "class P:\n    color = 'red'\np = P()\nprint(getattr(p, 'color'), getattr(p, 'size', 'n/a'))", "red n/a")
nb.ask("What is printed?", """
class Account:
    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("negative balance")
        self.owner = owner
        self.balance = balance
try:
    acc = Account(owner="Malak", balance=-5)
except ValueError as e:
    print("refused:", e)
""", "refused: negative balance")

nb.h2("A5. Exceptions: raise e vs raise")
nb.ul("Inside <code>except … as e</code>: bare <code>raise</code> re-raises the current exception unchanged; <code>raise e</code> raises the same object again (explicitly); <code>raise OtherError(…)</code> replaces it.",
      "<code>except (A, B) as e</code> works; the exception object's <code>args</code> property holds the arguments.")
nb.ask("What is printed?", "try:\n    try:\n        raise ValueError('v')\n    except ValueError as e:\n        raise TypeError('t')\nexcept Exception as e:\n    print(type(e).__name__, e.args)", "TypeError ('t',)")

nb.h2("A6. pathlib and file modes")
nb.table(["code", "does"],
         [["<code>from pathlib import Path</code>", ""],
          ["<code>p = Path('data') / 'notes.txt'</code>", "join paths with <b>/</b>"],
          ["<code>p.is_absolute()</code>, <code>Path.cwd()</code>, <code>p.resolve()</code>", "relative vs absolute paths"],
          ["<code>p.write_text('hi')</code> / <code>p.read_text()</code>", "text without open/close"],
          ["<code>p.write_bytes(b'..')</code> / <code>p.read_bytes()</code>", "binary"],
          ["<code>for f in Path('.').iterdir()</code>", "list a folder's content"],
          ["<code>p.name</code>, <code>p.suffix</code>, <code>p.stem</code>, <code>p.parent</code>, <code>p.exists()</code>", "parts of a path"]])
nb.ask("What is printed?", "from pathlib import Path\np = Path('data') / 'notes.txt'\nprint(p.name, p.suffix, p.stem, p.parent, p.is_absolute())", "notes.txt .txt notes data False")
nb.ask("What is printed?", "from pathlib import Path\np = Path('hello.txt')\nn = p.write_text('hi there')\nprint(n, p.read_text().upper(), p.exists())", "8 HI THERE True")
nb.ul("Modes recap: <code>r w a x b t +</code>. <code>x</code> = create, fails if the file exists (FileExistsError). Always prefer <code>with open(...) as f:</code>.")

nb.h2("A7. pip &amp; requirements.txt")
nb.ul("<code>python -m pip install requests</code> = same as pip, but uses the pip of <b>that</b> Python.",
      "<code>pip freeze &gt; requirements.txt</code> records exact versions (<code>requests==2.31.0</code>); <code>pip install -r requirements.txt</code> rebuilds the same environment → <b>reproducible</b>.",
      "PyPI packages = external; standard library = shipped with Python; local modules = your files.")

nb.h2("A8. Testing &amp; debugging")
nb.table(["term", "meaning"],
         [["unit test", "checks one small unit (a function/class) for one behaviour"],
          ["test case", "one input + its <b>expected result</b>, compared with the <b>actual result</b>"],
          ["test suite", "a collection of test cases"],
          ["typical / boundary / invalid", "normal input · edge values (0, empty, max) · wrong input (should raise)"],
          ["regression", "something that worked breaks after a change → rerun tests after every change"],
          ["isolation", "tests don't depend on each other or on order"]])
nb.table(["error kind", "when", "example"],
         [["syntax error", "before running (code can't be parsed)", "missing <code>:</code>, bad indentation"],
          ["runtime error", "while running → exception + traceback", "ZeroDivisionError"],
          ["logic error", "runs fine, <b>wrong result</b>, no message", "<code>&lt;</code> instead of <code>&lt;=</code>"]])
nb.ul("Read a traceback <b>from the bottom</b>: last line = exception type + message; the line just above = where it happened.",
      "Debug by printing values / stepping through, fix the cause, then rerun the tests.")
nb.ask("Test with assert: what happens?", "def area(w, h):\n    return w * h\n\nassert area(2, 3) == 6\nassert area(0, 5) == 0\nassert area(2, 2) == 5, 'square failed'", "!AssertionError")

nb.h2("A9. Working in a team (Git)")
nb.ul("<b>Shared repository</b>: everyone works on the same code history.",
      "<b>Branch</b>: isolate your change so others can work in parallel. <b>Commit</b>: a saved, described step (clear message: what + why).",
      "<b>Pull / merge request</b>: propose merging your branch; teammates <b>review</b> it (specific, constructive comments); you answer and revise.",
      "<b>Merge conflict</b>: two people changed the same lines → a human decides the final version; prevent with small changes and communication.",
      "<b>CI</b> (continuous integration): runs the automated tests on every change; merge when review + tests are green. Issues / task records document bugs, requirements, decisions.")

nb.h2("A10. AI-assisted coding")
nb.ul("Give the AI <b>clear requirements, context, examples, constraints</b>; refine the prompt if the output is wrong or incomplete.",
      "<b>Human-in-the-loop (HITL)</b>: you review, test and approve every AI output before using it; <b>you</b> stay responsible.",
      "Check correctness, readability, security; <b>run and test</b> generated code; verify that the functions/modules/APIs it mentions <b>really exist</b> (AI can invent them).",
      "Never paste passwords, keys, personal data or proprietary code into an AI tool.")
nb.ask("An AI suggests <code>import string_utils</code> and calls <code>string_utils.smart_title()</code>. What should you do first?",
       ans="Verify the module/function really exist and behave as claimed (docs, run it, tests) before using it: never trust it blindly.")

# ================================================================ PART B
nb.raw("<div class='chapter'></div>")
nb.h2("B. Mock exam: 40 questions · 65 minutes")
nb.p("Real exam: one question at a time, single or multiple choice, ~70% to pass. Do this under time, write your answers, then check the key at the back. "
     "<b>Target: 28/40 or more.</b> Questions are mixed like the real exam: 6 modules · 5 exceptions · 8 strings · 12 OOP · 9 misc.")

Q = []
def q(text, code=None, ans="", out=None):
    Q.append((text, code, ans, out))

# Modules (6)
q("What is printed?", "import math\nprint(math.ceil(-2.5) + math.floor(2.5))", "", "0")
q("Which import makes <code>sqrt(4)</code> callable <b>without</b> a prefix? a) <code>import math</code> b) <code>from math import sqrt</code> c) <code>import math as sqrt</code> d) <code>import sqrt from math</code>", None, "<b>b</b>")
q("What is printed?", "from random import randint\nprint(randint(5, 5))", "", "5")
q("Which is true about <code>__pycache__</code>? a) holds machine code b) holds semi-compiled .pyc files c) must be created by hand d) is a package", None, "<b>b</b>")
q("A package folder <code>pkg</code> contains <code>__init__.py</code> and <code>mod.py</code> (with <code>def f(): return 1</code>). Which call is valid after <code>import pkg.mod</code>? a) <code>mod.f()</code> b) <code>pkg.f()</code> c) <code>pkg.mod.f()</code> d) <code>f()</code>", None, "<b>c</b>")
q("What is printed when the file is run directly?", "if __name__ == '__main__':\n    print('A')\nelse:\n    print('B')", "", "A")
# Exceptions (5)
q("What is printed?", "try:\n    x = {}['k']\nexcept IndexError:\n    print('I')\nexcept LookupError:\n    print('L')\nelse:\n    print('E')", "", "L")
q("What is printed?", "def f():\n    try:\n        return 1\n    finally:\n        print('F', end='')\nprint(f())", "", "F1")
q("What is printed?", "class E(Exception):\n    pass\ntry:\n    raise E('x', 'y')\nexcept Exception as e:\n    print(len(e.args))", "", "2")
q("Which exception is NOT a subclass of <code>Exception</code>? a) ValueError b) KeyboardInterrupt c) OverflowError d) KeyError", None, "<b>b</b>")
q("What is printed?", "try:\n    assert False\nexcept AssertionError:\n    print('assert')\nexcept:\n    print('other')", "", "assert")
# Strings (8)
q("What is printed?", "s = 'abcdef'\nprint(s[-2:], s[:-4], s[::2])", "", "ef ab ace")
q("What is printed?", "print('xyz'.find('a'), 'xyz'.rfind('z'))", "", "-1 2")
q("What happens?", "print('abc'.index('d'))", "", "!ValueError")
q("What is printed?", "print('12'.isdigit(), '1 2'.isdigit(), 'aB'.isalpha())", "", "True False True")
q("What is printed?", "print(sorted(['b', 'C', 'a']))", "", "['C', 'a', 'b']")
q("What is printed?", "print(':'.join('abc').upper().split(':'))", "", "['A', 'B', 'C']")
q("What is printed?", "print(ord('c') - ord('a'), chr(ord('a') - 32))", "", "2 A")
q("What is printed?", "s = 'banana'\nprint(s.replace('a', 'o', 2), s.count('an'))", "", "bonona 2")
# OOP (12)
q("What is printed?", "class A:\n    def __init__(self):\n        self.x = 1\na = A()\na.y = 2\nprint(len(a.__dict__))", "", "2")
q("What is printed?", "class A:\n    n = 0\n    def __init__(self):\n        A.n += 1\nA(); A(); a = A()\nprint(a.n)", "", "3")
q("What is printed?", "class A:\n    def __init__(self):\n        self.__p = 5\na = A()\nprint(a._A__p)", "", "5")
q("What is printed?", "class A:\n    def f(self):\n        return 'A'\nclass B(A):\n    pass\nprint(B().f(), issubclass(B, A), isinstance(A(), B))", "", "A True False")
q("What is printed?", "class A:\n    v = 1\nclass B(A):\n    v = 2\nclass C(B):\n    pass\nprint(C.v, C.__bases__[0].__name__)", "", "2 B")
q("What is printed?", "class X:\n    def __str__(self):\n        return 'X obj'\nprint(X())", "", "X obj")
q("What is printed?", "class L:\n    def m(self): return 'L'\nclass R:\n    def m(self): return 'R'\nclass S(R, L):\n    pass\nprint(S().m())", "", "R")
q("What is printed?", "class A:\n    def go(self):\n        return self.name()\n    def name(self):\n        return 'a'\nclass B(A):\n    def name(self):\n        return 'b'\nprint(B().go())", "", "b")
q("What is printed?", "class A:\n    pass\na = A()\nb = a\nc = A()\nprint(a is b, a is c, a == c)", "", "True False False")
q("What is printed?", "class A:\n    x = 5\na = A()\nprint(hasattr(a, 'x'), hasattr(A, 'y'))", "", "True False")
q("What is printed?", "class P:\n    def __init__(self, n):\n        self.n = n\nclass Q(P):\n    def __init__(self):\n        super().__init__(7)\nprint(Q().n)", "", "7")
q("What happens?", "class A:\n    pass\nprint(A().__name__)", "", "!AttributeError")
# Misc (9)
q("What is printed?", "print([x * x for x in range(5) if x % 2])", "", "[1, 9]")
q("What is printed?", "f = lambda a, b=3: a * b\nprint(f(2), f(2, 2))", "", "6 4")
q("What is printed?", "print(list(map(lambda x: x + 1, filter(lambda x: x > 1, [1, 2, 3]))))", "", "[3, 4]")
q("What is printed?", "def gen():\n    for c in 'ab':\n        yield c * 2\nprint(list(gen()))", "", "['aa', 'bb']")
q("What is printed?", "def outer(x):\n    def inner(y):\n        return x + y\n    return inner\nadd5 = outer(5)\nprint(add5(1), outer(1)(1))", "", "6 2")
q("Which mode erases an existing file's content? a) <code>'r'</code> b) <code>'a'</code> c) <code>'w'</code> d) <code>'r+'</code>", None, "<b>c</b>")
q("What is printed?", "b = bytearray(2)\nb[0] = 65\nprint(b)", "", "bytearray(b'A\\x00')")
q("What does <code>f.readlines()</code> return? a) a string b) a list of strings c) a generator d) an int", None, "<b>b</b>")
q("What is printed?", "print([[i] * i for i in range(1, 4)])", "", "[[1], [2, 2], [3, 3, 3]]")
assert len(Q) == 40, len(Q)
nb.selftest("Mock exam (40)", Q)

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_6.pdf")
    finish()
