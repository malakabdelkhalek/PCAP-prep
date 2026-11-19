from lib import NB

nb = NB(5, "Miscellaneous", "Course Module 4 · exam section 5 (≈ 9 questions, 22%): generators, comprehensions, lambda, map/filter, closures, files · + os / datetime / calendar",
        "PCAP Notebook 5 ~ Miscellaneous")

# ---------------------------------------------------------------- 1
nb.h2("1. Iterators: the iterator protocol")
nb.ul("An object works in <code>for x in obj</code> if it follows the <b>iterator protocol</b>:",
      "<code>__iter__()</code> → returns the iterator (usually <code>self</code>); called <b>once</b> at the start.",
      "<code>__next__()</code> → returns the next value; when there is nothing left it must <span class='y'>raise StopIteration</span> (that ends the loop quietly).")
nb.ask("Course example (shortened): what is printed?", """
class Fib:
    def __init__(self, nn):
        self.__n = nn
        self.__i = 0
        self.__p1 = self.__p2 = 1
    def __iter__(self):
        print("__iter__")
        return self
    def __next__(self):
        self.__i += 1
        if self.__i > self.__n:
            raise StopIteration
        if self.__i in [1, 2]:
            return 1
        ret = self.__p1 + self.__p2
        self.__p1, self.__p2 = self.__p2, ret
        return ret

for i in Fib(6):
    print(i, end=' ')
""", "__iter__\n1 1 2 3 5 8", why="__next__ is called 7 times: 6 values + 1 StopIteration.")

# ---------------------------------------------------------------- 2
nb.h2("2. Generators: yield")
nb.ul("A function with <code>yield</code> is a <b>generator</b>: calling it does <span class='r'>not</span> run the body, it returns a <b>generator object</b>.",
      "Each <code>next()</code> (or each loop turn) runs until the next <code>yield</code>, gives the value, and <b>pauses</b> (keeps its local variables). <code>return</code> would end everything.",
      "You can loop on it, use it in a list comprehension, or convert it: <code>list(gen())</code>.")
nb.heart("<ul><li>A generator is <b>used up</b> after one full pass: a second loop gives nothing.</li>"
         "<li><code>next()</code> on an exhausted generator → <b>StopIteration</b>.</li>"
         "<li><code>len(gen)</code> → TypeError. <code>(x for x in …)</code> with <b>parentheses</b> = a generator, <b>brackets</b> = a list.</li></ul>")
nb.ask("Course example: what is printed?", """
def powers_of_2(n):
    power = 1
    for i in range(n):
        yield power
        power *= 2

t = [x for x in powers_of_2(5)]
print(t)
print(list(powers_of_2(3)))
""", "[1, 2, 4, 8, 16]\n[1, 2, 4]")
nb.ask("Course example: what is printed?", """
def fibonacci(n):
    p = pp = 1
    for i in range(n):
        if i in [0, 1]:
            yield 1
        else:
            n = p + pp
            pp, p = p, n
            yield n

print(list(fibonacci(10)))
""", "[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]")
nb.ask("What is printed?", "def gen():\n    yield 1\n    yield 2\n\ng = gen()\nprint(list(g), list(g))", "[1, 2] []", why="the second <code>list(g)</code> finds it already exhausted.")
nb.ask("What happens?", "def gen():\n    yield 'a'\n\ng = gen()\nprint(next(g))\nprint(next(g))", "a\n!StopIteration")
nb.ask("What is printed?", "def f():\n    print('start')\n    yield 1\n\ng = f()\nprint('created')\nprint(next(g))", "created\nstart\n1",
       why="the body starts only at the first <code>next()</code>.")
nb.ask("What is printed?", "lst = [x * x for x in range(4)]\ngen = (x * x for x in range(4))\nprint(lst, type(gen).__name__, sum(gen))", "[0, 1, 4, 9] generator 14")

