"""
arcade.java.experiments_data — 10 VTU Java OOP Lab Experiments (1BCS302, 2025 Scheme).
Each experiment features detailed 3-part structured block breakdowns:
  1) Block Purpose & Role
  2) Inside the Block (Components, Variables & Logic)
  3) Step-by-Step Execution Flow
"""

JAVA_EXPERIMENTS = [
    {
        "num": 1,
        "title": "Matrix Addition of Order N",
        "file": "java-lab/programs/Lab01MatrixAddition.java",
        "concept": "In Java, multi-dimensional arrays are objects containing references to 1D arrays on the Heap. Matrix addition computes element-wise sums: C[i][j] = A[i][j] + B[i][j].",
        "problem": "Develop a Java program to add TWO matrices of suitable order N using 2D arrays and Scanner input.",
        "blocks": [
            {
                "title": "Scanner Input & Dynamic 2D Array Heap Allocation",
                "code": "Scanner sc = new Scanner(System.in);\nint n = sc.nextInt();\nint[][] a = new int[n][n];\nint[][] b = new int[n][n];\nint[][] c = new int[n][n];",
                "purpose": "Reads matrix dimension N from console and dynamically instantiates three 2D integer array objects on the JVM Heap.",
                "inside": [
                    "`Scanner sc`: Utility object from `java.util` wrapping standard input stream `System.in`.",
                    "`int[][] a`: Reference variable on Call Stack pointing to an array-of-arrays object on the Heap.",
                    "`new int[n][n]`: Dynamic heap allocation. Java allocates 1 top-level reference array pointing to N separate 1D integer row arrays. All cells default initialized to 0."
                ],
                "flow": [
                    "Step 1: Scanner parses integer `n` from keyboard input stream.",
                    "Step 2: JVM allocates top-level array object of length `n` containing reference pointers.",
                    "Step 3: JVM allocates `n` sub-arrays of size `n` for rows and wires reference pointers.",
                    "Step 4: Variable `a` stores memory reference to root array."
                ]
            },
            {
                "title": "Nested Row-Column Traversal & Element-Wise Sum",
                "code": "for (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        c[i][j] = a[i][j] + b[i][j];\n    }\n}",
                "purpose": "Iterates through every matrix coordinate (i, j) in row-major order and computes the algebraic sum.",
                "inside": [
                    "`for (int i = 0; i < n; i++)`: Outer loop iterating row indices 0 through N - 1.",
                    "`for (int j = 0; j < n; j++)`: Inner loop iterating column indices 0 through N - 1.",
                    "`a[i][j] + b[i][j]`: Dereferences row object `a[i]`, reads cell `j`, adds to corresponding cell in `b`, and writes to `c[i][j]`."
                ],
                "flow": [
                    "Step 1: Outer loop sets row `i = 0`.",
                    "Step 2: Inner loop visits columns `j = 0, 1, ..., n-1`.",
                    "Step 3: Sum calculated and stored in `c[i][j]` with O(N^2) complexity.",
                    "Step 4: Repeats until all N*N elements are evaluated."
                ]
            }
        ],
        "challenge": {
            "prompt": "In Java, what is the default initial value of elements in a newly instantiated 'new int[3][3]' array before any assignment?",
            "opts": [
                "A) Garbage values left in RAM",
                "B) 0",
                "C) null",
                "D) -1"
            ],
            "correct_opt": "B",
            "hint": "Java guarantees automatic zero-initialization for all primitive numeric array slots on the Heap.",
            "praise": "Exactly! Java guarantees zero-initialization for numeric primitives (0 for int, false for boolean, null for objects).",
            "roast": "Unlike C/C++, Java automatically initializes all primitive int array elements to 0 on the heap!"
        }
    },
    {
        "num": 2,
        "title": "Stack Class and Object Encapsulation",
        "file": "java-lab/programs/Lab02StackOperations.java",
        "concept": "Object-Oriented Encapsulation. The internal representation of the Stack (array and top pointer) is hidden (private), exposed only through well-defined public methods (push, pop, display).",
        "problem": "Develop a Stack class in Java to implement Stack operations (push, pop, display). Create at least two separate stack objects to prove independent encapsulation.",
        "blocks": [
            {
                "title": "Encapsulated State & Constructor Initialization",
                "code": "class Stack {\n    private int[] s;\n    private int top;\n    private int capacity;\n\n    public Stack(int cap) {\n        this.capacity = cap;\n        this.s = new int[capacity];\n        this.top = -1;\n    }\n}",
                "purpose": "Encapsulates stack memory and metadata as private fields, ensuring external classes cannot corrupt the `top` pointer.",
                "inside": [
                    "`private int[] s`: Information hiding. Restricts direct access from outside the class.",
                    "`this.capacity = cap`: Resolves shadow variable collision between parameter `cap` and instance variable.",
                    "`this.top = -1`: Initializes stack to logically empty state."
                ],
                "flow": [
                    "Step 1: Caller invokes `new Stack(5)`.",
                    "Step 2: JVM allocates Stack instance on Heap.",
                    "Step 3: Constructor sets `capacity = 5`, instantiates internal array `s`, sets `top = -1`."
                ]
            },
            {
                "title": "Public push() and pop() API Methods",
                "code": "public void push(int item) {\n    if (top == capacity - 1) {\n        System.out.println(\"Stack Overflow!\");\n        return;\n    }\n    s[++top] = item; // Pre-increment advances top before writing\n}\n\npublic int pop() {\n    if (top == -1) {\n        System.out.println(\"Stack Underflow!\");\n        return -1;\n    }\n    return s[top--]; // Post-decrement returns value then decrements top\n}",
                "purpose": "Provides safe public mutations with strict boundary checks protecting the underlying array.",
                "inside": [
                    "`s[++top] = item`: Pre-increment operator advances `top` pointer first, then places `item` at the new index.",
                    "`s[top--]`: Post-decrement operator captures value at current `top`, and then decrements `top` pointer."
                ],
                "flow": [
                    "Step 1: Boundary check verified (`top == capacity - 1` or `top == -1`).",
                    "Step 2: Pointer manipulated and data transferred.",
                    "Step 3: Calling code receives return value or confirmation."
                ]
            }
        ],
        "challenge": {
            "prompt": "If you instantiate 'Stack s1 = new Stack(5)' and 'Stack s2 = new Stack(5)', do they share the same array in RAM?",
            "opts": [
                "A) Yes, because they were created from the same class blueprint.",
                "B) No, each 'new' operator allocates a distinct object with its own separate array on the Heap.",
                "C) Only if they have the same capacity.",
                "D) They share memory unless declared static."
            ],
            "correct_opt": "B",
            "hint": "Each 'new' creates a completely distinct instance in heap memory.",
            "praise": "Spot on! Independent object encapsulation is the foundation of OOP.",
            "roast": "Each 'new' invocation allocates an independent, isolated object instance on the heap!"
        }
    },
    {
        "num": 3,
        "title": "Student Class and Array of Objects",
        "file": "java-lab/programs/Lab03StudentDemo.java",
        "concept": "In Java, an 'Array of Objects' is actually an Array of References. Declaring 'Student[] s = new Student[N]' allocates N null pointers; each object must be instantiated individually.",
        "problem": "Create a Java class Student (USN, Name, Branch, Phone). Write a program to read N student records and print them in a tabular format.",
        "blocks": [
            {
                "title": "Student Class Blueprint & Parameterized Constructor",
                "code": "class Student {\n    String usn, name, branch, phone;\n\n    Student(String u, String n, String b, String p) {\n        this.usn = u;\n        this.name = n;\n        this.branch = b;\n        this.phone = p;\n    }\n\n    void display() {\n        System.out.printf(\"%-15s %-20s %-10s %-12s\\n\", usn, name, branch, phone);\n    }\n}",
                "purpose": "Defines the entity structure and initialization logic for individual student records.",
                "inside": [
                    "`String usn, name...`: Reference fields holding pointers to string literal objects on the Heap.",
                    "`System.out.printf`: Formatted output ensuring consistent column widths in terminal tables."
                ],
                "flow": [
                    "Step 1: Student attributes passed to constructor.",
                    "Step 2: Values assigned to object instance variables on the heap."
                ]
            },
            {
                "title": "Two-Phase Array of Objects Allocation",
                "code": "Student[] students = new Student[n]; // Phase 1: Allocates n NULL references!\nfor (int i = 0; i < n; i++) {\n    // read inputs...\n    students[i] = new Student(u, name, b, phone); // Phase 2: Instantiates actual object\n}",
                "purpose": "Demonstrates the essential two-stage lifecycle of object arrays in Java.",
                "inside": [
                    "`new Student[n]`: Creates an array object holding N null references. Does NOT instantiate any Student objects!",
                    "`students[i] = new Student(...)`: Critical step! Instantiates actual Student object on heap and assigns reference to array index."
                ],
                "flow": [
                    "Step 1: Phase 1 allocates array of N null pointers.",
                    "Step 2: Phase 2 loop calls `new Student()` for each index, preventing fatal NullPointerExceptions."
                ]
            }
        ],
        "challenge": {
            "prompt": "What happens if you run 'Student[] s = new Student[3]; s[0].display();' without calling 'new Student()'?",
            "opts": [
                "A) It prints empty blank strings.",
                "B) NullPointerException crash, because s[0] contains null (no object exists yet).",
                "C) It compiles and runs fine with default values.",
                "D) The compiler refuses to compile the file."
            ],
            "correct_opt": "B",
            "hint": "s[0] is null. Dereferencing null (calling .display() on it) throws java.lang.NullPointerException.",
            "praise": "Critical exam trap! Always instantiate each array element before invoking methods on it.",
            "roast": "s[0] is null! Calling any method on null throws java.lang.NullPointerException."
        }
    },
    {
        "num": 4,
        "title": "Runtime Polymorphism and Method Overriding",
        "file": "java-lab/programs/Lab04ShapePolymorphism.java",
        "concept": "Dynamic Method Dispatch. A superclass reference variable (Shape s) can point to any subclass object (Circle, Triangle) and resolves the overridden method at runtime via the JVM Virtual Method Table (vtable).",
        "problem": "Create a base class Shape with draw() and erase(). Create subclasses Circle, Triangle, Square that override draw() and erase(). Demonstrate polymorphism using a single Shape reference.",
        "blocks": [
            {
                "title": "Base Class & Subclass Method Overriding",
                "code": "class Shape {\n    void draw() { System.out.println(\"Drawing generic Shape\"); }\n    void erase() { System.out.println(\"Erasing generic Shape\"); }\n}\n\nclass Circle extends Shape {\n    @Override\n    void draw() { System.out.println(\"Drawing Circle ⭕\"); }\n    @Override\n    void erase() { System.out.println(\"Erasing Circle\"); }\n}",
                "purpose": "Establishes inheritance hierarchy where subclasses provide specialized implementations of inherited methods.",
                "inside": [
                    "`extends Shape`: Establishes 'IS-A' inheritance relationship.",
                    "`@Override`: Compiler check ensuring method signature exactly matches the superclass declaration."
                ],
                "flow": [
                    "Step 1: `Circle` inherits `draw()` and `erase()` contracts from `Shape`.",
                    "Step 2: Subclass overrides method bodies with specialized behavior."
                ]
            },
            {
                "title": "Dynamic Method Dispatch via Superclass Reference",
                "code": "Shape s; // Superclass reference variable on Call Stack\n\ns = new Circle();   // s points to Circle on Heap\ns.draw();           // JVM invokes Circle.draw()!\n\ns = new Triangle(); // s points to Triangle on Heap\ns.draw();           // Dynamic dispatch invokes Triangle.draw()!",
                "purpose": "Demonstrates runtime polymorphism where the exact method executed depends on the actual heap object, not the reference type.",
                "inside": [
                    "`Shape s`: Declared type is Shape, but runtime type changes dynamically.",
                    "`JVM VTable Lookup`: At runtime, the JVM inspects the object header of the heap instance, identifies the class vtable, and dispatches the subclass method."
                ],
                "flow": [
                    "Step 1: Reference `s` declared on call stack.",
                    "Step 2: `new Circle()` allocated on heap; `s` points to it.",
                    "Step 3: `s.draw()` invokes `Circle.draw()` via dynamic dispatch.",
                    "Step 4: `s` reassigned to `new Triangle()`; subsequent call invokes `Triangle.draw()`."
                ]
            }
        ],
        "challenge": {
            "prompt": "How does the JVM determine which draw() method to execute when you run 's.draw()' on a Shape reference?",
            "opts": [
                "A) Based on the declared reference type at compile time.",
                "B) At runtime, by checking the actual object type on the heap using the Virtual Method Table (Dynamic Method Dispatch).",
                "C) It calls all subclass draw methods simultaneously.",
                "D) By alphabetical sorting of class names."
            ],
            "correct_opt": "B",
            "hint": "This is the very definition of Runtime Polymorphism (Dynamic Dispatch).",
            "praise": "100% correct! Dynamic method dispatch resolves method calls based on the runtime heap object.",
            "roast": "Dynamic dispatch checks the actual object type in heap memory at runtime via the vtable!"
        }
    },
    {
        "num": 5,
        "title": "Resizable Interface Implementation",
        "file": "java-lab/programs/Lab05ResizableInterface.java",
        "concept": "Interfaces define a 100% abstract behavioral contract. Classes implement interfaces to guarantee specific capabilities, supporting multiple inheritance of type.",
        "problem": "Create an interface Resizable with resizeWidth(int width) and resizeHeight(int height). Implement it in a Rectangle class.",
        "blocks": [
            {
                "title": "Interface Declaration & Implementation Contract",
                "code": "interface Resizable {\n    void resizeWidth(int width);   // implicitly public and abstract\n    void resizeHeight(int height);\n}\n\nclass Rectangle implements Resizable {\n    private int width, height;\n\n    public Rectangle(int w, int h) {\n        this.width = w;\n        this.height = h;\n    }\n\n    @Override\n    public void resizeWidth(int w) {\n        this.width = w;\n    }\n\n    @Override\n    public void resizeHeight(int h) {\n        this.height = h;\n    }\n}",
                "purpose": "Separates interface contract from concrete implementation, ensuring Rectangle can be resized through interface references.",
                "inside": [
                    "`interface Resizable`: Contract defining pure abstract methods.",
                    "`implements Resizable`: Rectangle pledges to provide concrete implementations for all interface methods.",
                    "`public void resizeWidth()`: Methods implementing interface contracts MUST be declared `public` because interface methods are public by default."
                ],
                "flow": [
                    "Step 1: Interface specifies method signatures.",
                    "Step 2: Class implements interface and overrides methods with `public` visibility.",
                    "Step 3: State fields mutated safely."
                ]
            }
        ],
        "challenge": {
            "prompt": "Why MUST methods implementing an interface be declared with 'public' visibility?",
            "opts": [
                "A) Because Java compiler crashes otherwise.",
                "B) Because all methods in an interface are implicitly 'public abstract'. You cannot reduce visibility of an inherited method in Java.",
                "C) Only for interfaces with more than 3 methods.",
                "D) It is optional."
            ],
            "correct_opt": "B",
            "hint": "Java does not permit reducing method visibility when overriding (public cannot become package-private).",
            "praise": "Golden rule of Java interfaces! Implementing methods must always be explicitly public.",
            "roast": "Interface methods are implicitly public; subclasses cannot reduce visibility, so they must be declared public!"
        }
    },
    {
        "num": 6,
        "title": "User-Defined Packages (mypack)",
        "file": "java-lab/programs/Lab06PackageDemo.java",
        "concept": "Packages prevent naming collisions and enforce access protection boundaries. Physical directory paths mirror package namespace hierarchies.",
        "problem": "Create a user-defined package named 'mypack' containing a class with a public method. Write a driver program in another file to import and invoke it.",
        "blocks": [
            {
                "title": "Package Declaration & Public Class Visibility",
                "code": "// Saved in directory: mypack/MyClass.java\npackage mypack;\n\npublic class MyClass {\n    public void displayMessage() {\n        System.out.println(\"Hello from mypack.MyClass!\");\n    }\n}",
                "purpose": "Namespaces the class under `mypack`, mapping it to the `mypack/` directory structure.",
                "inside": [
                    "`package mypack;`: Must be the very FIRST non-comment line in the source file.",
                    "`public class`: Necessary so classes outside the package can import and instantiate it.",
                    "`public void`: Method must be public to be accessible across package boundaries."
                ],
                "flow": [
                    "Step 1: File placed in `mypack/` directory.",
                    "Step 2: Compiled using `javac -d . MyClass.java` to generate package hierarchy.",
                    "Step 3: Class exported for external use."
                ]
            },
            {
                "title": "Importing & Consuming Packaged Classes",
                "code": "// Saved outside mypack directory\nimport mypack.MyClass;\n\npublic class Lab06PackageDemo {\n    public static void main(String[] args) {\n        MyClass obj = new MyClass();\n        obj.displayMessage();\n    }\n}",
                "purpose": "Brings the external package class into scope for invocation in the main program.",
                "inside": [
                    "`import mypack.MyClass;`: Tells compiler where to resolve `MyClass` identifier.",
                    "`new MyClass()`: Instantiates the packaged class across boundary."
                ],
                "flow": [
                    "Step 1: Compiler resolves `mypack.MyClass` on CLASSPATH.",
                    "Step 2: Class loaded into JVM Method Area and executed."
                ]
            }
        ],
        "challenge": {
            "prompt": "What compiler command automatically creates the physical package folder structure from a Java source file?",
            "opts": [
                "A) javac -p . File.java",
                "B) javac -d . File.java",
                "C) javac -folder File.java",
                "D) java -make-dirs File.java"
            ],
            "correct_opt": "B",
            "hint": "The '-d' flag specifies destination directory for package hierarchies.",
            "praise": "Correct! 'javac -d .' places class files into the appropriate package folder hierarchy.",
            "roast": "The flag is 'javac -d <destination> <file.java>'!"
        }
    },
    {
        "num": 7,
        "title": "Custom Exception Handling (Division By Zero)",
        "file": "java-lab/programs/Lab07CustomException.java",
        "concept": "Robust error management via exception handling. Custom exceptions extend Exception (checked) or RuntimeException (unchecked), separating error-handling code from normal logic.",
        "problem": "Create a custom exception class DivisionByZeroException. Read two numbers, check if denominator is zero, throw the custom exception, and handle it gracefully with try-catch-finally.",
        "blocks": [
            {
                "title": "Custom Exception Class Definition",
                "code": "class DivisionByZeroException extends Exception {\n    public DivisionByZeroException(String message) {\n        super(message); // Passes error description to java.lang.Exception\n    }\n}",
                "purpose": "Creates a domain-specific checked exception by inheriting from `java.lang.Exception`.",
                "inside": [
                    "`extends Exception`: Designates this as a Checked Exception, requiring either try-catch handling or a `throws` declaration.",
                    "`super(message)`: Calls parent constructor to store the detail error message retrieved later via `getMessage()`."
                ],
                "flow": [
                    "Step 1: Exception class loaded by JVM.",
                    "Step 2: Custom message string stored in internal Throwable message field."
                ]
            },
            {
                "title": "Explicit throw and try-catch-finally Unwinding",
                "code": "try {\n    if (b == 0) {\n        throw new DivisionByZeroException(\"Denominator cannot be zero!\");\n    }\n    double result = (double) a / b;\n    System.out.println(\"Result: \" + result);\n} catch (DivisionByZeroException e) {\n    System.out.println(\"Caught Custom Exception: \" + e.getMessage());\n} finally {\n    System.out.println(\"Finally block always executes (closing resources).\");\n}",
                "purpose": "Monitors division operations, explicitly triggers custom exception on invalid input, and guarantees cleanup execution.",
                "inside": [
                    "`throw new ...`: Explicitly instantiates and raises exception object, interrupting normal control flow.",
                    "`catch (...)`: Intercepts matching exception object and executes recovery logic.",
                    "`finally`: Guaranteed execution block! Runs whether exception occurs or not, ideal for closing files, sockets, and scanners."
                ],
                "flow": [
                    "Step 1: `try` block checks if `b == 0`.",
                    "Step 2: If zero, `throw` creates exception and halts try block.",
                    "Step 3: Call stack unwinds to matching `catch` block.",
                    "Step 4: `finally` executes unconditionally before proceeding."
                ]
            }
        ],
        "challenge": {
            "prompt": "Does the 'finally' block execute if an exception is caught and handled inside the catch block?",
            "opts": [
                "A) No, finally only runs when no exception occurs.",
                "B) Yes, the finally block ALWAYS executes regardless of whether an exception was thrown, caught, or not thrown at all.",
                "C) Only on Windows systems.",
                "D) Only if the catch block returns 0."
            ],
            "correct_opt": "B",
            "hint": "finally is designed for cleanup (releasing locks, closing streams) and is guaranteed to run.",
            "praise": "Universal Java truth! The finally block is guaranteed to execute.",
            "roast": "The 'finally' block is guaranteed to run whether an exception occurs or not!"
        }
    },
    {
        "num": 8,
        "title": "Multithreading and Concurrent Execution",
        "file": "java-lab/programs/Lab08ThreadConcurrency.java",
        "concept": "Concurrency enables simultaneous execution of two or more parts of a program. Creating threads via 'extends Thread' or 'implements Runnable' allows OS time-slicing across cores.",
        "problem": "Create multiple threads in Java to demonstrate concurrent execution and context switching using Thread.sleep() and start().",
        "blocks": [
            {
                "title": "Thread Subclass & run() Payload",
                "code": "class ChildThread extends Thread {\n    @Override\n    public void run() {\n        for (int i = 1; i <= 5; i++) {\n            System.out.println(\"[Child] Count: \" + i);\n            try {\n                Thread.sleep(500); // 500ms delay simulates work\n            } catch (InterruptedException e) {\n                System.out.println(\"Thread interrupted\");\n            }\n        }\n    }\n}",
                "purpose": "Defines the thread execution body. The code inside `run()` executes concurrently on a separate OS thread call stack.",
                "inside": [
                    "`extends Thread`: Inherits thread lifecycle management capabilities.",
                    "`run()`: The entry point for the new thread (equivalent to `main` for that thread).",
                    "`Thread.sleep(500)`: Moves thread from RUNNABLE to TIMED_WAITING state, allowing CPU scheduler to switch to other threads."
                ],
                "flow": [
                    "Step 1: Subclass overrides `run()`.",
                    "Step 2: Loop simulates background task with delays."
                ]
            },
            {
                "title": "Spawning Threads: start() vs run()",
                "code": "ChildThread t = new ChildThread(); // State: NEW\nt.start();                         // Spawns separate OS call stack! State: RUNNABLE\n\n// Main thread executes concurrently in parallel\nfor (int i = 1; i <= 5; i++) {\n    System.out.println(\"[Main] Count: \" + i);\n    Thread.sleep(500);\n}",
                "purpose": "Spawns a true concurrent thread and demonstrates interleaved execution with the main thread.",
                "inside": [
                    "`new ChildThread()`: State is `NEW`. Object exists, but no OS thread is running.",
                    "`t.start()`: Calls JVM native method `start0()`, creates a brand new thread call stack, and calls `run()` asynchronously.",
                    "WARNING: Calling `t.run()` directly does NOT create a thread — it just runs synchronously on the main thread!"
                ],
                "flow": [
                    "Step 1: `t.start()` creates new thread call stack in memory.",
                    "Step 2: OS scheduler alternates execution slices between Main and Child thread.",
                    "Step 3: Console displays interleaved outputs demonstrating true concurrency."
                ]
            }
        ],
        "challenge": {
            "prompt": "What happens if you invoke 't.run()' instead of 't.start()' on a Thread object?",
            "opts": [
                "A) It spawns a background thread with higher priority.",
                "B) It does NOT spawn a new thread; it simply executes run() as a normal method call synchronously on the current (main) thread.",
                "C) An IllegalThreadStateException is thrown.",
                "D) The JVM terminates."
            ],
            "correct_opt": "B",
            "hint": "Only start() allocates a new thread call stack. Calling run() directly is just a plain method call.",
            "praise": "Examiner classic! start() spawns a thread; run() executes on the calling thread.",
            "roast": "Calling run() does NOT create a new thread! Always use start() to initiate concurrent execution."
        }
    },
    {
        "num": 9,
        "title": "Java Enumerations and valueOf()",
        "file": "java-lab/programs/Lab09DepartmentEnum.java",
        "concept": "Enums are type-safe lists of named constants. In Java, enums are full-featured classes that can contain fields, constructors, and methods, preventing invalid constant assignments.",
        "problem": "Create an enum Department (CSE, ISE, ECE, MECH, CIVIL). Demonstrate values(), ordinal(), and converting a user String to enum constant via valueOf().",
        "blocks": [
            {
                "title": "Enum Declaration & Type-Safe Constants",
                "code": "enum Department {\n    CSE, ISE, ECE, MECH, CIVIL\n}\n\n// Iterating all constants\nfor (Department d : Department.values()) {\n    System.out.println(d + \" at ordinal index: \" + d.ordinal());\n}",
                "purpose": "Defines a strictly type-safe set of constants and iterates them using built-in utility methods.",
                "inside": [
                    "`enum Department`: Implicitly inherits from `java.lang.Enum`. Constants are public static final objects.",
                    "`Department.values()`: Static method returning an array of all enum constants in order of declaration.",
                    "`d.ordinal()`: Returns the zero-based position index of the constant."
                ],
                "flow": [
                    "Step 1: Enum class loaded with 5 singleton constant instances.",
                    "Step 2: `values()` returns array `[CSE, ISE, ECE, MECH, CIVIL]`.",
                    "Step 3: Loop prints each identifier and its ordinal position."
                ]
            },
            {
                "title": "String to Enum Conversion via valueOf()",
                "code": "String input = sc.next().toUpperCase();\ntry {\n    Department dept = Department.valueOf(input);\n    System.out.println(\"Valid Department: \" + dept);\n} catch (IllegalArgumentException e) {\n    System.out.println(\"Invalid Department: \" + input);\n}",
                "purpose": "Parses user text into an enum constant, protecting against invalid department codes.",
                "inside": [
                    "`Department.valueOf(input)`: Case-sensitive lookup method converting string to matching enum constant.",
                    "`IllegalArgumentException`: Thrown automatically if `input` does not match any declared enum identifier."
                ],
                "flow": [
                    "Step 1: User input normalized to uppercase.",
                    "Step 2: `valueOf()` validates string against enum constant names.",
                    "Step 3: If invalid, catch block handles `IllegalArgumentException` gracefully."
                ]
            }
        ],
        "challenge": {
            "prompt": "What exception is thrown by Enum.valueOf() if the supplied string does not match any constant in the enum?",
            "opts": [
                "A) NullPointerException",
                "B) IllegalArgumentException",
                "C) ClassCastException",
                "D) IndexOutOfBoundsException"
            ],
            "correct_opt": "B",
            "hint": "Passing an unrecognized argument throws java.lang.IllegalArgumentException.",
            "praise": "Spot on! IllegalArgumentException is thrown when valueOf cannot find the identifier.",
            "roast": "Enum.valueOf() throws java.lang.IllegalArgumentException on unmatched strings!"
        }
    },
    {
        "num": 10,
        "title": "Wrapper Classes and Autoboxing / Unboxing",
        "file": "java-lab/programs/Lab10MarksCalculator.java",
        "concept": "Wrapper classes (Integer, Double, Character) convert primitive data types into first-class Java objects. Autoboxing (primitive -> object) and Unboxing (object -> primitive) happen automatically.",
        "problem": "Develop a Java program using Wrapper classes to read student test scores as Strings, parse them using Integer.parseInt(), calculate totals using autoboxed Integers, and unbox to primitives.",
        "blocks": [
            {
                "title": "Parsing Strings to Numbers with Static Wrapper Methods",
                "code": "String strScore = \"85\";\nint mark1 = Integer.parseInt(strScore);     // String -> primitive int\ndouble gpa = Double.parseDouble(\"3.75\");    // String -> primitive double",
                "purpose": "Converts raw textual input from files, GUI forms, or CLI scanners into computable primitive numbers.",
                "inside": [
                    "`Integer.parseInt(s)`: Static method parsing signed decimal integer string. Throws `NumberFormatException` if string contains non-digits.",
                    "`Double.parseDouble(s)`: Parses floating-point string representation."
                ],
                "flow": [
                    "Step 1: String passed to wrapper utility method.",
                    "Step 2: Characters validated as valid numeric digits.",
                    "Step 3: Binary primitive number returned."
                ]
            },
            {
                "title": "Autoboxing & Unboxing Mechanisms",
                "code": "// Autoboxing: Primitive int automatically converted to Integer object\nInteger boxedMark = mark1; // Equivalent to: Integer.valueOf(mark1)\n\n// Unboxing: Integer object automatically converted to primitive int\nint primitiveTotal = boxedMark + 10; // Equivalent to: boxedMark.intValue() + 10",
                "purpose": "Enables seamless interoperability between primitive types and Java collection frameworks.",
                "inside": [
                    "Autoboxing: Java compiler automatically converts `int` to `Integer` via `Integer.valueOf()`.",
                    "Unboxing: Java compiler automatically converts `Integer` to `int` via `intValue()` when arithmetic is performed."
                ],
                "flow": [
                    "Step 1: Compiler detects assignment of primitive to wrapper reference.",
                    "Step 2: Synthesizes `Integer.valueOf()` bytecode instruction (Autoboxing).",
                    "Step 3: Compiler detects arithmetic on wrapper reference, synthesizes `intValue()` call (Unboxing)."
                ]
            }
        ],
        "challenge": {
            "prompt": "What does the Java compiler actually emit behind the scenes when you write 'Integer x = 50;'?",
            "opts": [
                "A) Integer x = (Integer) 50;",
                "B) Integer x = Integer.valueOf(50);",
                "C) Integer x = new int(50);",
                "D) Integer x = String.valueOf(50);"
            ],
            "correct_opt": "B",
            "hint": "Autoboxing translates directly to Integer.valueOf() invocations in bytecode.",
            "praise": "Exactly right! Java compiler synthesizes Integer.valueOf() calls for autoboxing.",
            "roast": "Under the hood, autoboxing invokes `Integer.valueOf(50)`!"
        }
    }
]

