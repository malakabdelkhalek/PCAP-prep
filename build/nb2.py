from lib import NB

nb = NB(2, "Strings", "Course Module 2 (part 1) · exam section 3 (≈ 8 questions, 18%) · they ask → you answer",
        "PCAP Notebook 2 ~ Strings")

# ---------------------------------------------------------------- 1
nb.h2("1. Characters are numbers")
nb.ul("A computer stores every character as a number. Some are <b>whitespaces</b>, some are <b>control characters</b> (invisible, control devices).",
      "<b>code point</b> = the number that makes a character. Ex: 32 = space, 65 = 'A', 97 = 'a'.",
      "<b>ASCII</b> = most used code. Room for 256 chars, but the standard part is the <span class='y'>first 128</span> (Latin letters, digits, signs).",
      "<b>I18N</b> (internationalization: I + 18 letters + N) = software usable in every language/alphabet.",
      "<b>code page</b> = a standard that uses the upper 128 code points (128–255) for national characters → the <span class='r'>same code point can mean different characters</span> in different code pages.",
      "<b>Unicode</b> = the long-term solution: unique characters for <b>more than a million</b> code points. First 128 = ASCII; first 256 = ISO/IEC 8859-1 (Western Europe).",
      "Unicode only <b>names</b> characters; storing them is done by an encoding:")
nb.table(["encoding", "how it stores", "remember"],
         [["<b>UCS-4</b>", "<span class='y'>32 bits (4 bytes) for every char</span>", "Universal Character Set; simple, wastes space; may start with a BOM"],
          ["<b>UTF-8</b>", "<span class='y'>as many bits as needed</span> (1 to 4 bytes)", "Unicode Transformation Format; most used; ASCII chars take 8 bits"]])
nb.heart("<ul><li><b>BOM</b> (Byte Order Mark) = invisible bits at the start of a file announcing its encoding (UCS-4, UTF-8…).</li>"
         "<li>Python 3 is fully <b>I18Ned</b>: Unicode/UTF-8 in variable names and in all input/output.</li>"
         "<li><code>ord('a')</code> = 97 · <code>chr(97)</code> = 'a' · <code>ord('A')</code> = 65 · <code>ord(' ')</code> = 32 · <code>ord('0')</code> = 48.</li>"
         "<li>Uppercase letters have <b>smaller</b> codes than lowercase: 'Z' (90) &lt; 'a' (97).</li></ul>")
nb.ask("What is printed?", "print(ord('a'), ord(' '), chr(945), chr(65))", "97 32 α A")
nb.ask("What happens?", "print(ord('ab'))", "!TypeError", why="<code>ord()</code> needs a <b>one-character</b> string.")
nb.ask("What happens?", "print(chr(-1))", "!ValueError", why="invalid code point → ValueError (wrong type → TypeError).")
nb.ask("Course exercise 3: what is printed?", "for ch in \"abc\":\n    print(chr(ord(ch) + 1), end='')", "bcd")

# ---------------------------------------------------------------- 2
nb.h2("2. Strings are immutable sequences")
nb.ul("Multiline strings use triple quotes; the line break inside counts as <b>one</b> character <code>\\n</code>.",
      "Indexing <code>s[0]</code>, negative <code>s[-1]</code>, slices <code>s[1:4]</code>, <code>s[::-1]</code>, <code>for ch in s</code>: all work like lists.",
      "<code>+</code> concatenates (order matters, not commutative); <code>*</code> repeats (<code>'ab'*3</code> = <code>3*'ab'</code>).",
      "<code>in</code> / <code>not in</code> look for a <b>substring</b> anywhere: <code>'f' in 'abcdef'</code>.")
nb.heart("<b>Immutable</b> = you can never change a string in place:"
         "<ul><li><code>s[0] = 'X'</code> → <b>TypeError</b></li><li><code>del s[0]</code> → <b>TypeError</b> (but <code>del s</code> deletes the whole variable: OK)</li>"
         "<li><code>s.append('x')</code>, <code>s.insert(…)</code> → <b>AttributeError</b> (strings have no such methods)</li>"
         "<li>Every method (<code>upper</code>, <code>replace</code>…) returns a <span class='y'>new string</span>; the original stays the same.</li></ul>")
nb.ask("Course exercise 1: length of this string?", 'multiline = """\n"""\nprint(len(multiline))', "1",
       why="the only character is the invisible newline.")