# ---------------------------------------------------------------- 3
nb.h2("3. List comprehensions")
nb.code("""
[expression for item in iterable]                    # transform
[expression for item in iterable if condition]       # filter (keep only some)
[A if cond else B for item in iterable]              # conditional expression (keep all)
[x * y for x in X for y in Y]                        # nested loops: x outer, y inner
[[x * y for y in Y] for x in X]                      # list of lists
""")
nb.trap("<ul><li>The <code>if … else</code> goes <b>before</b> <code>for</code>; a filter <code>if</code> (no else) goes <b>after</b>. "
        "<code>[x for x in L if x else 0]</code> → <b>SyntaxError</b>.</li>"
        "<li>Several <code>for</code> clauses read left → right like nested loops (first = outer).</li></ul>")
nb.ask("Course example: what is printed?", "print([10 ** ex for ex in range(6)])\nprint([1 if x % 2 == 0 else 0 for x in range(10)])",
       "[1, 10, 100, 1000, 10000, 100000]\n[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]")
nb.ask("What is printed?", "print([x for x in range(10) if x % 3 == 0])", "[0, 3, 6, 9]")
nb.ask("What is printed?", "print([(x, y) for x in range(2) for y in 'ab'])", "[(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]")
nb.ask("What is printed?", "board = [[i * j for j in range(3)] for i in range(3)]\nprint(board, board[2][1])", "[[0, 0, 0], [0, 1, 2], [0, 2, 4]] 2")
nb.ask("What is printed? (flatten a list of lists)", "m = [[1, 2], [3], [4, 5]]\nprint([x for row in m for x in row])", "[1, 2, 3, 4, 5]")
nb.ask("What is printed?", "print(len([[0] * 3 for _ in range(4)]), [c.upper() for c in 'hey' if c != 'e'])", "4 ['H', 'Y']")

# ---------------------------------------------------------------- 4
nb.h2("4. lambda")
nb.ul("<code>lambda parameters: expression</code> = a function <b>without a name</b> (anonymous), with <span class='y'>one expression</span> whose value is returned automatically (no <code>return</code> keyword).",
      "You can name it (<code>sqr = lambda x: x * x</code>), call it directly <code>(lambda x: x + 1)(2)</code>, or pass it as an argument to another function.",
      "It can have 0 parameters (<code>lambda: 2</code>), several, or defaults (<code>lambda x, y=2: x ** y</code>).")
nb.ask("Course example: what is printed?", """
two = lambda: 2
sqr = lambda x: x * x
pwr = lambda x, y: x ** y

for a in range(-2, 3):
    print(sqr(a), end=" ")
    print(pwr(a, two()))
""", "4 4\n1 1\n0 0\n1 1\n4 4")
nb.ask("Course example: what is printed?", """
def print_function(args, fun):
    for x in args:
        print('f(', x, ')=', fun(x), sep='')

print_function([x for x in range(-2, 3)], lambda x: 2 * x**2 - 4 * x + 2)
""", "f(-2)=18\nf(-1)=8\nf(0)=2\nf(1)=0\nf(2)=2")
nb.ask("What is printed?", "f = lambda x, y=10: x + y\nprint(f(1), f(1, 2), (lambda: 'hi')())", "11 3 hi")
nb.ask("What is printed?", "pairs = [(1, 'b'), (3, 'a'), (2, 'c')]\nprint(sorted(pairs, key=lambda p: p[1]))", "[(3, 'a'), (1, 'b'), (2, 'c')]")

# ---------------------------------------------------------------- 5
nb.h2("5. map() and filter()")
nb.table(["", "<code>map(function, iterable, …)</code>", "<code>filter(function, iterable)</code>"],
         [["does", "applies the function to <b>every</b> element", "keeps elements for which the function returns <b>True</b>"],
          ["returns", "an <span class='y'>iterator</span> (not a list!)", "an <span class='y'>iterator</span>"],
          ["extra", "several iterables → function takes several args, stops at the shortest", "<code>filter(None, L)</code> keeps the truthy elements"]])
