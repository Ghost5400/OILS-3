"""
☕ OILS-3: OBJECT-ORIENTED PROGRAMMING WITH JAVA ARCADE ENGINE (1BCS302)
Part of OILS-3: Oops, I Learnt Something! (3rd Sem Engineering Edition)

Features:
- 10 Interactive VTU 2025 Scheme Lab Experiments with Block-by-Block Logic
- "Your Turn to Code" Hands-On Coding Challenges
- Interactive OOP Visualizers (Polymorphism Dispatch, Exception Stack, Thread Life-Cycle)
- 25 External Examiner Viva Questions with Lives & Roasts
"""

import sys
import time
import os
import random

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_input(prompt_text=""):
    sys.stdout.flush()
    while prompt_text.startswith("\n"):
        sys.stdout.write("\n")
        prompt_text = prompt_text[1:]
    sys.stdout.write(prompt_text)
    sys.stdout.flush()
    try:
        import msvcrt
        chars = []
        while True:
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                break
            elif ch == "\003":
                raise KeyboardInterrupt
            elif ch == "\b":
                if chars:
                    chars.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif ch >= " ":
                chars.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()
        return "".join(chars)
    except ImportError:
        try:
            return sys.stdin.readline().rstrip("\r\n")
        except (EOFError, KeyboardInterrupt):
            return ""

def spinner(label="Compiling & Running", duration=1.0, color=Color.CYAN):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {color}{frames[i % len(frames)]}{Color.RESET}  {label}...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {Color.GREEN}✔{Color.RESET}  {label}... complete!      \n")
    sys.stdout.flush()

def anim_correct():
    for f in [f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT! JVM VERIFIED!  ✅{Color.RESET}",
              f"{Color.WHITE}{Color.BOLD}  ✅  CORRECT! JVM VERIFIED!  ✅{Color.RESET}",
              f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT! JVM VERIFIED!  ✅{Color.RESET}"]:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.15)
    print()

def anim_wrong():
    for f in [f"{Color.RED}{Color.BOLD}  ❌  COMPILATION ERROR!  ❌{Color.RESET}",
              f"{Color.WHITE}{Color.BOLD}  ❌  COMPILATION ERROR!  ❌{Color.RESET}",
              f"{Color.RED}{Color.BOLD}  ❌  COMPILATION ERROR!  ❌{Color.RESET}"]:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.15)
    print()

