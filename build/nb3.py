from lib import NB

nb = NB(3, "Exceptions", "Course Module 2 (part 2) + Module 3 \"More about exceptions\" · exam section 2 (≈ 5 questions, 14%) · they ask → you answer",
        "PCAP Notebook 3 ~ Exceptions")

# ---------------------------------------------------------------- 1
nb.h2("1. What is an exception?")
nb.ul("When Python doesn't know what to do with your code it: <b>(1)</b> stops the program and <b>(2)</b> creates a special object called an <b>exception</b>. Both together = <span class='y'>raising an exception</span>.",
      "If nobody handles it → the program ends with a traceback, e.g. <code>ValueError: math domain error</code>.",
      "<code>1/0</code> → ZeroDivisionError · <code>[][0]</code> → IndexError · <code>{}['k']</code> → KeyError · <code>int('x')</code> → ValueError · <code>'a'+1</code> → TypeError · <code>undefined_name</code> → NameError · <code>obj.nothing</code> → AttributeError.")

# ---------------------------------------------------------------- 2
nb.h2("2. try / except")
nb.code("""
try:
    risky code            # stops at the FIRST error
except ZeroDivisionError:
    print("can't divide by 0")
except ValueError:
    print("not an integer")
except:                   # anything else (must be LAST)
    print("something went wrong")
print("THE END.")
""")
nb.heart("<ul><li>Python checks the <code>except</code> branches <b>top to bottom</b> and runs only the <span class='y'>first one that matches</span>. The others are skipped.</li>"
         "<li>A branch matches if the exception is that class <b>or a subclass</b> of it.</li>"
         "<li>The bare <code>except:</code> must be the <b>last</b> branch (otherwise <b>SyntaxError</b>). It equals <code>except BaseException:</code>.</li>"
         "<li>Several exceptions in one branch: <code>except (ValueError, TypeError):</code> — parentheses required.</li>"
         "<li>If no branch matches, the exception continues upward (and may stop the program).</li></ul>")
nb.ask("Course example: what is printed?", "try:\n    print('1')\n    x = 1 / 0\n    print('2')\nexcept:\n    print('Oh dear, something went wrong...')\nprint('3')",
       "1\nOh dear, something went wrong...\n3", why="'2' is never printed: the try block stops at the error.")
nb.ask("Course exercise 1: what is printed?", "try:\n    print(1/0)\nexcept ZeroDivisionError:\n    print('zero')\nexcept ArithmeticError:\n    print('arith')\nexcept:\n    print('some')", "zero")
nb.ask("Course exercise 2: what is printed?", "try:\n    print(1/0)\nexcept ArithmeticError:\n    print('arith')\nexcept ZeroDivisionError:\n    print('zero')\nexcept:\n    print('some')", "arith",
       why="ArithmeticError is the parent of ZeroDivisionError, it matches first; the 'zero' branch is dead code.")
nb.ask("What happens?", "try:\n    x = int('hello')\nexcept ZeroDivisionError:\n    print('zero')\nprint('end')", "!ValueError",
       why="no branch matches → unhandled → 'end' is never printed.")
nb.ask("What is printed?", "try:\n    x = [1, 2][5]\nexcept (IndexError, KeyError):\n    print('lookup problem')", "lookup problem")
nb.trap("<code>except:</code> placed before another <code>except</code> is a <b>SyntaxError</b> (the program doesn't even start). "
        "<code>try</code> needs at least one <code>except</code> or a <code>finally</code>.")
nb.ask("What happens?", "try:\n    x = 1/0\nexcept:\n    print('a')\nexcept ZeroDivisionError:\n    print('b')", ans="<b>SyntaxError</b>: default 'except:' must be last. Nothing runs at all.")
nb.check("compile('try:\\n x=1\\nexcept:\\n pass\\nexcept ZeroDivisionError:\\n pass\\n','s','exec')", "!SyntaxError")

# ---------------------------------------------------------------- 3
nb.h2("3. The exception tree (hierarchy)")
nb.code("""
BaseException
 ├── KeyboardInterrupt        # Ctrl-C
 ├── SystemExit               # sys.exit()
 ├── GeneratorExit
 └── Exception
      ├── ArithmeticError     (abstract)
      │    ├── ZeroDivisionError
      │    ├── OverflowError
      │    └── FloatingPointError
      ├── LookupError         (abstract)
      │    ├── IndexError
      │    └── KeyError
      ├── AssertionError
      ├── ImportError ── ModuleNotFoundError
      ├── MemoryError
      ├── NameError
      ├── TypeError
      ├── AttributeError
      ├── ValueError ── UnicodeError
      ├── OSError (= IOError) ── FileNotFoundError, PermissionError…
      └── StopIteration, RuntimeError …
""")
nb.heart("<ul><li><b>BaseException</b> = the most general of all. <code>except:</code> ≡ <code>except BaseException:</code>.</li>"
         "<li><b>KeyboardInterrupt</b> is NOT under Exception → <code>except Exception</code> doesn't catch Ctrl-C.</li>"
         "<li><b>abstract</b> = a general category (ArithmeticError, LookupError) · <b>concrete</b> = a real raised one (ZeroDivisionError, IndexError).</li>"
         "<li><code>1E250 ** 2</code> → <b>OverflowError</b> (float too big). Big <b>ints</b> never overflow.</li></ul>")
