from lib import NB

nb = NB(4, "Object-Oriented Programming", "Course Module 3 · exam section 4 (≈ 12 questions, 34% — the biggest!) · they ask → you answer",
        "PCAP Notebook 4 ~ OOP")

# ---------------------------------------------------------------- 1
nb.h2("1. Vocabulary")
nb.table(["word", "meaning"],
         [["<b>class</b>", "an idea / a recipe used to create objects. <code>class Name: …</code>"],
          ["<b>object</b> (instance)", "one incarnation of a class (the cake from the recipe). <code>obj = Name()</code>"],
          ["<b>property / attribute</b>", "data stored in the object or class (a variable)"],
          ["<b>method</b>", "a function inside a class (an activity)"],
          ["<b>encapsulation</b>", "hiding data inside the object (private names, <code>__x</code>)"],
          ["<b>inheritance</b>", "a new class (<b>subclass</b>) gets everything from an existing one (<b>superclass</b>) and can add/change things"],
          ["<b>polymorphism</b>", "a subclass changes a superclass behaviour; same method name, different forms"],
          ["<b>overriding</b>", "redefining in the subclass a method that exists in the superclass"]])
nb.ul("Each object has: a <b>name</b> (identifies it), a set of <b>properties</b> (can be empty), a set of <b>methods</b> (can be empty).",
      "Inheritance diagram: superclasses <b>above</b>, arrows go <b>from subclass to superclass</b>.",
      "<b>Procedural</b> approach: data and functions separate (e.g. a global list + push/pop functions). <b>Object</b> approach: data + methods packed together in a class → several independent stacks, hidden data, reuse by inheritance.")

# ---------------------------------------------------------------- 2
nb.h2("2. The Stack: constructor, self, private")
nb.code("""
class Stack:
    def __init__(self):                # constructor
        self.__stack_list = []         # private property
    def push(self, val):
        self.__stack_list.append(val)
    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val

stack_object = Stack()                 # create an object
stack_object.push(3)                   # Python sends stack_object as self
""")
nb.heart("<ul><li>The constructor is <b>always</b> named <code>__init__</code>; it runs automatically when you create the object; it builds the object's properties.</li>"
         "<li>Every method needs <b>at least one parameter</b>, conventionally <code>self</code> = the object it is called on. You <b>never</b> pass self yourself when calling <code>obj.method()</code>.</li>"
         "<li>A property is <b>created</b> the first time you assign it: <code>self.x = …</code>.</li>"
         "<li>Name starting with <code>__</code> (and not ending with <code>__</code>) = <span class='y'>private</span>: <code>obj.__stack_list</code> from outside → <b>AttributeError</b>.</li>"
         "<li>Public name: no leading <code>__</code>, at most one trailing <code>_</code>.</li></ul>")
nb.ask("What happens?", "class Stack:\n    def __init__(self):\n        self.__stack_list = []\n\nstack_object = Stack()\nprint(len(stack_object.__stack_list))", "!AttributeError")
nb.ask("Course example: what is printed?", """
class Stack:
    def __init__(self):
        self.__stack_list = []
    def push(self, val):
        self.__stack_list.append(val)
    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val

little_stack = Stack()
another_stack = Stack()
funny_stack = Stack()
little_stack.push(1)
another_stack.push(little_stack.pop() + 1)
funny_stack.push(another_stack.pop() - 2)
print(funny_stack.pop())
""", "0", why="1 → 1+1 = 2 → 2-2 = 0. Each object has its own list.")
nb.ask("What happens?", "class A:\n    def show():\n        print('hi')\n\nA().show()", "!TypeError",
       why="Python passes the object automatically, but <code>show</code> has no parameter to receive it.")

# ---------------------------------------------------------------- 3
nb.h2("3. Subclass: AddingStack")
nb.code("""
class AddingStack(Stack):              # AddingStack inherits from Stack
    def __init__(self):
        Stack.__init__(self)           # MUST call the superclass constructor
        self.__sum = 0
    def get_sum(self):
        return self.__sum
    def push(self, val):               # overriding
        self.__sum += val
        Stack.push(self, val)          # call the superclass version
    def pop(self):
        val = Stack.pop(self)
        self.__sum -= val
        return val
""")
nb.heart("<ul><li>Python does <b>not</b> call the superclass constructor for you: forget <code>Stack.__init__(self)</code> and the object has no <code>__stack_list</code>.</li>"
         "<li>Calling through the class name <code>Stack.push(self, val)</code> → you must pass <b>self</b> explicitly. "
         "With <code>super()</code>: <code>super().push(val)</code> → <b>no self</b>.</li>"
         "<li>Interface (method names) stays the same, implementation changes = overriding.</li></ul>")
