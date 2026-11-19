"""Teacher-mode whiteboards. Every ["run", ...] output and every "try" answer is checked
against real Python before export."""
import json, sys
sys.path.insert(0, ".")
from lib import run_snippet, norm

BOARDS, ERR = [], []


def check(code, out, where):
    got = norm(run_snippet(code.strip() + "\n"))
    if got != norm(out):
        ERR.append(f"{where}\n{code}\nexpected {out!r}\ngot {got!r}")


def board(bid, ch, t, title, steps):
    for i, st in enumerate(steps):
        for el in st.get("add", []):
            if el[0] == "run":
                setup = el[3] if len(el) > 3 else ""
                check(setup + "\n" + el[1], el[2], f"{bid} step {i+1}")
            if el[0] == "try":
                q = el[1]
                if q.get("code"):
                    check(q["code"], q["ok"], f"{bid} try")
                for b in q["bad"]:
                    if norm(b) == norm(q["ok"]):
                        ERR.append(f"{bid}: distractor == answer")
    BOARDS.append({"id": bid, "ch": ch, "t": t, "title": title, "steps": steps})


S = lambda say, *add: {"say": say, "add": list(add)}

STACK = """class Stack:
    def __init__(self):
        self.__stack_list = []
    def push(self, val):
        self.__stack_list.append(val)
    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val"""

ADDING = STACK + """
class AddingStack(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.__sum = 0
    def get_sum(self):
        return self.__sum
    def push(self, val):
        self.__sum += val
        Stack.push(self, val)
    def pop(self):
        val = Stack.pop(self)
        self.__sum -= val
        return val"""

# ---------------------------------------------------------------- OOP 1
board("oop1", "oop", "oop.basics", "Classes, objects & self", [
    S("Let's start with the big idea. A class is a recipe. An object is the cake you bake from that recipe. One recipe, as many cakes as you want.",
      ["h", "Class = recipe · Object = cake"],
      ["dia", {"w": 360, "h": 205, "items": [
          ["box", 110, 8, 140, 50, "class Stack", "blue", "the recipe"],
          ["box", 8, 140, 104, 44, "stack_1", "green"], ["box", 128, 140, 104, 44, "stack_2", "green"], ["box", 248, 140, 104, 44, "stack_3", "green"],
          ["arrow", 160, 60, 60, 136, "green"], ["arrow", 180, 60, 180, 136, "green", "Stack()"], ["arrow", 200, 60, 300, 136, "green"],
          ["text", 180, 200, "objects = instances", "muted", 15]]}]),
    S("Every object has three things. A name, so you can find it. Properties, which are its data. And methods, which are the things it can do.",
      ["w", "Every object has: {o:a name} + {b:properties} (data) + {g:methods} (actions)"]),
    S("Here is the Stack from your course. Look at __init__. That's the constructor. Python runs it automatically the moment you create an object, and it builds the object's properties.",
      ["code", STACK.split("    def pop")[0].rstrip(), {"0": "← the recipe", "1": "← runs when you create it", "2": "← creates a property"}]),
    S("Now the most important trick of the whole chapter: self. When you write stack_object dot push of 3, Python secretly rewrites it. The object goes into self, and 3 goes into val.",
      ["dia", {"w": 360, "h": 165, "items": [
          ["ctext", 180, 32, "stack_object.push(3)", "ink", 18],
          ["ctext", 180, 122, "Stack.push(stack_object, 3)", "ink", 18],
          ["arrow", 137, 44, 214, 104, "blue"], ["arrow", 272, 44, 306, 104, "orange"],
          ["text", 216, 156, "→ self", "blue", 16], ["text", 306, 156, "→ val", "orange", 16]]}]),
    S("That's why every method needs at least one parameter to receive the object. Forget self, and Python crashes with a TypeError.",
      ["run", "class A:\n    def show():\n        print('hi')\n\nA().show()", "!TypeError"],
      ["sticky", "Methods: {r:declare} WITH self · {g:call} WITHOUT it", "p"]),
    S("Each object keeps its own data. Here two stacks live side by side and never mix.",
      ["run", "a = Stack()\nb = Stack()\na.push(1)\na.push(2)\nb.push(9)\nprint(a.pop(), b.pop())", "2 9", STACK]),
    S("Your turn! Read it carefully, then pick the output.",
      ["try", {"q": "What is printed?", "code": "class P:\n    def __init__(self, x=2):\n        self.x = x\n\nprint(P().x + P(5).x)", "ok": "7", "bad": ["10", "5", "!TypeError"],
               "why": "P() uses the default x=2, P(5) gets x=5: 2 + 5 = 7."}]),
])

