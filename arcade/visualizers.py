"""
arcade.visualizers — Interactive Memory, Runtime & Architecture Visualizers
22 Deep Step-by-Step & Animated Visualizers for DSA (1BCSL306) & Java OOP (1BCS302).
"""
import os
import sys
import time
from arcade.core import Color, clear_screen, prompt_input
from arcade.session import _record_visualizer_explored

# ════════════════════════════════════════════════════════════════════════════════
# REUSABLE STEPPER & ANIMATION ENGINE
# ════════════════════════════════════════════════════════════════════════════════

def _run_visualizer_steps(vis_id, title, subtitle, steps, takeaways):
    """
    Renders multi-step visualizers with support for both:
    1. Interactive Step-by-Step mode (user presses Enter to step through)
    2. Auto-Play Live Animation mode (automatically steps through with pauses)
    """
    clear_screen()
    _record_visualizer_explored(vis_id)

    border = "═" * 78
    print(f"\n{Color.CYAN}{Color.BOLD}╔{border}╗")
    print(f"║  {title:<76}║")
    print(f"╚{border}╝{Color.RESET}\n")
    print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
    print(f"  {Color.WHITE}{subtitle}{Color.RESET}\n")
    print(f"  {Color.DIM}Animation Controls:{Color.RESET}")
    print(f"    {Color.GREEN}[Enter]{Color.RESET}  Step-by-Step Mode (You control each step)")
    print(f"    {Color.CYAN}[A]{Color.RESET}      Auto-Play Live Animation (Runs frame-by-frame automatically)\n")

    mode_choice = prompt_input(f"  {Color.BOLD}Choose playback mode [Enter / A]: {Color.RESET}").strip().upper()
    auto_play = mode_choice in ("A", "AUTO", "PLAY")

    for i, s in enumerate(steps, 1):
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔{border}╗")
        print(f"║  {title:<76}║")
        print(f"╚{border}╝{Color.RESET}")
        print(f"  {Color.YELLOW}{Color.BOLD}Step {i}/{len(steps)}: {s['title']}{Color.RESET}\n")
        
        if s.get("code"):
            print(f"  {Color.BOLD}Code / Expression:{Color.RESET} {Color.WHITE}{s['code']}{Color.RESET}\n")
        
        if s.get("diagram"):
            print(s["diagram"])
        
        if s.get("desc"):
            print(f"\n  {Color.GREEN}↳ What happens:{Color.RESET} {s['desc']}")
        if s.get("why"):
            print(f"  {Color.YELLOW}↳ Why it matters:{Color.RESET} {s['why']}")

        print()
        if i < len(steps):
            if auto_play:
                time.sleep(1.2)
            else:
                next_in = prompt_input(f"  {Color.DIM}Press Enter for next step (or 'A' to switch to Auto-Play, 'Q' to quit)... {Color.RESET}").strip().upper()
                if next_in in ("A", "AUTO"):
                    auto_play = True
                elif next_in in ("Q", "QUIT", "EXIT"):
                    break

    print(f"\n{Color.CYAN}{'─'*78}{Color.RESET}")
    print(f"  {Color.BOLD}💡 Key Viva Takeaways & Examiner Tips:{Color.RESET}")
    for idx, t in enumerate(takeaways, 1):
        print(f"  {idx}. {t}")
    print(f"{Color.CYAN}{'─'*78}{Color.RESET}\n")
    prompt_input("  Press Enter to return to Visualizer Menu... ")


# ════════════════════════════════════════════════════════════════════════════════
# 1. DSA MEMORY & ARCHITECTURE VISUALIZERS (DSA-V1 to DSA-V12)
# ════════════════════════════════════════════════════════════════════════════════

def vis_dsa_memory():
    """DSA-V1: Memory Architecture & Pointer Lifecycle (Stack vs Heap)"""
    steps = [
        {
            "title": "Declaring the pointer variable",
            "code": "int *ptr;",
            "diagram": r"""    CALL STACK (Fast, Automatic)       HEAP SPACE (Dynamic, Manual)
    ┌──────────────────────────────┐   ┌──────────────────────────────┐
    │  [main frame]                │   │                              │
    │  ptr: [ 0x3FA8C0 (Garbage) ] │   │  (Free memory chunks)        │
    └──────────────────────────────┘   └──────────────────────────────┘""",
            "desc": "Allocates 8 bytes on Call Stack for pointer `ptr`. Contains random garbage address until initialized.",
            "why": "Dereferencing an uninitialized pointer causes Segmentation Fault / Undefined Behavior!"
        },
        {
            "title": "Allocating memory dynamically via malloc()",
            "code": "ptr = (int *)malloc(sizeof(int));",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌──────────────────────────────┐
    │  ptr: [ 0x7FFF0040 ] ────────┼──>│  0x7FFF0040: [ ? ? ? ? ]     │
    └──────────────────────────────┘   └──────────────────────────────┘""",
            "desc": "OS kernel reserves 4 bytes on Heap at address 0x7FFF0040. `ptr` stores this exact address.",
            "why": "malloc() does NOT initialize memory! Memory contains raw uninitialized byte values."
        },
        {
            "title": "Dereferencing the pointer to write data",
            "code": "*ptr = 42;",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌──────────────────────────────┐
    │  ptr: [ 0x7FFF0040 ] ────────┼──>│  0x7FFF0040: [   42   ]      │
    └──────────────────────────────┘   └──────────────────────────────┘""",
            "desc": "The '*' dereference operator follows the stored address directly to Heap slot 0x7FFF0040 and writes 42.",
            "why": "The pointer remains on the stack, but the data payload lives safely on the heap."
        },
        {
            "title": "Freeing the allocated heap memory",
            "code": "free(ptr);",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌──────────────────────────────┐
    │  ptr: [ 0x7FFF0040 ] ──⚡────┼──>│  0x7FFF0040: [ DEALLOCATED ] │
    └──────────────────────────────┘   └──────────────────────────────┘
    ⚠️ DANGLING POINTER ALERT: ptr still contains 0x7FFF0040!""",
            "desc": "free() notifies the OS memory allocator that 0x7FFF0040 can be reused. It does NOT erase `ptr`!",
            "why": "`ptr` is now a Dangling Pointer! Reading *ptr now causes unpredictable bugs or security vulnerabilities."
        },
        {
            "title": "Neutralizing the dangling pointer",
            "code": "ptr = NULL;",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌──────────────────────────────┐
    │  ptr: [ NULL (0x0) ] ──X     │   │                              │
    └──────────────────────────────┘   └──────────────────────────────┘""",
            "desc": "`ptr` is explicitly reset to 0x0 (NULL), pointing to nowhere safe.",
            "why": "Any accidental attempt to read *ptr will now predictably crash with a clean null-pointer error rather than silent data corruption."
        }
    ]
    takeaways = [
        "Stack memory is deallocated automatically when function scope ends; Heap memory requires explicit free().",
        "Failing to call free() causes Memory Leaks that exhaust RAM over time.",
        "Always set `ptr = NULL;` immediately after `free(ptr);` to prevent Dangling Pointer vulnerabilities."
    ]
    _run_visualizer_steps(
        "DSA-V1",
        "🧠 DSA-V1: MEMORY ARCHITECTURE & POINTER LIFECYCLE (Stack vs Heap)",
        "Understand exactly what happens in RAM when you allocate, dereference, free, and nullify pointers in C.",
        steps,
        takeaways
    )


def vis_dsa_recursion():
    """DSA-V2: Recursion & System Call Stack (Factorial & Call Frames)"""
    steps = [
        {
            "title": "Call stack initial call: fact(3)",
            "code": "int fact(int n) { if (n<=1) return 1; return n * fact(n-1); }",
            "diagram": r"""    SYSTEM CALL STACK (Push Phase)
    ┌─────────────────────────────────┐
    │ [Frame 1] fact(n=3)             │ ──> Pauses waiting for fact(2)
    └─────────────────────────────────┘""",
            "desc": "main() pushes frame fact(3). The CPU pauses fact(3) because it needs the return value of fact(2).",
            "why": "Every recursive call allocates a new stack frame holding its own local variables and return address."
        },
        {
            "title": "Recursive push: fact(2)",
            "code": "fact(2)",
            "diagram": r"""    SYSTEM CALL STACK (Push Phase)
    ┌─────────────────────────────────┐
    │ [Frame 2] fact(n=2)             │ ──> Pauses waiting for fact(1)
    ├─────────────────────────────────┤
    │ [Frame 1] fact(n=3)             │
    └─────────────────────────────────┘""",
            "desc": "CPU pushes frame fact(2) on top of fact(3). Memory grows upwards on the stack.",
            "why": "Call stack depth is now 2. Stack overflow occurs if base condition is missing or unreachable."
        },
        {
            "title": "Base case reached: fact(1)",
            "code": "fact(1) -> if (n <= 1) return 1;",
            "diagram": r"""    SYSTEM CALL STACK (Base Case Hit!)
    ┌─────────────────────────────────┐
    │ [Frame 3] fact(n=1)  --> returns 1
    ├─────────────────────────────────┤
    │ [Frame 2] fact(n=2)             │
    ├─────────────────────────────────┤
    │ [Frame 1] fact(n=3)             │
    └─────────────────────────────────┘""",
            "desc": "Frame 3 hits the base condition `n <= 1` and returns 1 immediately without creating any further calls.",
            "why": "The base case halts infinite recursion and begins the Stack Unwinding phase."
        },
        {
            "title": "Stack unwinding: fact(1) pops and returns to fact(2)",
            "code": "fact(2) receives 1: calculates 2 * 1 = 2",
            "diagram": r"""    SYSTEM CALL STACK (Unwinding Phase)
    ┌─────────────────────────────────┐
    │ [Frame 2] fact(n=2)  --> returns 2
    ├─────────────────────────────────┤
    │ [Frame 1] fact(n=3)             │
    └─────────────────────────────────┘
    (Frame 3 popped from memory)""",
            "desc": "Frame 3 is removed from the stack. Frame 2 multiplies `2 * 1 = 2` and returns 2 to Frame 1.",
            "why": "Popping frames releases stack memory back to the operating system."
        },
        {
            "title": "Final resolution: fact(3) pops and returns to main()",
            "code": "fact(3) receives 2: calculates 3 * 2 = 6",
            "diagram": r"""    SYSTEM CALL STACK (Complete!)
    ┌─────────────────────────────────┐
    │ [main frame] result = 6         │
    └─────────────────────────────────┘
    (All recursive frames popped clean)""",
            "desc": "Frame 1 receives 2, calculates `3 * 2 = 6`, and returns 6 to main(). Call stack is clean.",
            "why": "Recursion uses O(N) auxiliary space on the call stack due to activation frames."
        }
    ]
    takeaways = [
        "Recursion inherently uses O(N) auxiliary call-stack memory for depth N.",
        "A missing base case causes Stack Overflow (SIGSEGV / segmentation fault) when stack limit is exceeded.",
        "Tail call optimization (TCO) allows compilers to convert certain recursions into iterative loops."
    ]
    _run_visualizer_steps(
        "DSA-V2",
        "🔄 DSA-V2: RECURSION & SYSTEM CALL STACK (Push & Pop Frames)",
        "Watch activation frames push onto the call stack and unwind with return values during recursive execution.",
        steps,
        takeaways
    )