nb.ask("Course example: what is printed?", """
class Stack:
    def __init__(self):
        self.__stack_list = []
    def push(self, val):
        self.__stack_list.append(val)
    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val

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
        return val

stack_object = AddingStack()
for i in range(5):
    stack_object.push(i)
print(stack_object.get_sum())
for i in range(5):
    print(stack_object.pop(), end=' ')
""", "10\n4 3 2 1 0")
nb.ask("What happens?", "class Base:\n    def __init__(self):\n        self.items = []\n\nclass Child(Base):\n    def __init__(self):\n        self.n = 0\n\nc = Child()\nc.items.append(1)", "!AttributeError",
       why="Child's constructor never called Base's, so <code>items</code> was never created.")

# ---------------------------------------------------------------- 4
nb.h2("4. Instance variables &amp; __dict__")
nb.ul("Instance variables belong to <b>one object</b>; different objects of the same class can have <b>different sets</b> of variables.",
      "You can add one anytime, even from outside: <code>obj.third = 5</code>.",
      "<code>obj.__dict__</code> = a <span class='y'>dictionary of the object's instance variables</span> (name → value).")
nb.ask("Course example: what is printed?", """
class ExampleClass:
    def __init__(self, val = 1):
        self.first = val
    def set_second(self, val):
        self.second = val

example_object_1 = ExampleClass()
example_object_2 = ExampleClass(2)
example_object_2.set_second(3)
example_object_3 = ExampleClass(4)
example_object_3.third = 5
print(example_object_1.__dict__)
print(example_object_2.__dict__)
print(example_object_3.__dict__)
""", "{'first': 1}\n{'first': 2, 'second': 3}\n{'first': 4, 'third': 5}")

# ---------------------------------------------------------------- 5
nb.h2("5. Name mangling (\"private\" is not really private)")
nb.heart("Inside a class, <code>__name</code> becomes <code>_ClassName__name</code>. "
         "So <code>obj._ExampleClass__first</code> <b>works</b> from outside. "
         "<span class='r'>But</span> a <code>__name</code> created <b>outside</b> the class (<code>obj.__third = 5</code>) is <b>not</b> mangled. Methods <code>__m()</code> are mangled the same way.")
nb.ask("Course example: what is printed?", """
class ExampleClass:
    def __init__(self, val = 1):
        self.__first = val
    def set_second(self, val = 2):
        self.__second = val

example_object_1 = ExampleClass()
example_object_2 = ExampleClass(2)
example_object_2.set_second(3)
example_object_3 = ExampleClass(4)
example_object_3.__third = 5
print(example_object_1.__dict__)
print(example_object_2.__dict__)
print(example_object_3.__dict__)
print(example_object_1._ExampleClass__first)
""", "{'_ExampleClass__first': 1}\n{'_ExampleClass__first': 2, '_ExampleClass__second': 3}\n{'_ExampleClass__first': 4, '__third': 5}\n1")
nb.ask("Course example: what is printed?", """
class Classy:
    def visible(self):
        print("visible")
    def __hidden(self):
        print("hidden")

obj = Classy()
obj.visible()
try:
    obj.__hidden()
except:
    print("failed")
obj._Classy__hidden()
""", "visible\nfailed\nhidden")

# ---------------------------------------------------------------- 6
nb.h2("6. Class variables")
nb.ul("Defined in the class body (outside methods): <span class='y'>one single copy shared by all objects</span>; exists even before any object is created.",
      "Not shown in <code>obj.__dict__</code>, but shown in <code>ClassName.__dict__</code>.",
      "Read it through the class or through any object: <code>ExampleClass.counter</code> or <code>obj.counter</code>.")
nb.trap("<b>Writing</b> through an object <code>obj.counter = 9</code> does NOT change the class variable: it <b>creates an instance variable</b> with the same name that hides the class one (for that object only). "
        "To change the shared value write <code>ClassName.counter = …</code>. But a <b>mutable</b> class variable (list) changed with <code>.append()</code> is shared by everyone.")
