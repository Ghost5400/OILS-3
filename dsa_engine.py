"""
🌳 OILS-3: DATA STRUCTURES LABORATORY ARCADE ENGINE (1BCSL306)
Part of OILS-3: Oops, I Learnt Something! (3rd Sem Engineering Edition)

Features:
- 12 Interactive VTU 2025 Scheme Lab Experiments with Block-by-Block Logic
- "Your Turn to Code" Hands-On Coding Challenges
- Interactive Data Structure Visualizers (Stack, Queue, Linked List, BST)
- 25 External Examiner Viva Questions with Lives & Roasts
"""

import sys
import time
import os
import random

# Color & styling classes (synchronized with master play.py)
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

def spinner(label="Simulating", duration=1.0, color=Color.CYAN):
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
    for f in [f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT! MASTERED!  ✅{Color.RESET}",
              f"{Color.WHITE}{Color.BOLD}  ✅  CORRECT! MASTERED!  ✅{Color.RESET}",
              f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT! MASTERED!  ✅{Color.RESET}"]:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.15)
    print()

def anim_wrong():
    for f in [f"{Color.RED}{Color.BOLD}  ❌  WRONG! SEGFAULT DETECTED!  ❌{Color.RESET}",
              f"{Color.WHITE}{Color.BOLD}  ❌  WRONG! SEGFAULT DETECTED!  ❌{Color.RESET}",
              f"{Color.RED}{Color.BOLD}  ❌  WRONG! SEGFAULT DETECTED!  ❌{Color.RESET}"]:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.15)
    print()

# ==============================================================================
# 12 EXPERIMENT DATABASE
# ==============================================================================