def vis_dsa_linked_reversal():
    """DSA-V3: Singly Linked List 3-Pointer Reversal (prev, curr, next)"""
    steps = [
        {
            "title": "Initial 3-pointer setup",
            "code": "prev = NULL; curr = head;",
            "diagram": r"""    prev          curr
     │             │
     ▼             ▼
   [NULL]        [ 10 | • ] ───> [ 20 | • ] ───> [ 30 | NULL ]""",
            "desc": "`prev` starts at NULL. `curr` points to the head node (10).",
            "why": "You must maintain three pointers simultaneously to reverse links without losing downstream nodes."
        },
        {
            "title": "Node 1: Saving next pointer and reversing link",
            "code": "next = curr->next;  curr->next = prev;",
            "diagram": r"""    prev          curr          next
     │             │             │
     ▼             ▼             ▼
   [NULL] <─── [ 10 | • ]      [ 20 | • ] ───> [ 30 | NULL ]""",
            "desc": "`next` bookmarks Node 20. Then Node 10's link is reversed to point backward to `prev` (NULL).",
            "why": "If you don't save `curr->next` before reassigning, Node 20 and the rest of the list are lost forever in memory!"
        },
        {
            "title": "Node 1: Advancing prev and curr pointers",
            "code": "prev = curr;  curr = next;",
            "diagram": r"""                 prev          curr
                                 │             │
                                 ▼             ▼
   [NULL] <─── [ 10 | • ]      [ 20 | • ] ───> [ 30 | NULL ]""",
            "desc": "`prev` slides forward to Node 10. `curr` slides forward to Node 20.",
            "why": "Both pointers shift right by 1 node to repeat the reversal on the next element."
        },
        {
            "title": "Node 2: Reversing Node 20's link",
            "code": "next = curr->next;  curr->next = prev;  prev = curr;  curr = next;",
            "diagram": r"""                               prev          curr
                                 │             │
                                 ▼             ▼
   [NULL] <─── [ 10 | • ] <─── [ 20 | • ]      [ 30 | NULL ]""",
            "desc": "Node 20's next pointer now points backward to Node 10. `prev` advances to 20, `curr` to 30.",
            "why": "Two of the three nodes are now reversed in place in O(1) space."
        },
        {
            "title": "Node 3: Final node reversal and head update",
            "code": "next = curr->next; curr->next = prev; prev = curr; curr = next; head = prev;",
            "diagram": r"""                                             head / prev   curr
                                                   │         │
                                                   ▼         ▼
   [NULL] <─── [ 10 | • ] <─── [ 20 | • ] <─── [ 30 | • ]   [NULL]""",
            "desc": "Node 30's link points to 20. `curr` becomes NULL (end of list). `head` is updated to `prev` (30).",
            "why": "The list is now completely reversed: 30 -> 20 -> 10 -> NULL, in O(N) time and O(1) auxiliary space!"
        }
    ]
    takeaways = [
        "In-place linked list reversal requires 3 pointers: prev, curr, and next.",
        "Always save `next = curr->next` BEFORE overwriting `curr->next = prev`.",
        "Time Complexity: O(N) single pass. Space Complexity: O(1) in-place pointers."
    ]
    _run_visualizer_steps(
        "DSA-V3",
        "🔗 DSA-V3: LINKED LIST 3-POINTER REVERSAL (prev, curr, next)",
        "Step through the pointer choreography that reverses a singly linked list in-place without allocating memory.",
        steps,
        takeaways
    )


def vis_dsa_floyd_cycle():
    """DSA-V4: Floyd's Cycle Detection Algorithm (Tortoise & Hare)"""
    steps = [
        {
            "title": "Cycle setup and initial pointer positions",
            "code": "Node *slow = head, *fast = head;",
            "diagram": r"""    slow, fast
        │
        ▼
      [ 1 ] ──> [ 2 ] ──> [ 3 ] ──> [ 4 ]
                            ▲         │
                            │         ▼
                          [ 6 ] <── [ 5 ]
    (Cycle: 3 -> 4 -> 5 -> 6 -> 3)""",
            "desc": "List has 6 nodes with a loop starting at Node 3. Both `slow` (Tortoise) and `fast` (Hare) start at Node 1.",
            "why": "How can we detect this cycle without storing visited nodes in a hash set or modifying node structures?"
        },
        {
            "title": "Step 1 & 2: Advancing slow (1 step) and fast (2 steps)",
            "code": "slow = slow->next; fast = fast->next->next;",
            "diagram": r"""                slow                  fast
                  │                     │
                  ▼                     ▼
      [ 1 ] ──> [ 2 ] ──> [ 3 ] ──> [ 4 ] ──> [ 5 ]
                            ▲                   │
                            └─────── [ 6 ] <────┘""",
            "desc": "`slow` advances 1 step to Node 2. `fast` advances 2 steps to Node 3, then Node 4.",
            "why": "Because fast moves at 2x speed, the relative distance between them inside the loop decreases by 1 each step."
        },
        {
            "title": "Step 3: Fast wraps around the cycle",
            "code": "slow -> Node 3, fast -> Node 6 -> Node 3 (wrapped!)",
            "diagram": r"""                          slow, fast
                              │
                              ▼
      [ 1 ] ──> [ 2 ] ──> [ 3 ] ──> [ 4 ]
                            ▲         │
                            │         ▼
                          [ 6 ] <── [ 5 ]""",
            "desc": "`slow` moves to Node 3. `fast` jumps through Node 5 to Node 6, and wraps back to Node 3!",
            "why": "The gap between them inside the cycle is shrinking monotonically."
        },
        {
            "title": "Step 4: Collision detected!",
            "code": "slow -> Node 4, fast -> Node 5; next step: slow -> Node 5, fast -> Node 5 (COLLISION!)",
            "diagram": r"""                                    slow & fast MEET HERE!
                                              │
                                              ▼
      [ 1 ] ──> [ 2 ] ──> [ 3 ] ──> [ 4 ]   [ 5 ] 💥
                            ▲                 │
                            └────── [ 6 ] <───┘""",
            "desc": "At Node 5, `slow == fast`! Collision confirmed! A cycle definitely exists in the linked list.",
            "why": "Mathematical theorem: In any cycle of length C, fast catches slow within C iterations."
        },
        {
            "title": "Phase 2: Resetting slow to head to find cycle entry",
            "code": "slow = head; while (slow != fast) { slow = slow->next; fast = fast->next; }",
            "diagram": r"""      slow                                  fast
        │                                     │
        ▼                                     ▼
      [ 1 ] ──> [ 2 ] ──> [ 3 ] ──> [ 4 ]   [ 5 ]
                            ▲                 │
                            └────── [ 6 ] <───┘
    Advance BOTH at 1 step per turn:
    --> slow to 2, fast to 6
    --> slow to 3, fast to 3  ==> MATCH AT NODE 3! (Cycle Start Node!)""",
            "desc": "Reset `slow` to head. Keep `fast` at collision point (Node 5). Move BOTH at 1 step per turn. They meet EXACTLY at Node 3!",
            "why": "Proof: Distance from head to cycle entry equals distance from collision point to cycle entry modulo C!"
        }
    ]
    takeaways = [
        "Floyd's algorithm detects cycles in O(N) time and O(1) auxiliary space (no hash sets needed).",
        "If fast reaches NULL, the list is linear (no cycle).",
        "To find the entry node: reset slow to head, keep fast at collision point, advance both by 1 step."
    ]
    _run_visualizer_steps(
        "DSA-V4",
        "🐢 DSA-V4: FLOYD'S CYCLE DETECTION (Tortoise & Hare Algorithm)",
        "Visualize how two pointers moving at different speeds detect cycles and pinpoint the exact loop entry node in O(1) space.",
        steps,
        takeaways
    )