nb.table(["exception", "location (course)"],
         [["ArithmeticError", "BaseException ← Exception ← ArithmeticError"],
          ["AssertionError", "BaseException ← Exception ← AssertionError"],
          ["IndexError", "BaseException ← Exception ← LookupError ← IndexError"],
          ["KeyError", "BaseException ← Exception ← LookupError ← KeyError"],
          ["KeyboardInterrupt", "BaseException ← KeyboardInterrupt"],
          ["OverflowError", "BaseException ← Exception ← ArithmeticError ← OverflowError"],
          ["MemoryError", "BaseException ← Exception ← MemoryError"],
          ["ImportError", "BaseException ← Exception ← ImportError <i>(slides say StandardError: old Python 2)</i>"]])
nb.ask("Course exercise: which exception do you catch to stop the keyboard from interrupting your program?", ans="<b>KeyboardInterrupt</b>")
nb.ask("Course exercise: the most general of all Python exceptions?", ans="<b>BaseException</b>")
nb.ask("Course exercise: which exception?", "huge_value = 1E250 ** 2", "!OverflowError")
nb.ask("What is printed?", "print(issubclass(ZeroDivisionError, ArithmeticError), issubclass(KeyError, LookupError), issubclass(KeyboardInterrupt, Exception))",
       "True True False")
nb.ask("What is printed?", "try:\n    d = {'a': 1}\n    print(d['b'])\nexcept LookupError:\n    print('lookup')\nexcept KeyError:\n    print('key')", "lookup")

# ---------------------------------------------------------------- 4
nb.h2("4. Exceptions inside functions")
nb.ul("An exception raised in a function can be handled <b>inside</b> it, or it travels <b>up</b> to the caller (and the caller's caller…) until a matching <code>except</code> is found.")
nb.ask("What is printed?", "def bad(n):\n    return 1 / n\n\ndef middle(n):\n    return bad(n)\n\ntry:\n    middle(0)\nexcept ArithmeticError:\n    print('caught at the top')", "caught at the top")
nb.ask("What is printed?", "def f(n):\n    try:\n        return 1 / n\n    except ZeroDivisionError:\n        print('inside')\n        return None\n\ntry:\n    print(f(0))\nexcept:\n    print('outside')", "inside\nNone",
       why="handled inside the function, so the outside except never runs.")

# ---------------------------------------------------------------- 5
nb.h2("5. raise, bare raise, assert")
nb.ul("<code>raise ZeroDivisionError</code> or <code>raise ValueError('message')</code>: raise an exception yourself (to test your handlers, or to pass part of the handling to someone else).",
      "<b>Bare</b> <code>raise</code> (no name) — only inside an <code>except</code> branch: <span class='y'>re-raises the same exception</span>.",
      "Bare <code>raise</code> outside any except → <span class='r'>RuntimeError</span>.",
      "<code>assert expression</code>: does nothing if the expression is true (non-zero, non-empty, not None); otherwise raises <b>AssertionError</b>. Think of it as an <b>airbag</b>.")
nb.ask("Course example: what is printed?", "def bad_fun(n):\n    raise ZeroDivisionError\n\ntry:\n    bad_fun(0)\nexcept ArithmeticError:\n    print('What happened? An error?')\nprint('THE END.')",
       "What happened? An error?\nTHE END.")
nb.ask("Course example: what is printed?", "def bad_fun(n):\n    try:\n        return n / 0\n    except:\n        print('I did it again!')\n        raise\n\ntry:\n    bad_fun(0)\nexcept ArithmeticError:\n    print('I see!')\nprint('THE END.')",
       "I did it again!\nI see!\nTHE END.", why="the bare <code>raise</code> sends the same ZeroDivisionError up to the caller.")
nb.ask("What happens?", "raise", "!RuntimeError", why="no active exception to re-raise.")
nb.ask("Course exercise 3: what is printed?", "def foo(x):\n    assert x\n    return 1/x\n\ntry:\n    print(foo(0))\nexcept ZeroDivisionError:\n    print('zero')\nexcept:\n    print('some')", "some",
       why="<code>assert 0</code> fails first → AssertionError, which only the bare except catches.")
