"""
arcade.java.studio — Java OOP Lab Studio (1BCS302 — 10 Experiments, VTU 2025 Scheme).
"""
import os
import time
import random

from arcade.core import (
    PROJECT_ROOT, Color, clear_screen, prompt_input, spinner,
    print_slow, anim_correct, anim_wrong,
)
from arcade.session import (
    _SESSION, _award_xp, _break_streak, _unlock_badge,
    _save_to_local_db, _show_session_header,
)
from arcade.vault import _view_source_file

JAVA_DISASTER_SCENARIOS = [
    {
        "title": "🚨 DISASTER 1: The Infamous NullPointerException in Object Array",
        "story": "In Experiment 03 (Student Class), you wrote:\n  Student[] s = new Student[5];\n  s[0].display();\n\nYour JVM immediately crashes in flames with:\n\033[91mjava.lang.NullPointerException: Cannot invoke Student.display() because s[0] is null\033[0m!",
        "prompt": "Why was s[0] null when you just declared 'new Student[5]'?",
        "choices": [
            "'new Student[5]' allocates an array of 5 NULL references; you must instantiate each element with 's[0] = new Student(...)'.",
            "Java does not support arrays of custom classes.",
            "Student class must be declared 'static'.",
            "You must reboot the JVM to register new classes."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In Java, arrays of objects are arrays of references. All slots start as null until explicitly instantiated with 'new'!"
    },
    {
        "title": "🚨 DISASTER 2: The Fake-Out Synchronous Thread",
        "story": "In Experiment 08 (Multithreading), you created a worker thread:\n  MyThread t = new MyThread(\"Worker\");\n  t.run();\n\nThe examiner looks at your terminal and points out that the main thread waited for the worker to finish before continuing. Why did concurrency fail?",
        "prompt": "What was the mistake in starting the thread?",
        "choices": [
            "You called 't.run()' directly instead of 't.start()'. Calling run() executes sequentially on the caller thread without creating a new OS thread!",
            "Thread class only works on Linux operating systems.",
            "You forgot to extend Runnable instead of Thread.",
            "Java requires root privileges to execute concurrent threads."
        ],
        "ans_idx": 1,
        "reaction": "CORRECT! Calling run() is just a standard method call. Calling start() registers with the JVM scheduler and allocates a new thread stack!"
    },
    {
        "title": "🚨 DISASTER 3: The Case-Sensitive Enum Crash",
        "story": "In Experiment 09 (Department Enum), the user typed 'cse' in lowercase. Your program crashed with:\n\033[91mjava.lang.IllegalArgumentException: No enum constant Department.cse\033[0m!",
        "prompt": "Why did Enum.valueOf() reject the input?",
        "choices": [
            "Enum constants are strictly CASE-SENSITIVE in Java. You must convert user input using '.toUpperCase()' before calling valueOf()!",
            "Enums cannot store words shorter than 4 letters.",
            "Enums only accept integer inputs.",
            "valueOf() is deprecated in Java 21."
        ],
        "ans_idx": 1,
        "reaction": "NAILED IT! Department.valueOf(\"cse\") fails because the constant is named CSE. Always sanitize with input.trim().toUpperCase()!"
    },
    {
        "title": "🚨 DISASTER 4: The Unhandled Checked Exception Compiler Strike",
        "story": "In Experiment 07 (Custom Exceptions), you wrote a helper that calls 'divide(10, 0)'. The Java compiler refuses to build your code:\n\033[91munreported exception DivisionByZeroException; must be caught or declared to be thrown\033[0m!",
        "prompt": "Why is the compiler forcing you to handle DivisionByZeroException?",
        "choices": [
            "Because DivisionByZeroException extends 'Exception' (Checked Exception). The compiler enforces handling via try-catch or 'throws' in the signature!",
            "Because division by zero is illegal under federal copyright laws.",
            "Because custom exceptions must extend RuntimeException instead.",
            "You forgot to import java.lang.Throwable."
        ],
        "ans_idx": 1,
        "reaction": "SPOT ON! Checked exceptions (inheriting from Exception but not RuntimeException) are verified at compile-time by the javac compiler!"
    },
    {
        "title": "🚨 DISASTER 5: The Autoboxing NullPointerException Trap",
        "story": "In Experiment 10 (Wrapper Classes), you wrote:\n  Double mark = null;\n  double total = mark + 10.0;\n\nSuddenly, your program crashes with NullPointerException on an arithmetic line!",
        "prompt": "Why did an addition operation throw NullPointerException?",
        "choices": [
            "Unboxing invokes 'mark.doubleValue()'. Since mark is null, invoking a method on it triggers NullPointerException during automatic unboxing!",
            "Java does not support adding primitives to wrapper classes.",
            "The double literal 10.0 must be cast to (Double).",
            "Wrapper classes cannot be used in arithmetic operations."
        ],
        "ans_idx": 1,
        "reaction": "ARCHITECTURAL MASTERY! When unboxing occurs behind the scenes, Java calls .doubleValue(). If the object reference is null, it immediately throws NPE!"
    },
    {
        "title": "🚨 DISASTER 6: The Package Directory Hierarchy Mismatch",
        "story": "In Experiment 06 (Packages), you put 'package mypack;' at the top of 'MyClass.java', but you saved the file directly in the root project folder instead of a subfolder named 'mypack/'.\njavac gives an error when importing!",
        "prompt": "What fundamental rule of Java packages was violated?",
        "choices": [
            "The directory structure MUST mirror the package hierarchy. Classes in 'package mypack;' must reside in a physical folder named 'mypack'.",
            "Package names cannot start with the letter 'm'.",
            "Java packages require a package.json file.",
            "Packages can only be created inside the JDK bin directory."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In Java, package namespaces are directly tied to filesystem directory paths."
    },
    {
        "title": "🚨 DISASTER 7: The Missing @Override Spelling Blunder",
        "story": "In Experiment 04 (Shape Polymorphism), you wanted to override 'void draw()', but accidentally typed 'void Draw()' with a capital D. You ran 'Shape s = new Circle(); s.draw();' and it printed 'Drawing a generic Shape' instead of Circle!",
        "prompt": "Why didn't runtime polymorphism call Circle's method?",
        "choices": [
            "Java is case-sensitive! 'Draw()' is a completely new method, NOT an override of 'draw()'. Using '@Override' would have caught this at compile time!",
            "Dynamic method dispatch only works with abstract classes.",
            "Shape references cannot access subclass methods.",
            "Circle must implement the Drawable interface."
        ],
        "ans_idx": 1,
        "reaction": "BINGO! Without @Override, the compiler thought you were creating a new method Draw(), silently leaving the original draw() un-overridden!"
    },
    {
        "title": "🚨 DISASTER 8: The Forgotten public Modifier in Interface Methods",
        "story": "In Experiment 05 (Resizable), you implemented 'void resizeWidth(int w)' inside class Rectangle without writing 'public'. The compiler shouts:\n\033[91mresizeWidth() in Rectangle cannot implement resizeWidth() in Resizable; attempting to assign weaker access privileges; was public\033[0m!",
        "prompt": "Why must interface methods ALWAYS be declared 'public' when implemented in a class?",
        "choices": [
            "All interface methods are implicitly 'public abstract'. A class cannot reduce the visibility of an inherited interface method (package-private is weaker than public)!",
            "Classes can only have public methods in Java.",
            "Interfaces cannot be implemented by concrete classes.",
            "You must use the 'protected' keyword instead."
        ],
        "ans_idx": 1,
        "reaction": "GOLDEN JAVA CONTRACT RULE! Interface methods are implicitly public. A subclass cannot reduce visibility to default package-private!"
    }
]


# Extract Java experiments & visualizers from java_engine

# ==============================================================================

JAVA_EXPERIMENTS = [
    {
        "num": 1,
        "title": "Matrix Addition of Order N",
        "file": "java-lab/programs/Lab01MatrixAddition.java",
        "problem": "Develop a Java program to add TWO matrices of suitable order N using 2D arrays and Scanner input.",
        "concept": "In Java, multi-dimensional arrays are objects containing references to 1D arrays. Matrix addition adds corresponding cells: C[i][j] = A[i][j] + B[i][j].",
        "blocks": [
            {
                "title": "2D Array Memory Allocation on Heap",
                "code": "int[][] a = new int[n][n];\nint[][] b = new int[n][n];\nint[][] c = new int[n][n];",
                "explanation": "In Java, multi-dimensional arrays are objects on the heap. 'new int[n][n]' dynamically allocates contiguous row references."
            },
            {
                "title": "Nested Matrix Traversal & Summation",
                "code": "for (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        c[i][j] = a[i][j] + b[i][j];\n    }\n}",
                "explanation": "Outer loop iterates rows (i), inner loop iterates columns (j). Each cell c[i][j] stores the sum of corresponding cells."
            }
        ],
        "challenge": {
            "prompt": "What is the idiomatic Java statement to declare and instantiate a 2D integer array named 'matrix' with 3 rows and 4 columns?",
            "opts": [
                "[A] int matrix[3][4] = new int[][];",
                "[B] int[][] matrix = new int[3][4];",
                "[C] int[][] matrix = malloc(3 * 4 * sizeof(int));",
                "[D] Array<int, 2> matrix = new Array(3, 4);"
            ],
            "correct_opt": "B",
            "hint": "Type goes on the left (int[][]), and 'new int[rows][cols]' allocates the heap memory.",
            "praise": "Clean Java syntax! Heap memory allocated for a 3x4 matrix.",
            "roast": "Java does not use C-style size-in-declaration syntax or malloc! Use: int[][] matrix = new int[3][4];"
        }
    },
    {
        "num": 2,
        "title": "Stack Class and Object Encapsulation",
        "file": "java-lab/programs/Lab02StackOperations.java",
        "problem": "Develop a stack class to hold a maximum of 10 integers with suitable methods. Illustrate Stack operations with a menu-driven main.",
        "concept": "Encapsulation bundles data (arr, top) and operations (push, pop) inside a class. Private fields protect internal state from outside tampering.",
        "blocks": [
            {
                "title": "Encapsulation: Private Fields & Invariant Protection",
                "code": "public class Stack {\n    private int[] arr;\n    private int top;\n    private int capacity;\n}",
                "explanation": "Fields are marked 'private' to prevent external code from corrupting top pointer directly, enforcing access via push() and pop()."
            },
            {
                "title": "State Verification in push() and pop()",
                "code": "public void push(int x) {\n    if (top == capacity - 1) throw new IllegalStateException(\"Stack Overflow\");\n    arr[++top] = x;\n}",
                "explanation": "Validates preconditions before modifying state. If full, refuses push and signals error without corrupting memory."
            }
        ],
        "challenge": {
            "prompt": "In Java OOP encapsulation, which access modifier should be used on 'arr' and 'top' to prevent unauthorized external tampering?",
            "opts": [
                "[A] public",
                "[B] private",
                "[C] protected",
                "[D] transient"
            ],
            "correct_opt": "B",
            "hint": "Information hiding: only methods inside the same class can directly access 'private' fields.",
            "praise": "Master of Encapsulation! Making fields 'private' forces users to go through push() and pop() methods.",
            "roast": "If fields are 'public', outside code can write 'stack.top = -999' and corrupt the ADT invariants!"
        }
    },
    {
        "num": 3,
        "title": "Student Class and Array of Objects",
        "file": "java-lab/programs/Lab03StudentDemo.java",
        "problem": "Create a class Student (USN, Name, Branch, Phone). Create an array of N Student objects and print their details with formatted headings.",
        "concept": "Student[] students = new Student[n] creates an array of NULL references. Each index must be instantiated with: students[i] = new Student(...);",
        "blocks": [
            {
                "title": "Instance Field Disambiguation via 'this'",
                "code": "public Student(String usn, String name, double cgpa) {\n    this.usn = usn;\n    this.name = name;\n    this.cgpa = cgpa;\n}",
                "explanation": "'this' keyword distinguishes instance fields from constructor parameters of the same name, avoiding variable shadowing bugs."
            },
            {
                "title": "Array of Object References Allocation",
                "code": "Student[] students = new Student[n];\nfor (int i = 0; i < n; i++) {\n    students[i] = new Student(usn, name, cgpa);\n}",
                "explanation": "Allocating 'new Student[n]' creates an array of null references. You must instantiate each individual Student object in a loop."
            }
        ],
        "challenge": {
            "prompt": "Inside a constructor, how do you resolve shadowing when parameter names are identical to instance field names (e.g., usn, name)?",
            "opts": [
                "[A] Use the 'this' keyword (e.g., this.usn = usn;)",
                "[B] Use the 'super' keyword (e.g., super.usn = usn;)",
                "[C] Rename the constructor to match the field name",
                "[D] Declare the parameter static"
            ],
            "correct_opt": "A",
            "hint": "'this' refers to the current object instance, distinguishing 'this.field' from parameter 'field'.",
            "praise": "Spot on! 'this.usn = usn;' cleanly resolves parameter shadowing.",
            "roast": "Without 'this.', writing 'usn = usn;' just assigns the parameter to itself, leaving the instance field null!"
        }
    },
    {
        "num": 4,
        "title": "Runtime Polymorphism and Method Overriding",
        "file": "java-lab/programs/Lab04ShapePolymorphism.java",
        "problem": "Create base class Shape with draw() and erase(). Create subclasses Circle, Triangle, Square. Demonstrate polymorphism using superclass reference.",
        "concept": "Dynamic Method Dispatch: When an overridden method is called via a superclass reference (Shape s = new Circle(); s.draw()), Java resolves the call at runtime to Circle's draw().",
        "blocks": [
            {
                "title": "Abstract Superclass Polymorphic Blueprint",
                "code": "abstract class Shape {\n    abstract void draw();\n    abstract void erase();\n}",
                "explanation": "Defines interface contract without concrete implementation. Guarantees every subclass will provide draw() and erase() methods."
            },
            {
                "title": "Dynamic Method Dispatch (Virtual Method Invocation)",
                "code": "Shape s = new Circle(); // Superclass reference to subclass object\ns.draw(); // Invokes Circle's draw() at runtime via vtable!",
                "explanation": "The JVM inspects the actual object on the heap at runtime (Circle), resolving the call dynamically rather than at compile time."
            }
        ],
        "challenge": {
            "prompt": "When an abstract class 'Shape' has a method 'draw()', how does Java determine which subclass version (Circle, Triangle) to execute at runtime?",
            "opts": [
                "[A] Static compile-time early binding based on reference type",
                "[B] Dynamic method dispatch based on the actual object instance type on the heap",
                "[C] Random selection from loaded shape classes",
                "[D] Method overloading based on parameter count"
            ],
            "correct_opt": "B",
            "hint": "Java uses dynamic method dispatch (vtable lookup) at runtime to invoke the method of the actual object in memory.",
            "praise": "Polymorphism unlocked! Dynamic method dispatch routes calls to the true concrete instance.",
            "roast": "At runtime, the JVM looks at the ACTUAL heap object, not the reference variable type!"
        }
    },
    {
        "num": 5,
        "title": "Resizable Interface Implementation",
        "file": "java-lab/programs/Lab05ResizableInterface.java",
        "problem": "Create interface Resizable with resizeWidth(int width) and resizeHeight(int height). Create class Rectangle that implements Resizable.",
        "concept": "Interfaces define a strict contract. Any class that implements an interface MUST provide concrete implementations for all its abstract methods.",
        "blocks": [
            {
                "title": "Interface Definition Contract",
                "code": "interface Resizable {\n    void resizeWidth(int width);\n    void resizeHeight(int height);\n}",
                "explanation": "Interfaces declare 100% abstract methods. Classes implementing Resizable must provide concrete definitions for both methods."
            },
            {
                "title": "Class Implementation of Interface",
                "code": "class Rectangle implements Resizable {\n    @Override\n    public void resizeWidth(int w) { this.width = w; }\n    @Override\n    public void resizeHeight(int h) { this.height = h; }\n}",
                "explanation": "'implements' keyword fulfills interface contract. Methods must be declared 'public' since interface methods are implicitly public."
            }
        ],
        "challenge": {
            "prompt": "Which keyword must a Java class use to fulfill a contract defined by an interface like 'Resizable'?",
            "opts": [
                "[A] extends",
                "[B] implements",
                "[C] inherits",
                "[D] uses"
            ],
            "correct_opt": "B",
            "hint": "Classes 'extend' other classes, but 'implement' interfaces.",
            "praise": "Contract sealed! 'class Rectangle implements Resizable' binds the class to implement resizeWidth and resizeHeight.",
            "roast": "'extends' is for class or interface inheritance. A class 'implements' an interface!"
        }
    },
    {
        "num": 6,
        "title": "User-Defined Packages (mypack)",
        "file": "java-lab/programs/Lab06PackageDemo.java",
        "problem": "Develop a Java program to create a package named mypack and import & implement it in a suitable class.",
        "concept": "Packages group related classes and prevent namespace collisions. The source file must begin with: package mypack; and live in a matching folder.",
        "blocks": [
            {
                "title": "Package Declaration & Public Class Visibility",
                "code": "package mypack;\npublic class MyPackageClass {\n    public void display() { System.out.println(\"Inside mypack\"); }\n}",
                "explanation": "'package mypack;' groups the class into the mypack namespace. The class and methods must be 'public' to be accessible externally."
            },
            {
                "title": "Cross-Package Import & Instantiation",
                "code": "import mypack.MyPackageClass;\npublic class Lab06PackageDemo {\n    MyPackageClass obj = new MyPackageClass();\n    obj.display();\n}",
                "explanation": "'import mypack.MyPackageClass;' loads the class definition from the mypack directory structure into the caller's scope."
            }
        ],
        "challenge": {
            "prompt": "To allow a class in package 'mypack' to be imported and used by code in the default package, what access modifier must the class and its constructor have?",
            "opts": [
                "[A] package-private (default / no modifier)",
                "[B] public",
                "[C] protected",
                "[D] private"
            ],
            "correct_opt": "B",
            "hint": "Classes without 'public' cannot be seen outside their own package.",
            "praise": "Spot on! 'public class MyPackageClass' makes the class visible across package boundaries.",
            "roast": "Default package-private visibility restricts access to the same folder/package. It MUST be declared 'public'!"
        }
    },
    {
        "num": 7,
        "title": "Custom Exception Handling (Division By Zero)",
        "file": "java-lab/programs/Lab07CustomException.java",
        "problem": "Develop a Java program to raise a user-defined exception for Division By Zero using try, catch, throw, throws, and finally.",
        "concept": "Custom exceptions extend java.lang.Exception. 'throw' triggers the exception. 'throws' declares it in the method signature. 'finally' executes unconditionally.",
        "blocks": [
            {
                "title": "Custom Checked Exception Definition",
                "code": "class DivisionByZeroException extends Exception {\n    public DivisionByZeroException(String message) {\n        super(message);\n    }\n}",
                "explanation": "Inheriting from Exception creates a custom checked exception. Passing message to super() preserves error details in getMessage()."
            },
            {
                "title": "Explicit throw and catch Blocks",
                "code": "if (b == 0) throw new DivisionByZeroException(\"Divisor cannot be zero!\");\ntry {\n    compute(a, b);\n} catch (DivisionByZeroException e) {\n    System.out.println(\"Caught: \" + e.getMessage());\n}",
                "explanation": "'throw' fires the exception object immediately. Execution aborts normal path and jumps straight to the matching catch block."
            }
        ],
        "challenge": {
            "prompt": "What keyword is used in Java to actively instantiate and throw an exception when an illegal condition occurs (e.g. divisor == 0)?",
            "opts": [
                "[A] throws",
                "[B] throw (e.g., throw new DivisionByZeroException(\"...\");)",
                "[C] catch",
                "[D] assert"
            ],
            "correct_opt": "B",
            "hint": "'throws' declares what a method might throw, while 'throw' actually fires the exception object.",
            "praise": "Exception hurled! 'throw new CustomException(...)' transfers control immediately to the nearest catch block.",
            "roast": "'throws' is used in the method signature declaration. 'throw' is the active verb that throws an exception object!"
        }
    },
    {
        "num": 8,
        "title": "Multithreading and Concurrent Execution",
        "file": "java-lab/programs/Lab08ThreadConcurrency.java",
        "problem": "Create MyThread extending Thread. Call super(name) in constructor and start the thread. Observe concurrent execution of main and child threads.",
        "concept": "Calling start() registers the thread with the OS/JVM scheduler and spawns a new call stack that runs run(). Calling run() directly runs synchronously!",
        "blocks": [
            {
                "title": "Extending Thread & Overriding run()",
                "code": "class WorkerThread extends Thread {\n    @Override\n    public void run() {\n        System.out.println(\"Thread running: \" + getName());\n    }\n}",
                "explanation": "The run() method contains the concurrent task payload. It represents the entry point for the new concurrent execution unit."
            },
            {
                "title": "Spawning Concurrency via start()",
                "code": "WorkerThread t1 = new WorkerThread();\nt1.start(); // Spawns OS thread, runs concurrently with main!",
                "explanation": "Calling start() registers a new thread with the OS scheduler. Calling run() directly would run synchronously on main thread!"
            }
        ],
        "challenge": {
            "prompt": "To run a class extending Thread in a new concurrent thread of execution, which method must you invoke from main?",
            "opts": [
                "[A] thread.run()",
                "[B] thread.start()",
                "[C] thread.execute()",
                "[D] thread.fork()"
            ],
            "correct_opt": "B",
            "hint": "Calling .run() directly executes synchronously on the current thread! You must call .start() to spawn a new OS thread.",
            "praise": "Concurrency Master! Calling thread.start() registers a new thread of execution with the JVM scheduler.",
            "roast": "CLASSIC EXAM TRAP! Calling .run() runs on the MAIN thread synchronously! You MUST call .start() to go concurrent."
        }
    },
    {
        "num": 9,
        "title": "Java Enumerations and valueOf()",
        "file": "java-lab/programs/Lab09DepartmentEnum.java",
        "problem": "Create enumeration Department { CSE, ISE, ECE, MECH }. Accept department name as input and display selected department using valueOf().",
        "concept": "Enums provide type-safe constants. Enum.valueOf(String) matches input text to constant. If input doesn't match, throws IllegalArgumentException.",
        "blocks": [
            {
                "title": "Type-Safe Enum Declaration",
                "code": "enum Department {\n    CSE, ISE, ECE, MECH, CIVIL\n}",
                "explanation": "Java enums are full type-safe classes with fixed instances. Prevents passing arbitrary strings or invalid integer status codes."
            },
            {
                "title": "Parsing User Input via valueOf() with Exception Guard",
                "code": "try {\n    Department dept = Department.valueOf(input.toUpperCase());\n} catch (IllegalArgumentException e) {\n    System.out.println(\"Invalid department name entered!\");\n}",
                "explanation": "valueOf() converts input text to corresponding enum constant. If input doesn't match any constant, IllegalArgumentException is caught."
            }
        ],
        "challenge": {
            "prompt": "What runtime exception does 'Department.valueOf(str)' throw if the user inputs a string that does not match any enum constant?",
            "opts": [
                "[A] NullPointerException",
                "[B] IllegalArgumentException",
                "[C] ClassCastException",
                "[D] EnumNotFoundException"
            ],
            "correct_opt": "B",
            "hint": "When valueOf() receives an invalid enum string, Java throws java.lang.IllegalArgumentException.",
            "praise": "Bullseye! Catching IllegalArgumentException protects your console app from crashing on bad user input.",
            "roast": "The JVM throws IllegalArgumentException when an argument doesn't match known enum constants!"
        }
    },
    {
        "num": 10,
        "title": "Wrapper Classes and Autoboxing / Unboxing",
        "file": "java-lab/programs/Lab10MarksCalculator.java",
        "problem": "Read marks of 3 subjects as strings, convert them into wrapper Double objects, calculate total and average using autoboxing/unboxing, and display.",
        "concept": "Autoboxing automatically converts primitive double to Double object. Unboxing automatically converts Double object to primitive double in arithmetic.",
        "blocks": [
            {
                "title": "Autoboxing & Auto-unboxing",
                "code": "Double wrappedScore = 89.5; // Autoboxing: primitive double -> Double object\ndouble rawScore = wrappedScore; // Unboxing: Double object -> primitive double",
                "explanation": "Java compiler automatically converts between primitive types (double) and Wrapper classes (Double) seamlessly."
            },
            {
                "title": "Parsing Numeric Strings via Static Wrapper Methods",
                "code": "double val = Double.parseDouble(\"94.75\");\nDouble obj = Double.valueOf(\"94.75\");",
                "explanation": "parseDouble() extracts primitive value; valueOf() returns a cached Double object instance from the heap pool."
            }
        ],
        "challenge": {
            "prompt": "Which static method on class Double converts a String (e.g. '88.5') into a Double object or primitive double?",
            "opts": [
                "[A] Double.valueOf(str) or Double.parseDouble(str)",
                "[B] (Double)str",
                "[C] str.toDouble()",
                "[D] Double.convert(str)"
            ],
            "correct_opt": "A",
            "hint": "Double.valueOf() returns a Double object (autoboxing), while Double.parseDouble() returns a primitive double.",
            "praise": "Spot on! Double.valueOf() and Double.parseDouble() are standard methods for String parsing.",
            "roast": "You cannot cast String directly to Double with '(Double)str'! Use Double.valueOf(str) or Double.parseDouble(str)."
        }
    }
]
JAVA_VIVA_GAUNTLET = [
    {
        "q": "Why does Java NOT support multiple inheritance through classes?",
        "options": [
            "A) Because JVM bytecodes only support one class file at a time.",
            "B) To avoid the Diamond Problem (ambiguity when two parent classes define the same method).",
            "C) Because multiple inheritance was patented by C++.",
            "D) Because Java classes cannot have more than 10 methods."
        ],
        "ans": "B",
        "tip": "The Diamond Problem happens when class D extends B and C, which both extend A. If B and C override a method, D does not know which one to inherit! Interfaces solve this because they contain no state.",
        "praise": "Spot on! The Diamond Problem is the classic reason Java uses interfaces instead.",
        "roast": "Multiple inheritance of classes leads to ambiguity (the Diamond Problem)."
    },
    {
        "q": "What is the difference between final, finally, and finalize in Java?",
        "options": [
            "A) They are identical keywords used for backward compatibility.",
            "B) final is a modifier (constant/cannot override/cannot inherit); finally is a block in exception handling; finalize is a method called by the Garbage Collector.",
            "C) final is for loops; finally is for classes; finalize is for interfaces.",
            "D) final is deprecated; finally and finalize are active."
        ],
        "ans": "B",
        "tip": "final variable = constant; final method = cannot override; final class = cannot extend. finally = block after try/catch. finalize() = called before GC destroys object.",
        "praise": "Examiner favorite! You nailed the distinction between all three.",
        "roast": "Don't confuse them: final = modifier; finally = block; finalize = GC cleanup method."
    },
    {
        "q": "Why must super() or this() always be the very FIRST statement in a constructor?",
        "options": [
            "A) Because Java syntax rules say all method calls must be capitalized first.",
            "B) Because the superclass state must be fully initialized before the subclass can configure its own state.",
            "C) To prevent the garbage collector from running during object allocation.",
            "D) It is an optional recommendation that does not affect compilation."
        ],
        "ans": "B",
        "tip": "Object construction proceeds from superclass down to subclass. The child relies on parent fields being ready.",
        "praise": "Architectural mastery! Subclass fields depend on parent initialization completing first.",
        "roast": "The parent object must exist before the child can add its own state to it."
    },
    {
        "q": "What happens if you invoke thread.run() instead of thread.start() in Java?",
        "options": [
            "A) It throws an IllegalThreadStateException.",
            "B) It runs the run() code synchronously on the CURRENT thread without creating a new separate thread.",
            "C) It starts two threads at the same time.",
            "D) The JVM immediately crashes with an OutOfMemoryError."
        ],
        "ans": "B",
        "tip": "start() allocates a new call stack and requests OS scheduling. run() is just a normal method call executed on the current caller's thread!",
        "praise": "Brilliant! Calling run() directly bypasses all concurrency.",
        "roast": "Calling run() does NOT create a thread; it just executes sequentially on the current thread."
    },
    {
        "q": "What is the difference between String, StringBuilder, and StringBuffer in Java?",
        "options": [
            "A) String is mutable; StringBuilder and StringBuffer are immutable.",
            "B) String is immutable; StringBuilder is mutable and not synchronized (fast); StringBuffer is mutable and thread-safe (synchronized).",
            "C) StringBuffer is for numbers; StringBuilder is for text.",
            "D) They have identical performance characteristics."
        ],
        "ans": "B",
        "tip": "Strings cannot be modified after creation. For heavy concatenation, use StringBuilder (single-threaded) or StringBuffer (multi-threaded).",
        "praise": "Precise and complete! Immutability vs Thread-safety.",
        "roast": "String is immutable. StringBuilder is fast/unsynchronized. StringBuffer is thread-safe."
    }
]

# ==============================================================================
# INTERACTIVE OOP VISUALIZERS
# ==============================================================================

def visualizer_polymorphism():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}========== 🎭 RUNTIME POLYMORPHISM & VIRTUAL METHOD TABLE =========={Color.RESET}\n")
    print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
    print("Concept: Superclass reference pointing to different objects on the Heap:\n")
    print(f"  {Color.YELLOW}Shape s;{Color.RESET} (Reference variable allocated on Call Stack)")
    prompt_input(f"  {Color.DIM}Press Enter for Step 1 (Instantiating Circle)...{Color.RESET}")
    print(f"\n  [Step 1] s = {Color.GREEN}new Circle(){Color.RESET};  --> Heap allocates Circle object with its own vtable")
    print(f"           s.draw();           --> JVM invokes {Color.GREEN}Circle.draw() ⭕{Color.RESET}")
    prompt_input(f"  {Color.DIM}Press Enter for Step 2 (Reassigning to Triangle)...{Color.RESET}")
    print(f"\n  [Step 2] s = {Color.BLUE}new Triangle(){Color.RESET}; --> Heap allocates Triangle object")
    print(f"           s.draw();             --> Dynamic dispatch invokes {Color.BLUE}Triangle.draw() 🔺{Color.RESET}")
    prompt_input(f"  {Color.DIM}Press Enter for Step 3 (Reassigning to Square)...{Color.RESET}")
    print(f"\n  [Step 3] s = {Color.MAGENTA}new Square(){Color.RESET};   --> Heap allocates Square object")
    print(f"           s.draw();           --> Dynamic dispatch invokes {Color.MAGENTA}Square.draw() ⬛{Color.RESET}")
    print(f"\n{Color.CYAN}────────────────────────────────────────────────────────────────────────{Color.RESET}")
    print("Why Examiners Love This:")
    print("1. Method call `s.draw()` resolves at RUNTIME based on the ACTUAL OBJECT type, not reference type.")
    print("2. This is the definition of Dynamic Method Dispatch (Runtime Polymorphism).")
    print(f"{Color.CYAN}────────────────────────────────────────────────────────────────────────{Color.RESET}\n")
    prompt_input("Press Enter to return...")

def visualizer_threads():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}========== 🧵 THREAD LIFE-CYCLE STATE MACHINE =========={Color.RESET}\n")
    print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
    print("""
     [NEW] ──(start())──> [RUNNABLE] <───> [TIMED_WAITING] (sleep / wait)
                               │
                               └──(run() ends)──> [TERMINATED]
    """)
    print("Step-by-step thread execution trace:\n")
    print("  [Step 1] Thread t = new MyThread();  --> State: [NEW] (Object created, no thread spawned yet)")
    prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
    print("  [Step 2] t.start();                   --> State: [RUNNABLE] (JVM scheduler allocates thread call stack)")
    prompt_input(f"  {Color.DIM}Press Enter for Step 3 (Concurrent execution)...{Color.RESET}")
    print("\n  [Step 3] JVM context switching between Main & Child thread:")
    for i in range(1, 4):
        print(f"     {Color.BLUE}[Main Thread]  Running task iteration {i}{Color.RESET}")
        time.sleep(0.35)
        print(f"     {Color.GREEN}[Child Thread] Running concurrent iteration {i}{Color.RESET}")
        time.sleep(0.35)
    prompt_input(f"\n  {Color.DIM}Press Enter for Step 4...{Color.RESET}")
    print("\n  [Step 4] run() method completes      --> State: [TERMINATED] (Thread terminates cleanly)")
    print(f"\n{Color.GREEN}✔ Concurrent execution and life-cycle demonstrated cleanly!{Color.RESET}\n")
    prompt_input("Press Enter to return...")