def vis_dsa_infix_postfix():
    """DSA-V5: Infix to Postfix Conversion & Operator Stack (Shunting-Yard)"""
    steps = [
        {
            "title": "Infix expression and operator precedence rules",
            "code": "Expression: (A + B * C) / (D - E)",
            "diagram": r"""    OPERATOR PRECEDENCE TABLE:
    ┌──────────┬────────────┬────────────────┐
    │ Operator │ Precedence │ Associativity  │
    ├──────────┼────────────┼────────────────┤
    │  ^       │  3 (High)  │ Right to Left  │
    │  * , /   │  2 (Med)   │ Left to Right  │
    │  + , -   │  1 (Low)   │ Left to Right  │
    │  (       │  0 (Stack) │ N/A            │
    └──────────┴────────────┴────────────────┘""",
            "desc": "Higher precedence operators bind tighter. Parentheses override natural precedence.",
            "why": "CPUs evaluate expressions using Postfix (Reverse Polish Notation) because it needs no parentheses!"
        },
        {
            "title": "Scanning '(' and operand 'A'",
            "code": "Scan '(', Scan 'A'",
            "diagram": r"""    OPERATOR STACK            POSTFIX OUTPUT
    ┌─────────┐
    │   (     │               A
    └─────────┘""",
            "desc": "'(' is pushed to Operator Stack. 'A' is an operand, so it goes directly to the Postfix output.",
            "why": "Operands maintain their exact relative order; only operators get rearranged."
        },
        {
            "title": "Scanning '+' and operand 'B'",
            "code": "Scan '+', Scan 'B'",
            "diagram": r"""    OPERATOR STACK            POSTFIX OUTPUT
    ┌─────────┐
    │   +     │
    │   (     │               A  B
    └─────────┘""",
            "desc": "'+' pushed onto stack on top of '('. 'B' appended to output.",
            "why": "'+' waits on the stack because higher precedence operators might arrive later."
        },
        {
            "title": "Scanning '*' and operand 'C'",
            "code": "Scan '*', Scan 'C' (Precedence '*' > '+')",
            "diagram": r"""    OPERATOR STACK            POSTFIX OUTPUT
    ┌─────────┐
    │   *     │
    │   +     │
    │   (     │               A  B  C
    └─────────┘""",
            "desc": "'*' has higher precedence (2) than '+' (1), so it is pushed onto stack. 'C' output.",
            "why": "Higher precedence operator sits on top so it will be popped and evaluated first."
        },
        {
            "title": "Encountering ')' — Popping operators inside bracket",
            "code": "Scan ')' -> Pop until '('",
            "diagram": r"""    OPERATOR STACK            POSTFIX OUTPUT
    ┌─────────┐
    │ (empty) │               A  B  C  *  +
    └─────────┘""",
            "desc": "Closing bracket ')' pops '*' then '+' to the output. The '(' is discarded.",
            "why": "Parenthesized sub-expression is now completely converted: `(A + B * C)` became `A B C * +`."
        },
        {
            "title": "Scanning '/' and converting '(D - E)'",
            "code": "Scan '/', then convert '(D - E)'",
            "diagram": r"""    OPERATOR STACK            POSTFIX OUTPUT
    ┌─────────┐
    │   /     │               A  B  C  *  +  D  E  -
    └─────────┘""",
            "desc": "'/' pushed to stack. '(D - E)' converts to `D E -` by same rules.",
            "why": "Only the division operator '/' remains on the stack."
        },
        {
            "title": "End of input: Flushing stack to output",
            "code": "End of String -> Pop remaining operators",
            "diagram": r"""    OPERATOR STACK            FINAL POSTFIX EXPRESSION
    ┌─────────┐
    │ (empty) │               A  B  C  *  +  D  E  -  /
    └─────────┘""",
            "desc": "Stack is flushed: '/' is popped to output. Final postfix: `A B C * + D E - /`.",
            "why": "Evaluating this postfix with an operand stack requires ZERO backtracking or parentheses!"
        }
    ]
    takeaways = [
        "Operands always pass directly to the output; operators pass through the stack.",
        "Pop operators of greater than or equal precedence before pushing a new operator.",
        "Parentheses '(' force sub-expression priority; ')' triggers popping until matching '('."
    ]
    _run_visualizer_steps(
        "DSA-V5",
        "📥 DSA-V5: INFIX TO POSTFIX CONVERSION (Shunting-Yard & Stack)",
        "Step through operator precedence, parenthesis handling, and the stack mechanics that compilers use to parse expressions.",
        steps,
        takeaways
    )


def vis_dsa_circular_queue():
    """DSA-V6: Circular Queue Modulo Ring vs Linear Queue"""
    steps = [
        {
            "title": "Linear Queue limitation: False Overflow",
            "code": "int q[5]; front = 2, rear = 4; // 2 elements dequeued",
            "diagram": r"""    LINEAR QUEUE (Slots 0 & 1 are empty, rear is at index 4)
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    │ [EMPTY]  │ [EMPTY]  │  Job 3   │  Job 4   │  Job 5   │
    └──────────┴──────────┴──────────┴──────────┴──────────┘
      Index 0    Index 1    Index 2    Index 3    Index 4 (rear)
                            (front)
    Attempting to enqueue Job 6: rear == MAX-1 ==> OVERFLOW! (Even though 2 slots are free!)""",
            "desc": "In a linear queue, elements dequeue from front, but rear cannot move left. Memory is wasted!",
            "why": "Linear queue reports Queue Full even when only 3 out of 5 slots are occupied."
        },
        {
            "title": "The Circular Queue solution: Modulo Ring Buffer",
            "code": "rear = (rear + 1) % MAX; // (4 + 1) % 5 = 0!",
            "diagram": r"""    CIRCULAR QUEUE RING BUFFER (MAX = 5)
                      [Index 0] <── rear wraps here!
                     /         \
           [Index 4]             [Index 1]
               |                    |
           [Index 3]             [Index 2] (front)
                     \         /
                      (Ring Connected)""",
            "desc": "Modulo operator `% MAX` wraps index 4 + 1 = 5 back to 0! Index 0 is reused.",
            "why": "Solves false overflow by connecting the end of the array back to the beginning."
        },
        {
            "title": "Enqueue into wrapped slot: Job 6 inserted at Index 0",
            "code": "q[rear] = Job_6; count++;",
            "diagram": r"""    CIRCULAR BUFFER SLOTS:
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    │  Job 6   │ [EMPTY]  │  Job 3   │  Job 4   │  Job 5   │
    └──────────┴──────────┴──────────┴──────────┴──────────┘
      Index 0    Index 1    Index 2    Index 3    Index 4
      (rear)                (front)""",
            "desc": "Job 6 is placed in Slot 0. Front remains at Slot 2. 4 items currently stored.",
            "why": "No shifting of elements is needed: enqueue is O(1) time complexity."
        },
        {
            "title": "Full condition check in circular queue",
            "code": "(rear + 1) % MAX == front",
            "diagram": r"""    If we enqueue Job 7 at Index 1:
    (rear + 1) % 5 = (1 + 1) % 5 = 2 == front!
    ==> TRUE QUEUE FULL! No vacant slots wasted!""",
            "desc": "Circular queue is full ONLY when every single slot is genuinely occupied.",
            "why": "Operating systems use circular ring buffers for network packet queues and audio streams."
        }
    ]
    takeaways = [
        "Linear queues suffer from false overflow where vacant front slots cannot be reused.",
        "Circular queues wrap around using formula: `rear = (rear + 1) % MAX`.",
        "Full condition: `(rear + 1) % MAX == front`. Empty condition: `front == -1`."
    ]
    _run_visualizer_steps(
        "DSA-V6",
        "🔄 DSA-V6: CIRCULAR QUEUE & MODULO RING BUFFER",
        "See why linear queues suffer from false overflow and how the modulo operator `% MAX` recycles empty memory slots.",
        steps,
        takeaways
    )


def vis_dsa_quicksort_partition():
    """DSA-V7: QuickSort In-Place Partitioning (Lomuto Scheme)"""
    steps = [
        {
            "title": "Initial array and pivot selection",
            "code": "int arr[] = {35, 10, 80, 20, 90, 45, 50}; // pivot = 50",
            "diagram": r"""    ARRAY SLOTS:
    ┌───────┬───────┬───────┬───────┬───────┬───────┬───────────┐
    │  35   │  10   │  80   │  20   │  90   │  45   │  [ 50 ]   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────────┘
      idx 0   idx 1   idx 2   idx 3   idx 4   idx 5   Pivot (50)
    i = -1, j = 0""",
            "desc": "Lomuto partition chooses last element (50) as Pivot. `i` tracks boundary of smaller elements.",
            "why": "Partitioning goal: place all elements < 50 to the left, and all elements > 50 to the right."
        },
        {
            "title": "j scans elements: 35 and 10 are <= 50",
            "code": "arr[j] <= pivot -> i++; swap(arr[i], arr[j]);",
            "diagram": r"""      i=1     j=1
       ▼       ▼
    ┌───────┬───────┬───────┬───────┬───────┬───────┬───────────┐
    │  35   │  10   │  80   │  20   │  90   │  45   │  [ 50 ]   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────────┘
    35 <= 50 (i=0), 10 <= 50 (i=1). Both stay in place.""",
            "desc": "35 and 10 are already smaller than pivot. `i` advances to index 1.",
            "why": "Elements <= pivot are grouped at the beginning of the array."
        },
        {
            "title": "Element 80 > 50 (skipped), then element 20 <= 50 (SWAP!)",
            "code": "j=3: arr[3]=20 <= 50 -> i=2; swap(arr[2], arr[3])",
            "diagram": r"""              i=2     j=3
               ▼       ▼
    ┌───────┬───────┬───────┬───────┬───────┬───────┬───────────┐
    │  35   │  10   │  20   │  80   │  90   │  45   │  [ 50 ]   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────────┘
    80 and 20 SWAPPED! 20 is now in the smaller elements zone!""",
            "desc": "80 was too large. When 20 is found, `i` increments to 2, and 20 swaps with 80!",
            "why": "In-place swapping avoids creating auxiliary arrays, keeping space complexity to O(log N) stack frames."
        },
        {
            "title": "Element 45 <= 50 (SWAP with 90)",
            "code": "j=5: arr[5]=45 <= 50 -> i=3; swap(arr[3], arr[5])",
            "diagram": r"""                      i=3             j=5
                       ▼               ▼
    ┌───────┬───────┬───────┬───────┬───────┬───────┬───────────┐
    │  35   │  10   │  20   │  45   │  90   │  80   │  [ 50 ]   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────────┘
    90 and 45 SWAPPED! Smaller zone is now [35, 10, 20, 45].""",
            "desc": "45 is swapped into index 3. Smaller elements boundary is now indices 0 through 3.",
            "why": "All elements processed except the pivot itself."
        },
        {
            "title": "Final Step: Swapping pivot into its permanent position",
            "code": "swap(arr[i + 1], arr[high]); // swap arr[4] (90) with pivot (50)",
            "diagram": r"""    ┌───────────────────────┐       ┌───────────────────┐
    │   ELEMENTS < PIVOT    │ PIVOT │  ELEMENTS > PIVOT │
    ├───────┬───────┬───────┼───────┼───────┬───────────┤
    │  35   │  10   │  20   │  45   │ [ 50 ]│  80   │  90   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────┘
                                       ▲
                                    index 4 (PERMANENT SORTED SPOT!)""",
            "desc": "Pivot 50 swaps into index 4. Pivot 50 will NEVER move again for the rest of the algorithm!",
            "why": "QuickSort now recursively partitions left subarray [0..3] and right subarray [5..6]."
        }
    ]
    takeaways = [
        "Partitioning places the pivot into its final sorted position in O(N) time with O(1) space.",
        "Average Time Complexity: O(N log N). Worst Case: O(N²) if array is already sorted and pivot is extreme.",
        "To prevent O(N²) worst-case in production, use randomized pivot or median-of-three."
    ]
    _run_visualizer_steps(
        "DSA-V7",
        "⚡ DSA-V7: QUICKSORT IN-PLACE PARTITIONING (Lomuto Scheme)",
        "Watch two pointers i and j scan and swap elements until the pivot settles into its exact permanent sorted slot.",
        steps,
        takeaways
    )