DSA_EXPERIMENTS = [
    {
        "num": 1,
        "part": "A",
        "title": "Library Book Management (Structures & Dynamic Memory)",
        "file": "dsa-lab/programs/lab01_library_management.c",
        "problem": "Define Book structure (Book_ID, Title, Author, Price, Status). Dynamically allocate memory for N books on the heap using malloc(). Implement create(), display(), search(), issueBook(), and returnBook().",
        "concept": "Dynamic memory allocation using malloc(N * sizeof(Book)). Pointers allow allocating exact bytes at runtime rather than fixed array sizes.",
        "blocks": [
            {
                "title": "Dynamic Heap Allocation",
                "code": "books = (Book *)malloc(bookCount * sizeof(Book));\nif (books == NULL) {\n    printf(\"Memory allocation failed!\\n\");\n    return;\n}",
                "explanation": "malloc() requests contiguous bytes on the Heap. It returns a void* pointer cast to (Book*). Always check if books == NULL to protect against Out-Of-Memory crashes!"
            },
            {
                "title": "State Transition in issueBook()",
                "code": "if (books[pos].Availability_Status == 0) {\n    printf(\"Cannot issue: Already issued!\\n\");\n} else {\n    books[pos].Availability_Status = 0;\n}",
                "explanation": "Checks if the book is currently available (1). If yes, flips Availability_Status to 0 (Issued). Guard against double-issuing."
            }
        ],
        "challenge": {
            "prompt": "Write the C line to dynamically allocate memory for 'n' structures of type 'Book' to pointer 'books':",
            "answers": [
                "books = (Book *)malloc(n * sizeof(Book));",
                "books = malloc(n * sizeof(Book));",
                "books=(Book*)malloc(n*sizeof(Book));",
                "books=(Book *)malloc(n * sizeof(Book));"
            ],
            "hint": "Use: books = (Book *)malloc(n * sizeof(Book));",
            "praise": "Spot on! You safely allocated heap memory for N book structures.",
            "roast": "Watch your pointer casting and sizeof! Correct syntax: books = (Book *)malloc(n * sizeof(Book));"
        }
    },
    {
        "num": 2,
        "part": "A",
        "title": "Sparse Matrix Triplet Representation, Addition & Transpose",
        "file": "dsa-lab/programs/lab02_sparse_matrix.c",
        "problem": "Read two matrices of equal dimensions. Represent each sparse matrix in three-column triplet form (row, column, value), add them, and compute the transpose.",
        "concept": "A sparse matrix has mostly 0s. The 3-column triplet saves memory by only storing non-zero cells. Row 0 holds metadata: a[0].r = rows, a[0].c = cols, a[0].v = total non-zero elements.",
        "blocks": [
            {
                "title": "Metadata Initialization",
                "code": "a[0].r = rows; a[0].c = cols; a[0].v = count;",
                "explanation": "Slot 0 is the matrix header. It tells all algorithms the original matrix dimensions and how many non-zero entries follow in indices 1..count."
            },
            {
                "title": "Sparse Matrix Transpose",
                "code": "for (int col = 0; col < a[0].c; col++)\n    for (int i = 1; i <= a[0].v; i++)\n        if (a[i].c == col) {\n            t[k].r = a[i].c; t[k].c = a[i].r; t[k].v = a[i].v; k++;\n        }",
                "explanation": "Scans columns 0..c-1 so that transposed triplets are automatically sorted by their new row (original column)."
            }
        ],
        "challenge": {
            "prompt": "In a 3-column triplet array 'a', write the expression to check if matrix A and B have matching dimensions for addition:",
            "answers": [
                "a[0].r == b[0].r && a[0].c == b[0].c",
                "a[0].r==b[0].r && a[0].c==b[0].c",
                "(a[0].r == b[0].r) && (a[0].c == b[0].c)",
                "a[0].r == b[0].r && a[0].c == b[0].c;"
            ],
            "hint": "Check if a[0].r == b[0].r and a[0].c == b[0].c",
            "praise": "Correct! You verified both row and column counts before addition.",
            "roast": "Remember, matrix addition requires BOTH rows and columns to match: a[0].r == b[0].r && a[0].c == b[0].c"
        }
    },
    {
        "num": 3,
        "part": "A",
        "title": "Stack Operations Using an Array (PUSH, POP, PEEK)",
        "file": "dsa-lab/programs/lab03_stack_operations.c",
        "problem": "Implement an integer stack using an array. Support PUSH, POP, PEEK and DISPLAY operations with overflow and underflow detection.",
        "concept": "LIFO (Last-In First-Out) data structure. Top pointer tracks the latest inserted element. Top starts at -1 (empty) and stops at capacity - 1 (full).",
        "blocks": [
            {
                "title": "PUSH Operation with Overflow Check",
                "code": "if (top == capacity - 1) {\n    printf(\"STACK OVERFLOW!\\n\");\n    return;\n}\ntop = top + 1;\nstack[top] = element;",
                "explanation": "Must check top == capacity - 1 BEFORE incrementing top, otherwise you will corrupt memory beyond the array boundary!"
            },
            {
                "title": "POP Operation with Underflow Check",
                "code": "if (top == -1) {\n    printf(\"STACK UNDERFLOW!\\n\");\n    return;\n}\nint deleted = stack[top];\ntop = top - 1;",
                "explanation": "Must check top == -1 BEFORE popping. Retrieving an element when top == -1 reads garbage or faults."
            }
        ],
        "challenge": {
            "prompt": "Write the 2 lines of C code to push 'val' into 'stack' after verifying it is not full:",
            "answers": [
                "top = top + 1; stack[top] = val;",
                "stack[++top] = val;",
                "top++; stack[top] = val;",
                "++top; stack[top] = val;",
                "top = top + 1; stack[top] = val"
            ],
            "hint": "Increment top first, then assign: stack[++top] = val; or top++; stack[top] = val;",
            "praise": "Clean stack push! You incremented TOP before writing.",
            "roast": "Always increment top BEFORE assigning, e.g.: top = top + 1; stack[top] = val;"
        }
    },
    {
        "num": 4,
        "part": "A",
        "title": "Printer Queue Simulation Using an Array",
        "file": "dsa-lab/programs/lab04_printer_queue.c",
        "problem": "Simulate a printer queue. Insert print-job IDs, process next job, display pending jobs, and detect queue overflow and underflow.",
        "concept": "FIFO (First-In First-Out). Elements enter at REAR and leave from FRONT. When the last remaining element is processed (front == rear), both pointers reset to -1.",
        "blocks": [
            {
                "title": "Single-Element Reset on Dequeue",
                "code": "if (front == rear) {\n    front = -1;\n    rear = -1;\n} else {\n    front = front + 1;\n}",
                "explanation": "If front == rear, the queue only had 1 job. Once removed, the queue is completely empty, so reset both pointers to -1 to reclaim capacity."
            }
        ],
        "challenge": {
            "prompt": "What is the condition that indicates a linear queue is completely empty?",
            "answers": [
                "front == -1",
                "front == -1 || front > rear",
                "front==-1",
                "front == -1;"
            ],
            "hint": "front == -1",
            "praise": "Correct! When front == -1, the queue is empty.",
            "roast": "In a linear queue, emptiness is signaled when front == -1."
        }
    },
    {
        "num": 5,
        "part": "A",
        "title": "Polynomial Addition Using Circular Linked List with Header",
        "file": "dsa-lab/programs/lab05_polynomial_addition.c",
        "problem": "Represent polynomials using header-node singly circular linked lists. Each term stores coefficient and exponent. Read two polynomials and add them into POLYSUM.",
        "concept": "A dummy header node points to itself when empty (head->next == head). Eliminates special case logic for empty list and end-of-list NULL checks.",
        "blocks": [
            {
                "title": "Circular Header Initialization",
                "code": "Node *h = (Node *)malloc(sizeof(Node));\nh->c = 0;\nh->e = -1;\nh->next = h;",
                "explanation": "The header node's next pointer points back to itself, closing the circular loop!"
            },
            {
                "title": "Polynomial Term Merging",
                "code": "if (p->e == q->e) {\n    int sum = p->c + q->c;\n    if (sum != 0) insertSorted(res, sum, p->e);\n    p = p->next; q = q->next;\n}",
                "explanation": "When powers are identical, add coefficients. If they cancel to 0, omit the term. Then advance both pointers."
            }
        ],
        "challenge": {
            "prompt": "Write the C assignment that makes a newly allocated header node 'h' circular (pointing to itself):",
            "answers": [
                "h->next = h;",
                "h->next=h;",
                "h->next = h"
            ],
            "hint": "h->next = h;",
            "praise": "Spot on! The circular loop is closed.",
            "roast": "To make a header node circular, point its next back to itself: h->next = h;"
        }
    },
    {
        "num": 6,
        "part": "A",
        "title": "Binary Tree Creation & Traversals (Level-Order via Queue)",
        "file": "dsa-lab/programs/lab06_binary_tree_traversals.c",
        "problem": "Create a Binary Tree by inserting integer keys in level order using a queue. Implement and display preorder, inorder, and postorder traversals.",
        "concept": "Level-order creation uses a queue: root is enqueued first. When a new node arrives, attach to parent's left if empty, else to right and dequeue parent.",
        "blocks": [
            {
                "title": "Recursive Inorder Traversal",
                "code": "void inorder(TreeNode *root) {\n    if (root != NULL) {\n        inorder(root->left);\n        printf(\"%d \", root->data);\n        inorder(root->right);\n    }\n}",
                "explanation": "Left -> Root -> Right. For a Binary Search Tree, this traversal prints keys in ascending sorted order!"
            }
        ],
        "challenge": {
            "prompt": "What is the visit order of Preorder traversal? (Use words: Root, Left, Right separated by dashes):",
            "answers": [
                "Root-Left-Right",
                "Root - Left - Right",
                "root-left-right",
                "Root, Left, Right"
            ],
            "hint": "Root-Left-Right",
            "praise": "Exact! Preorder visits Root first, then Left subtree, then Right subtree.",
            "roast": "Preorder means Root comes PRE (before children): Root-Left-Right."
        }
    },
    {
        "num": 7,
        "part": "B",
        "title": "Infix-to-Postfix Conversion with Bracket Validation",
        "file": "dsa-lab/programs/lab07_infix_to_postfix.c",
        "problem": "Compiler expression tool: Validate proper bracket nesting (), {}, [] and arithmetic syntax using a stack, then convert valid infix to postfix.",
        "concept": "Operands are output immediately. Operators wait on the stack until operators of lower precedence arrive. Brackets force sub-expression priority.",
        "blocks": [
            {
                "title": "Bracket Matching Logic",
                "code": "if (isOpeningBracket(ch)) {\n    bStack[++top] = ch;\n} else if (isClosingBracket(ch)) {\n    if (top == -1 || !isMatchingPair(bStack[top--], ch)) return 0;\n}",
                "explanation": "Closing bracket must match the opening bracket currently at top of stack (e.g. ')' matches '(', but not '[')."
            }
        ],
        "challenge": {
            "prompt": "What is the postfix conversion of the infix expression: (A + B) * C",
            "answers": [
                "A B + C *",
                "AB+C*",
                "A B + C * ",
                "AB+ C*"
            ],
            "hint": "A B + C *",
            "praise": "Correct! (A+B) evaluates first to AB+, which is then multiplied by C: AB+C*.",
            "roast": "Brackets have highest precedence: (A+B) becomes AB+, then * C gives: A B + C *"
        }
    },
    {
        "num": 8,
        "part": "B",
        "title": "Student Record Management Using Singly Linked List (SLL)",
        "file": "dsa-lab/programs/lab08_student_sll.c",
        "problem": "Manage student records (USN, Name, Sem, Dept) using SLL. Support insertion, display, display by semester, insert after name, and delete by USN/Name.",
        "concept": "SLL consists of nodes chained via 'next' pointers. Inserting after a node requires linking the new node first before updating the existing node's pointer.",
        "blocks": [
            {
                "title": "Insert After Node 'p'",
                "code": "newNode->next = p->next;\np->next = newNode;",
                "explanation": "CRITICAL ORDER: Attach newNode to the rest of the list (p->next) FIRST. Then attach p to newNode. If reversed, the rest of the list is lost!"
            }
        ],
        "challenge": {
            "prompt": "Write the 2 lines of C code to insert 'newNode' directly after node 'p' in an SLL:",
            "answers": [
                "newNode->next = p->next; p->next = newNode;",
                "newNode->next=p->next; p->next=newNode;",
                "newNode->next = p->next; p->next = newNode"
            ],
            "hint": "newNode->next = p->next; p->next = newNode;",
            "praise": "Perfect pointer manipulation! No memory leaks or orphaned nodes.",
            "roast": "Order matters! First: newNode->next = p->next; Second: p->next = newNode;"
        }
    },
    {
        "num": 9,
        "part": "B",
        "title": "Manufacturing Parts Inventory Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab09_parts_hash_table.c",
        "problem": "Manage machine parts using a hash table with linear probing. Keyed by alphanumeric Part Number. Implement add, search, remove, and display.",
        "concept": "Hash function maps key to index. On collision, probe sequentially: (start + i) % TABLE_SIZE. Mark deleted slots with DELETED tombstone.",
        "blocks": [
            {
                "title": "Tombstone (DELETED) Slot Management",
                "code": "if (table[idx].status == DELETED && firstDeleted == -1) {\n    firstDeleted = idx;\n}",
                "explanation": "DELETED slots allow new inserts to recycle the slot while ensuring searches continue past it to find items inserted later in the probe chain."
            }
        ],
        "challenge": {
            "prompt": "In linear probing, what slot status causes a search to STOP and conclude the key does not exist?",
            "answers": [
                "EMPTY",
                "empty",
                "SlotStatus.EMPTY"
            ],
            "hint": "EMPTY",
            "praise": "Correct! Hitting an EMPTY slot proves the key was never inserted.",
            "roast": "An EMPTY slot terminates the probe chain. DELETED slots must be bypassed."
        }
    },
    {
        "num": 10,
        "part": "B",
        "title": "Hierarchical Numeric Data Using Binary Search Tree (BST)",
        "file": "dsa-lab/programs/lab10_bst_numeric.c",
        "problem": "Store hierarchical numeric keys in a BST. Implement recursive insertion, search, and tree traversals. Ignore duplicates.",
        "concept": "For every node X: Left subtree < X < Right subtree. Inorder traversal of a BST visits keys in strictly ascending sorted order.",
        "blocks": [
            {
                "title": "Recursive BST Insertion",
                "code": "if (val < root->key) root->left = insertBST(root->left, val);\nelse if (val > root->key) root->right = insertBST(root->right, val);\nelse printf(\"Duplicate ignored\\n\");",
                "explanation": "Smaller values go left, larger go right. If key matches, ignore duplicate to maintain set property."
            }
        ],
        "challenge": {
            "prompt": "Which tree traversal on a Binary Search Tree always prints elements in ascending sorted order?",
            "answers": [
                "Inorder",
                "inorder",
                "In-order",
                "in order"
            ],
            "hint": "Inorder",
            "praise": "Spot on! Inorder traversal (Left -> Root -> Right) always produces sorted output on a BST.",
            "roast": "Inorder traversal visits Left, Root, Right, which guarantees sorted output."
        }
    },
    {
        "num": 11,
        "part": "B",
        "title": "Employee Record Management Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab11_employee_hash_table.c",
        "problem": "Manage employee records (Emp No, Name, Designation, Dept) in a hash table of size 17. Implement insertion, search, delete, and display by department.",
        "concept": "Hash function: h(k) = k % 17. Linear probing resolves collisions. Tombstone markers protect search probe chains.",
        "blocks": [
            {
                "title": "Modulo Hash Function",
                "code": "int hashFunction(int empNum) {\n    return empNum % 17;\n}",
                "explanation": "Computes slot index in range [0, 16] in O(1) time."
            }
        ],
        "challenge": {
            "prompt": "If TABLE_SIZE is 17, what is the hash index for employee number 122? (122 % 17):",
            "answers": [
                "3",
                "slot 3",
                "index 3"
            ],
            "hint": "122 % 17 = 122 - (17 * 7) = 122 - 119 = 3",
            "praise": "Accurate math! 122 % 17 = 3.",
            "roast": "17 * 7 = 119, so 122 % 17 = 3."
        }
    },
    {
        "num": 12,
        "part": "B",
        "title": "City Connectivity Using Graphs & Depth-First Search (DFS)",
        "file": "dsa-lab/programs/lab12_city_connectivity.c",
        "problem": "Represent N cities and interconnected roads using an Adjacency Matrix. Implement DFS to find all cities reachable from a source and test if two cities are connected.",
        "concept": "Adjacency matrix: adj[u][v] = 1 means road exists between u and v. DFS explores as far as possible along each branch before backtracking using a visited array.",
        "blocks": [
            {
                "title": "Recursive DFS with Visited Array",
                "code": "void dfs(int u) {\n    visited[u] = 1;\n    for (int v = 0; v < numCities; v++) {\n        if (adjMatrix[u][v] == 1 && !visited[v]) {\n            dfs(v);\n        }\n    }\n}",
                "explanation": "Marking visited[u] = 1 prevents infinite cycles in circular road networks!"
            }
        ],
        "challenge": {
            "prompt": "Why is a 'visited' array mandatory when performing DFS on a cyclic graph?",
            "answers": [
                "To prevent infinite loops",
                "prevent infinite loops",
                "to avoid infinite cycles",
                "avoid infinite loops",
                "infinite loop"
            ],
            "hint": "To prevent infinite loops",
            "praise": "Exactly! Without the visited array, DFS would cycle forever in graph loops.",
            "roast": "The visited array prevents infinite recursion/loops when cycles exist in the graph."
        }
    }
]