nb.trap("<code>print(map(…))</code> prints <code>&lt;map object at 0x…&gt;</code>. Wrap it: <code>list(map(…))</code>. Like a generator, a map/filter object can be used <b>only once</b>.")
nb.ask("Course example: what is printed?", """
list_1 = [x for x in range(5)]
list_2 = list(map(lambda x: 2 ** x, list_1))
print(list_2)
for x in map(lambda x: x * x, list_2):
    print(x, end=' ')
""", "[1, 2, 4, 8, 16]\n1 4 16 64 256")
nb.ask("What is printed?", "data = [-4, 3, 8, 0, -2, 6]\nprint(list(filter(lambda x: x > 0 and x % 2 == 0, data)))", "[8, 6]")
nb.ask("What is printed?", "print(list(map(lambda x, y: x + y, [1, 2, 3], [10, 20])))", "[11, 22]")
nb.ask("What is printed?", "print(list(filter(None, [0, 1, '', 'a', [], [2]])))", "[1, 'a', [2]]")
nb.ask("What is printed?", "m = map(str.upper, ['a', 'b'])\nprint(list(m), list(m))", "['A', 'B'] []")

# ---------------------------------------------------------------- 6
nb.h2("6. Closures")
nb.ul("<b>Closure</b> = a technique that <span class='y'>stores values even though the context that created them no longer exists</span>.",
      "An inner function uses a variable of the outer function; the outer function returns the inner one; the returned function still remembers the variable.",
      "Great for <b>function factories</b>: make many specialised functions from one template.")
nb.ask("Course example: what is printed?", """
def outer(par):
    loc = par
    def inner():
        return loc
    return inner

var = 1
fun = outer(var)
print(fun())
""", "1")
nb.ask("What is printed?", """
def make_power(n):
    def power(x):
        return x ** n
    return power

square = make_power(2)
cube = make_power(3)
print(square(4), cube(2))
""", "16 8", why="each returned function remembers its own n.")
nb.ask("What happens?", "def outer(par):\n    loc = par\n    def inner():\n        return loc\n    return inner\n\nprint(loc)", "!NameError",
       why="loc only lives inside the closure, not in the global scope.")
nb.ask("What is printed? (classic trap)", "funcs = [lambda: i for i in range(3)]\nprint([f() for f in funcs])", "[2, 2, 2]",
       why="the lambdas look up <code>i</code> when they are <b>called</b>, after the loop ended (i = 2).")

# ---------------------------------------------------------------- 7
nb.h2("7. Files: names, streams, open modes")
nb.ul("Unix/Linux file names are <b>case-sensitive</b>; Windows keeps the case but ignores it.",
      "Separators: <code>\\</code> on Windows, <code>/</code> on Unix. In Python strings write <code>'C:\\\\dir\\\\file'</code> or simply <code>'C:/dir/file'</code> (Python converts).",
      "A program talks to files through a <b>stream</b> (handle). <b>Opening</b> = binding the stream to a file (first operation); <b>closing</b> = unbinding (last operation).",
      "<code>stream = open(file, mode='r', encoding=None)</code>: the only way to get a stream object (never a constructor). Fails → exception, e.g. <b>FileNotFoundError</b>.")
nb.table(["mode", "meaning", "file must exist?", "notes"],
         [["<code>r</code>", "read", "<b>yes</b>", "default mode"],
          ["<code>w</code>", "write", "no", "creates it, or <span class='r'>erases</span> its content"],
          ["<code>a</code>", "append", "no", "writes at the <b>end</b>, keeps old content"],
          ["<code>r+</code>", "read + update", "<b>yes</b> (and writeable)", ""],
          ["<code>w+</code>", "write + update", "no", "erases content"],
          ["<code>x</code>", "exclusive create", "must <b>NOT</b> exist", "else FileExistsError"],
          ["<code>…t</code> / <code>…b</code>", "text (default) / binary", "", "<code>'rb'</code>, <code>'wt'</code>…"]])
