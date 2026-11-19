from lib import NB

nb = NB(1, "Modules, Packages &amp; PIP", "Course Module 1 · exam section 1 (≈ 6 questions, 12%) · they ask → you answer",
        "PCAP Notebook 1 ~ Modules, Packages & PIP")

# ---------------------------------------------------------------- 0
nb.h2("0. The big picture")
nb.ul("<b>module</b> = one <span class='y'>.py file</span> with definitions (functions, variables, classes) you can <b>import</b>.",
      "<b>package</b> = a <span class='y'>folder</span> of modules (+ an <code>__init__.py</code>). Module : package = file : folder.",
      "<b>standard library</b> = all modules shipped with Python (math, random, platform, sys, os…) = a library where modules are the books.",
      "<b>PyPI</b> = the online repo of free packages (\"The Cheese Shop\"); <b>pip</b> = the tool that installs them.",
      "Exam questions here are mostly <b>\"what is printed?\"</b> and <b>\"which import is valid?\"</b>.")

# ---------------------------------------------------------------- 1
nb.h2("1. The 4 ways to import")
nb.table(["form", "what enters YOUR namespace", "how you call pi"],
         [["<code>import math</code>", "only the name <b>math</b>", "<code>math.pi</code>"],
          ["<code>from math import pi, sin</code>", "only <b>pi</b> and <b>sin</b>", "<code>pi</code>"],
          ["<code>import math as m</code>", "only <b>m</b> (math is NOT defined!)", "<code>m.pi</code>"],
          ["<code>from math import *</code>", "every public name of math", "<code>pi</code>"]])
nb.ul("<b>namespace</b> = the space where names live; inside one namespace each name is <span class='y'>unique</span>.",
      "<code>import math</code> → math's names do <b>not</b> enter your namespace → your own <code>pi</code> is safe. You must <b>qualify</b>: <code>math.pi</code>.",
      "<code>from math import pi</code> → <code>pi</code> enters your namespace and can <span class='r'>overwrite</span> (or be overwritten by) your own <code>pi</code>.",
      "Several modules: <code>import math, sys</code> or one per line (preferred).",
      "Many aliases at once: <code>from module import n as a, m as b</code>.")
nb.heart("<ul><li>After <code>import math as m</code> the name <code>math</code> is <span class='r'>inaccessible</span> → <code>math.pi</code> = <b>NameError</b>.</li>"
         "<li><code>as</code> is a keyword. The alias replaces the name, it does not add a second one.</li>"
         "<li>Last assignment wins: a later <code>from … import pi</code> overwrites your <code>pi</code>, and your later <code>pi = …</code> overwrites the imported one.</li></ul>")

nb.ask("What happens?", "import math as m\nprint(m.floor(2.7))\nprint(math.floor(2.7))", "2\n!NameError",
       why="after aliasing, only <code>m</code> exists.")
nb.ask("What is printed?", """
from math import pi
pi = 3
print(pi)
""", "3", why="your assignment comes after the import, so it wins.")
nb.ask("What is printed?", """
pi = 3
from math import pi
print(pi)
""", "3.141592653589793", why="the import comes last, so it overwrites your <code>pi</code>.")
nb.ask("What is printed?", """
def sin(x):
    return "mine"
import math
print(sin(0), math.sin(0))
""", "mine 0.0", why="<code>import math</code> doesn't touch your namespace; <code>math.sin(0)</code> returns a float.")

nb.trap("<code>from math import *</code> imports every name <b>except</b> the ones starting with <code>_</code>. "
        "It is <span class='r'>risky</span>: it can silently overwrite your names. Don't use it in real code, but know it for the exam.")
nb.ask("Module <code>m.py</code> contains <code>a = 1</code> and <code>_b = 2</code>. What happens?", "from m import *\nprint(a)\nprint(_b)",
       "1\n!NameError", files={"m.py": "a = 1\n_b = 2\n"}, why="<code>*</code> skips names beginning with an underscore.")

# ---------------------------------------------------------------- 2
nb.h2("2. dir() – what's inside a module")
nb.ul("<code>dir(module)</code> returns an <span class='y'>alphabetically sorted list</span> of all names in the module.",
      "Module must be imported first with <code>import math</code> (not <code>from math import …</code>), otherwise <code>dir(math)</code> → NameError.",
      "Works in the console too: <code>import math</code> then <code>dir(math)</code>.")