# ---------------------------------------------------------------- OOP 2
board("oop2", "oop", "oop.private", "Private names & name mangling", [
    S("Want to hide a property from the outside world? Start its name with two underscores. That makes it private.",
      ["w", "{r:__}name  →  private (hidden from outside the class)"],
      ["code", "class Stack:\n    def __init__(self):\n        self.__stack_list = []", {"2": "← two underscores"}]),
    S("From outside the class, Python pretends it doesn't exist. You get an AttributeError.",
      ["run", "obj = Stack()\nprint(obj.__stack_list)", "!AttributeError", "class Stack:\n    def __init__(self):\n        self.__stack_list = []"]),
    S("But here's the secret: it isn't really hidden. Python just renames it. It glues an underscore and the class name in front. This is called name mangling.",
      ["dia", {"w": 360, "h": 130, "items": [
          ["ctext", 180, 28, "self.__stack_list", "red", 18],
          ["arrow", 180, 42, 180, 88, "red", "Python renames it"],
          ["ctext", 180, 115, "self._Stack__stack_list", "green", 18]]}],
      ["w", "inside class {b:Stack}:  {o:__x}  becomes  {g:_Stack__x}"]),
    S("So if you use the renamed version, it works perfectly from outside.",
      ["run", "obj = Stack()\nprint(len(obj._Stack__stack_list))", "0", "class Stack:\n    def __init__(self):\n        self.__stack_list = []"]),
    S("Exam trap! Mangling only happens for names written INSIDE the class. If you create a double-underscore name from outside, it keeps its name exactly.",
      ["run", "class E:\n    def __init__(self):\n        self.__a = 1\n\ne = E()\ne.__b = 2\nprint(e.__dict__)", "{'_E__a': 1, '__b': 2}"],
      ["sticky", "{r:__a} written inside → {g:_E__a}\n{r:__b} written outside → stays {r:__b}", "y"]),
    S("Private methods work exactly the same way: two underscores, and they get renamed too.",
      ["run", "class Classy:\n    def __hidden(self):\n        print('hidden')\n\nobj = Classy()\nobj._Classy__hidden()", "hidden"]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class A:\n    def __init__(self):\n        self.__p = 5\n\na = A()\nprint(hasattr(a, '__p'), hasattr(a, '_A__p'))", "ok": "False True",
               "bad": ["True False", "True True", "False False"], "why": "Inside class A, __p was stored as _A__p."}]),
])