nb.heart("<ul><li>3 basic modes: <b>read</b>, <b>write</b>, <b>update</b>. Writing to a read stream (or reading a write stream) → <b>UnsupportedOperation</b> (io module; inherits OSError and ValueError).</li>"
         "<li>Pre-opened streams (module <code>sys</code>): <code>sys.stdin</code> (keyboard, used by <code>input()</code>), <code>sys.stdout</code> (screen, used by <code>print()</code>), <code>sys.stderr</code> (screen, for errors).</li>"
         "<li>Close with <code>stream.close()</code>. Better: <code>with open(…) as f:</code> closes automatically.</li></ul>")
nb.ask("What happens? (file <code>nothing.txt</code> doesn't exist)", "f = open('nothing.txt')", "!FileNotFoundError")
nb.ask("What happens?", "f = open('a.txt', 'w')\nf.write('x')\nf.close()\nf = open('a.txt', 'r')\nf.write('y')", "!UnsupportedOperation")
nb.ask("What is printed?", "for m in ['w', 'a', 'a']:\n    f = open('t.txt', m)\n    f.write(m)\n    f.close()\nprint(open('t.txt').read())", "waa")
nb.ask("What happens?", "open('t.txt', 'w').close()\nopen('t.txt', 'x')", "!FileExistsError")

# ---------------------------------------------------------------- 8
nb.h2("8. Stream errors: errno &amp; strerror")
nb.ul("An <b>IOError</b> (= OSError) object has a property <code>errno</code> (error number). Compare it with constants of the <code>errno</code> module.",
      "<code>os.strerror(number)</code> → the error <b>message</b> as a string.")
nb.table(["constant", "meaning"],
         [["<code>errno.ENOENT</code>", "No such file or directory"], ["<code>errno.EACCES</code>", "Permission denied"],
          ["<code>errno.EEXIST</code>", "File exists"], ["<code>errno.EISDIR</code>", "Is a directory"],
          ["<code>errno.EMFILE</code>", "Too many open files"], ["<code>errno.EBADF</code> / <code>EFBIG</code> / <code>ENOSPC</code>", "Bad file number / File too large / No space left on device"]])
nb.ask("What is printed?", "import errno\nfrom os import strerror\ntry:\n    s = open('missing.txt', 'rt')\nexcept IOError as exc:\n    print(exc.errno == errno.ENOENT, strerror(exc.errno))",
       "True No such file or directory")

# ---------------------------------------------------------------- 9
nb.h2("9. Reading and writing text files")
nb.table(["method", "returns", "at end of file"],
         [["<code>read(n)</code>", "string of up to n characters", "<code>''</code>"],
          ["<code>read()</code>", "the <b>whole</b> file as one string (careful with huge files)", "<code>''</code>"],
          ["<code>readline()</code>", "one line, <b>with</b> its <code>'\\n'</code>", "<code>''</code>"],
          ["<code>readlines(n)</code>", "a <span class='y'>list</span> of lines (n = max chars, optional)", "<code>[]</code>"],
          ["<code>for line in f</code>", "the stream is iterable: line by line", ""],
          ["<code>write(s)</code>", "writes s; <span class='r'>adds no newline</span>; returns nb of chars", ""]])
nb.ask("What is printed?", """
f = open('text.txt', 'wt')
for i in range(3):
    f.write("line #" + str(i + 1) + "\\n")
f.close()

s = open('text.txt', 'rt')
print(repr(s.readline()))
print(s.readlines())
print(repr(s.read()))
s.close()
""", "'line #1\\n'\n['line #2\\n', 'line #3\\n']\n''")
nb.ask("What is printed?", "with open('t.txt', 'w') as f:\n    n = f.write('ab\\ncd')\nwith open('t.txt') as f:\n    print(n, f.read(1), len(f.readlines()))", "5 a 2")
nb.ask("What is printed?", "with open('t.txt', 'w') as f:\n    f.write('Hi')\n    f.write('There')\nprint(open('t.txt').read())", "HiThere", why="write() never adds a newline.")