nb.ask("What is printed?", 'multiline = """L1\nL2"""\nprint(len(multiline))', "5")
nb.ask("What happens?", "s = 'abc'\ns[0] = 'A'", "!TypeError")
nb.ask("What happens?", "s = 'abc'\ns.append('d')", "!AttributeError")
nb.ask("What is printed?", "s = 'hello'\ns.upper()\nprint(s)", "hello", why="<code>upper()</code> returned a new string that nobody stored.")
nb.ask("What is printed?", "s = 'silly walks'\nprint(s[-1], s[2:5], s[::-1], s[::3])", "s lly sklaw yllis slwk", why="<code>[::3]</code> takes indexes 0, 3, 6, 9 → s, l, w, k.")
nb.ask("What is printed?", "print('ab' * 2 + 'c', 3 * '-', '' * 5 == '')", "ababc --- True")
nb.ask("What happens?", "print('Score: ' + 10)", "!TypeError", why="no automatic conversion: write <code>str(10)</code>.")
nb.ask("What is printed?", "print('f' in 'abcdef', 'F' in 'abcdef', 'cd' in 'abcdef', '' in 'abc')", "True False True True",
       why="the empty string is in every string.")
nb.trap("<code>len('\\n')</code> = 1 (one escape char) but <code>len('\\\\n')</code> = 2 (backslash + n). A backslash at the very end of a string <code>'abc\\'</code> → SyntaxError.")
nb.ask("What is printed?", "print(len('\\n'), len('\\\\n'), len('a\\tb'))", "1 2 3")

# ---------------------------------------------------------------- 3
nb.h2("3. Sequence functions &amp; methods (lists too)")
nb.table(["tool", "does", "if not found / empty"],
         [["<code>min(s)</code> / <code>max(s)</code>", "smallest / biggest element (by code point)", "empty → <b>ValueError</b>"],
          ["<code>s.index(x)</code>", "index of the <b>first</b> x", "<b>ValueError</b>"],
          ["<code>s.count(x)</code>", "how many x", "0 (no error)"],
          ["<code>list(s)</code>", "list of the characters", "<code>list('')</code> = []"]])
nb.ask("What is printed?", "print(min('aAbByYzZ'), max('aAbByYzZ'))", "A z")
nb.ask("Course example: what is printed? (note the space!)", "t = 'The Knights Who Say \"Ni!\"'\nprint('[' + min(t) + ']')", "[ ]",
       why="the space (32) is the smallest code point in the string.")
nb.ask("What is printed?", "print('aAbByYzZaA'.index('b'), 'abcabc'.count('b'), 'abcabc'.count('d'))", "2 2 0")
nb.ask("Course exercise 2: what is printed?", "s = 'yesteryears'\nthe_list = list(s)\nprint(the_list[3:6])", "['t', 'e', 'r']")
nb.ask("What happens?", "print(max(''))", "!ValueError")

# ---------------------------------------------------------------- 4
nb.h2("4. String methods (all return NEW values)")
nb.h3("Changing case")
nb.table(["method", "example → result"],
         [["<code>capitalize()</code>", "<code>'aBcD'</code> → <code>'Abcd'</code> (1st char up only if it's a letter, rest lower)"],
          ["<code>title()</code>", "<code>'i KNOW that'</code> → <code>'I Know That'</code> (every word)"],
          ["<code>upper()</code> / <code>lower()</code>", "all up / all down"],
          ["<code>swapcase()</code>", "<code>'I know'</code> → <code>'i KNOW'</code>"]])
nb.ask("What is printed?", "print(' alpha'.capitalize(), '123abc'.capitalize(), 'ALPHA'.capitalize())", " alpha 123abc Alpha",
       why="the first character (index 0) is a space or a digit, so nothing goes up; the rest goes lower.")
nb.ask("What is printed?", "print('I know that I know nothing. Part 1.'.title())", "I Know That I Know Nothing. Part 1.")
nb.h3("Searching")
nb.table(["method", "returns", "not found"],
         [["<code>find(sub, start, end)</code>", "first index", "<span class='y'><b>-1</b></span> (strings only)"],
          ["<code>rfind(sub, start, end)</code>", "<b>last</b> index (searches from the right)", "-1"],
          ["<code>index(sub)</code> / <code>rindex(sub)</code>", "first / last index", "<span class='r'>ValueError</span>"],
          ["<code>startswith(x)</code> / <code>endswith(x)</code>", "True/False", "False"],
          ["<code>count(sub)</code>", "number of occurrences", "0"]])
nb.ask("What is printed?", "print('kappa'.find('a', 2), 'kappa'.find('z'), 'kappa'.find('a', 10))", "4 -1 -1",
       why="the start index may be outside the string, no error.")
nb.ask("Course example: what is printed?", "print('tau tau tau'.rfind('ta'))\nprint('tau tau tau'.rfind('ta', 9))\nprint('tau tau tau'.rfind('ta', 3, 9))",
       "8\n-1\n4")