# ==============================================================================
# EXPERIMENT RUNNER
# ==============================================================================

def mode_java_disaster():
    clear_screen()
    print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║       🚨 MODE: JAVA OOP DISASTER RECOVERY (8 REAL EMERGENCIES)     ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_slow("These are real-world JVM crashes, NullPointerExceptions, and concurrency bugs.", 0.012, Color.CYAN)
    print_slow("Find the bug and fix the crash before the server goes down!\n", 0.012)

    score = 0
    scenarios = list(JAVA_DISASTER_SCENARIOS)
    random.shuffle(scenarios)
    for i, s in enumerate(scenarios, 1):
        clear_screen()
        print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║     🚨 JAVA EMERGENCY {i}/{len(scenarios)}: JVM CRASH IN PROGRESS            ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print(f"{Color.BOLD}{Color.WHITE}{s['title']}{Color.RESET}\n")
        print_slow(s['story'], 0.010, Color.WHITE)
        print(f"\n{Color.CYAN}{Color.BOLD}Diagnostic Question:{Color.RESET}\n  {s['prompt']}\n")

        for idx, ch in enumerate(s["choices"], 1):
            print(f"  {Color.YELLOW}[{idx}]{Color.RESET} {ch}")

        while True:
            pick = prompt_input(f"\n{Color.BOLD}Your decision [1 - 4] (0=Menu): {Color.RESET}").strip()
            if pick in ["0", "menu", "q", "exit"]:
                return
            if pick in ["1", "2", "3", "4"]:
                pick = int(pick)
                break
            print(f"{Color.RED}Please enter 1, 2, 3, or 4!{Color.RESET}")

        spinner("Analyzing JVM bytecode & call stack", duration=0.6, color=Color.RED)

        if pick == s["ans_idx"]:
            anim_correct()
            _award_xp(150, "java disaster averted")
            _unlock_badge("java_marshal")
            score += 150
            print(f"\n{Color.GREEN}{Color.BOLD}✅ DISASTER AVERTED! (+150 XP){Color.RESET}")
            print(f"{Color.GREEN}{s['reaction']}{Color.RESET}\n")
        else:
            anim_wrong()
            _break_streak()
            print(f"\n{Color.RED}{Color.BOLD}❌ WRONG DIAGNOSIS! Correct answer was [{s['ans_idx']}]:{Color.RESET}")
            print(f"   {Color.WHITE}{s['choices'][s['ans_idx']-1]}{Color.RESET}")
            print(f"\n{Color.DIM}{s['reaction']}{Color.RESET}\n")
        prompt_input(f"{Color.DIM}Press Enter for next scenario...{Color.RESET}")

    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*51}")
    print(f"  Java Disaster Recovery Complete! Score: {score}/{len(scenarios)*150}")
    print(f"{'═'*51}{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def run_java_experiment_lab(exp):
    base_dir = PROJECT_ROOT
    source_path = os.path.join(base_dir, exp["file"])

    # Stage 1: The Big Picture & Intuition
    clear_screen()
    print()
    _show_session_header(subject="java")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  ☕ JAVA EXPERIMENT {exp['num']:02d}: {exp['title']:<55} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    print(f"{Color.YELLOW}{Color.BOLD}[Stage 1/4] 💡 THE OOP CONCEPT & MENTAL MODEL:{Color.RESET}")
    print()
    print_slow(f"  {exp['concept']}", 0.008, Color.WHITE)
    print()
    print(f"{Color.CYAN}{Color.BOLD}🎯 VTU Lab Requirement:{Color.RESET}")
    print(f"  {exp['problem']}")
    print()
    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the complete Java code first...{Color.RESET}")

    # Stage 2: Complete Source Code First
    clear_screen()
    print()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  📄 [Stage 2/4] COMPLETE VERIFIED JAVA PROGRAM CODE                           ║")
    print(f"║  Source: {exp['file']:<68} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    funny_spinners = [
        "Warming up the JVM (this might take longer than your exam prep)",
        "malloc()-ing your Java knowledge (wait, wrong language...)",
        "Garbage collecting your misconceptions",
        "Loading bytecode into your cerebral cortex",
        "Asking the JVM scheduler to prioritize your learning",
    ]
    spinner(random.choice(funny_spinners), duration=0.5, color=Color.BLUE)
    print()

    if os.path.isfile(source_path):
        with open(source_path, "r", encoding="utf-8", errors="replace") as sf:
            lines = sf.readlines()
        preview_limit = min(36, len(lines))
        for idx in range(preview_limit):
            print(f"{Color.DIM}{idx+1:3d} |{Color.RESET} {lines[idx]}", end="")
        if len(lines) > preview_limit:
            print(f"\n  {Color.YELLOW}... [{len(lines) - preview_limit} more lines in full file: {exp['file']}]{Color.RESET}")
    else:
        print(f"  {Color.RED}Source file available in {exp['file']}{Color.RESET}")

    print()
    print(Color.DIM + ("─" * 80) + Color.RESET)
    print(f"  {Color.CYAN}Options:{Color.RESET}  {Color.YELLOW}[V]{Color.RESET} View Full Code in Vault   {Color.GREEN}[Enter]{Color.RESET} Continue to Logic Breakdown")
    sub_pick = prompt_input("  Your choice: ").strip().upper()
    if sub_pick == "V":
        _view_source_file(source_path, exp['title'])

    # Stage 3: Block-by-Block Logic Walkthrough
    clear_screen()
    print()
    print(Color.MAGENTA + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🔍 [Stage 3/4] DEEP BLOCK-BY-BLOCK LOGIC (How the Code Works)                ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    for idx, b in enumerate(exp["blocks"], 1):
        print(f"  {Color.YELLOW}{Color.BOLD}🧱 Block {idx}: {b['title']}{Color.RESET}")
        print("  " + Color.DIM + ("─" * 68) + Color.RESET)
        for l in b["code"].splitlines():
            print(f"    {Color.WHITE}{Color.BOLD}{l}{Color.RESET}")
        print(f"  {Color.CYAN}  ↳ Why this matters:{Color.RESET} {b['explanation']}")
        print()

    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Ready? Press Enter to test your understanding with a quick challenge!{Color.RESET}")

    # Stage 4: Guided Code Challenge (MCQ)
    clear_screen()
    ch = exp["challenge"]
    print()
    print(Color.YELLOW + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🎮 [Stage 4/4] GUIDED CODE CHALLENGE — Check Your Understanding!             ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()
    _show_session_header(subject="java")

    print(f"{Color.BOLD}{Color.WHITE}{ch['prompt']}{Color.RESET}")
    print()

    if "opts" in ch:
        for opt in ch["opts"]:
            print(f"  {Color.CYAN}{opt}{Color.RESET}")
        print()
        print("  " + Color.DIM + "(Tip: Type A, B, C, D or 'H' for a Hint  |  No shame in hints!)" + Color.RESET)
        print()

        while True:
            ans = prompt_input(f"{Color.BOLD}Your Answer [A/B/C/D] (or 'H' for Hint): {Color.RESET}").strip().upper()
            if ans == "H":
                print(f"\n  {Color.YELLOW}💡 HINT: {ch['hint']}{Color.RESET}\n")
                continue
            if ans in ("A", "B", "C", "D"):
                break
            print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

        spinner(random.choice([
            "Evaluating against Java JVM standards",
            "Running javac on your answer (mentally)",
            "Checking your answer against the Oracle docs",
            "Consulting the Java Language Specification",
        ]), duration=0.6, color=Color.BLUE)

        if ans == ch.get("correct_opt", "A"):
            anim_correct()
            _award_xp(50, "MCQ correct")
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 {ch['praise']}{Color.RESET}\n")
        else:
            anim_wrong()
            _break_streak()
            print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
            print(f"   {Color.YELLOW}✅ Expected Answer was ({ch.get('correct_opt', 'A')}): {ch['hint']}{Color.RESET}\n")
    else:
        print(f"  {Color.DIM}Hint: {ch['hint']}{Color.RESET}\n")
        user_ans = prompt_input(f"{Color.GREEN}Your Answer > {Color.RESET}").strip()
        norm_user = "".join(user_ans.split()).lower()
        norm_accepted = ["".join(a.split()).lower() for a in ch.get("answers", [])]

        if norm_user in norm_accepted or any(norm_user in a for a in norm_accepted):
            anim_correct()
            _award_xp(50, "correct")
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 {ch['praise']}{Color.RESET}\n")
        else:
            anim_wrong()
            _break_streak()
            print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
            print(f"   {Color.YELLOW}Expected: {ch['hint']}{Color.RESET}\n")

    # Mark experiment as done
    exp_id = f"JAVA-{exp['num']}"
    if exp_id not in _SESSION["experiments_done"]:
        _SESSION["experiments_done"].append(exp_id)
        _save_to_local_db()

    print(f"{Color.DIM}File location: {exp['file']}{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Java Lab Studio...{Color.RESET}")


def mode_java_viva():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎓 JAVA OOP VIVA PREP & CONCEPT MASTERY (1BCS302) 🎓{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
    print("  Stress-free practice with Socratic hints and examiner expectations.\n")

    score = 0
    questions = list(JAVA_VIVA_GAUNTLET)
    random.shuffle(questions)

    for idx, q in enumerate(questions, 1):
        print(f"\n{Color.CYAN}{Color.BOLD}[Question {idx}/{len(questions)}]{Color.RESET}")
        print(f"{Color.BOLD}{q['q']}{Color.RESET}\n")
        for opt in q["options"]:
            print(f"  {opt}")

        attempt = 1
        solved = False
        while attempt <= 2 and not solved:
            prompt_str = "\nYour Answer [A / B / C / D] (or 'H' for Clue, 0 to Exit): " if attempt == 1 else "\nSecond Try [A / B / C / D]: "
            ans = prompt_input(prompt_str).strip().upper()

            if ans in ("0", "EXIT", "Q"):
                return
            if ans == "H":
                print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                continue
            if ans not in ("A", "B", "C", "D"):
                print(f"  {Color.RED}Please type A, B, C, or D!{Color.RESET}")
                continue

            if ans == q["ans"]:
                solved = True
                anim_correct()
                _award_xp(10, "java viva correct")
                score += 1
                if attempt == 1:
                    print(f"  {Color.GREEN}{Color.BOLD}✔ {q['praise']}{Color.RESET}")
                else:
                    print(f"  {Color.GREEN}{Color.BOLD}🎉 Excellent recovery buddy! You got it right! ❤️{Color.RESET}")
            else:
                anim_wrong()
                if attempt == 1:
                    print(f"  {Color.YELLOW}🌱 Not quite buddy! {q['roast']}{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                    attempt += 1
                else:
                    print(f"  {Color.MAGENTA}🤝 No worries buddy! The correct answer is [{q['ans']}].{Color.RESET}")
                    attempt += 1

        print(f"\n  {Color.CYAN}💡 Examiner Expectation: {q['tip']}{Color.RESET}")
        prompt_input(f"\n{Color.DIM}Press Enter for next question...{Color.RESET}")

    print(f"\n{Color.CYAN}===================================================={Color.RESET}")
    print(f"  🎉 Viva Practice Complete! Mastered: {Color.BOLD}{score}/{len(questions)} Concepts{Color.RESET}")
    print(f"{Color.CYAN}===================================================={Color.RESET}\n")
    prompt_input("Press Enter to return...")


def mode_java_studio():
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  ☕ JAVA OOP LAB STUDIO: 1BCS302 (VTU 2025 Scheme — 10 Experiments)")
        print(f"{Color.CYAN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="java")
        print(f"  {Color.YELLOW}[V1]{Color.RESET} 🔄 Interactive Runtime Polymorphism Visualizer (Dynamic Dispatch)")
        print(f"  {Color.YELLOW}[V2]{Color.RESET} 🧵 Interactive Concurrency Visualizer (Race Conditions & Threads)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨 Java Lab Disaster Recovery (8 Real Exam Emergencies)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 External Examiner Java Viva Gauntlet (3 Lives)")
        print(f"  {Color.CYAN}{'─'*78}{Color.RESET}")
        print(f"  {Color.BOLD}VTU PRESCRIBED OOP EXPERIMENTS{Color.RESET}")
        for i in range(10):
            exp = JAVA_EXPERIMENTS[i]
            done = "✅" if f"JAVA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        # Streak motivator
        streak = _SESSION["streak"]
        if streak >= 3:
            print(f"\n  {Color.RED}{Color.BOLD}🔥 You're on a {streak}-streak! JVM is impressed!{Color.RESET}")
        elif streak >= 1:
            print(f"\n  {Color.YELLOW}⚡ Streak: {streak} — keep going!{Color.RESET}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 10, V1, V2, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "V1":
            visualizer_polymorphism()
        elif choice == "V2":
            visualizer_threads()
        elif choice == "DR":
            mode_java_disaster()
        elif choice == "VG":
            mode_java_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 10:
                run_java_experiment_lab(JAVA_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)