nb.ask("What is printed?", "try:\n    assert 'abc', 'message'\n    assert [], 'empty list!'\nexcept AssertionError as e:\n    print(e)", "empty list!",
       why="non-empty string passes; empty list fails; the text after the comma becomes the message.")

# ---------------------------------------------------------------- 6
nb.h2("6. else and finally")
nb.code("""
try:      ...   # risky
except:   ...   # only if an exception happened
else:     ...   # only if NO exception happened
finally:  ...   # ALWAYS, no matter what
""")
nb.heart("<ul><li>Order is fixed: <b>try → except(s) → else → finally</b>. <code>else</code> must come after the last except.</li>"
         "<li><code>finally</code> runs even if the exception was not handled, and even if the try/except did <code>return</code>.</li>"
         "<li>If <code>finally</code> has its own <code>return</code>, it <span class='r'>overrides</span> the other return.</li></ul>")
nb.ask("Course example: what is printed?", "def reciprocal(n):\n    try:\n        n = 1 / n\n    except ZeroDivisionError:\n        print('Division failed')\n        n = None\n    else:\n        print('Everything went fine')\n    finally:\n        print(\"It's time to say goodbye\")\n        return n\n\nprint(reciprocal(2))\nprint(reciprocal(0))",
       "Everything went fine\nIt's time to say goodbye\n0.5\nDivision failed\nIt's time to say goodbye\nNone")
nb.ask("Course exercise 1: what is printed?", "import math\ntry:\n    print(math.sqrt(9))\nexcept ValueError:\n    print('inf')\nelse:\n    print('fine')", "3.0\nfine")
nb.ask("Course exercise 2: what is printed?", "import math\ntry:\n    print(math.sqrt(-9))\nexcept ValueError:\n    print('inf')\nelse:\n    print('fine')\nfinally:\n    print('the end')", "inf\nthe end")
nb.ask("What is printed?", "def f():\n    try:\n        return 'try'\n    finally:\n        print('finally ran')\n\nprint(f())", "finally ran\ntry")
nb.ask("What is printed?", "def f():\n    try:\n        return 'try'\n    finally:\n        return 'finally'\n\nprint(f())", "finally")
nb.ask("What happens?", "try:\n    x = 1 / 0\nfinally:\n    print('cleanup')", "cleanup\n!ZeroDivisionError", why="finally runs, then the unhandled error continues.")

# ---------------------------------------------------------------- 7
nb.h2("7. Exceptions are objects (classes)")
nb.ul("Raising an exception = creating an <b>object</b> of an exception class. Catch it with <code>except ValueError as e:</code>.",
      "<code>print(e)</code> = <code>print(e.__str__())</code> = the message.",
      "<code>e.args</code> = <span class='y'>tuple of the arguments</span> given to the constructor: <code>raise Exception('a', 'b')</code> → <code>('a', 'b')</code>.",
      "No argument → <code>args == ()</code> and <code>str(e) == ''</code>. One argument → <code>str(e)</code> is that argument. Several → <code>str(e)</code> looks like the tuple.")
nb.ask("Course example: what is printed?", "try:\n    i = int('Hello!')\nexcept Exception as e:\n    print(e)", "invalid literal for int() with base 10: 'Hello!'")
nb.ask("What is printed?", "for a in [(), ('my exception',), ('my', 'exception')]:\n    try:\n        raise Exception(*a)\n    except Exception as e:\n        print(repr(str(e)), e.args)",
       "'' ()\n'my exception' ('my exception',)\n\"('my', 'exception')\" ('my', 'exception')")
nb.trap("<code>e.args</code> is filled with what you passed to the constructor <b>even if your own <code>__init__</code> doesn't call the parent's</b>.")
nb.ask("Course exercise 3: what is printed?", "class NewValueError(ValueError):\n    def __init__(self, name, color, state):\n        self.data = (name, color, state)\n\ntry:\n    raise NewValueError('Enemy warning', 'Red alert', 'High readiness')\nexcept NewValueError as nve:\n    for arg in nve.args:\n        print(arg, end='! ')",
       "Enemy warning! Red alert! High readiness! ")
nb.ul("Exception classes know their tree: <code>ZeroDivisionError.__bases__</code> → <code>(ArithmeticError,)</code>; <code>BaseException.__subclasses__()</code> lists the children (course's <code>print_exception_tree</code> walks the tree recursively).")