nb.ask("Course example: what is printed?", """
class ExampleClass:
    counter = 0
    def __init__(self, val = 1):
        self.__first = val
        ExampleClass.counter += 1

example_object_1 = ExampleClass()
example_object_2 = ExampleClass(2)
example_object_3 = ExampleClass(4)
print(example_object_1.__dict__, example_object_1.counter)
print(example_object_3.__dict__, example_object_3.counter)
""", "{'_ExampleClass__first': 1} 3\n{'_ExampleClass__first': 4} 3")
nb.ask("What is printed?", """
class C:
    n = 1
a = C()
b = C()
a.n = 5
C.n = 7
print(a.n, b.n, C.n, a.__dict__)
""", "5 7 7 {'n': 5}")
nb.ask("What is printed?", """
class Team:
    members = []
t1 = Team()
t2 = Team()
t1.members.append('Malak')
print(t2.members)
""", "['Malak']", why="<code>append</code> changes the one shared list; no new instance variable is created.")
nb.ask("Course example: what is printed?", """
class ExampleClass:
    varia = 1
    def __init__(self, val):
        ExampleClass.varia = val

example_object = ExampleClass(2)
print(ExampleClass.__dict__['varia'], example_object.__dict__)
""", "2 {}")

# ---------------------------------------------------------------- 7
nb.h2("7. Does it exist? hasattr()")
nb.ul("Reading an attribute that doesn't exist → <b>AttributeError</b>.",
      "<code>hasattr(obj_or_class, 'name')</code> → True/False. The name is a <span class='y'>string</span>.",
      "A class var is visible from the object (<code>hasattr(obj, 'a')</code> True), but an instance var is not visible from the class.")
nb.ask("Course example: what is printed?", """
class ExampleClass:
    a = 1
    def __init__(self):
        self.b = 2

example_object = ExampleClass()
print(hasattr(example_object, 'b'))
print(hasattr(example_object, 'a'))
print(hasattr(ExampleClass, 'b'))
print(hasattr(ExampleClass, 'a'))
""", "True\nTrue\nFalse\nTrue")
nb.ask("Course example: what happens?", """
class ExampleClass:
    def __init__(self, val):
        if val % 2 != 0:
            self.a = 1
        else:
            self.b = 1

example_object = ExampleClass(1)
print(example_object.a)
print(example_object.b)
""", "1\n!AttributeError")

# ---------------------------------------------------------------- 8
nb.h2("8. Methods in detail")
nb.ul("A method may be <b>called</b> without arguments, but never <b>declared</b> without a parameter (self).",
      "Extra parameters go after self: <code>def method(self, par)</code> → call <code>obj.method(1)</code>.",
      "Through <code>self</code> a method reads instance and class variables (<code>self.varia</code>) and calls other methods (<code>self.other()</code>).",
      "Constructors are functions: they can have default values: <code>def __init__(self, value=None)</code>.")
nb.ask("Course example: what is printed?", """
class Classy:
    varia = 2
    def method(self):
        print(self.varia, self.var)

obj = Classy()
obj.var = 3
obj.method()
""", "2 3")
nb.ask("What is printed?", """
class Classy:
    def __init__(self, value=None):
        self.var = value

obj_1 = Classy("object")
obj_2 = Classy()
print(obj_1.var, obj_2.var)
""", "object None")
nb.ask("What is printed?", """
class Classy:
    def other(self):
        return "other"
    def method(self):
        return "method+" + self.other()

obj = Classy()
print(obj.method(), Classy.method(obj))
""", "method+other method+other", why="<code>Classy.method(obj)</code> = <code>obj.method()</code> (self passed by hand).")

# ---------------------------------------------------------------- 9
nb.h2("9. Introspection: __name__, __module__, __bases__, type()")
nb.table(["attribute", "on a class", "on an object"],
         [["<code>__dict__</code>", "class vars + methods", "instance vars"],
          ["<code>__name__</code>", "class name (string)", "<span class='r'>AttributeError</span> → use <code>type(obj).__name__</code>"],
          ["<code>__module__</code>", "module name of the definition (<code>'__main__'</code> for the run file)", "works too (read from the class)"],
          ["<code>__bases__</code>", "<b>tuple of classes</b> (not names) = direct superclasses, in order", "<span class='r'>AttributeError</span>"]])