def vis_dsa_mergesort_tree():
    """DSA-V8: MergeSort Divide & Conquer Tree"""
    steps = [
        {
            "title": "Divide phase: Recursively splitting array into halves",
            "code": "mergesort(arr, 0, 7) -> mid = 3",
            "diagram": r"""                    [ 38, 27, 43, 3, 9, 82, 10 ]
                                 /              \
                     [ 38, 27, 43, 3 ]      [ 9, 82, 10 ]
                        /         \            /       \
                   [ 38, 27 ]   [ 43, 3 ]   [ 9, 82 ]  [ 10 ]
                    /      \     /     \     /     \
                  [38]    [27] [43]    [3]  [9]   [82]""",
            "desc": "Array is recursively halved until single-element subarrays are reached.",
            "why": "A single element array is inherently sorted by definition (Base Case)."
        },
        {
            "title": "Conquer & Merge: Merging atomic pairs",
            "code": "merge([38], [27]) -> compare 38 and 27 -> [27, 38]",
            "diagram": r"""                  [38]    [27]       [43]    [3]       [9]    [82]
                     \   /              \   /             \   /
                   [ 27, 38 ]         [ 3, 43 ]         [ 9, 82 ]""",
            "desc": "Adjacent single elements are merged in sorted order into 2-element arrays.",
            "why": "Two-pointer merge compares heads of two sorted lists in O(N) time."
        },
        {
            "title": "Merging 4-element sorted halves",
            "code": "merge([27, 38], [3, 43])",
            "diagram": r"""    Left:  [ 27, 38 ]      Right: [ 3, 43 ]
      Step 1: Compare 27 vs 3  --> Take 3   [ 3 ]
      Step 2: Compare 27 vs 43 --> Take 27  [ 3, 27 ]
      Step 3: Compare 38 vs 43 --> Take 38  [ 3, 27, 38 ]
      Step 4: Right remaining  --> Take 43  [ 3, 27, 38, 43 ]""",
            "desc": "Two pointers scan Left and Right sorted lists, copying smaller value to auxiliary array.",
            "why": "Because both input lists are already sorted, merge needs only 1 pass!"
        },
        {
            "title": "Final Merge: Producing fully sorted array",
            "code": "merge([3, 27, 38, 43], [9, 10, 82])",
            "diagram": r"""    FINAL SORTED ARRAY:
    ┌───────┬───────┬───────┬───────┬───────┬───────┬───────┐
    │   3   │   9   │  10   │  27   │  38   │  43   │  82   │
    └───────┴───────┴───────┴───────┴───────┴───────┴───────┘""",
            "desc": "The two sorted halves combine into the final 7-element sorted array.",
            "why": "MergeSort is STABLE (preserves original order of equal keys) and guaranteed O(N log N) worst-case."
        }
    ]
    takeaways = [
        "Time Complexity: Guaranteed O(N log N) in best, average, AND worst cases.",
        "Space Complexity: O(N) auxiliary memory needed for merging subarrays.",
        "MergeSort is a STABLE sorting algorithm, making it ideal for linked lists and complex objects."
    ]
    _run_visualizer_steps(
        "DSA-V8",
        "🔀 DSA-V8: MERGESORT DIVIDE & CONQUER TREE",
        "Trace the binary recursion tree splitting arrays to atomic elements and two-pointer merging them back in sorted order.",
        steps,
        takeaways
    )


def vis_dsa_bst_operations():
    """DSA-V9: Binary Search Tree Invariant & Inorder Traversal"""
    steps = [
        {
            "title": "The BST Invariant definition",
            "code": "BST Property: Left Subtree < Root < Right Subtree",
            "diagram": r"""                     [ 50 ]  <── ROOT
                    /      \
         [ Values < 50 ]    [ Values > 50 ]""",
            "desc": "Every single node in a BST enforces: all keys in left subtree are strictly smaller, right are larger.",
            "why": "This invariant allows binary search: halving the search space at each decision node."
        },
        {
            "title": "Inserting 30, 70, 20, 40 step-by-step",
            "code": "insert(30), insert(70), insert(20), insert(40)",
            "diagram": r"""                     [ 50 ]
                    /      \
                 [ 30 ]    [ 70 ]
                /      \
             [ 20 ]   [ 40 ]""",
            "desc": "30 < 50 goes left. 70 > 50 goes right. 20 < 30 goes left of 30. 40 > 30 goes right of 30.",
            "why": "Average insertion and search time is O(log N) in a balanced tree."
        },
        {
            "title": "Inorder Traversal: Left -> Root -> Right",
            "code": "void inorder(Node *root) { inorder(root->left); printf(root->val); inorder(root->right); }",
            "diagram": r"""    INORDER VISITATION PATH:
    1. Leftmost node:     Visit [ 20 ]
    2. Parent of 20:      Visit [ 30 ]
    3. Right child of 30: Visit [ 40 ]
    4. Root node:         Visit [ 50 ]
    5. Right child:       Visit [ 70 ]

    OUTPUT SEQUENCE: 20 ──> 30 ──> 40 ──> 50 ──> 70  (SORTED!)""",
            "desc": "Because Left < Root < Right, an Inorder traversal ALWAYS yields elements in strictly ascending sorted order!",
            "why": "The easiest way to check if a binary tree is a valid BST is to check if its Inorder traversal is strictly sorted."
        }
    ]
    takeaways = [
        "BST Invariant: Left Subtree < Root < Right Subtree for every node in the tree.",
        "Inorder traversal (Left -> Root -> Right) of any valid BST produces strictly ascending sorted order.",
        "Worst-case search in an unbalanced (skewed) BST degrades to O(N) linear time."
    ]
    _run_visualizer_steps(
        "DSA-V9",
        "🌲 DSA-V9: BINARY SEARCH TREE (BST Invariant & Inorder Traversal)",
        "Visualize tree construction rule Left < Root < Right and see why Inorder traversal is mathematically guaranteed to sort keys.",
        steps,
        takeaways
    )


def vis_dsa_avl_rotations():
    """DSA-V10: AVL Tree Self-Balancing Rotations"""
    steps = [
        {
            "title": "Balance Factor definition and imbalance",
            "code": "Balance Factor (BF) = Height(Left) - Height(Right)",
            "diagram": r"""    Valid AVL Tree: BF must be -1, 0, or +1 for EVERY node!
    Insert 30, then 20, then 10:
             [ 30 ] (BF = +2) ⚠️ IMBALANCED!
            /
         [ 20 ]    (BF = +1)
        /
     [ 10 ]        (BF = 0)
    Left-Left (LL) Heavy Imbalance detected at Node 30!""",
            "desc": "Node 30 has left height 2, right height 0. Balance factor is +2. Rotation is mandatory!",
            "why": "Unbalanced BSTs degrade to linked lists with O(N) search. AVL trees guarantee O(log N)."
        },
        {
            "title": "LL Imbalance fix: Single Right Rotation",
            "code": "rightRotate(30)",
            "diagram": r"""         [ 30 ]                  [ 20 ] (New Root)
        /            Rotate     /      \
     [ 20 ]          Right   [ 10 ]    [ 30 ]
    /               ══════>
 [ 10 ]
    Height is restored from 3 down to 2! Balanced (all BF = 0)!""",
            "desc": "Node 20 lifts up to become the new parent. Node 30 becomes its right child.",
            "why": "Single Right Rotation restores balance in O(1) time without violating BST ordering."
        },
        {
            "title": "Left-Right (LR) Imbalance: Double rotation required",
            "code": "Insert 30, then 10, then 20 (Zig-Zag shape)",
            "diagram": r"""         [ 30 ] (BF = +2)
        /
     [ 10 ]    (BF = -1)  <── Zig-zag! Left child is right-heavy!
        \
        [ 20 ]

    Step 1: Left Rotate on 10  ==> converts to LL: [ 30 ] -> [ 20 ] -> [ 10 ]
    Step 2: Right Rotate on 30 ==> balanced root:  [ 20 ] with children [10, 30]!""",
            "desc": "A zig-zag shape requires 2 rotations: Left rotation on child, followed by Right rotation on root.",
            "why": "4 rotation types cover all imbalances: LL (Right), RR (Left), LR (Left-Right), RL (Right-Left)."
        }
    ]
    takeaways = [
        "AVL tree is a self-balancing BST where Balance Factor for every node is in {-1, 0, +1}.",
        "LL imbalance requires 1 Right rotation; RR requires 1 Left rotation.",
        "LR and RL imbalances require Double rotations (Left-then-Right, or Right-then-Left)."
    ]
    _run_visualizer_steps(
        "DSA-V10",
        "⚖️ DSA-V10: AVL TREE BALANCING & ROTATIONS",
        "Understand balance factors and visualize Single (LL/RR) and Double (LR/RL) rotations maintaining O(log N) tree height.",
        steps,
        takeaways
    )


def vis_dsa_hash_collision():
    """DSA-V11: Hash Table Collision Resolution (Linear Probing & Tombstones)"""
    steps = [
        {
            "title": "Hash Table setup and modulo hashing",
            "code": "Table size = 7, h(k) = k % 7",
            "diagram": r"""    SLOT   0      1      2      3      4      5      6
          [---]  [---]  [---]  [---]  [---]  [---]  [---]
    Insert Key 10: 10 % 7 = Slot 3. Empty -> Insert 10 at Slot 3.""",
            "desc": "Hash function maps arbitrary integers into table indices 0..6.",
            "why": "Average hash table lookup is O(1) constant time."
        },
        {
            "title": "Collision: Key 17 also hashes to Slot 3!",
            "code": "Insert Key 17: 17 % 7 = 3 (COLLISION!)",
            "diagram": r"""    SLOT   0      1      2      3      4      5      6
          [---]  [---]  [---]  [ 10 ] [---]  [---]  [---]
                                  ▲
                         17 wants Slot 3 (COLLISION!)
    Linear Probe: check (3 + 1) % 7 = Slot 4. Slot 4 is empty -> Insert 17!""",
            "desc": "Linear probing checks consecutive adjacent slots until a vacant slot is found.",
            "why": "Open addressing resolves collisions by finding alternative slots within the table itself."
        },
        {
            "title": "Chaining collisions: Key 24",
            "code": "Insert Key 24: 24 % 7 = 3",
            "diagram": r"""    SLOT   0      1      2      3      4      5      6
          [---]  [---]  [---]  [ 10 ] [ 17 ] [ 24 ] [---]
    24 collides at Slot 3, collides at Slot 4, placed in Slot 5!""",
            "desc": "Clustering occurs when consecutive filled slots cause longer probe chains.",
            "why": "Primary clustering increases search time when load factor exceeds 0.7."
        },
        {
            "title": "The Tombstone Problem on Deletion",
            "code": "delete(17) -> Why setting Slot 4 to EMPTY breaks future searches!",
            "diagram": r"""    If Slot 4 is set to EMPTY:
    Search for 24:
      1. Check Slot 3 (10 != 24)
      2. Check Slot 4 (EMPTY!) --> Search stops and reports 'NOT FOUND' (BUG!)

    SOLUTION: MARK SLOT 4 AS [TOMBSTONE / DELETED]!
    Search continues past tombstones, but new insertions can reuse them!""",
            "desc": "A deleted slot must NEVER be marked empty; it must be marked with a Tombstone marker.",
            "why": "This is one of the most frequently asked hash table viva traps!"
        }
    ]
    takeaways = [
        "Collisions occur when two different keys produce the same hash index (Pigeonhole Principle).",
        "Linear probing checks `(h(k) + i) % size` sequentially for the next empty slot.",
        "Deleted slots must hold a Tombstone marker so search probe chains do not terminate prematurely."
    ]
    _run_visualizer_steps(
        "DSA-V11",
        "🔑 DSA-V11: HASH TABLE COLLISIONS & TOMBSTONES",
        "Visualize open addressing linear probing, primary clustering, and why tombstone markers are mandatory upon deletion.",
        steps,
        takeaways
    )