# ---------------------------------------------------------------- 10
nb.h2("10. Binary files: bytearray")
nb.ul("<code>bytearray(10)</code> = a <b>mutable</b> array of 10 bytes, all <b>zeros</b>. Acts like a list: <code>len</code>, indexing, loops.",
      "Each element must be an <b>int</b> (else TypeError) in <b>0–255</b> (else ValueError).",
      "Write: <code>open('f.bin', 'wb').write(data)</code>.",
      "Read into an existing bytearray: <code>bf.readinto(data)</code> (fills it, returns the number of bytes read).",
      "<code>bf.read()</code> → a <b>bytes</b> object (like bytearray but <span class='y'>immutable</span>); <code>bf.read(5)</code> → at most 5 bytes.")
nb.ask("Course example: what is printed?", """
data = bytearray(10)
for i in range(len(data)):
    data[i] = 10 + i
bf = open('file.bin', 'wb')
bf.write(data)
bf.close()

data2 = bytearray(10)
bf = open('file.bin', 'rb')
bf.readinto(data2)
bf.close()
print(hex(data2[0]), hex(data2[-1]))
bf = open('file.bin', 'rb')
print(bytearray(bf.read(5)))
""", "0xa 0x13\nbytearray(b'\\n\\x0b\\x0c\\r\\x0e')")
nb.ask("What happens?", "data = bytearray(3)\ndata[0] = 256", "!ValueError")
nb.ask("What happens?", "data = bytearray(3)\ndata[0] = 'a'", "!TypeError")
nb.ask("What is printed?", "b = bytearray(3)\nprint(b, len(b), list(b))", "bytearray(b'\\x00\\x00\\x00') 3 [0, 0, 0]")
nb.ask("What happens?", "b = bytes(3)\nb[0] = 1", "!TypeError", why="bytes are immutable.")

# ---------------------------------------------------------------- 11
nb.h2("11. The os module <span class='tag'>course</span>")
nb.table(["call", "does"],
         [["<code>os.uname()</code>", "object: sysname, nodename, release, version, machine (Unix only)"],
          ["<code>os.name</code>", "<code>'posix'</code> (Unix) · <code>'nt'</code> (Windows) · <code>'java'</code> (Jython)"],
          ["<code>os.mkdir(path)</code>", "create <b>one</b> folder (FileExistsError if it exists)"],
          ["<code>os.makedirs(path)</code>", "create a folder <b>and its parents</b> (like <code>mkdir -p</code>)"],
          ["<code>os.listdir(path='.')</code>", "list of names in a folder (no '.', '..')"],
          ["<code>os.chdir(path)</code> / <code>os.getcwd()</code>", "change / get current working directory"],
          ["<code>os.rmdir(path)</code> / <code>os.removedirs(path)</code>", "remove one empty folder / folder + its empty parents"],
          ["<code>os.system(cmd)</code>", "run a shell command, returns its exit value"]])
nb.ask("Course exercise: on Unix, what is printed?", "import os\nprint(os.name)", "posix")
nb.ask("Course exercise: in an empty folder, what is printed?", "import os\nos.mkdir('hello')\nprint(os.listdir())", "['hello']")
nb.ask("What happens?", "import os\nos.mkdir('a/b/c')", "!FileNotFoundError", why="mkdir can't create the missing parents; use <code>makedirs</code>.")