# ==============================================================================
# 10 JAVA EXPERIMENTS DATABASE
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
                "title": "2D Array Dynamic Allocation",
                "code": "int[][] A = new int[rows][cols];\nint[][] B = new int[rows][cols];\nint[][] C = new int[rows][cols];",
                "explanation": "Allocates array references on the Heap. All elements default to 0."
            },
            {
                "title": "Element-Wise Summation",
                "code": "for (int i = 0; i < rows; i++) {\n    for (int j = 0; j < cols; j++) {\n        C[i][j] = A[i][j] + B[i][j];\n    }\n}",
                "explanation": "Nested loops iterate row-by-row and col-by-col in O(R * C) time."
            }
        ],
        "challenge": {
            "prompt": "Write the Java code line to declare and allocate a 2D integer array named 'matrix' with 3 rows and 4 columns:",
            "answers": [
                "int[][] matrix = new int[3][4];",
                "int [][] matrix = new int[3][4];",
                "int matrix[][] = new int[3][4];",
                "int[][] matrix=new int[3][4];"
            ],
            "hint": "int[][] matrix = new int[3][4];",
            "praise": "Clean Java syntax! Heap memory allocated for a 3x4 matrix.",
            "roast": "Standard Java array declaration: int[][] matrix = new int[3][4];"
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
                "title": "Class Encapsulation & Guard Checks",
                "code": "class Stack {\n    private int[] arr = new int[10];\n    private int top = -1;\n    public void push(int val) { ... }\n}",
                "explanation": "Fields are marked private. Callers must interact solely through public methods."
            }
        ],
        "challenge": {
            "prompt": "In class Stack, what keyword is used to hide 'arr' and 'top' from direct external access?",
            "answers": [
                "private",
                "private keyword"
            ],
            "hint": "private",
            "praise": "Correct! 'private' achieves data hiding and encapsulation.",
            "roast": "Use the 'private' access modifier to enforce encapsulation."
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
                "title": "Instantiation Loop",
                "code": "Student[] students = new Student[n];\nfor (int i = 0; i < n; i++) {\n    students[i] = new Student(usn, name, branch, phone);\n}",
                "explanation": "Avoids NullPointerException by instantiating each individual object in heap memory."
            }
        ],
        "challenge": {
            "prompt": "Inside a constructor, what keyword distinguishes instance variables from parameter variables with the same name?",
            "answers": [
                "this",
                "this keyword",
                "this."
            ],
            "hint": "this (e.g. this.name = name;)",
            "praise": "Spot on! 'this' references the current instance.",
            "roast": "Use 'this' to disambiguate: this.name = name;"
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
                "title": "Polymorphic Call",
                "code": "Shape s;\ns = new Circle();\ns.draw(); // Calls Circle's draw()\ns = new Triangle();\ns.draw(); // Calls Triangle's draw()",
                "explanation": "One interface, multiple implementations. The JVM executes based on the object type on the heap."
            }
        ],
        "challenge": {
            "prompt": "What annotation should be placed above a method in a subclass that overrides a superclass method?",
            "answers": [
                "@Override",
                "@override",
                "Override"
            ],
            "hint": "@Override",
            "praise": "Exactly right! @Override tells the compiler to check method signature matching.",
            "roast": "Use the @Override annotation."
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
                "title": "Interface Contract",
                "code": "interface Resizable {\n    void resizeWidth(int width);\n    void resizeHeight(int height);\n}\nclass Rectangle implements Resizable { ... }",
                "explanation": "All interface methods are implicitly public abstract."
            }
        ],
        "challenge": {
            "prompt": "What keyword does a Java class use to declare that it fulfills an interface contract?",
            "answers": [
                "implements",
                "implements keyword"
            ],
            "hint": "implements",
            "praise": "Correct! Classes use 'implements' for interfaces.",
            "roast": "Classes 'implement' interfaces and 'extend' other classes."
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
                "title": "Package Declaration & Import",
                "code": "// In mypack/MyPackageClass.java\npackage mypack;\npublic class MyPackageClass { ... }\n\n// In PackageDemo.java\nimport mypack.MyPackageClass;",
                "explanation": "The class and its methods must be declared 'public' to be accessible outside the package."
            }
        ],
        "challenge": {
            "prompt": "What access modifier must a class have so it can be imported from outside its package?",
            "answers": [
                "public",
                "public modifier",
                "public access"
            ],
            "hint": "public",
            "praise": "Spot on! Default (package-private) classes cannot be imported outside their package.",
            "roast": "A class must be declared 'public' to be imported across packages."
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
                "title": "Custom Exception Class",
                "code": "class DivisionByZeroException extends Exception {\n    public DivisionByZeroException(String msg) {\n        super(msg);\n    }\n}",
                "explanation": "Passes the custom error message up to the Exception base class."
            }
        ],
        "challenge": {
            "prompt": "What keyword is used to explicitly instantiate and throw an exception object in Java?",
            "answers": [
                "throw",
                "throw keyword"
            ],
            "hint": "throw (e.g. throw new MyException(\"error\");)",
            "praise": "Exact! 'throw' raises the exception; 'throws' declares it.",
            "roast": "Use 'throw' to trigger an exception: throw new Exception();"
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
                "title": "Thread Spawning",
                "code": "class MyThread extends Thread {\n    public MyThread(String name) {\n        super(name);\n        start(); // Starts child thread asynchronously!\n    }\n}",
                "explanation": "Spawns a concurrent OS thread. Main thread and Child thread interleave execution."
            }
        ],
        "challenge": {
            "prompt": "What method must be called to start a new thread asynchronously (NOT run directly)?",
            "answers": [
                "start()",
                "start",
                "thread.start()"
            ],
            "hint": "start()",
            "praise": "Correct! Calling start() spawns the thread. Calling run() does NOT create a new thread.",
            "roast": "Always call start() to initiate asynchronous execution."
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
                "title": "valueOf() Parsing & Exception Handling",
                "code": "try {\n    Department d = Department.valueOf(input.toUpperCase());\n} catch (IllegalArgumentException e) {\n    System.out.println(\"Invalid department!\");\n}",
                "explanation": "Safely converts string to enum constant while handling unrecognized inputs."
            }
        ],
        "challenge": {
            "prompt": "What runtime exception is thrown by valueOf() if the provided string does not match any enum constant?",
            "answers": [
                "IllegalArgumentException",
                "IllegalArgumentException exception"
            ],
            "hint": "IllegalArgumentException",
            "praise": "Spot on! IllegalArgumentException is thrown for invalid enum names.",
            "roast": "valueOf() throws IllegalArgumentException if the name doesn't match."
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
                "title": "Parsing and Autoboxing",
                "code": "Double m1 = Double.valueOf(str1);\nDouble total = m1 + m2 + m3; // Unboxes to double for +, then autoboxes to Double",
                "explanation": "Combines object wrappers and primitive arithmetic seamlessly."
            }
        ],
        "challenge": {
            "prompt": "What static method on class Double parses a String into a Double wrapper object?",
            "answers": [
                "Double.valueOf()",
                "Double.valueOf",
                "valueOf()",
                "valueOf"
            ],
            "hint": "Double.valueOf()",
            "praise": "Exact! Double.valueOf(str) returns a Double wrapper object.",
            "roast": "Use Double.valueOf(str) or Double.parseDouble(str)."
        }
    }
]