# ---------------------------------------------------------------- 8
nb.h2("8. Your own exceptions")
nb.ul("Create one by <b>inheriting</b> from an existing exception (usually <code>Exception</code>): <code>class MyError(Exception): pass</code>.",
      "It fits in the tree: <code>except ParentError</code> also catches your subclass.",
      "Add data by overriding <code>__init__</code> and calling the parent: <code>Exception.__init__(self, message)</code> or <code>super().__init__(message)</code>.",
      "Put the <b>more specific</b> class first in the except list.")
nb.ask("Course example: what is printed?", "class MyZeroDivisionError(ZeroDivisionError):\n    pass\n\ndef do_the_division(mine):\n    if mine:\n        raise MyZeroDivisionError('some worse news')\n    else:\n        raise ZeroDivisionError('some bad news')\n\nfor mode in [False, True]:\n    try:\n        do_the_division(mode)\n    except MyZeroDivisionError:\n        print('My division by zero')\n    except ZeroDivisionError:\n        print('Original division by zero')",
       "Original division by zero\nMy division by zero")
nb.ask("Course example (pizza): what is printed?", """
class PizzaError(Exception):
    def __init__(self, pizza, message):
        Exception.__init__(self, message)
        self.pizza = pizza

class TooMuchCheeseError(PizzaError):
    def __init__(self, pizza, cheese, message):
        PizzaError.__init__(self, pizza, message)
        self.cheese = cheese

def make_pizza(pizza, cheese):
    if pizza not in ['margherita', 'capricciosa', 'calzone']:
        raise PizzaError(pizza, "no such pizza on the menu")
    if cheese > 100:
        raise TooMuchCheeseError(pizza, cheese, "too much cheese")
    print("Pizza ready!")

for (pz, ch) in [('calzone', 0), ('margherita', 110), ('mafia', 20)]:
    try:
        make_pizza(pz, ch)
    except TooMuchCheeseError as tmce:
        print(tmce, ':', tmce.cheese)
    except PizzaError as pe:
        print(pe, ':', pe.pizza)
""", "Pizza ready!\ntoo much cheese : 110\nno such pizza on the menu : mafia")

# ---------------------------------------------------------------- self-test
nb.raw("<div class='chapter'></div>")
nb.selftest("Exceptions", [
    ("What is printed?", "try:\n    print('a')\n    x = int('1.5')\n    print('b')\nexcept ValueError:\n    print('c')\nelse:\n    print('d')\nfinally:\n    print('e')", "", "a\nc\ne"),
    ("What is printed?", "try:\n    x = [1][1]\nexcept LookupError:\n    print('L')\nexcept IndexError:\n    print('I')", "", "L"),
    ("What is printed?", "try:\n    raise ValueError('bad', 42)\nexcept ValueError as e:\n    print(e.args[1])", "", "42"),
    ("What is printed?", "def f():\n    try:\n        raise KeyError\n    except KeyError:\n        print('k')\n        raise\ntry:\n    f()\nexcept Exception:\n    print('x')", "", "k\nx"),
    ("Which branch catches Ctrl-C: <code>except Exception:</code> or <code>except:</code>?", None, "Only <code>except:</code> (KeyboardInterrupt is not a subclass of Exception).", None),
    ("What is printed?", "class A(Exception): pass\nclass B(A): pass\ntry:\n    raise B\nexcept A:\n    print('A')\nexcept B:\n    print('B')", "", "A"),
    ("What is printed?", "try:\n    assert 1 == 2, 'no'\nexcept AssertionError as e:\n    print('AE:', e)", "", "AE: no"),
    ("Where must <code>else</code> go in a try statement?", None, "After the <b>last except</b>, before <code>finally</code>.", None),
    ("What is printed?", "def f(x):\n    try:\n        return 10 / x\n    except ZeroDivisionError:\n        return -1\n    finally:\n        print('F', end=' ')\nprint(f(0))", "", "F -1"),
    ("What is printed?", "try:\n    print(undefined)\nexcept NameError as e:\n    print(type(e).__name__)", "", "NameError"),
    ("Is <code>ArithmeticError</code> abstract or concrete? And <code>IndexError</code>?", None, "ArithmeticError = <b>abstract</b> (a category); IndexError = <b>concrete</b>.", None),
    ("What is printed?", "e = Exception()\nprint(len(e.args), str(e) == '')", "", "0 True"),
    ("What is printed?", "try:\n    try:\n        1/0\n    except ValueError:\n        print('inner')\nexcept ZeroDivisionError:\n    print('outer')", "", "outer"),
    ("What does the bare <code>raise</code> do when there is no active exception?", None, "Raises <b>RuntimeError</b>.", None),
])

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_3.pdf")
    finish()