nb.ask("What is the type of the result?", "import math\nprint(type(dir(math)).__name__)", "list")
nb.ask("What happens?", "from math import pi\nprint(dir(math))", "!NameError", why="only <code>pi</code> was imported, the name <code>math</code> does not exist.")

# ---------------------------------------------------------------- 3
nb.h2("3. The math module")
nb.table(["function", "meaning", "example"],
         [["<code>ceil(x)</code>", "smallest int ≥ x (go <b>up</b>)", "ceil(-1.4) = <b>-1</b>"],
          ["<code>floor(x)</code>", "largest int ≤ x (go <b>down</b>)", "floor(-1.4) = <b>-2</b>"],
          ["<code>trunc(x)</code>", "cut the decimals (go <b>toward 0</b>)", "trunc(-1.4) = <b>-1</b>"],
          ["<code>factorial(x)</code>", "x!  (x integral, ≥ 0)", "factorial(5) = 120"],
          ["<code>hypot(x, y)</code>", "√(x²+y²), hypotenuse", "hypot(3, 4) = <b>5.0</b>"],
          ["<code>sqrt(x)</code>", "square root, always <b>float</b>", "sqrt(9) = <b>3.0</b>"],
          ["<code>pi, e</code>", "constants (float)", "e == exp(1) → True"],
          ["<code>exp, log(x), log(x,b), log10, log2</code>", "e<sup>x</sup>, ln, log base b…", "log10(100) = 2.0"]])
nb.heart("<ul><li><code>ceil</code>, <code>floor</code>, <code>trunc</code>, <code>factorial</code> return <b>int</b>. "
         "<code>sqrt</code>, <code>hypot</code>, <code>exp</code>, <code>log</code>… return <b>float</b>.</li>"
         "<li>Positive numbers: <code>trunc = floor</code>. Negative numbers: <code>trunc = ceil</code>.</li>"
         "<li><code>pow(x, y)</code> is <b>built-in</b> (no import needed).</li>"
         "<li><code>sqrt(-1)</code> → <b>ValueError</b> (math domain error). <code>factorial(-1)</code> → <b>ValueError</b>.</li></ul>")
nb.ask("Course example: what is printed?", """
from math import ceil, floor, trunc
x = 1.4
y = 2.6
print(floor(x), floor(y))
print(floor(-x), floor(-y))
print(ceil(x), ceil(y))
print(ceil(-x), ceil(-y))
print(trunc(x), trunc(y))
print(trunc(-x), trunc(-y))
""", "1 2\n-2 -3\n2 3\n-1 -2\n1 2\n-1 -2")
nb.ask("Course exercise 1: value of <code>result</code>?", "import math\nresult = math.e == math.exp(1)\nprint(result)", "True")
nb.ask("What is printed?", "import math\nprint(math.hypot(3, 4), math.sqrt(16), math.factorial(4))", "5.0 4.0 24")
nb.ask("What happens?", "import math\nprint(math.sqrt(-4))", "!ValueError")

# ---------------------------------------------------------------- 4
nb.h2("4. The random module")
nb.table(["function", "returns", "range"],
         [["<code>random()</code>", "a float", "<span class='y'>0.0 ≤ x &lt; 1.0</span> (1.0 never)"],
          ["<code>seed()</code> / <code>seed(n)</code>", "sets the start value", "same seed → <b>same sequence</b>"],
          ["<code>randrange(end)</code>", "int", "0 … end-1"],
          ["<code>randrange(beg, end, step)</code>", "int", "beg … end-1 (end <b>excluded</b>)"],
          ["<code>randint(left, right)</code>", "int", "left … right (<b>both included</b>)"],
          ["<code>choice(seq)</code>", "<b>one</b> element", "from the sequence"],
          ["<code>sample(seq, k)</code>", "a <b>list</b> of k <b>unique</b> elements", "k ≤ len(seq) else ValueError"]])
nb.heart("<ul><li><code>randint(a, b) == randrange(a, b+1)</code>.</li><li><code>randrange(1)</code> is always <b>0</b>.</li>"
         "<li><code>randrange</code>/<code>randint</code> can <b>repeat</b> values → for a lottery use <code>sample</code> (no repeats).</li>"
         "<li><code>seed()</code> with no argument uses the current time.</li></ul>")