# ---------------------------------------------------------------- OOP 3
CEX = "class ExampleClass:\n    counter = 0\n    def __init__(self, val = 1):\n        self.__first = val\n        ExampleClass.counter += 1"
board("oop3", "oop", "oop.classvar", "Class variables vs instance variables", [
    S("Instance variables belong to ONE object. You create them with self dot something, so every object gets its own copy.",
      ["dia", {"w": 360, "h": 100, "items": [
          ["box", 20, 14, 140, 68, "obj_1", "green", "first = 1"], ["box", 200, 14, 140, 68, "obj_2", "green", "first = 2"]]}]),
    S("A class variable is written directly in the class body, outside any method. There is only ONE copy, and every object shares it.",
      ["code", CEX, {"1": "← class variable", "3": "← instance variable", "4": "← changes the ONE copy"}],
      ["dia", {"w": 360, "h": 205, "items": [
          ["box", 100, 8, 160, 58, "ExampleClass", "blue", "counter = 3"],
          ["box", 8, 146, 100, 44, "obj_1", "green"], ["box", 130, 146, 100, 44, "obj_2", "green"], ["box", 252, 146, 100, 44, "obj_3", "green"],
          ["arrow", 58, 144, 140, 70, "blue"], ["arrow", 180, 144, 180, 70, "blue", "shared"], ["arrow", 302, 144, 220, 70, "blue"]]}]),
    S("That's why every object reads the same value. Three objects were created, so counter is 3 for everyone.",
      ["run", "o1 = ExampleClass()\no2 = ExampleClass(2)\no3 = ExampleClass(4)\nprint(o1.counter, o3.counter, ExampleClass.counter)", "3 3 3", CEX]),
    S("Now the biggest trap of this chapter. Writing through an object does NOT change the class variable. It creates a NEW instance variable that hides the class one, only for that object.",
      ["run", "class C:\n    n = 1\n\na = C()\nb = C()\na.n = 5\nC.n = 7\nprint(a.n, b.n, C.n)", "5 7 7"],
      ["dia", {"w": 360, "h": 205, "items": [
          ["box", 110, 8, 140, 52, "class C", "blue", "n = 7"],
          ["box", 30, 128, 120, 56, "a", "green", "n = 5"], ["circle", 90, 168, 42, 15, "red"],
          ["text", 90, 200, "own n hides C.n!", "red", 14],
          ["box", 210, 128, 120, 56, "b", "green", "(no own n)"], ["arrow", 270, 126, 220, 64, "blue", "reads C.n"]]}]),
    S("__dict__ shows only an object's OWN variables. Class variables live in the class's __dict__.",
      ["run", "print(a.__dict__, b.__dict__, 'n' in C.__dict__)", "{'n': 5} {} True", "class C:\n    n = 1\n\na = C()\nb = C()\na.n = 5\nC.n = 7"]),
    S("Careful with lists. dot append changes the one shared list. No new variable is created, so everyone sees the change.",
      ["run", "class Team:\n    members = []\n\nt1 = Team()\nt2 = Team()\nt1.members.append('Malak')\nprint(t2.members)", "['Malak']"],
      ["sticky", "{r:obj.x = …} → new instance variable\n{g:obj.list.append(…)} → changes the shared one", "y"]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class K:\n    count = 0\n    def __init__(self):\n        K.count += 1\n        self.count = 10\n\nk1 = K()\nk2 = K()\nprint(K.count, k1.count)", "ok": "2 10",
               "bad": ["10 10", "2 2", "0 10"], "why": "K.count counts the objects (2); self.count = 10 creates an instance variable that hides it."}]),
])

# ---------------------------------------------------------------- OOP 4
board("oop4", "oop", "oop.intro", "Looking inside: hasattr, __dict__, __name__, __bases__", [
    S("Reading a property that doesn't exist crashes with AttributeError. In this course example, the object only gets a OR b, depending on the value.",
      ["run", "class ExampleClass:\n    def __init__(self, val):\n        if val % 2 != 0:\n            self.a = 1\n        else:\n            self.b = 1\n\nobj = ExampleClass(1)\nprint(obj.a)\nprint(obj.b)", "1\n!AttributeError"]),
    S("So ask first, with hasattr. Give it the object or the class, and the name as a STRING, in quotes.",
      ["run", "class ExampleClass:\n    a = 1\n    def __init__(self):\n        self.b = 2\n\nobj = ExampleClass()\nprint(hasattr(obj, 'b'), hasattr(obj, 'a'))\nprint(hasattr(ExampleClass, 'b'), hasattr(ExampleClass, 'a'))", "True True\nFalse True"],
      ["sticky", "class var → visible from objects {g:✓}\ninstance var → NOT visible from the class {r:✗}", "b"]),
    S("Every class carries a few built-in labels. Learn these three.",
      ["w", "{b:Class.__name__}  →  'Classy'  (the name, a string)"],
      ["w", "{b:obj.__module__}  →  '__main__'  (where it was defined)"],
      ["w", "{b:Class.__bases__}  →  (object,)  (a {o:tuple} of parent classes)"]),
    S("Trap! Objects don't have __name__. Only classes do. To get the class name from an object, use type of the object, dot __name__.",
      ["run", "class Classy:\n    pass\n\nobj = Classy()\nprint(Classy.__name__, type(obj).__name__)\nprint(obj.__name__)", "Classy Classy\n!AttributeError"]),
    S("__bases__ gives a tuple of the direct parents, in the order you wrote them. No parent written? Then the parent is object, because everything inherits from object.",
      ["run", "class A: pass\nclass B: pass\nclass C(A, B): pass\nprint([k.__name__ for k in C.__bases__], A.__bases__[0].__name__)", "['A', 'B'] object"]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class A:\n    x = 1\n    def __init__(self):\n        self.y = 2\n\nprint('x' in A.__dict__, 'y' in A().__dict__, 'x' in A().__dict__)", "ok": "True True False",
               "bad": ["True True True", "False True False", "True False False"], "why": "x lives in the class's __dict__; y in each object's; an object's __dict__ never lists class variables."}]),
])