# ==============================================================================
# 25 EXTERNAL EXAMINER JAVA VIVA QUESTIONS
# ==============================================================================

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
    print("Concept: Superclass reference pointing to different objects on the Heap:")
    print(f"""
    {Color.YELLOW}Shape s;{Color.RESET} (Reference on Stack)
        │
        ├──> {Color.GREEN}new Circle(){Color.RESET}   ==> s.draw() invokes {Color.GREEN}Circle.draw() ⭕{Color.RESET}
        ├──> {Color.BLUE}new Triangle(){Color.RESET} ==> s.draw() invokes {Color.BLUE}Triangle.draw() 🔺{Color.RESET}
        └──> {Color.MAGENTA}new Square(){Color.RESET}   ==> s.draw() invokes {Color.MAGENTA}Square.draw() ⬛{Color.RESET}
    """)
    print("How the JVM resolves this at runtime:")
    print("1. Method call `s.draw()` looks up the object's Virtual Method Table (vtable) pointer.")
    print("2. Even though `s` is declared of type Shape, the JVM calls the child's overridden implementation.")
    print("3. This enables loose coupling and extensibility without changing the caller code!\n")
    prompt_input("Press Enter to return...")

def visualizer_threads():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}========== 🧵 THREAD LIFE-CYCLE STATE MACHINE =========={Color.RESET}\n")
    print(f"""
     [NEW] ──(start())──> [RUNNABLE] <───> [TIMED_WAITING] (sleep / wait)
                               │
                               └──(run() ends)──> [TERMINATED]
    """)
    print("Demonstration: Main Thread & Child Thread concurrency:")
    for i in range(1, 4):
        print(f"  {Color.BLUE}[Main Thread] Iteration {i}{Color.RESET}")
        time.sleep(0.3)
        print(f"  {Color.GREEN}[Child Thread] Iteration {i}{Color.RESET}")
        time.sleep(0.3)
    print(f"\n{Color.GREEN}✔ Concurrent execution complete!{Color.RESET}\n")
    prompt_input("Press Enter to return...")