# ---------------------------------------------------------------- 12
nb.h2("12. datetime &amp; time <span class='tag'>course</span>")
nb.ul("<code>date(2019, 11, 4)</code>, <code>date.today()</code>, <code>.year .month .day</code>.",
      "<code>date.fromtimestamp(time.time())</code>: timestamp = seconds since the <b>Unix epoch</b> (1 Jan 1970 00:00:00 UTC).",
      "<code>date.fromisoformat('2019-11-04')</code> (YYYY-MM-DD) · <code>d.replace(year=1992)</code> returns a new date.",
      "<code>d.weekday()</code>: <span class='y'>Monday = 0</span> … Sunday = 6 (<code>isoweekday()</code>: Monday = 1).",
      "<code>time(14, 53, 20, 1)</code> → hour, minute, second, microsecond (0 ≤ µs &lt; 1 000 000).",
      "<code>datetime(2019, 11, 4, 14, 53)</code> → <code>.date()</code>, <code>.time()</code>, <code>.timestamp()</code>; <code>datetime.today()</code>, <code>now()</code>, <code>utcnow()</code>.",
      "time module: <code>time.time()</code>, <code>time.sleep(s)</code>, <code>ctime(ts)</code> → string, <code>gmtime(ts)</code>/<code>localtime(ts)</code> → struct_time, <code>asctime(st)</code> → string, <code>mktime(tuple)</code> → seconds.")
nb.table(["directive", "means", "directive", "means"],
         [["<code>%Y</code>", "2020", "<code>%y</code>", "20"], ["<code>%m</code>", "01 (month)", "<code>%B</code> / <code>%b</code>", "November / Nov"],
          ["<code>%d</code>", "04 (day)", "<code>%A</code> / <code>%a</code>", "Wednesday / Wed"],
          ["<code>%H</code>", "14 (24h)", "<code>%I</code> %p", "02 PM"], ["<code>%M</code>", "53 (minutes)", "<code>%S</code>", "00 (seconds)"]])
nb.heart("<code>strftime</code> = date → <b>string</b> (f = format). <code>strptime</code> = string → date (p = parse). "
         "date − date = <b>timedelta</b>; date + timedelta = date; date + date = <span class='r'>TypeError</span>.")
nb.ask("What is printed?", "from datetime import date\nd = date(2019, 11, 4)\nprint(d.weekday(), d.strftime('%Y/%m/%d'), d.replace(year=1992))", "0 2019/11/04 1992-11-04")
nb.ask("Course exercise 1: what is printed?", "from datetime import time\nt = time(14, 53)\nprint(t.strftime('%H:%M:%S'))", "14:53:00")
nb.ask("Course: what is printed?", "from datetime import datetime\ndt = datetime(2020, 11, 4, 14, 53)\nprint(dt.strftime('%y/%B/%d %H:%M:%S'))", "20/November/04 14:53:00")
nb.ask("Course exercise 2: what is printed?", "from datetime import datetime\ndt1 = datetime(2020, 9, 29, 14, 41, 0)\ndt2 = datetime(2020, 9, 28, 14, 41, 0)\nprint(dt1 - dt2)", "1 day, 0:00:00")
nb.ask("Course: what is printed?", "from datetime import date, timedelta\ndelta = timedelta(weeks=2, days=2, hours=3)\nprint(delta, '|', delta.days, delta.seconds)\nprint(date(2019, 10, 4) + delta * 2)",
       "16 days, 3:00:00 | 16 10800\n2019-11-05")
nb.ask("What is printed?", "from datetime import datetime\nprint(datetime.strptime('2019/11/04 14:53:00', '%Y/%m/%d %H:%M:%S'))", "2019-11-04 14:53:00")