# ---------------------------------------------------------------- OOP 5
board("oop5", "oop", "oop.inherit", "Inheritance & super()", [
    S("Inheritance: a new class, the subclass, gets everything from an existing class, the superclass. Then it can add things or change them. In diagrams, arrows go from the subclass UP to the superclass.",
      ["dia", {"w": 360, "h": 170, "items": [
          ["box", 110, 8, 140, 52, "Stack", "blue", "superclass"], ["box", 110, 110, 140, 52, "AddingStack", "green", "subclass"],
          ["arrow", 180, 108, 180, 64, "red", "inherits from"]]}],
      ["w", "class {g:AddingStack}({b:Stack}):   ← parent goes in the brackets"]),
    S("Important: Python does NOT call the parent's constructor for you. You must do it yourself, first thing in your own __init__.",
      ["code", "class AddingStack(Stack):\n    def __init__(self):\n        Stack.__init__(self)\n        self.__sum = 0", {"2": "← don't forget this!"}]),
    S("Forget it, and the parent's properties are never created.",
      ["run", "class Base:\n    def __init__(self):\n        self.items = []\n\nclass Child(Base):\n    def __init__(self):\n        self.n = 0\n\nc = Child()\nc.items.append(1)", "!AttributeError"]),
    S("Two ways to call the parent. Through the class name, you must pass self yourself. Through super, you don't pass self.",
      ["w", "Stack.push({r:self}, val)    ← class name: {r:WITH self}"],
      ["w", "super().push(val)          ← super(): {g:NO self}"]),
    S("Overriding means the subclass writes a method with the same name. Python uses the subclass version first. Here AddingStack's push also keeps a running sum.",
      ["run", "stack_object = AddingStack()\nfor i in range(5):\n    stack_object.push(i)\nprint(stack_object.get_sum())\nfor i in range(5):\n    print(stack_object.pop(), end=' ')", "10\n4 3 2 1 0", ADDING]),
    S("Methods you don't override are simply inherited. Sub has no __str__ here, so Super's is used.",
      ["run", "class Super:\n    def __init__(self, name):\n        self.name = name\n    def __str__(self):\n        return \"My name is \" + self.name + \".\"\n\nclass Sub(Super):\n    def __init__(self, name):\n        super().__init__(name)\n\nprint(Sub(\"Andy\"))", "My name is Andy."]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class P:\n    def __init__(self, n):\n        self.n = n\n\nclass Q(P):\n    def __init__(self):\n        super().__init__(7)\n        self.m = 1\n\nq = Q()\nprint(q.n + q.m)", "ok": "8",
               "bad": ["7", "!TypeError", "!AttributeError"], "why": "super().__init__(7) sets n = 7, then m = 1."}]),
])

# ---------------------------------------------------------------- OOP 6
VEH = "class Vehicle: pass\nclass LandVehicle(Vehicle): pass\nclass TrackedVehicle(LandVehicle): pass"
board("oop6", "oop", "oop.inherit", "issubclass, isinstance, is", [
    S("Three tools that look alike but answer three different questions. Let's take them one by one.",
      ["w", "{b:issubclass}(Class, Class) · {g:isinstance}(object, Class) · a {o:is} b"]),
    S("issubclass of A, B asks: is class A below B in the family tree? And yes, every class is a subclass of itself!",
      ["dia", {"w": 300, "h": 212, "items": [
          ["box", 75, 6, 150, 42, "Vehicle", "blue"], ["box", 75, 86, 150, 42, "LandVehicle", "blue"], ["box", 75, 166, 150, 42, "TrackedVehicle", "blue"],
          ["arrow", 150, 84, 150, 52, "ink"], ["arrow", 150, 164, 150, 132, "ink"]]}],
      ["run", "print(issubclass(TrackedVehicle, Vehicle), issubclass(Vehicle, TrackedVehicle), issubclass(Vehicle, Vehicle))", "True False True", VEH]),
    S("isinstance of an object and a class asks: was this object made from that class, or from one of its children?",
      ["run", "l = LandVehicle()\nprint(isinstance(l, Vehicle), isinstance(l, TrackedVehicle), isinstance(l, object))", "True False True", VEH]),
    S("is checks whether two names point to the very SAME object in memory. Double equals compares values instead. Here object_3 is just a second name for object_1.",
      ["dia", {"w": 360, "h": 150, "items": [
          ["ctext", 62, 30, "object_1", "ink", 16], ["ctext", 62, 76, "object_3", "ink", 16], ["ctext", 62, 128, "object_2", "ink", 16],
          ["box", 200, 18, 140, 52, "SampleClass", "green", "val = 1"], ["box", 200, 98, 140, 46, "SampleClass", "green", "val = 2"],
          ["arrow", 112, 30, 196, 40, "blue"], ["arrow", 112, 76, 196, 56, "blue"], ["arrow", 112, 128, 196, 124, "blue"]]}],
      ["run", "class SampleClass:\n    def __init__(self, val):\n        self.val = val\n\nobject_1 = SampleClass(0)\nobject_2 = SampleClass(2)\nobject_3 = object_1\nobject_3.val += 1\nprint(object_1 is object_2, object_3 is object_1)\nprint(object_1.val, object_2.val, object_3.val)", "False True\n1 2 1"]),
    S("Here's the summary to remember.",
      ["sticky", "{b:issubclass} → two classes\n{g:isinstance} → object + class\n{o:is} → same object in memory?", "y"]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class A: pass\nclass B(A): pass\n\nb = B()\nprint(isinstance(b, A), issubclass(A, B), b is B())", "ok": "True False False",
               "bad": ["True True False", "True False True", "False False False"], "why": "b is a B, so also an A; A is the parent, not the child; B() makes a brand-new object."}]),
])