# ==============================================================================
# 25 EXTERNAL EXAMINER VIVA QUESTIONS
# ==============================================================================

DSA_VIVA_GAUNTLET = [
    {
        "q": "What is the difference between malloc() and calloc() in C dynamic memory allocation?",
        "options": [
            "A) malloc() initializes memory to zero; calloc() leaves garbage values.",
            "B) malloc() allocates uninitialized memory; calloc() allocates and initializes all bytes to zero.",
            "C) malloc() works on the Stack; calloc() works on the Heap.",
            "D) malloc() cannot fail; calloc() can fail."
        ],
        "ans": "B",
        "tip": "calloc(n, size) clears memory to zero. malloc(bytes) leaves whatever garbage bits were previously in RAM.",
        "praise": "Spot on! Examiners love asking this to test your understanding of heap initialization.",
        "roast": "Careful! calloc() zeroes out memory; malloc() leaves raw uninitialized garbage values."
    },
    {
        "q": "What is a 'Dangling Pointer' in C and how does it happen?",
        "options": [
            "A) A pointer that was declared but never assigned NULL.",
            "B) A pointer pointing to a memory location that has already been freed via free().",
            "C) A pointer that points to another pointer.",
            "D) A pointer initialized to point to address 0x0."
        ],
        "ans": "B",
        "tip": "After free(ptr), the pointer still holds the old address. Accessing it is undefined behavior! Always do ptr = NULL after free.",
        "praise": "Excellent! Setting ptr = NULL after free() is the mark of a professional C programmer.",
        "roast": "A dangling pointer still points to a memory address that the OS has already freed."
    },
    {
        "q": "Why is a Circular Queue superior to a standard Linear Queue implemented with an array?",
        "options": [
            "A) Circular queues use half the memory of linear queues.",
            "B) Linear queues suffer from 'false overflow' where rear reaches the end even if front slots are empty; circular queues reuse freed slots.",
            "C) Circular queues can store strings; linear queues can only store integers.",
            "D) Circular queues do not need front or rear pointers."
        ],
        "ans": "B",
        "tip": "In a linear queue, when elements are dequeued, front moves forward leaving vacant slots behind that can never be reused. Modulo arithmetic (rear+1)%MAX wraps around.",
        "praise": "Bingo! Modulo arithmetic solves the false overflow problem in circular queues.",
        "roast": "In a linear queue, once rear reaches MAX-1, it reports overflow even if index 0, 1, 2 are completely vacant!"
    },
    {
        "q": "Why do we use a dummy 'Header Node' in a Circular Linked List for Polynomial addition?",
        "options": [
            "A) Because C requires every list to have at least two nodes.",
            "B) It eliminates special-case checks for inserting into an empty list or deleting the first term.",
            "C) It automatically doubles the speed of CPU multiplication.",
            "D) It stores the degree of the polynomial in its coefficient."
        ],
        "ans": "B",
        "tip": "With a header node, the list is NEVER empty (header is always present). Insertion and deletion logic never have to branch for head == NULL.",
        "praise": "True systems engineering insight! Header nodes simplify pointer manipulation boundary conditions.",
        "roast": "Header nodes prevent messy 'if (head == NULL)' checks when manipulating linked lists."
    },
    {
        "q": "What is the worst-case time complexity of searching an element in an un-balanced Binary Search Tree (BST)?",
        "options": [
            "A) O(1)",
            "B) O(log N)",
            "C) O(N)",
            "D) O(N log N)"
        ],
        "ans": "C",
        "tip": "If elements are inserted in strictly sorted order (1, 2, 3, 4, 5), the BST degenerates into a linear linked list (skewed tree) of height N, taking O(N) time.",
        "praise": "Correct! When a BST degenerates into a skewed tree, it performs identically to a linked list.",
        "roast": "In the worst case (skewed tree), height = N, so search degrades from O(log N) to O(N)!"
    },
    {
        "q": "In Open Addressing Hash Tables, why must deleted slots be marked with a 'DELETED' tombstone instead of EMPTY?",
        "options": [
            "A) Because the OS does not allow changing an array slot to EMPTY.",
            "B) Because linear probe searches terminate on EMPTY; if marked EMPTY, keys inserted after it become permanently unreachable.",
            "C) Because EMPTY slots consume more RAM than DELETED slots.",
            "D) DELETED slots encrypt the data for cybersecurity."
        ],
        "ans": "B",
        "tip": "Linear probing stops searching as soon as it hits an EMPTY slot. If you reset a slot to EMPTY, you break the probe chain for collided keys!",
        "praise": "Outstanding! You understand collision resolution probe chains at an architectural level.",
        "roast": "If you mark a slot EMPTY upon deletion, any future search for collided keys behind it will prematurely abort and say 'Not Found'!"
    }
]