nb.ask("What happens?", "print('kappa'.index('z'))", "!ValueError")
nb.ask("What is printed?", "print('zeta'.endswith('a'), 'omega'.startswith('meg'), 'omega'.startswith('meg', 1))", "True False True")
nb.h3("Checking content: isxxx()")
nb.table(["method", "True only if <i>every</i> char is…", "watch out"],
         [["<code>isalnum()</code>", "letter or digit", "space, '.', '@' → False"],
          ["<code>isalpha()</code>", "letter", "digits → False"],
          ["<code>isdigit()</code>", "digit", "<code>'20E1'</code>, <code>'-5'</code>, <code>'1.5'</code> → False"],
          ["<code>islower()</code> / <code>isupper()</code>", "lower / upper letters (non-letters ignored, ≥1 letter needed)", "<code>'Mary'.islower()</code> → False"],
          ["<code>isspace()</code>", "whitespace (space, \\n, \\t)", "<code>' \\n '</code> → True"]])
nb.heart("<b>Every isxxx() on the empty string <code>''</code> returns False.</b>")
nb.ask("What is printed?", "print('Moooo'.isalnum(), 'Mu40'.isalnum(), 'Mu 40'.isalnum(), ''.isalnum())", "True True False False")
nb.ask("What is printed?", "print('2018'.isdigit(), 'Year2019'.isdigit(), '-5'.isdigit())", "True False False")
nb.ask("What is printed?", "print('moose'.islower(), 'Moose'.islower(), 'abc123'.islower(), 'ABC 1'.isupper())", "True False True True",
       why="digits and spaces are ignored; only the letters are checked.")
nb.ask("What is printed?", "print(' \\n '.isspace(), ' '.isspace(), 'mo ose'.isspace())", "True True False")
nb.h3("Cutting, joining, replacing")
nb.table(["method", "example → result"],
         [["<code>split()</code>", "<code>'phi  chi\\npsi'.split()</code> → <code>['phi', 'chi', 'psi']</code> (any whitespace, empties dropped)"],
          ["<code>split(sep, maxsplit)</code>", "<code>'a,b,,c'.split(',')</code> → <code>['a', 'b', '', 'c']</code>"],
          ["<code>sep.join(list)</code>", "<code>','.join(['omicron','pi','rho'])</code> → <code>'omicron,pi,rho'</code>"],
          ["<code>strip() lstrip() rstrip()</code>", "remove whitespace both / left / right"],
          ["<code>lstrip(chars)</code>", "<code>'www.cisco.com'.lstrip('w.')</code> → <code>'cisco.com'</code> (removes a <b>set</b> of chars)"],
          ["<code>replace(old, new, n)</code>", "<code>'This is it!'.replace('is','are',1)</code> → <code>'Thare is it!'</code>"],
          ["<code>center(w, fill)</code>", "<code>'[' + 'alpha'.center(10) + ']'</code> → <code>'[  alpha   ]'</code>"]])
nb.trap("<ul><li><code>join</code> is called on the <b>separator</b>, and every element must be a <b>string</b>: <code>','.join([1, 2])</code> → TypeError.</li>"
        "<li><code>strip('xyz')</code> removes <b>characters</b> from that set, not the word 'xyz'.</li>"
        "<li><code>split(' ')</code> keeps empty strings, <code>split()</code> doesn't.</li></ul>")
nb.ask("What is printed?", "print('This is it!'.replace('is', 'are', 2))", "Thare are it!", why="'is' inside 'This' is replaced first.")
nb.ask("What is printed?", "print('pythoninstitute.org'.rstrip('.org'))\nprint('[' + '  tau  '.lstrip() + ']')", "pythoninstitute\n[tau  ]")
nb.ask("What is printed?", "print(' a  b '.split(), len(' a  b '.split(' ')))", "['a', 'b'] 5")
nb.ask("What is printed?", "print('-'.join('abc'), '[' + 'gamma'.center(20, '*') + ']')", "a-b-c [*******gamma********]",
       why="a string is a sequence, so <code>join</code> takes its characters.")
nb.ask("What happens?", "print(', '.join(['a', 1]))", "!TypeError")
nb.ask("What is printed?", "print('a,b,c'.split(',', 1))", "['a', 'b,c']")

# ---------------------------------------------------------------- 5
nb.h2("5. Comparing strings")
nb.ul("Compared <b>character by character</b> using code points; the first difference decides.",
      "If one string is the start of the other, the <b>shorter</b> is smaller: <code>'alpha' &lt; 'alphabet'</code>.",
      "Uppercase &lt; lowercase: <code>'beta' &gt; 'Beta'</code>. Digits &lt; uppercase &lt; lowercase.",
      "Digits in strings are compared as <b>text</b>, not as numbers: <code>'10' &lt; '8'</code> is True ('1' &lt; '8').")