nb.heart("A class with no explicit superclass has <code>__bases__ == (object,)</code>: everything inherits from <b>object</b>.")
nb.ask("What is printed?", "class Classy:\n    pass\n\nobj = Classy()\nprint(Classy.__name__, type(obj).__name__, obj.__module__)\nprint(obj.__name__)",
       "Classy Classy __main__\n!AttributeError")
nb.ask("Course example: what is printed?", """
class SuperOne:
    pass
class SuperTwo:
    pass
class Sub(SuperOne, SuperTwo):
    pass

def printBases(cls):
    print('( ', end='')
    for x in cls.__bases__:
        print(x.__name__, end=' ')
    print(')')

printBases(SuperOne)
printBases(SuperTwo)
printBases(Sub)
""", "( object )\n( object )\n( SuperOne SuperTwo )")

# ---------------------------------------------------------------- 10
nb.h2("10. __str__: how an object prints itself")
nb.ul("<code>print(obj)</code> without <code>__str__</code> → <code>&lt;__main__.Star object at 0x7f…&gt;</code> (ugly).",
      "Define <code>def __str__(self): return …</code>; it must <span class='y'>return a string</span> (returning something else → TypeError when printed).",
      "<code>__str__</code> is inherited like any method.")
nb.ask("Course example: what is printed?", """
class Star:
    def __init__(self, name, galaxy):
        self.name = name
        self.galaxy = galaxy
    def __str__(self):
        return self.name + ' in ' + self.galaxy

sun = Star("Sun", "Milky Way")
print(sun)
""", "Sun in Milky Way")
nb.ask("What happens?", "class A:\n    def __str__(self):\n        return 42\n\nprint(A())", "!TypeError")

# ---------------------------------------------------------------- 11
nb.h2("11. issubclass, isinstance, is")
nb.table(["tool", "question", "remember"],
         [["<code>issubclass(A, B)</code>", "is class A a subclass of B?", "<span class='y'>every class is a subclass of itself</span>"],
          ["<code>isinstance(obj, B)</code>", "was obj made from B or a subclass of B?", "subclass object is an instance of all its superclasses"],
          ["<code>a is b</code>", "same object in memory?", "<code>==</code> compares values, <code>is</code> compares identity"]])
nb.ask("Course example: what is printed?", """
class Vehicle: pass
class LandVehicle(Vehicle): pass
class TrackedVehicle(LandVehicle): pass

for cls1 in [Vehicle, LandVehicle, TrackedVehicle]:
    for cls2 in [Vehicle, LandVehicle, TrackedVehicle]:
        print(issubclass(cls1, cls2), end="\\t")
    print()
""", "True\tFalse\tFalse\nTrue\tTrue\tFalse\nTrue\tTrue\tTrue")
nb.ask("What is printed?", "class Vehicle: pass\nclass LandVehicle(Vehicle): pass\n\nv = Vehicle()\nl = LandVehicle()\nprint(isinstance(l, Vehicle), isinstance(v, LandVehicle), isinstance(l, object))",
       "True False True")
nb.ask("Course example: what is printed?", """
class SampleClass:
    def __init__(self, val):
        self.val = val

object_1 = SampleClass(0)
object_2 = SampleClass(2)
object_3 = object_1
object_3.val += 1
print(object_1 is object_2)
print(object_2 is object_3)
print(object_3 is object_1)
print(object_1.val, object_2.val, object_3.val)
""", "False\nFalse\nTrue\n1 2 1", why="object_3 is just a second name for object_1.")
nb.ask("Course example: what is printed?", 'string_1 = "Mary had a little "\nstring_2 = "Mary had a little lamb"\nstring_1 += "lamb"\nprint(string_1 == string_2, string_1 is string_2)',
       "True False", why="same text, but two different string objects.")

# ---------------------------------------------------------------- 12
nb.h2("12. super() and inherited properties")
nb.ul("<code>super()</code> reaches the superclass <b>without naming it</b>: <code>super().__init__(name)</code> (no self!).",
      "Old way: <code>Super.__init__(self, name)</code> (with self).",
      "Subclass objects see the superclass's <b>class</b> variables automatically; superclass <b>instance</b> variables exist only if the superclass constructor was called.")