# ==============================================================================
# INTERACTIVE DATA STRUCTURE VISUALIZERS
# ==============================================================================

def visualizer_stack():
    stack = []
    cap = 5
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}========== 📦 INTERACTIVE STACK VISUALIZER (Capacity: {cap}) =========={Color.RESET}\n")
        print("Current Memory Container:")
        print("     +----------+")
        for i in range(cap - 1, -1, -1):
            if i < len(stack):
                is_top = (i == len(stack) - 1)
                tag = f" {Color.YELLOW}<-- [TOP]{Color.RESET}" if is_top else ""
                print(f"  [{i}] |  {Color.GREEN}{stack[i]:4d}{Color.RESET}    |{tag}")
            else:
                print(f"  [{i}] |  {Color.DIM}(empty){Color.RESET}  |")
        print("     +----------+\n")

        print(f"Actions: {Color.YELLOW}[1] Push{Color.RESET}  {Color.RED}[2] Pop{Color.RESET}  {Color.BLUE}[3] Peek{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input("Choose action: ").strip()

        if cmd == "1":
            if len(stack) >= cap:
                print(f"{Color.RED}🚨 STACK OVERFLOW! Stack is full ({cap}/{cap})!{Color.RESET}")
                time.sleep(1.0)
            else:
                val = prompt_input("Enter integer to push: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    stack.append(int(val))
                    spinner(f"Pushing {val} to stack", duration=0.6)
                else:
                    print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                    time.sleep(0.8)
        elif cmd == "2":
            if not stack:
                print(f"{Color.RED}🚨 STACK UNDERFLOW! Stack is empty.{Color.RESET}")
                time.sleep(1.0)
            else:
                popped = stack.pop()
                spinner(f"Popping {popped} from stack", duration=0.6)
        elif cmd == "3":
            if not stack:
                print(f"{Color.YELLOW}Stack is empty. Nothing to peek.{Color.RESET}")
            else:
                print(f"{Color.GREEN}✔ Top element is: {stack[-1]} (at index {len(stack)-1}){Color.RESET}")
            prompt_input("Press Enter to continue...")
        elif cmd in ("0", "b", "exit"):
            break

def visualizer_linked_list():
    nodes = [10, 25, 42]
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}========== 🔗 INTERACTIVE LINKED LIST VISUALIZER =========={Color.RESET}\n")
        print("Memory Pointer Chain:")
        if not nodes:
            print(f"  {Color.YELLOW}[HEAD] ---> NULL (Empty List){Color.RESET}\n")
        else:
            chain = f"  {Color.YELLOW}[HEAD]{Color.RESET} -> "
            for idx, val in enumerate(nodes):
                chain += f"[{Color.GREEN}{val}{Color.RESET}|•] -> "
            chain += f"{Color.RED}NULL{Color.RESET}"
            print(chain)
            print("         " + "        ".join([f"Node #{i+1}" for i in range(len(nodes))]) + "\n")

        print(f"Actions: {Color.YELLOW}[1] Insert Front{Color.RESET}  {Color.GREEN}[2] Insert End{Color.RESET}  {Color.RED}[3] Delete Front{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input("Choose action: ").strip()

        if cmd == "1":
            val = prompt_input("Enter integer for new node: ").strip()
            if val.isdigit():
                nodes.insert(0, int(val))
                spinner(f"Allocating node {val} with malloc() and updating HEAD", duration=0.7)
        elif cmd == "2":
            val = prompt_input("Enter integer for new node: ").strip()
            if val.isdigit():
                nodes.append(int(val))
                spinner(f"Traversing to end and linking node {val}", duration=0.7)
        elif cmd == "3":
            if not nodes:
                print(f"{Color.RED}List is empty. Nothing to delete!{Color.RESET}")
                time.sleep(0.8)
            else:
                removed = nodes.pop(0)
                spinner(f"Updating HEAD = HEAD->next and calling free({removed})", duration=0.7)
        elif cmd in ("0", "b", "exit"):
            break

# ==============================================================================
# EXPERIMENT RUNNER & CODE CHALLENGE ENGINE
# ==============================================================================

def run_experiment_lab(exp):
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}")
    print(f"  🌳 EXPERIMENT {exp['num']:02d} ({exp['part']}): {exp['title']}")
    print(f"{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}\n")

    print(f"{Color.YELLOW}{Color.BOLD}🎯 VTU PROBLEM REQUIREMENT:{Color.RESET}")
    print(f"  {exp['problem']}\n")

    print(f"{Color.BLUE}{Color.BOLD}💡 THE ENGINEERING CONCEPT & MENTAL MODEL:{Color.RESET}")
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

    # Normalization helper
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
    prompt_input(f"\n{Color.DIM}Press Enter to return to DSA Lab Studio...{Color.RESET}")

# ==============================================================================
# DSA VIVA GAUNTLET
# ==============================================================================

def mode_dsa_viva():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎓 DSA EXTERNAL EXAMINER VIVA GAUNTLET (3 LIVES) 🎓{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print("Answer the trap questions asked by external lab examiners.\n")

    lives = 3
    score = 0
    questions = list(DSA_VIVA_GAUNTLET)
    random.shuffle(questions)

    for idx, q in enumerate(questions, 1):
        if lives <= 0:
            print(f"\n{Color.RED}{Color.BOLD}💀 YOU FAILED THE VIVA! All 3 lives lost. Back to the lab to study!{Color.RESET}\n")
            break

        print(f"\n{Color.CYAN}{Color.BOLD}[Question {idx}/{len(questions)}] (Lives: {'❤️ ' * lives}){Color.RESET}")
        print(f"{Color.BOLD}{q['q']}{Color.RESET}\n")
        for opt in q["options"]:
            print(f"  {opt}")

        ans = prompt_input("\nYour Answer [A / B / C / D]: ").strip().upper()

        if ans == q["ans"]:
            anim_correct()
            score += 10
            print(f"{Color.GREEN}{q['praise']}{Color.RESET}")
        else:
            anim_wrong()
            lives -= 1
            print(f"{Color.RED}{q['roast']}{Color.RESET}")
            print(f"{Color.YELLOW}💡 Examiner Tip: {q['tip']}{Color.RESET}")

        time.sleep(0.5)

    print(f"\n{Color.CYAN}===================================================={Color.RESET}")
    print(f"  Viva Complete! Final Score: {Color.BOLD}{score} Points{Color.RESET}")
    print(f"{Color.CYAN}===================================================={Color.RESET}\n")
    prompt_input("Press Enter to return...")

# ==============================================================================
# DSA LAB STUDIO MAIN MENU
# ==============================================================================

def mode_dsa_studio():
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}================================================================================{Color.RESET}")
        print(f"  🌳 DSA LAB STUDIO: 1BCSL306 (VTU 2025 Scheme — 12 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}================================================================================{Color.RESET}\n")
        print(f"  {Color.YELLOW}[V1]{Color.RESET} 📦 Interactive Stack Visualizer (Push, Pop, Overflow)")
        print(f"  {Color.YELLOW}[V2]{Color.RESET} 🔗 Interactive Linked List Visualizer (Pointers, Head, Traversal)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 External Examiner DSA Viva Gauntlet (3 Lives)")
        print(f"  {Color.CYAN}------------------------------------------------------------------------------{Color.RESET}")
        print(f"  {Color.BOLD}PART A: FIXED EXPERIMENTS{Color.RESET}")
        for i in range(6):
            exp = DSA_EXPERIMENTS[i]
            print(f"  {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.BOLD}PART B: OPEN-ENDED EXPERIMENTS{Color.RESET}")
        for i in range(6, 12):
            exp = DSA_EXPERIMENTS[i]
            print(f"  {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select an experiment [01 - 12, V1, V2, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "V1":
            visualizer_stack()
        elif choice == "V2":
            visualizer_linked_list()
        elif choice == "VG":
            mode_dsa_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 12:
                run_experiment_lab(DSA_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)