def vis_dsa_graph_traversal():
    """DSA-V12: Graph Traversal Stepper (BFS Queue vs DFS Stack)"""
    steps = [
        {
            "title": "Sample Graph topology",
            "code": "Nodes A, B, C, D, E",
            "diagram": r"""           ( A )
          /     \
        ( B )   ( C )
        /   \
      ( D ) ( E )
    Edges: A-B, A-C, B-D, B-E""",
            "desc": "Graph with 5 vertices. How do BFS and DFS explore this network differently?",
            "why": "Both algorithms visit all vertices, but order and data structures differ fundamentally."
        },
        {
            "title": "Breadth-First Search (BFS): Queue Level-by-Level",
            "code": "BFS uses FIFO Queue",
            "diagram": r"""    BFS VISITATION ORDER (Level by Level):
    Level 0: [ A ]
    Level 1: [ B ], [ C ]
    Level 2: [ D ], [ E ]

    QUEUE TRACE:
    Enqueue A  --> Pop A, Enqueue B, C
    Pop B      --> Enqueue D, E
    Pop C      --> (No unvisited neighbors)
    Pop D, E   --> Complete!
    BFS Order: A ──> B ──> C ──> D ──> E""",
            "desc": "BFS explores all neighbors at distance 1 before moving to distance 2.",
            "why": "BFS is guaranteed to find the shortest path in unweighted graphs!"
        },
        {
            "title": "Depth-First Search (DFS): Stack / Recursive Backtracking",
            "code": "DFS uses LIFO Call Stack / Recursion",
            "diagram": r"""    DFS VISITATION ORDER (Deep Dive First):
    Start at A ──> Dives deep to B ──> Dives deep to D (Dead end!)
    Backtracks to B ──> Dives to E (Dead end!)
    Backtracks to B ──> Backtracks to A ──> Visits C

    DFS Order: A ──> B ──> D ──> E ──> C""",
            "desc": "DFS plunges down a path as far as possible before backtracking.",
            "why": "DFS is used for topological sorting, cycle detection, and maze solving."
        }
    ]
    takeaways = [
        "BFS uses a Queue (FIFO) and discovers nodes level-by-level (finds shortest path).",
        "DFS uses a Stack / Recursion (LIFO) and explores paths deeply before backtracking.",
        "Both algorithms require a `visited[]` array to prevent infinite loops in cyclic graphs."
    ]
    _run_visualizer_steps(
        "DSA-V12",
        "🕸️ DSA-V12: GRAPH TRAVERSAL STEPPER (BFS vs DFS)",
        "Compare Queue-driven Breadth-First Search against Stack-driven Depth-First Search side by side on an adjacency network.",
        steps,
        takeaways
    )


# ════════════════════════════════════════════════════════════════════════════════
# 2. JAVA OOP & JVM RUNTIME VISUALIZERS (JAVA-J1 to JAVA-J10)
# ════════════════════════════════════════════════════════════════════════════════

def vis_java_jvm_memory():
    """JAVA-J1: JVM Memory Layout (Metaspace, Stack Frames & Heap Generations)"""
    steps = [
        {
            "title": "JVM Memory Partitioning overview",
            "code": "JVM Runtime Data Areas: Metaspace | JVM Stack | Heap",
            "diagram": r"""    ┌──────────────────────────────────┬──────────────────────────────────┐
    │  METASPACE (Native Memory)       │  JVM STACK (Thread-private)      │
    │  - Class metadata & bytecodes    │  - One Stack per Thread          │
    │  - static variables              │  - Stack Frames for active methods│
    ├──────────────────────────────────┴──────────────────────────────────┤
    │  HEAP SPACE (Shared by ALL Threads)                                 │
    │  ┌───────────────────────┬────────────────────────────────────────┐ │
    │  │ YOUNG GEN (Eden + S0/S1)│ OLD GEN / TENURED (Long-lived Objects)  │ │
    │  └───────────────────────┴────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────┘""",
            "desc": "JVM divides RAM into Metaspace (metadata), Thread Stacks (local variables/frames), and Heap (objects).",
            "why": "Understanding these zones is essential to diagnosing OutOfMemoryError and StackOverflowError."
        },
        {
            "title": "Instantiating an object: Student s = new Student(\"Bob\");",
            "code": "Student s = new Student(\"Bob\");",
            "diagram": r"""    JVM STACK (main thread)            HEAP (Eden Space)
    ┌───────────────────────────┐      ┌───────────────────────────────┐
    │ [main frame]              │      │ 0xHEAP_40: Student instance   │
    │ s: [ 0xHEAP_40 ] ─────────┼─────>│   name: \"Bob\"                 │
    │                           │      │   usn:  null                  │
    └───────────────────────────┘      └───────────────────────────────┘""",
            "desc": "Variable `s` on JVM Stack is a reference (4 or 8 bytes) holding the address of Student on the Heap.",
            "why": "Objects are NEVER placed on the JVM Stack; only primitive values and object references live on the Stack."
        },
        {
            "title": "Generational Heap: Eden -> Survivor -> Tenured (Old Gen)",
            "code": "Minor GC collects Eden; survivors promote to Tenured after aging",
            "diagram": r"""    [ NEW OBJECTS ] ──> [ Eden Space ] ──(Minor GC)──> [ Survivor S0/S1 ]
                                                                 │
                                                   (Survives 15 GCs: Tenured!)
                                                                 ▼
                                                       [ OLD GENERATION ]""",
            "desc": "Short-lived temporary objects die in Eden. Long-lived objects migrate to Old Gen.",
            "why": "Weak Generational Hypothesis: most Java objects die shortly after creation."
        }
    ]
    takeaways = [
        "Metaspace holds class blueprints and static fields in native off-heap RAM.",
        "Stack holds local primitive values and object reference pointers; Heap holds actual object instances.",
        "Generational GC separates short-lived Eden objects from long-lived Tenured objects for high throughput."
    ]
    _run_visualizer_steps(
        "JAVA-J1",
        "☕ JAVA-J1: JVM RUNTIME MEMORY ARCHITECTURE",
        "See how Metaspace, Thread Stack Frames, and Generational Heap spaces collaborate during Java program execution.",
        steps,
        takeaways
    )


def vis_java_string_pool():
    """JAVA-J2: String Constant Pool vs General Heap (== vs .equals())"""
    steps = [
        {
            "title": "String Literal allocation in String Constant Pool",
            "code": "String s1 = \"Java\";",
            "diagram": r"""    JVM STACK                          HEAP SPACE
    ┌──────────────────────────────┐   ┌────────────────────────────────┐
    │  s1: [ 0xPOOL_01 ] ──────────┼──>│  STRING CONSTANT POOL          │
    │                              │   │  0xPOOL_01: [ \"Java\" ]        │
    └──────────────────────────────┘   └────────────────────────────────┘""",
            "desc": "Literal \"Java\" is interned into the String Constant Pool. `s1` points directly into the Pool.",
            "why": "String Constant Pool saves memory by reusing identical string literals across the entire application."
        },
        {
            "title": "Reusing literal from Pool: String s2 = \"Java\";",
            "code": "String s2 = \"Java\";  // s1 == s2 is TRUE!",
            "diagram": r"""    JVM STACK                          HEAP SPACE
    ┌──────────────────────────────┐   ┌────────────────────────────────┐
    │  s1: [ 0xPOOL_01 ] ──────────┼──>│  STRING CONSTANT POOL          │
    │  s2: [ 0xPOOL_01 ] ──────────┼──>│  0xPOOL_01: [ \"Java\" ]        │
    └──────────────────────────────┘   └────────────────────────────────┘
    Result: (s1 == s2) is TRUE! Both share the EXACT same memory address!""",
            "desc": "JVM detects that \"Java\" is already cached in the pool. `s2` receives the exact same address as `s1`.",
            "why": "`==` compares memory addresses (reference equality). Because addresses match, `s1 == s2` is TRUE!"
        },
        {
            "title": "Bypassing the Pool: String s3 = new String(\"Java\");",
            "code": "String s3 = new String(\"Java\");  // s1 == s3 is FALSE!",
            "diagram": r"""    JVM STACK                          HEAP SPACE
    ┌──────────────────────────────┐   ┌────────────────────────────────┐
    │  s1: [ 0xPOOL_01 ] ──────────┼──>│  STRING POOL: 0xPOOL_01 (\"Java\")│
    │  s3: [ 0xHEAP_99 ] ──────────┼──>│  GENERAL HEAP:                │
    └──────────────────────────────┘   │  0xHEAP_99: new String instance│
                                       └────────────────────────────────┘
    Result: (s1 == s3) is FALSE! Different memory addresses!
    Result: s1.equals(s3) is TRUE! Same characters!""",
            "desc": "`new String()` forcefully allocates a brand-new object on the general heap, ignoring pool deduplication.",
            "why": "Always use `.equals()` to compare String contents! `==` tests whether they are the same memory instance."
        },
        {
            "title": "The intern() method: String s4 = s3.intern();",
            "code": "String s4 = s3.intern();  // s1 == s4 is TRUE!",
            "diagram": r"""    s4 receives canonical pool address: 0xPOOL_01!
    Result: (s1 == s4) is TRUE!""",
            "desc": "Calling `.intern()` queries the pool: if present, returns the pool address; if absent, adds it.",
            "why": "Interning can drastically reduce memory footprint when dealing with millions of repeated strings."
        }
    ]
    takeaways = [
        "String literals are stored in the String Constant Pool and reused automatically.",
        "`new String(\"abc\")` always creates a new object in general Heap, bypassing the pool.",
        "Always use `.equals()` to compare string content. Use `==` only when comparing primitive values or identity."
    ]
    _run_visualizer_steps(
        "JAVA-J2",
        "🧵 JAVA-J2: STRING CONSTANT POOL VS HEAP (== vs .equals())",
        "Solve the #1 Java confusion: why literals share memory in the String Pool while new String() creates distinct heap instances.",
        steps,
        takeaways
    )