# ==============================================================================
# EXPERIMENT RUNNER
# ==============================================================================

def run_java_experiment_lab(exp):
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}")
    print(f"  ☕ JAVA EXPERIMENT {exp['num']:02d}: {exp['title']}")
    print(f"{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}\n")

    print(f"{Color.YELLOW}{Color.BOLD}🎯 VTU PROBLEM REQUIREMENT:{Color.RESET}")
    print(f"  {exp['problem']}\n")

    print(f"{Color.BLUE}{Color.BOLD}💡 THE OOP CONCEPT & MENTAL MODEL:{Color.RESET}")
    print(f"  {exp['concept']}\n")

    print(f"{Color.MAGENTA}{Color.BOLD}🔍 DEEP BLOCK-BY-BLOCK CODE LOGIC:{Color.RESET}")
    for idx, b in enumerate(exp["blocks"], 1):
        print(f"\n  {Color.BOLD}[Block {idx}: {b['title']}]{Color.RESET}")
        for l in b["code"].splitlines():
            print(f"    {Color.WHITE}{l}{Color.RESET}")
        print(f"    {Color.CYAN}↳ Logic:{Color.RESET} {b['explanation']}")

    print(f"\n{Color.GREEN}{Color.BOLD}--------------------------------------------------------------------------------{Color.RESET}")
    print(f"🎮 {Color.YELLOW}{Color.BOLD}YOUR TURN TO CODE! HANDS-ON CHALLENGE:{Color.RESET}")
    print(f"  {exp['challenge']['prompt']}\n")

    user_ans = prompt_input(f"{Color.GREEN}Code > {Color.RESET}").strip()

    norm_user = "".join(user_ans.split())
    norm_accepted = ["".join(a.split()) for a in exp["challenge"]["answers"]]

    if norm_user in norm_accepted or any(norm_user.startswith(a) for a in norm_accepted):
        anim_correct()
        print(f"\n{Color.GREEN}🎉 {exp['challenge']['praise']}{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"\n{Color.RED}⚠️  {exp['challenge']['roast']}{Color.RESET}")
        print(f"   {Color.YELLOW}Expected:{Color.RESET} {exp['challenge']['hint']}\n")

    print(f"{Color.DIM}File location: {exp['file']}{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Java Lab Studio...{Color.RESET}")

# ==============================================================================
# JAVA VIVA GAUNTLET
# ==============================================================================

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

# ==============================================================================
# JAVA LAB STUDIO MAIN MENU
# ==============================================================================

def mode_java_studio():
    while True:
        clear_screen()
        print(f"\n{Color.BLUE}{Color.BOLD}================================================================================{Color.RESET}")
        print(f"  ☕ JAVA OOP LAB STUDIO: 1BCS302 (VTU 2025 Scheme — 10 Experiments)")
        print(f"{Color.BLUE}{Color.BOLD}================================================================================{Color.RESET}\n")
        print(f"  {Color.YELLOW}[V1]{Color.RESET} 🎭 Runtime Polymorphism & Virtual Method Table Visualizer")
        print(f"  {Color.YELLOW}[V2]{Color.RESET} 🧵 Multithreading State Machine Visualizer")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 External Examiner Java Viva Practice (Stress-Free Mastery)")
        print(f"  {Color.CYAN}------------------------------------------------------------------------------{Color.RESET}")
        print(f"  {Color.BOLD}LAB EXPERIMENTS{Color.RESET}")
        for exp in JAVA_EXPERIMENTS:
            print(f"  {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select an experiment [01 - 10, V1, V2, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "V1":
            visualizer_polymorphism()
        elif choice == "V2":
            visualizer_threads()
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