# ---------------------------------------------------------------- OOP 7
board("oop7", "oop", "oop.mro", "Multiple inheritance & the MRO", [
    S("When you ask for an attribute, Python searches from the bottom up: the object, its class, then the parents. It stops at the FIRST match and never looks higher.",
      ["dia", {"w": 360, "h": 215, "items": [
          ["box", 100, 8, 160, 48, "Level1", "muted", "var = 100"], ["box", 100, 84, 160, 48, "Level2", "blue", "var = 200"], ["box", 100, 160, 160, 48, "Level3", "blue", "(nothing)"],
          ["arrow", 180, 158, 180, 136, "ink"], ["arrow", 180, 82, 180, 60, "ink"],
          ["num", 80, 184, "1", "red"], ["num", 80, 108, "2", "red"],
          ["text", 268, 112, "found! stop", "green", 15, "start"], ["text", 268, 36, "never checked", "muted", 14, "start"]]}],
      ["run", "class Level1:\n    var = 100\n    def fun(self):\n        return 101\nclass Level2(Level1):\n    var = 200\n    def fun(self):\n        return 201\nclass Level3(Level2):\n    pass\n\nobj = Level3()\nprint(obj.var, obj.fun())", "200 201"]),
    S("With two parents, Python searches left to right, in the order you wrote them in the brackets.",
      ["dia", {"w": 360, "h": 170, "items": [
          ["box", 20, 10, 140, 52, "Left", "blue", "var = 'L'"], ["box", 200, 10, 140, 52, "Right", "blue", "var = 'R'"],
          ["box", 100, 110, 160, 52, "Sub(Left, Right)", "green"],
          ["arrow", 150, 108, 90, 66, "ink"], ["arrow", 210, 108, 270, 66, "ink"],
          ["num", 100, 110, "1", "red"], ["num", 20, 10, "2", "red"], ["num", 200, 10, "3", "red"]]}],
      ["run", "class Left:\n    var = 'L'\n    var_left = 'LL'\nclass Right:\n    var = 'R'\n    var_right = 'RR'\nclass Sub(Left, Right):\n    pass\n\nobj = Sub()\nprint(obj.var, obj.var_left, obj.var_right)", "L LL RR"]),
    S("Now the famous diamond. B and C both inherit from A, and D inherits from both. Python checks D, then B, then C, and A only at the very end, after BOTH B and C.",
      ["dia", {"w": 360, "h": 260, "items": [
          ["box", 120, 8, 120, 50, "A", "blue", "hi → 'A'"], ["box", 16, 104, 124, 50, "B(A)", "blue", "(no hi)"], ["box", 220, 104, 124, 50, "C(A)", "blue", "hi → 'C'"],
          ["box", 120, 202, 120, 50, "D(B, C)", "green"],
          ["arrow", 150, 200, 90, 158, "ink"], ["arrow", 210, 200, 270, 158, "ink"], ["arrow", 90, 102, 150, 62, "ink"], ["arrow", 270, 102, 210, 62, "ink"],
          ["num", 120, 202, "1", "red"], ["num", 16, 104, "2", "red"], ["num", 220, 104, "3", "red"], ["num", 120, 8, "4", "red"]]}],
      ["run", "class A:\n    def hi(self): return 'A'\nclass B(A):\n    pass\nclass C(A):\n    def hi(self): return 'C'\nclass D(B, C):\n    pass\n\nprint(D().hi())\nprint([k.__name__ for k in D.__mro__])", "C\n['D', 'B', 'C', 'A', 'object']"],
      ["w", "This search order is the {o:MRO}: Method Resolution Order → {b:D.__mro__}"]),
    S("If you write an impossible order, like a parent BEFORE its own child, Python refuses to even create the class: TypeError.",
      ["run", "class Top:\n    pass\nclass Middle(Top):\n    pass\nclass Bottom(Top, Middle):\n    pass", "!TypeError"],
      ["sticky", "class Bottom({r:Top}, Middle) ✗  → Top is Middle's parent!\nclass Bottom(Middle, Top) {g:✓}", "p"]),
    S("Your turn!",
      ["try", {"q": "What is printed?", "code": "class A:\n    x = 'A'\nclass B(A):\n    pass\nclass C(A):\n    x = 'C'\nclass D(B, C):\n    pass\n\nprint(D.x)", "ok": "C",
               "bad": ["A", "B", "!TypeError"], "why": "MRO is D, B, C, A: B has no x, so C's x is found before A's."}]),
])