# ---------------------------------------------------------------- 13
nb.h2("13. calendar <span class='tag'>course</span>")
nb.ul("<code>calendar.calendar(2020)</code> → string of the year (print it) · <code>prcal(2020)</code> prints it directly.",
      "<code>calendar.month(2020, 11)</code> / <code>prmonth(2020, 11)</code> → one month.",
      "Default first day = <b>Monday (0)</b>; change with <code>setfirstweekday(calendar.SUNDAY)</code>.",
      "<code>weekday(y, m, d)</code> → 0–6 · <code>weekheader(n)</code> → day names of width n (max 3 letters) · <code>isleap(y)</code> · <code>leapdays(y1, y2)</code> (y2 <b>excluded</b>).",
      "<code>Calendar(firstweekday=0)</code> class: <code>iterweekdays()</code>, <code>itermonthdates(y, m)</code> (full weeks: includes days of the previous/next month), <code>itermonthdays(y, m)</code> (0 for days outside the month), <code>monthdays2calendar(y, m)</code> (weeks of (day, weekday) tuples).")
nb.ask("What is printed?", "import calendar\nprint(calendar.weekday(2020, 12, 24), calendar.isleap(2020), calendar.leapdays(2010, 2021))", "3 True 3")
nb.ask("Course exercise 1: what is printed?", "import calendar\nprint(calendar.weekheader(1))", "M T W T F S S")
nb.ask("Course exercise 2: what is printed?", "import calendar\nc = calendar.Calendar()\nfor weekday in c.iterweekdays():\n    print(weekday, end=' ')", "0 1 2 3 4 5 6")
nb.ask("What is printed?", "import calendar\nc = calendar.Calendar(calendar.SUNDAY)\nprint(list(c.iterweekdays()))\nprint(calendar.weekheader(2))", "[6, 0, 1, 2, 3, 4, 5]\nMo Tu We Th Fr Sa Su",
       why="the Calendar <b>object</b> starts on Sunday, but the module-level <code>weekheader</code> still starts on Monday (only <code>setfirstweekday</code> changes that).")

# ---------------------------------------------------------------- self-test
nb.raw("<div class='chapter'></div>")
nb.selftest("Miscellaneous", [
    ("What is printed?", "def g(n):\n    for i in range(n):\n        yield i * 2\nprint(list(g(4)), sum(g(4)))", "", "[0, 2, 4, 6] 12"),
    ("What is printed?", "print([x * 2 if x > 1 else x for x in range(4)])", "", "[0, 1, 4, 6]"),
    ("What is printed?", "print([i + j for i in range(2) for j in range(2)])", "", "[0, 1, 1, 2]"),
    ("What is printed?", "print(list(map(lambda s: s[0], ['ab', 'cd'])))", "", "['a', 'c']"),
    ("What is printed?", "print(list(filter(lambda n: n % 2, range(6))))", "", "[1, 3, 5]"),
    ("What is printed?", "def tag(t):\n    def wrap(s):\n        return '<' + t + '>' + s\n    return wrap\nb = tag('b')\nprint(b('hi'))", "", "<b>hi"),
    ("What is printed?", "f = lambda *a: len(a)\nprint(f(), f(1, 2, 3))", "", "0 3"),
    ("Which mode opens a file for appending text, creating it if it doesn't exist?", None, "<code>'a'</code> (or <code>'at'</code>).", None),
    ("What does <code>readline()</code> return at the end of the file?", None, "An empty string <code>''</code>.", None),
    ("What is printed?", "b = bytearray(4)\nb[1] = 255\nprint(sum(b), len(b))", "", "255 4"),
    ("Which stream does <code>input()</code> read from?", None, "<code>sys.stdin</code>", None),
    ("What is printed?", "with open('n.txt', 'w') as f:\n    f.write('1\\n2\\n3')\nwith open('n.txt') as f:\n    print(len(f.readlines()))", "", "3"),
    ("What is printed?", "from datetime import date\nprint(date(2024, 3, 1) - date(2024, 2, 1))", "2024 is a leap year.", "29 days, 0:00:00"),
    ("What is printed?", "g = (x for x in 'ab')\nnext(g)\nprint(list(g))", "", "['b']"),
    ("What does the function returned by a closure remember?", None, "The values of the enclosing function's variables, even after that function has finished.", None),
])

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_5.pdf")
    finish()