nb.ask("Which values can this print?", "from random import randrange, randint\nprint(randrange(1), randrange(0, 10, 2), randint(0, 1))",
       ans="1st is always <b>0</b>; 2nd one of <b>0, 2, 4, 6, 8</b>; 3rd <b>0 or 1</b>.")
nb.ask("What happens?", "from random import sample\nprint(sample([1, 2, 3], 4))", "!ValueError", why="you can't pick 4 unique items out of 3.")
nb.ask("Is the output always the same between runs?", "from random import random, seed\nseed(0)\nprint(random())",
       ans="<b>Yes.</b> A fixed seed always gives the same sequence (here 0.8444218515250481).")
nb.check("from random import random, seed\nseed(0)\nprint(random())", "0.8444218515250481")
nb.ask("What is printed?", "from random import sample\nprint(len(sample(range(10), 10)), len(set(sample(range(10), 10))))", "10 10",
       why="a sample never repeats elements.")

# ---------------------------------------------------------------- 5
nb.h2("5. The platform module")
nb.table(["function", "returns"],
         [["<code>platform(aliased=False, terse=False)</code>", "one human-readable string describing OS + hardware + Python"],
          ["<code>machine()</code>", "generic processor name, e.g. <code>'x86_64'</code>"],
          ["<code>processor()</code>", "<span class='y'>real CPU name</span> (if possible)"],
          ["<code>system()</code>", "generic OS name, e.g. <code>'Windows'</code>, <code>'Linux'</code>"],
          ["<code>version()</code>", "OS version string"],
          ["<code>python_implementation()</code>", "<code>'CPython'</code> (usually)"],
          ["<code>python_version_tuple()</code>", "<span class='y'>tuple of 3 strings</span>: major, minor, patch → ('3','11','4')"]])
nb.trap("<code>python_version_tuple()</code> holds <b>strings</b>, not ints, and always has <b>3</b> elements. "
        "<code>platform(1)</code> = aliased, <code>platform(0, 1)</code> = terse.")
nb.ask("Course exercise 4: what is printed?", "import platform\nprint(len(platform.python_version_tuple()))", "3")
nb.ask("Course exercise 3: which function tells you the name of the CPU?", ans="<code>platform.processor()</code>")
nb.ask("What is printed?", "import platform\nprint(type(platform.python_version_tuple()[0]).__name__)", "str")

# ---------------------------------------------------------------- 6
nb.h2("6. Writing your own module")
nb.ul("Put <code>module.py</code> and <code>main.py</code> in the same folder; <code>main.py</code> does <code>import module</code>.",
      "First import → Python creates <code>__pycache__/module.cpython-3x.pyc</code>: <span class='y'>semi-compiled</span> code (not machine code), so later imports are faster. Rebuilt automatically if the source changes.",
      "When imported, the module's code is <span class='y'>executed</span> (initialization) — <b>only once</b>, at the first import. Later imports are silently skipped.",
      "Every file has its own variable <code>__name__</code>.")
nb.heart("<ul><li>Run the file directly → <code>__name__ == \"__main__\"</code></li>"
         "<li>Imported as a module → <code>__name__ == \"module\"</code> (file name without .py)</li></ul>"
         "<pre>if __name__ == \"__main__\":\n    print(\"run directly: do some tests\")\nelse:\n    print(\"I was imported\")</pre>")
nb.ask("<code>mod1.py</code>: <code>print('mod1 loaded')</code>. <code>mod2.py</code>: <code>import mod1</code> + <code>print('mod2 loaded')</code>. What does main print?",
       "import mod1\nimport mod2", "mod1 loaded\nmod2 loaded",
       files={"mod1.py": "print('mod1 loaded')\n", "mod2.py": "import mod1\nprint('mod2 loaded')\n"},
       why="mod1 runs only once even though it is imported twice.")
nb.ask("<code>module.py</code> contains <code>print(__name__)</code>. What does <code>main.py</code> print?", "import module", "module",
       files={"module.py": "print(__name__)\n"})
nb.ask("Same <code>module.py</code>, but you run <code>module.py</code> itself. What is printed?", ans="<code>__main__</code>")
nb.ul("<b>Private variables?</b> Python <span class='r'>can't hide</span> module variables. Convention only: start the name with <code>_</code> or <code>__</code> = \"please don't touch\". Users can still read/modify it.",
      "To change a module-level variable inside a function you need <code>global __counter</code>.",
      "<code>#!/usr/bin/env python3</code> = <b>shebang</b>: a comment for Python, but tells Unix/macOS which program runs the file.",
      "A string at the top of the module = <b>doc-string</b>: explains the module.")