# ---------------------------------------------------------------- OOP 8
board("oop8", "oop", "oop.poly", "Polymorphism & __str__", [
    S("Polymorphism means: the same method call does different things depending on the object. Watch doanything. It's written only in One, but it calls self dot do_it.",
      ["run", "class One:\n    def do_it(self):\n        print(\"do_it from One\")\n    def doanything(self):\n        self.do_it()\n\nclass Two(One):\n    def do_it(self):\n        print(\"do_it from Two\")\n\nOne().doanything()\nTwo().doanything()", "do_it from One\ndo_it from Two"]),
    S("When the object is a Two, self is a Two, so Two's do_it runs. It doesn't matter where the code was written. The OBJECT decides.",
      ["dia", {"w": 360, "h": 150, "items": [
          ["ctext", 180, 26, "self.do_it()", "ink", 18],
          ["arrow", 150, 40, 80, 96, "blue", ""], ["arrow", 210, 40, 280, 96, "green", ""],
          ["box", 10, 100, 140, 44, "self is One", "blue"], ["box", 210, 100, 140, 44, "self is Two", "green"],
          ["text", 80, 66, "One.do_it", "blue", 14, "end"], ["text", 282, 66, "Two.do_it", "green", 14, "start"]]}]),
    S("Next, __str__. It decides what print of an object shows. Without it you get an ugly memory address.",
      ["run", "class Star:\n    def __init__(self, name, galaxy):\n        self.name = name\n        self.galaxy = galaxy\n    def __str__(self):\n        return self.name + ' in ' + self.galaxy\n\nprint(Star(\"Sun\", \"Milky Way\"))", "Sun in Milky Way"]),
    S("Trap: __str__ must RETURN a string. Return a number and print crashes with TypeError.",
      ["run", "class A:\n    def __str__(self):\n        return 42\n\nprint(A())", "!TypeError"],
      ["sticky", "print(obj) → calls obj.__str__() → must {r:return a str}", "y"]),
    S("Your turn! This one mixes both ideas.",
      ["try", {"q": "What is printed?", "code": "class Animal:\n    def __str__(self):\n        return self.sound()\n    def sound(self):\n        return '...'\n\nclass Cat(Animal):\n    def sound(self):\n        return 'Meow'\n\nprint(Cat(), Animal())", "ok": "Meow ...",
               "bad": ["... ...", "Meow Meow", "!TypeError"], "why": "Cat inherits __str__, but self.sound() runs Cat's version: polymorphism."}]),
])

if __name__ == "__main__":
    if ERR:
        print("\n\n".join(ERR)); sys.exit(1)
    json.dump(BOARDS, open("../app/boards.json", "w"))
    print(len(BOARDS), "boards,", sum(len(b["steps"]) for b in BOARDS), "steps, all verified")