def vis_java_pass_by_value():
    """JAVA-J3: Java Pass-by-Value vs Object References"""
    steps = [
        {
            "title": "The Golden Rule: Java is ALWAYS strictly Pass-by-Value",
            "code": "void swap(int a, int b) { int t = a; a = b; b = t; }",
            "diagram": r"""    CALL STACK:
    ┌──────────────────────────────┐
    │ [swap frame] a=20, b=10      │ <── Swaps local copies ONLY!
    ├──────────────────────────────┤
    │ [main frame] x=10, y=20      │ <── Untouched! x is still 10, y is 20!
    └──────────────────────────────┘""",
            "desc": "When passing primitive arguments (int, double, boolean), the raw bit values are copied into the method frame.",
            "why": "Changes made to parameter variables inside the method have ZERO effect on the caller's variables."
        },
        {
            "title": "Passing Object References: The address bits are copied!",
            "code": "void rename(Student s) { s.name = \"Alice\"; }",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌────────────────────────────────┐
    │ [rename frame] s: 0x40 ──────┼──>│  0x40: Student Object          │
    ├──────────────────────────────┤   │    name: \"Alice\" (MODIFIED!)   │
    │ [main frame]   stu: 0x40 ────┼──>│                                │
    └──────────────────────────────┘   └────────────────────────────────┘""",
            "desc": "The memory address (0x40) is copied by value. Following that address modifies the real object on the heap!",
            "why": "Students confuse this with pass-by-reference! It is NOT pass-by-reference; the pointer value was copied."
        },
        {
            "title": "The Reassignment Trap: Reassigning parameter reference",
            "code": "void rebind(Student s) { s = new Student(\"Charlie\"); }",
            "diagram": r"""    CALL STACK                         HEAP SPACE
    ┌──────────────────────────────┐   ┌────────────────────────────────┐
    │ [rebind frame] s: 0x99 ──────┼──>│  0x99: Student (\"Charlie\")    │
    ├──────────────────────────────┤   ├────────────────────────────────┤
    │ [main frame]   stu: 0x40 ────┼──>│  0x40: Student (\"Alice\")      │
    └──────────────────────────────┘   └────────────────────────────────┘
    main's variable 'stu' STILL points to 0x40 (\"Alice\")!""",
            "desc": "Reassigning parameter `s` changes only the local stack copy. The caller's reference variable remains unchanged!",
            "why": "If Java had pass-by-reference, `stu` in main would have changed to point to Charlie. But it does NOT!"
        }
    ]
    takeaways = [
        "Java is 100% strictly pass-by-value, without exception.",
        "For primitive types, the actual numeric value is copied.",
        "For object types, the object memory address (reference) is copied by value.",
        "Reassigning an object reference parameter inside a method NEVER alters the caller's reference variable."
    ]
    _run_visualizer_steps(
        "JAVA-J3",
        "📦 JAVA-J3: JAVA PASS-BY-VALUE VS OBJECT REFERENCES",
        "Demystify the #1 Java exam trap: why mutating object fields works across methods, but reassigning references fails completely.",
        steps,
        takeaways
    )


def vis_java_gc_reachability():
    """JAVA-J4: Garbage Collection Root Reachability & Cyclic References"""
    steps = [
        {
            "title": "GC Roots definition in the JVM",
            "code": "GC Roots: Active Thread Stacks | Static variables | JNI handles",
            "diagram": r"""    GC ROOTS (Always considered ALIVE):
    [ Thread Stack: local var 'root' ] ──> Points to Object A
    [ Metaspace: static field 'cache'] ──> Points to Object C""",
            "desc": "Garbage Collection begins tracing from GC Roots: objects intrinsically alive in the JVM.",
            "why": "Any object that cannot be reached by following pointer chains from a GC Root is eligible for GC."
        },
        {
            "title": "Tracing reachable objects (Mark Phase)",
            "code": "Root -> Object A -> Object B",
            "diagram": r"""    [ GC ROOT ] ──> [ Object A (ALIVE) ] ──> [ Object B (ALIVE) ]
                                                        
                    [ Object D ] <── [ Object E ]  (Isolated!)""",
            "desc": "Objects A and B are reachable from a GC Root. Objects D and E have no incoming links from Roots.",
            "why": "Unreachable objects D and E are marked as dead, even if they have memory inside them."
        },
        {
            "title": "The Cyclic Reference Test: A <-> B island of isolation",
            "code": "Node A; Node B; A.next = B; B.next = A; A = null; B = null;",
            "diagram": r"""    [ Object A ] <══════════> [ Object B ]
         ▲                         ▲
         │ (Both point to each     │
         │  other in a circle!)    │
         X                         X
    (References from Thread Stack were severed: A=null, B=null!)
    ==> Neither A nor B is reachable from ANY GC Root!""",
            "desc": "A and B point to each other in an infinite cycle, but no GC Root points to either of them.",
            "why": "Reference counting (like Python/C++) leaks cyclic objects. Java's Tracing GC collects them cleanly!"
        },
        {
            "title": "Sweep Phase: Reclaiming isolated memory",
            "code": "JVM Garbage Collector frees Objects A and B",
            "diagram": r"""    HEAP SPACE:
    [ Object A ] ──> [ FREED & RETURNED TO FREE LIST ]
    [ Object B ] ──> [ FREED & RETURNED TO FREE LIST ]""",
            "desc": "The Garbage Collector sweeps the unreachable cycle and reclaims memory for future allocations.",
            "why": "Java developers never need to manually break cycles to avoid memory leaks."
        }
    ]
    takeaways = [
        "Java GC uses Root Reachability (Tracing), NOT simple reference counting.",
        "GC Roots include local variables on thread stacks, active threads, and static class fields.",
        "Cyclic references (A points to B, B points to A) are cleanly collected if unreachable from GC Roots."
    ]
    _run_visualizer_steps(
        "JAVA-J4",
        "🧹 JAVA-J4: GC ROOT REACHABILITY & CYCLIC REFERENCES",
        "See how Java's tracing garbage collector traverses object graphs and cleanly collects isolated cycles without memory leaks.",
        steps,
        takeaways
    )


def vis_java_dynamic_dispatch():
    """JAVA-J5: Dynamic Method Dispatch & Virtual Method Table (vtable)"""
    steps = [
        {
            "title": "Class hierarchy setup: Animal vs Dog",
            "code": "class Animal { void speak() { println(\"Animal sound\"); } }\nclass Dog extends Animal { void speak() { println(\"Woof!\"); } }",
            "diagram": r"""    ANIMAL CLASS (Parent)             DOG CLASS (Child)
    ┌────────────────────────────┐     ┌────────────────────────────┐
    │ vtable:                    │     │ vtable:                    │
    │  [0] speak -> Animal.speak │     │  [0] speak -> Dog.speak    │ (OVERRIDDEN!)
    └────────────────────────────┘     └────────────────────────────┘""",
            "desc": "Each class with virtual methods gets a Virtual Method Table (vtable) generated by JVM compiler.",
            "why": "Method overriding replaces the parent's method pointer with the child's implementation in the vtable."
        },
        {
            "title": "Polymorphic reference declaration: Animal a = new Dog();",
            "code": "Animal a = new Dog();",
            "diagram": r"""    JVM STACK                          HEAP SPACE
    ┌────────────────────────────┐     ┌──────────────────────────────────┐
    │ Reference Type: Animal     │     │ Actual Object Type: Dog          │
    │ variable: 'a' ─────────────┼────>│  - Class pointer: Dog.class      │
    │                            │     │  - Object fields...              │
    └────────────────────────────┘     └──────────────────────────────────┘""",
            "desc": "Compiler checks that `Animal` has method `speak()`. At compile time, the call is considered legal.",
            "why": "Compile-time checks examine the REFERENCE type; runtime execution examines the OBJECT type."
        },
        {
            "title": "Runtime execution: a.speak() via vtable lookup",
            "code": "a.speak();  // Output: \"Woof!\"",
            "diagram": r"""    Execution Step-by-Step:
    1. JVM follows reference 'a' to Heap object.
    2. JVM reads object header: actual class is 'Dog'!
    3. JVM inspects Dog's vtable at slot [0] (speak).
    4. Slot [0] points directly to Dog.speak()!
    ==> Output: \"Woof!\" (Runtime Polymorphism achieved!)""",
            "desc": "The JVM resolves the method dynamically at runtime based on the actual object type in the Heap.",
            "why": "This is Dynamic Method Dispatch: the engine behind Java object-oriented runtime polymorphism."
        }
    ]
    takeaways = [
        "Compile-time checks are based on the Reference Type; runtime calls are based on the Object Type.",
        "Dynamic Method Dispatch is implemented via Virtual Method Tables (vtables) in the JVM.",
        "Methods marked `final`, `private`, or `static` do NOT use vtables (they use static binding at compile time)."
    ]
    _run_visualizer_steps(
        "JAVA-J5",
        "🎭 JAVA-J5: DYNAMIC METHOD DISPATCH & VTABLE RESOLUTION",
        "Trace compile-time type verification vs runtime object vtable resolution during polymorphic method invocations.",
        steps,
        takeaways
    )


def vis_java_exception_stack():
    """JAVA-J6: Exception Call Stack Unwinding & try-catch-finally"""
    steps = [
        {
            "title": "Nested method call stack frames",
            "code": "main() -> methodA() -> methodB() throws NullPointerException",
            "diagram": r"""    JVM CALL STACK (Before Exception):
    ┌─────────────────────────────────┐
    │ [Frame 3] methodB()             │ ──> Throws NullPointerException!
    ├─────────────────────────────────┤
    │ [Frame 2] methodA()             │ (No try-catch block here)
    ├─────────────────────────────────┤
    │ [Frame 1] main()                │ (Contains try { ... } catch (Exception e))
    └─────────────────────────────────┘""",
            "desc": "Three active stack frames. `methodB` throws an unchecked exception.",
            "why": "When an exception is thrown, the JVM begins searching down the stack for a matching catch block."
        },
        {
            "title": "Unwinding Frame 3: methodB pops without handler",
            "code": "methodB() has no catch block -> Frame popped!",
            "diagram": r"""    JVM CALL STACK (Unwinding):
    ┌─────────────────────────────────┐
    │ [Frame 2] methodA()             │ <── Exception propagates here!
    ├─────────────────────────────────┤
    │ [Frame 1] main()                │
    └─────────────────────────────────┘
    (Frame 3 popped from memory; execution in methodB terminated immediately)""",
            "desc": "No handler in `methodB`. Its stack frame is discarded and the exception propagates to `methodA`.",
            "why": "Unwinding cleans up local variables, but skipped code inside methodB will never execute."
        },
        {
            "title": "Unwinding Frame 2: methodA pops without handler",
            "code": "methodA() has no catch block -> Frame popped!",
            "diagram": r"""    JVM CALL STACK (Unwinding):
    ┌─────────────────────────────────┐
    │ [Frame 1] main()                │ <── Exception arrives at main()!
    └─────────────────────────────────┘
    (Frame 2 popped from memory)""",
            "desc": "`methodA` has no handler. Its stack frame is popped. Exception arrives in `main()`.",
            "why": "If main() had no handler, the thread would terminate with an UncaughtExceptionHandler stack trace."
        },
        {
            "title": "Matching catch found in main() & finally execution",
            "code": "catch (Exception e) { ... } finally { cleanup(); }",
            "diagram": r"""    [main frame]:
    1. Exception matches `catch (Exception e)` block!
    2. Catch block executes error recovery logic.
    3. FINALLY block executes GUARANTEED! (Closes files, sockets, DB connections)
    ==> Program recovers cleanly without crashing!""",
            "desc": "A matching handler is found. The exception is caught. The `finally` block runs unconditionally.",
            "why": "The `finally` block ALWAYS executes, even if return statements or further exceptions occur!"
        }
    ]
    takeaways = [
        "Stack Unwinding discards activation frames down the call stack until a matching catch block is located.",
        "Uncaught exceptions propagate all the way up to the JVM thread launcher, terminating the thread.",
        "`finally` blocks execute unconditionally, making them mandatory for releasing OS resources (files, sockets)."
    ]
    _run_visualizer_steps(
        "JAVA-J6",
        "💥 JAVA-J6: EXCEPTION CALL STACK UNWINDING & FINALLY",
        "Watch activation frames pop down the stack searching for catch handlers and see why finally blocks are guaranteed to run.",
        steps,
        takeaways
    )


def vis_java_concurrency_lock():
    """JAVA-J7: Multithreading & Synchronized Object Monitor"""
    steps = [
        {
            "title": "Object Monitor components in JVM memory",
            "code": "Object lock = new Object();",
            "diagram": r"""    OBJECT MONITOR (Every Java Object has an internal Monitor):
    ┌─────────────────────────────────────────────────────────────┐
    │  OWNER THREAD : [ NULL (Unlocked) ]                         │
    ├─────────────────────────────┬───────────────────────────────┤
    │  ENTRY SET (BLOCKED threads)│  WAIT SET (WAITING threads)   │
    │  [ Threads waiting for lock]│  [ Threads that called wait()]│
    └─────────────────────────────┴───────────────────────────────┘""",
            "desc": "Every Java heap object header contains a pointer to an internal Object Monitor mutex.",
            "why": "The monitor ensures mutual exclusion: only ONE thread can hold the lock at any instant."
        },
        {
            "title": "Thread-1 acquires lock: synchronized(lock)",
            "code": "Thread-1 enters synchronized block",
            "diagram": r"""    OBJECT MONITOR:
    ┌─────────────────────────────────────────────────────────────┐
    │  OWNER THREAD : [ Thread-1 (RUNNABLE / EXECUTING) ] 🔒      │
    ├─────────────────────────────┬───────────────────────────────┤
    │  ENTRY SET: (empty)         │  WAIT SET: (empty)            │
    └─────────────────────────────┴───────────────────────────────┘""",
            "desc": "Thread-1 enters synchronized block. It becomes the Owner Thread. Lock is acquired.",
            "why": "Thread-1 now has exclusive permission to execute the critical section."
        },
        {
            "title": "Thread-2 attempts entry: Contention & BLOCKED state",
            "code": "Thread-2 tries to enter synchronized(lock) while Thread-1 is inside",
            "diagram": r"""    OBJECT MONITOR:
    ┌─────────────────────────────────────────────────────────────┐
    │  OWNER THREAD : [ Thread-1 (Holding lock) ]                 │
    ├─────────────────────────────┬───────────────────────────────┤
    │  ENTRY SET: [ Thread-2 ⚠️ ] │  WAIT SET: (empty)            │
    │  (State: BLOCKED)           │                               │
    └─────────────────────────────┴───────────────────────────────┘""",
            "desc": "Thread-2 cannot acquire the lock. The OS suspends Thread-2 into the Entry Set in BLOCKED state.",
            "why": "BLOCKED threads consume zero CPU cycles while waiting for the owner thread to release the lock."
        },
        {
            "title": "Thread-1 exits: Lock released & Thread-2 wakes up",
            "code": "Thread-1 exits synchronized block -> Thread-2 acquires lock",
            "diagram": r"""    OBJECT MONITOR:
    ┌─────────────────────────────────────────────────────────────┐
    │  OWNER THREAD : [ Thread-2 (RUNNABLE / EXECUTING) ] 🔒      │
    ├─────────────────────────────┬───────────────────────────────┤
    │  ENTRY SET: (empty)         │  WAIT SET: (empty)            │
    └─────────────────────────────┴───────────────────────────────┘""",
            "desc": "Thread-1 releases the monitor. The OS schedules Thread-2, which transitions to RUNNABLE and enters.",
            "why": "Mutual exclusion protects shared mutable state from race conditions and data corruption."
        }
    ]
    takeaways = [
        "Every Java object has an intrinsic monitor lock used by `synchronized`.",
        "Threads unable to acquire a monitor are placed in the ENTRY SET in BLOCKED state.",
        "Synchronized blocks guarantee Mutual Exclusion (atomicity) and Memory Visibility (flushing CPU caches)."
    ]
    _run_visualizer_steps(
        "JAVA-J7",
        "🔒 JAVA-J7: MULTITHREADING & SYNCHRONIZED MONITOR LOCKS",
        "Step through the JVM Object Monitor structure, tracking Owner Thread, Entry Set, and BLOCKED thread states.",
        steps,
        takeaways
    )


def vis_java_producer_consumer():
    """JAVA-J8: Producer-Consumer Concurrency Pattern (wait & notify)"""
    steps = [
        {
            "title": "Bounded buffer and threads setup",
            "code": "Queue<Integer> buffer (Capacity = 2);",
            "diagram": r"""    BOUNDED BUFFER (Capacity = 2):
    ┌──────────┬──────────┐
    │  Item 1  │  Item 2  │  <── BUFFER IS FULL!
    └──────────┴──────────┘
    [ Producer Thread ] wanting to produce Item 3...""",
            "desc": "Buffer has 2 items and cannot accept any more. Producer thread is ready to put Item 3.",
            "why": "Producer must pause until Consumer creates space, without busy-waiting (spinning in a loop)."
        },
        {
            "title": "Producer calls wait(): Lock released and Thread sleeps",
            "code": "while (buffer.isFull()) { lock.wait(); }",
            "diagram": r"""    OBJECT MONITOR:
    Owner: [ NULL ] ──> Lock released!
    Wait-Set: [ Producer Thread (WAITING) 💤 ]
    (Producer is asleep in Wait Set; lock is free for Consumer!)""",
            "desc": "Calling `wait()` atomically releases the monitor lock and suspends Producer in the WAIT SET.",
            "why": "If `wait()` didn't release the lock, Consumer could never enter to consume, causing a DEADLOCK!"
        },
        {
            "title": "Consumer acquires lock, consumes Item, calls notify()",
            "code": "Item item = buffer.remove(); lock.notify();",
            "diagram": r"""    BOUNDED BUFFER:
    ┌──────────┬──────────┐
    │  Item 2  │ [EMPTY]  │  <── Buffer has space!
    └──────────┴──────────┘
    Consumer calls notify() ──> Signals Producer in Wait-Set!""",
            "desc": "Consumer takes Item 1. Buffer now has space. Consumer calls `notify()` to wake up one waiting thread.",
            "why": "Calling `notify()` moves the Producer from the WAIT SET to the ENTRY SET (RUNNABLE)."
        },
        {
            "title": "Producer re-acquires lock and inserts Item 3",
            "code": "buffer.add(Item 3);",
            "diagram": r"""    BOUNDED BUFFER:
    ┌──────────┬──────────┐
    │  Item 2  │  Item 3  │  <── Buffer safely updated!
    └──────────┴──────────┘
    Producer exits synchronized block.""",
            "desc": "Producer re-checks `while(isFull())` condition, inserts Item 3, and safely completes.",
            "why": "Always use `while(!condition)` instead of `if(!condition)` around `wait()` to guard against Spurious Wakeups!"
        }
    ]
    takeaways = [
        "`wait()` must only be called inside synchronized code; it atomically releases the monitor lock.",
        "`notify()` wakes one thread from the Wait-Set; `notifyAll()` wakes all waiting threads.",
        "Always use `while(condition)` around `wait()` to protect against Spurious Wakeups."
    ]
    _run_visualizer_steps(
        "JAVA-J8",
        "🏭 JAVA-J8: PRODUCER-CONSUMER CONCURRENCY (wait() & notify())",
        "Visualize thread signaling, bounded buffer management, lock releasing via wait(), and wakeups via notify().",
        steps,
        takeaways
    )


def vis_java_interfaces_abstract():
    """JAVA-J9: Interface vs Abstract Class (State vs Contract in Memory)"""
    steps = [
        {
            "title": "Abstract Class: Inheritance of State and Code",
            "code": "abstract class Vehicle { int speed; void honk() { println(\"Beep!\"); } }",
            "diagram": r"""    ABSTRACT CLASS (Carries State & Code):
    ┌──────────────────────────────────┐
    │  Vehicle                         │
    │  - Field: int speed              │ <── Instance Variable (STATE!)
    │  - Method: honk() [implemented]  │
    │  - abstract void drive();        │
    └──────────────────────────────────┘
    A class can extend ONLY ONE class (Single Inheritance of State)!""",
            "desc": "Abstract classes can hold instance variables, constructors, and partial implementations.",
            "why": "Java allows extending only ONE class to prevent state conflicts (the Diamond Problem)."
        },
        {
            "title": "Interface: Multiple Inheritance of Capabilities (Contracts)",
            "code": "interface Flyable { void fly(); }\ninterface Swimmable { void swim(); }",
            "diagram": r"""    INTERFACES (Pure Contracts / Capabilities):
    ┌────────────────────────┐      ┌────────────────────────┐
    │  Flyable               │      │  Swimmable             │
    │  - void fly();         │      │  - void swim();        │
    └────────────────────────┘      └────────────────────────┘
    Class AmphibiousPlane implements Flyable, Swimmable (ALLOWED!)""",
            "desc": "Interfaces define contracts without carrying instance state. A class can implement unlimited interfaces.",
            "why": "Because interfaces have no instance variables, implementing multiple interfaces causes NO state collision!"
        },
        {
            "title": "Java 8+ Default Methods in Interfaces",
            "code": "interface Flyable { default void land() { println(\"Landing safely\"); } }",
            "diagram": r"""    DEFAULT METHODS (Java 8+):
    ┌────────────────────────────────────────────────────────┐
    │  Flyable                                               │
    │  - void fly();                                         │
    │  - default void land() { ... } [Method Body Allowed!]  │
    └────────────────────────────────────────────────────────┘""",
            "desc": "Default methods allow adding new capabilities to interfaces without breaking existing implementing classes.",
            "why": "Solved the backward compatibility problem when adding Stream methods (`.stream()`) to Collections."
        }
    ]
    takeaways = [
        "Abstract classes can have instance variables and constructors; interfaces cannot have instance state.",
        "A class can inherit from only ONE class, but can implement MULTIPLE interfaces.",
        "Java 8+ interfaces support `default` and `static` methods with implementations."
    ]
    _run_visualizer_steps(
        "JAVA-J9",
        "🏛️ JAVA-J9: INTERFACE VS ABSTRACT CLASS (State vs Contract)",
        "Understand why Java forbids multiple class inheritance (Diamond Problem) while permitting multiple interface implementation.",
        steps,
        takeaways
    )


def vis_java_hashmap_internals():
    """JAVA-J10: Java HashMap Internals Under the Hood"""
    steps = [
        {
            "title": "HashMap internal architecture: Node<K,V>[] table",
            "code": "Map<String, Integer> map = new HashMap<>(); // default capacity = 16",
            "diagram": r"""    HASHMAP BUCKET TABLE: Node<K,V>[] table (Length = 16)
    [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9] [10] [11] [12] [13] [14] [15]
    [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]  [•]
    (All buckets initially null)""",
            "desc": "HashMap is an array of buckets. Each bucket holds the head of a linked list or Red-Black tree.",
            "why": "Array indexing allows O(1) instantaneous access once the bucket index is computed."
        },
        {
            "title": "Hashing and bitwise index calculation",
            "code": "hash = (h = key.hashCode()) ^ (h >>> 16);  index = (n - 1) & hash;",
            "diagram": r"""    Bucket Index Formula: index = (16 - 1) & hash = 15 & hash
    Key: \"Alice\" ──> hashCode() ──> hash spread ──> index = 4
    Place Node(\"Alice\", 95) at Bucket [4]!""",
            "desc": "Bitwise `(n - 1) & hash` computes the bucket index without slow modulo division.",
            "why": "Power-of-two table size (16, 32, 64) ensures `(n - 1) & hash` evenly distributes keys."
        },
        {
            "title": "Handling collisions via Separate Chaining",
            "code": "map.put(\"Bob\", 88); // Suppose \"Bob\" also hashes to index 4 (COLLISION!)",
            "diagram": r"""    Bucket [4]:
    ┌───────────────────────────┐      ┌───────────────────────────┐
    │ Node(\"Alice\", 95, next)   │ ────>│ Node(\"Bob\", 88, null)    │
    └───────────────────────────┘      └───────────────────────────┘
    \"Bob\" is appended as a linked list node behind \"Alice\" in Bucket 4!""",
            "desc": "When different keys hash to the same bucket index, they are chained together in a linked list.",
            "why": "Separate chaining guarantees no key is overwritten when collisions occur."
        },
        {
            "title": "Treeify Optimization (Java 8+): Red-Black Tree threshold",
            "code": "TREEIFY_THRESHOLD = 8; // If bucket list exceeds 8 nodes",
            "diagram": r"""    If a single bucket chain length >= 8 and table capacity >= 64:
    LinkedList: O(N) linear search  ──> Converts to Red-Black Tree: O(log N)!
              [ Node ]
             /        \
         [ Node ]    [ Node ]""",
            "desc": "Java 8 automatically converts overcrowded linked list buckets into balanced Red-Black Trees.",
            "why": "Prevents malicious hash collision attacks (HashDoS) from degrading HashMap lookups to O(N)."
        }
    ]
    takeaways = [
        "Bucket index is computed using bitwise AND: `(length - 1) & hash`.",
        "Collisions are resolved via Separate Chaining (linked list of `Node<K,V>`).",
        "In Java 8+, if a bucket's linked list reaches length 8, it converts to a Red-Black tree for O(log N) worst-case speed."
    ]
    _run_visualizer_steps(
        "JAVA-J10",
        "🗄️ JAVA-J10: JAVA HASHMAP INTERNALS UNDER THE HOOD",
        "Trace bucket array indexing, bitwise hashing, separate chaining collision resolution, and Java 8 treeify optimization.",
        steps,
        takeaways
    )


# ════════════════════════════════════════════════════════════════════════════════
# 3. VISUAL CONCEPT THEATER (MAIN 22-VISUALIZER HUB)
# ════════════════════════════════════════════════════════════════════════════════

def visualizer_theater_hub():
    """Main menu entry point for the Visual Concept Studio (22 Visualizers)."""
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   🎬 VISUAL CONCEPT THEATER — 22 Deep Memory & Architecture Visualizers      ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
        print("  Explore 22 step-by-step & animated visualizers covering the toughest concepts in DSA and Java:\n")

        print(f"  {Color.GREEN}{Color.BOLD}🌳 DATA STRUCTURES & ALGORITHMS (12 DSA VISUALIZERS):{Color.RESET}")
        print(f"    {Color.YELLOW}[1]{Color.RESET}  🧠 V1:  Memory Architecture & Pointers (Stack vs Heap, Dangling Pointers)")
        print(f"    {Color.YELLOW}[2]{Color.RESET}  🔄 V2:  Recursion & System Call Stack (Call Frame Pushing & Popping)")
        print(f"    {Color.YELLOW}[3]{Color.RESET}  🔗 V3:  Linked List 3-Pointer Reversal (prev, curr, next In-Place)")
        print(f"    {Color.YELLOW}[4]{Color.RESET}  🐢 V4:  Floyd's Cycle Detection (Tortoise & Hare, Finding Loop Entry)")
        print(f"    {Color.YELLOW}[5]{Color.RESET}  📥 V5:  Infix to Postfix Conversion (Operator Precedence & Stack)")
        print(f"    {Color.YELLOW}[6]{Color.RESET}  🔄 V6:  Circular Queue & Modulo Ring Buffer ((rear + 1) % MAX)")
        print(f"    {Color.YELLOW}[7]{Color.RESET}  ⚡ V7:  QuickSort In-Place Partitioning (Lomuto Two-Pointer Scan)")
        print(f"    {Color.YELLOW}[8]{Color.RESET}  🔀 V8:  MergeSort Divide & Conquer Tree (Splitting & Two-Pointer Merge)")
        print(f"    {Color.YELLOW}[9]{Color.RESET}  🌲 V9:  Binary Search Tree (Left < Root < Right & Inorder Traversal)")
        print(f"    {Color.YELLOW}[10]{Color.RESET} ⚖️ V10: AVL Tree Self-Balancing Rotations (LL, RR, LR, RL Rotations)")
        print(f"    {Color.YELLOW}[11]{Color.RESET} 🔑 V11: Hash Table Collision Resolution (Linear Probing & Tombstones)")
        print(f"    {Color.YELLOW}[12]{Color.RESET} 🕸️ V12: Graph Traversal Stepper (BFS Queue vs DFS Call Stack)")

        print(f"\n  {Color.BLUE}{Color.BOLD}☕ JAVA OOP & JVM RUNTIME (10 JAVA VISUALIZERS):{Color.RESET}")
        print(f"    {Color.CYAN}[13]{Color.RESET} ☕ J1:  JVM Runtime Memory Layout (Metaspace, Stack Frames & Heap)")
        print(f"    {Color.CYAN}[14]{Color.RESET} 🧵 J2:  String Constant Pool vs Heap (== vs .equals() & intern())")
        print(f"    {Color.CYAN}[15]{Color.RESET} 📦 J3:  Java Pass-by-Value vs Object References (The Reassignment Trap)")
        print(f"    {Color.CYAN}[16]{Color.RESET} 🧹 J4:  GC Root Reachability & Cyclic Reference Island Collection")
        print(f"    {Color.CYAN}[17]{Color.RESET} 🎭 J5:  Dynamic Method Dispatch & Virtual Method Table (vtable)")
        print(f"    {Color.CYAN}[18]{Color.RESET} 💥 J6:  Exception Call Stack Propagation & finally Block Guarantee")
        print(f"    {Color.CYAN}[19]{Color.RESET} 🔒 J7:  Multithreading Concurrency & Synchronized Monitor Locks")
        print(f"    {Color.CYAN}[20]{Color.RESET} 🏭 J8:  Producer-Consumer Concurrency Pattern (wait() & notify())")
        print(f"    {Color.CYAN}[21]{Color.RESET} 🏛️ J9:  Interface vs Abstract Class (State vs Contract & Diamond Problem)")
        print(f"    {Color.CYAN}[22]{Color.RESET} 🗄️ J10: Java HashMap Internals (Buckets, Chaining & Treeify at 8)")

        print(f"\n  {Color.DIM}[0]   ⬅️   Back to Main Menu{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Choose visualizer to explore [1 - 22, 0=Back]: {Color.RESET}").strip()

        action_map = {
            "1": vis_dsa_memory,
            "2": vis_dsa_recursion,
            "3": vis_dsa_linked_reversal,
            "4": vis_dsa_floyd_cycle,
            "5": vis_dsa_infix_postfix,
            "6": vis_dsa_circular_queue,
            "7": vis_dsa_quicksort_partition,
            "8": vis_dsa_mergesort_tree,
            "9": vis_dsa_bst_operations,
            "10": vis_dsa_avl_rotations,
            "11": vis_dsa_hash_collision,
            "12": vis_dsa_graph_traversal,
            "13": vis_java_jvm_memory,
            "14": vis_java_string_pool,
            "15": vis_java_pass_by_value,
            "16": vis_java_gc_reachability,
            "17": vis_java_dynamic_dispatch,
            "18": vis_java_exception_stack,
            "19": vis_java_concurrency_lock,
            "20": vis_java_producer_consumer,
            "21": vis_java_interfaces_abstract,
            "22": vis_java_hashmap_internals,
        }

        if choice in ("0", "B", "BACK", "EXIT", "Q"):
            return
        elif choice in action_map:
            action_map[choice]()