nb.ask("Course exercise: how do you stop users from running your module as a script?",
       ans="<pre>import sys\nif __name__ == \"__main__\":\n    print(\"Don't do that!\")\n    sys.exit()</pre>")
nb.ask("<code>counter.py</code> has <code>__counter = 0</code> and <code>def inc(): global __counter; __counter += 1</code>. What is printed?",
       "import counter\ncounter.inc()\ncounter.inc()\nprint(counter.__counter)", "2",
       files={"counter.py": "__counter = 0\ndef inc():\n    global __counter\n    __counter += 1\n"},
       why="the underscore is only a convention: <code>module.__counter</code> is still reachable from outside.")

# ---------------------------------------------------------------- 7
nb.h2("7. Where does Python look? sys.path")
nb.ul("<code>sys.path</code> is a <span class='y'>list of folders</span> searched <b>in order</b> during an import.",
      "<b>First</b> element = the folder of the script you started.",
      "First folder that contains the module wins; the others are ignored. Not found anywhere → <b>ModuleNotFoundError</b> (an ImportError).",
      "It can contain a <b>.zip</b> file: Python treats zips like folders.",
      "Add a folder: <code>sys.path.append('..\\\\modules')</code> (goes last) or <code>sys.path.insert(0, path)</code> (goes first).")
nb.trap("Windows paths in strings need <b>double backslashes</b>: <code>\"C:\\\\Users\\\\user\\\\py\\\\modules\"</code> (or use <code>/</code>). "
        "A relative path like <code>'..\\\\modules'</code> only works if you start from the right folder.")
nb.ask("Course exercise 2: modules are in <code>D:\\Python\\Project\\Modules</code>. Make Python search there.",
       ans="<pre>import sys\nsys.path.append(\"D:\\\\Python\\\\Project\\\\Modules\")</pre>")
nb.ask("What is the type of <code>sys.path</code>?", "import sys\nprint(type(sys.path).__name__)", "list")
nb.ask("What happens?", "import modul_that_does_not_exist", "!ModuleNotFoundError",
       why="it is a subclass of <b>ImportError</b>, so <code>except ImportError</code> catches it.")

# ---------------------------------------------------------------- 8
nb.h2("8. Packages")
nb.ul("A package is a folder of modules (and sub-packages). Names use dots like folders: <code>extra.good.best.tau.funT()</code>.",
      "<span class='y'><code>__init__.py</code> makes the folder a package</span>. It is executed when any module of the package is imported (package initialization). It can be empty, but <b>must not be omitted</b> (course rule).",
      "Sub-folders can have their own <code>__init__.py</code> too.",
      "The package's parent folder must be on <code>sys.path</code>.")
nb.code("""
extra/                    # package
  __init__.py
  iota.py                 # funI()
  good/                   # sub-package
    __init__.py
    alpha.py   beta.py
    best/  __init__.py  sigma.py  tau.py   # funT()
  ugly/  __init__.py  psi.py  omega.py
""")
nb.heart("Three valid ways to call <code>funT()</code>:"
         "<pre>import extra.good.best.tau\nextra.good.best.tau.funT()\n\nfrom extra.good.best.tau import funT\nfunT()\n\nimport extra.good.best.tau as t\nt.funT()</pre>"
         "<span class='r'>Wrong:</span> <code>import tau</code> (no full path) → ModuleNotFoundError.")
nb.ask("<code>extra/__init__.py</code> prints <code>'extra init'</code>, <code>extra/iota.py</code> defines <code>funI()</code> returning <code>'Iota'</code>. What is printed?",
       "import extra.iota\nprint(extra.iota.funI())", "extra init\nIota",
       files={"extra/__init__.py": "print('extra init')\n", "extra/iota.py": "def funI():\n    return 'Iota'\n"})
nb.ask("Same package. What happens?", "import extra.iota\nprint(iota.funI())", "extra init\n!NameError",
       files={"extra/__init__.py": "print('extra init')\n", "extra/iota.py": "def funI():\n    return 'Iota'\n"},
       why="<code>import extra.iota</code> only defines the name <code>extra</code>; you must write the full path.")