nb.heart("<ul><li>string <code>==</code> number → always <b>False</b>; <code>!=</code> → always <b>True</b> (no error).</li>"
         "<li>string <code>&lt; &gt; &lt;= &gt;=</code> number → <span class='r'>TypeError</span>.</li></ul>")
nb.ask("What is printed?", "print('10' == '010', '10' > '010', '10' > '8', '20' < '80')", "False True False True")
nb.ask("What is printed?", "print('10' == 10, '10' != 10, '10' == 1)", "False True False")
nb.ask("What happens?", "print('10' > 10)", "!TypeError")
nb.ask("Course exercise 1: which are True?", "print('smith' > 'Smith')\nprint('Smiths' < 'Smith')\nprint('Smith' > '1000')\nprint('11' < '8')",
       "True\nFalse\nTrue\nTrue")

# ---------------------------------------------------------------- 6
nb.h2("6. Sorting: sorted() vs sort()")
nb.table(["", "<code>sorted(x)</code>", "<code>lst.sort()</code>"],
         [["kind", "function", "<b>list</b> method (strings have none)"],
          ["original", "unchanged", "<b>changed</b> in place"],
          ["returns", "a <b>new list</b>", "<span class='r'>None</span>"],
          ["works on", "any iterable (even a string → list of chars)", "lists only"]])
nb.ask("What is printed?", "lst = ['omega', 'alpha', 'pi', 'gamma']\nprint(lst.sort())\nprint(lst)", "None\n['alpha', 'gamma', 'omega', 'pi']")
nb.ask("What is printed?", "print(sorted('bca'), sorted(['b', 'B', 'a', 'A']))", "['a', 'b', 'c'] ['A', 'B', 'a', 'b']")
nb.ask("Course exercise 2: what is printed?", "s1 = 'Where are the snows of yesteryear?'\ns2 = s1.split()\ns3 = sorted(s2)\nprint(s3[1])", "are",
       why="'Where' starts with uppercase, so it comes first; then 'are'.")

# ---------------------------------------------------------------- 7
nb.h2("7. Strings ↔ numbers")
nb.ul("<code>str(x)</code> always works. <code>int('13')</code>, <code>float('1.3')</code>, <code>float('13')</code> work.",
      "<code>int('12.8')</code> → <span class='r'>ValueError</span> (int() won't read a dot). <code>int(12.8)</code> = 12 (a float is fine).")
nb.ask("Course exercise 3: what happens?", "s1 = '12.8'\ni = int(s1)\ns2 = str(i)\nf = float(s2)\nprint(s1 == s2)", "!ValueError")
nb.ask("What is printed?", "print(int(float('12.8')), float('13'), str(1.0) + '1')", "12 13.0 1.01")

# ---------------------------------------------------------------- self-test
nb.raw("<div class='chapter'></div>")
nb.selftest("Strings", [
    ("What is printed?", "s = 'abcdef'\nprint(s[1:-1:2])", "", "bd"),
    ("What is printed?", "print('Python'.find('th'), 'Python'.rfind('o'), 'Python'.find('Z'))", "", "2 4 -1"),
    ("What is printed?", "print(len('Hello\\tWorld\\n'))", "", "12"),
    ("What is printed?", "x = 'abc'\ny = x\nx += 'd'\nprint(x, y)", "<code>+=</code> builds a new string, <code>y</code> still points to the old one.", "abcd abc"),
    ("What is printed?", "print('ABC'.lower().isupper(), 'aBc'.swapcase())", "", "False AbC"),
    ("What is printed?", "print('$'.join(['a', 'b']).split('$'))", "", "['a', 'b']"),
    ("What is printed?", "print(sorted('Hello')[0])", "", "H"),
    ("What is printed?", "print('apple' < 'Apple', 'abc' < 'abcd', '9' > '10')", "", "False True True"),
    ("What happens?", "print('7' + 3)", "", "!TypeError"),
    ("What is printed?", "print('Mississippi'.count('ss'), 'Mississippi'.replace('ss', 'SS', 1))", "", "2 MiSSissippi"),
    ("How many bytes does UCS-4 use per character? And UTF-8?", None, "UCS-4: always <b>4</b>. UTF-8: <b>as many as needed</b> (1–4).", None),
    ("What is a code page?", None, "A standard that uses the upper 128 code points for national characters (same number, different char per code page).", None),
    ("What is printed?", "print(''.isdigit(), ' '.isspace(), 'A1'.isalnum())", "", "False True True"),
    ("What is printed?", "print('xxhixx'.strip('x'), 'banana'.lstrip('ab'))", "", "hi nana"),
    ("What is printed?", "print(chr(ord('Z') + 7))", "", "a"),
    ("What is printed?", "print(list('ab') * 2, 'ab'.center(4, '.'))", "", "['a', 'b', 'a', 'b'] .ab."),
])

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_2.pdf")
    finish()