nb.ask("Course example: what is printed?", """
class Super:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "My name is " + self.name + "."

class Sub(Super):
    def __init__(self, name):
        super().__init__(name)

obj = Sub("Andy")
print(obj)
""", "My name is Andy.", why="Sub has no __str__, so Super's is used (inherited).")
nb.ask("Course example: what is printed?", """
class Super:
    def __init__(self):
        self.supVar = 11
class Sub(Super):
    def __init__(self):
        super().__init__()
        self.subVar = 12

obj = Sub()
print(obj.subVar, obj.supVar)
""", "12 11")

# ---------------------------------------------------------------- 13
nb.h2("13. Multiple inheritance &amp; the MRO")
nb.heart("<ul><li>Python searches an attribute <b>bottom → top</b> (the object, its class, then superclasses) and stops at the <b>first</b> one found.</li>"
         "<li>With several superclasses, it searches <span class='y'>left → right</span> in the order written: <code>class Sub(Left, Right)</code> → Left first.</li>"
         "<li>This order = <b>MRO</b> (Method Resolution Order). See it with <code>Sub.__mro__</code> or <code>Sub.mro()</code>.</li>"
         "<li><b>Diamond</b>: <code>D(B, C)</code>, B and C both from A → MRO <b>D, B, C, A, object</b> (A only after both B and C).</li>"
         "<li>Impossible order → <b>TypeError</b>: Cannot create a consistent MRO.</li></ul>")
nb.ask("Course example: what is printed?", """
class Level1:
    var = 100
    def fun(self):
        return 101
class Level2(Level1):
    var = 200
    def fun(self):
        return 201
class Level3(Level2):
    pass

obj = Level3()
print(obj.var, obj.fun())
""", "200 201")
nb.ask("Course example: what is printed?", """
class Left:
    var = "L"
    var_left = "LL"
    def fun(self):
        return "Left"
class Right:
    var = "R"
    var_right = "RR"
    def fun(self):
        return "Right"
class Sub(Left, Right):
    pass

obj = Sub()
print(obj.var, obj.var_left, obj.var_right, obj.fun())
""", "L LL RR Left")
nb.ask("Course example: what happens?", """
class Top:
    def m_top(self):
        print("top")
class Middle(Top):
    def m_middle(self):
        print("middle")
class Bottom(Top, Middle):
    pass
""", "!TypeError", why="Top is listed before its own subclass Middle → no consistent MRO.")
nb.ask("Course diamond: what is printed?", """
class Top:
    def m_top(self):
        print("top")
class Middle_Left(Top):
    def m_middle(self):
        print("middle_left")
class Middle_Right(Top):
    def m_middle(self):
        print("middle_right")
class Bottom(Middle_Left, Middle_Right):
    def m_bottom(self):
        print("bottom")

object = Bottom()
object.m_bottom()
object.m_middle()
object.m_top()
""", "bottom\nmiddle_left\ntop")
nb.ask("What is printed?", """
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B"
class C(A):
    def who(self): return "C"
class D(C, B):
    pass
print(D().who(), [k.__name__ for k in D.__mro__])
""", "C ['D', 'C', 'B', 'A', 'object']")

# ---------------------------------------------------------------- 14
nb.h2("14. Polymorphism")
nb.ul("A superclass method that calls <code>self.do_it()</code> will run the <span class='y'>subclass's</span> <code>do_it</code> if the object is a subclass object. The object decides, not the place where the code is written.")
nb.ask("Course example: what is printed?", """
class One:
    def do_it(self):
        print("do_it from One")
    def doanything(self):
        self.do_it()

class Two(One):
    def do_it(self):
        print("do_it from Two")

one = One()
two = Two()
one.doanything()
two.doanything()
""", "do_it from One\ndo_it from Two")