nb.ask("Course exercise 3: tree <code>abc/def/mymodule.py</code>; write an import that lets you use mymodule's entities.",
       ans="<code>import abc.def.mymodule</code>  <i>(then <code>abc.def.mymodule.something</code>; in real Python <code>def</code> is a keyword, but this is the course's answer).</i>")

# ---------------------------------------------------------------- 9
nb.h2("9. PIP and PyPI")
nb.ul("<b>PyPI</b> (Python Package Index), nickname <b>The Cheese Shop</b>: repo of free packages, <code>https://pypi.org</code>.",
      "<b>pip</b> = \"pip installs packages\". It is a <span class='y'>console tool</span> (not a Python function); you run it in a terminal.")
nb.table(["command", "does"],
         [["<code>pip --version</code> / <code>pip3 --version</code>", "show pip version"],
          ["<code>pip help</code> / <code>pip help install</code>", "help (for one operation)"],
          ["<code>pip list</code>", "list installed packages"],
          ["<code>pip show name</code>", "info on a package, incl. its <b>dependencies</b>"],
          ["<code>pip search text</code>", "search PyPI (course; disabled on real PyPI now)"],
          ["<code>pip install name</code>", "install <b>system-wide</b> (may need admin)"],
          ["<code>pip install --user name</code>", "install for <b>you only</b>"],
          ["<code>pip install -U name</code>", "<b>update</b> an installed package"],
          ["<code>pip install name==1.2</code>", "install a specific version"],
          ["<code>pip uninstall name</code>", "remove a package"]])
nb.trap("pip resolves <b>dependencies</b> automatically: installing one package may install others. "
        "<code>-U</code> = upgrade, <code>--user</code> = only for me.")
nb.ask("You don't have admin rights. Which command installs <code>pygame</code>?", ans="<code>pip install --user pygame</code>")
nb.ask("Which command shows which packages <code>pygame</code> depends on?", ans="<code>pip show pygame</code>")

# ---------------------------------------------------------------- self-test
nb.raw("<div class='chapter'></div>")
nb.selftest("Modules, Packages & PIP", [
    ("What is printed?", "import math\nprint(math.floor(-3.5), math.ceil(-3.5), math.trunc(-3.5))", "", "-4 -3 -3"),
    ("What is printed?", "from math import sqrt\nprint(sqrt(25) == 5, type(sqrt(25)).__name__)", "", "True float"),
    ("What happens?", "import random as r\nprint(random.randint(1, 2))", "<code>random</code> no longer exists after aliasing.", "!NameError"),
    ("Which range can <code>randint(1, 6)</code> return? And <code>randrange(1, 6)</code>?", None, "<b>1–6</b> and <b>1–5</b>.", None),
    ("What is printed?", "from random import choice\nprint(choice([7, 7, 7]))", "", "7"),
    ("True or false: <code>import math</code> puts <code>pi</code> into your namespace.", None, "<b>False</b>: only <code>math</code>; you write <code>math.pi</code>.", None),
    ("What does <code>dir(math)</code> return?", None, "An <b>alphabetically sorted list</b> of the names in math.", None),
    ("Which file must a folder contain to be a (regular) package?", None, "<code>__init__.py</code>", None),
    ("A module is imported 3 times in one program. How many times is its code executed?", None, "<b>Once</b>, at the first import.", None),
    ("You run <code>main.py</code> directly. What is its <code>__name__</code>?", None, "<code>'__main__'</code>", None),
    ("What is the first element of <code>sys.path</code>?", None, "The folder of the script that was started.", None),
    ("What does the <code>.pyc</code> file in <code>__pycache__</code> contain?", None, "Semi-compiled Python bytecode (not machine code), to load faster.", None),
    ("What is printed?", "import platform\nt = platform.python_version_tuple()\nprint(type(t).__name__, len(t))", "", "tuple 3"),
    ("What is printed?", "from math import pi as PI\nprint(round(PI, 2))", "", "3.14"),
    ("Which pip command upgrades <code>numpy</code>?", None, "<code>pip install -U numpy</code>", None),
    ("Does <code>from mod import *</code> import <code>_secret</code>?", None, "<b>No</b>, names starting with <code>_</code> are skipped.", None),
])

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_1.pdf")
    finish()