# ---------------------------------------------------------------- 15
nb.h2("15. Course exercises (Dog)")
DOG = """
class Dog:
    kennel = 0
    def __init__(self, breed):
        self.breed = breed
        Dog.kennel += 1
    def __str__(self):
        return self.breed + " says: Woof!"

class SheepDog(Dog):
    def __str__(self):
        return super().__str__() + " Don't run away, Little Lamb!"

class GuardDog(Dog):
    def __str__(self):
        return super().__str__() + " Stay where you are, Mister Intruder!"

rocky = SheepDog("Collie")
luna = GuardDog("Dobermann")
"""
nb.code(DOG)
nb.check(DOG + "print(rocky)\nprint(luna)", "Collie says: Woof! Don't run away, Little Lamb!\nDobermann says: Woof! Stay where you are, Mister Intruder!")
nb.ask("Exercise 1: <code>print(rocky)</code> and <code>print(luna)</code>?", out="Collie says: Woof! Don't run away, Little Lamb!\nDobermann says: Woof! Stay where you are, Mister Intruder!")
nb.check(DOG + "print(issubclass(SheepDog, Dog), issubclass(SheepDog, GuardDog))\nprint(isinstance(rocky, GuardDog), isinstance(luna, GuardDog))", "True False\nFalse True")
nb.ask("Exercise 2:", "print(issubclass(SheepDog, Dog), issubclass(SheepDog, GuardDog))\nprint(isinstance(rocky, GuardDog), isinstance(luna, GuardDog))", out="True False\nFalse True", run=False)
nb.check(DOG + "print(luna is luna, rocky is luna)\nprint(rocky.kennel)", "True False\n2")
nb.ask("Exercise 3:", "print(luna is luna, rocky is luna)\nprint(rocky.kennel)", out="True False\n2", run=False,
       why="kennel is a class variable incremented by both constructors.")

# ---------------------------------------------------------------- self-test
nb.raw("<div class='chapter'></div>")
nb.selftest("OOP", [
    ("What is printed?", "class A:\n    x = 1\n    def __init__(self):\n        self.y = 2\na = A()\nprint('x' in a.__dict__, 'x' in A.__dict__, 'y' in a.__dict__)", "", "False True True"),
    ("What is printed?", "class A:\n    def __init__(self):\n        self.__v = 1\na = A()\nprint(hasattr(a, '__v'), hasattr(a, '_A__v'))", "", "False True"),
    ("What is printed?", "class A:\n    def f(self): return 'A'\nclass B(A):\n    def f(self): return 'B' + super().f()\nprint(B().f())", "", "BA"),
    ("What is printed?", "class A: pass\nclass B(A): pass\nprint(issubclass(B, B), isinstance(A(), B), B.__bases__[0].__name__)", "", "True False A"),
    ("What is printed?", "class C:\n    count = 0\n    def __init__(self):\n        C.count += 1\n        self.count = 10\nc1 = C(); c2 = C()\nprint(C.count, c1.count)", "", "2 10"),
    ("What is printed?", "class X:\n    def __init__(self, v=5):\n        self.v = v\na = X()\nb = X(7)\nb = a\nb.v = 9\nprint(a.v)", "", "9"),
    ("What is printed?", "class P:\n    def hi(self): return self.name()\n    def name(self): return 'P'\nclass Q(P):\n    def name(self): return 'Q'\nprint(P().hi(), Q().hi())", "", "P Q"),
    ("What is printed?", "class A:\n    v = 'A'\nclass B:\n    v = 'B'\nclass C(B, A):\n    pass\nprint(C.v)", "", "B"),
    ("What happens?", "class A:\n    pass\nprint(A().__bases__)", "", "!AttributeError"),
    ("What is the first parameter of every method called by convention, and who passes it?", None, "<code>self</code>; Python passes the object automatically.", None),
    ("What is printed?", "class A:\n    def __init__(self):\n        self.a = 1\nclass B(A):\n    def __init__(self):\n        A.__init__(self)\n        self.b = 2\nprint(sorted(B().__dict__))", "", "['a', 'b']"),
    ("What is printed?", "class K:\n    def __str__(self):\n        return 'K!'\nprint(str(K()) + '?', type(K()).__name__)", "", "K!? K"),
    ("Name the 3 things every object has (course).", None, "A name, a set of properties, a set of methods.", None),
    ("What is printed?", "class A: pass\nclass B: pass\nclass C(A, B): pass\nprint([k.__name__ for k in C.__bases__])", "", "['A', 'B']"),
])

if __name__ == "__main__":
    from lib import finish
    import sys
    nb.render(sys.argv[1] if len(sys.argv) > 1 else "PCAP_4.pdf")
    finish()
