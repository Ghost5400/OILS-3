"""
arcade.dsa.studio — DSA Lab Studio (1BCSL306 — 12 Experiments, VTU 2025 Scheme).
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

DSA_DISASTER_SCENARIOS = [
    {
        "title": "🚨 DISASTER 1: The 2:00 AM Segfault on Single-Node Deletion",
        "story": "You are presenting your Singly Linked List to the examiner. With an evil smile, the examiner asks you to create a list with just ONE student and select 'Delete from End'.\n\nYou press Enter, and BAM!\n\033[91mSegmentation fault (core dumped)\033[0m\nYour screen freezes and the examiner reaches for their red pen!",
        "prompt": "Why did the deletion crash on a single-node list?",
        "choices": [
            "Your while loop did 'while (p->next->next != NULL)' without checking if 'p->next' was NULL first! Dereferencing NULL->next crashed the CPU.",
            "Linux GCC does not support deleting memory on Tuesdays.",
            "You used 'scanf' instead of 'gets_s'.",
            "You forgot to include <math.h> for pointer calculations."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In a 1-node list, head->next is NULL. Checking head->next->next is an illegal memory access on NULL, triggering instant SIGSEGV!"
    },
    {
        "title": "🚨 DISASTER 2: The Infinite Modulo Loop in Circular Queue",
        "story": "Your Circular Queue accepted the first 3 characters fine. But when the queue wrapped around, your program locked up at 100% CPU utilization and stopped responding to keyboard input!",
        "prompt": "What algorithmic blunder caused the circular queue to freeze?",
        "choices": [
            "You wrote '(rear + 1) / MAX' instead of '(rear + 1) % MAX' (integer division instead of modulo remainder), keeping rear stuck at 0 forever!",
            "You declared the queue array as 'char' instead of 'int'.",
            "Circular queues require dynamic memory allocation via calloc().",
            "Modulo operator only works on floating point numbers in C."
        ],
        "ans_idx": 1,
        "reaction": "NAILED IT! Modulo remainder (%) is required for wrapping around. Integer division (/) calculates quotient, collapsing rear to 0 and trapping the while loop!"
    },
    {
        "title": "🚨 DISASTER 3: The Valgrind Memory Leak Nightmare",
        "story": "Your Polynomial Addition program calculated 8x^3 + 4x^2 + 2x + 3 correctly. But the external examiner runs:\n  valgrind --leak-check=full ./poly\n\nValgrind reports in blazing red:\n\033[91mLEAK SUMMARY: definitely lost: 1,024 bytes in 16 blocks\033[0m!",
        "prompt": "What did you forget to do before the program exited?",
        "choices": [
            "You calculated POLYSUM but never traversed the circular linked lists to free() each allocated term node and header node!",
            "You used malloc() instead of realloc().",
            "Circular linked list headers cannot be freed by modern OS kernels.",
            "You passed the pointers by value instead of double pointers."
        ],
        "ans_idx": 1,
        "reaction": "SPOT ON! Every malloc() MUST have a matching free(). For a circular list, you must traverse until p == head, freeing each node along the way."
    },
    {
        "title": "🚨 DISASTER 4: The Dangling Pointer Zombie Dereference",
        "story": "To save memory in your Binary Search Tree, you called:\n  free(root);\nAnd on the very next line you wrote:\n  printf(\"%d\", root->data);\n\nThe examiner stares at you and taps the desk with a pen.",
        "prompt": "What catastrophic bug did you just commit?",
        "choices": [
            "Use-After-Free / Dangling Pointer! Memory was already handed back to the OS; reading root->data is undefined behavior.",
            "Stack overflow condition.",
            "A syntax error caught by the preprocessor.",
            "Memory thrashing."
        ],
        "ans_idx": 1,
        "reaction": "BINGO! Calling free(root) does not erase the address inside 'root'. It creates a Dangling Pointer. Always set root = NULL after free()!"
    },
    {
        "title": "🚨 DISASTER 5: The Infix-to-Postfix Stack Overflow Disaster",
        "story": "You tested 'A + B * C' and it worked. Then the examiner typed an expression with 20 nested brackets: '((((...A+B...))))'. Your stack immediately crashed!",
        "prompt": "What boundary check was missing in push()?",
        "choices": [
            "You did not check 'if (top == MAX - 1)' before incrementing top, corrupting adjacent program memory on deep bracket nesting!",
            "Parentheses cannot be stored in char arrays.",
            "Operator precedence only supports up to 3 levels in computer science.",
            "You need to use a linked list because arrays cannot store characters."
        ],
        "ans_idx": 1,
        "reaction": "CORRECT! Always enforce overflow guards: 'if (top >= MAX - 1) { report_overflow(); return; }'."
    },
    {
        "title": "🚨 DISASTER 6: The Hash Table Infinite Linear Probe Lockup",
        "story": "You have a Hash Table of size 17. You insert 17 employees. Then you search for an employee that doesn't exist. The terminal completely hangs and never returns!",
        "prompt": "Why did linear probing loop indefinitely during search on a full table?",
        "choices": [
            "Linear probing stops searching ONLY when it finds an EMPTY slot. Since the table was 100% full, it had zero EMPTY slots and looped in an endless circle!",
            "Employee number modulo 17 returned a negative index.",
            "The hash function corrupted the CPU registers.",
            "Linear probing cannot be used with prime table sizes."
        ],
        "ans_idx": 1,
        "reaction": "BRILLIANT! If load factor reaches 1.0 (no EMPTY slots), linear probing will spin forever unless you limit the loop to TABLE_SIZE iterations!"
    },
    {
        "title": "🚨 DISASTER 7: The Graph DFS Infinite Cycle Loop",
        "story": "You built a road map between City A, City B, and City C where roads form a triangle (A-B, B-C, C-A). You run DFS from City A to check connectivity, but your program crashes with a Stack Overflow due to infinite recursive calls!",
        "prompt": "What crucial data structure flag did you fail to check?",
        "choices": [
            "You forgot to check 'if (!visited[v])' before recurring, causing DFS to cycle endlessly A -> B -> C -> A -> B -> C...",
            "Graphs cannot have cycles in C.",
            "Adjacency matrices only support directed trees.",
            "Depth-First Search cannot be implemented with recursion."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY RIGHT! In cyclic graphs, the 'visited[u] = 1' flag is the lifeline that stops traversal from looping indefinitely."
    },
    {
        "title": "🚨 DISASTER 8: The SLL Reverse-Link Orphan Catastrophe",
        "story": "You wanted to insert a new node 'newNode' after node 'p'. You wrote:\n  p->next = newNode;\n  newNode->next = p->next;\n\nSuddenly, your entire list after node 'p' vanished into the void!",
        "prompt": "Why did the rest of the list disappear from memory?",
        "choices": [
            "You overwrote p->next FIRST! Now newNode->next points to itself (infinite circular trap) and the rest of the list was orphaned in RAM!",
            "You forgot to call malloc() twice.",
            "Nodes can only be inserted at the beginning of an SLL.",
            "Singly Linked Lists do not support pointers."
        ],
        "ans_idx": 1,
        "reaction": "GOLDEN RULE OF POINTERS! Always attach the new node's leash FIRST: 'newNode->next = p->next;' and THEN 'p->next = newNode;'!"
    }
]


# Extract DSA experiments & visualizers from dsa_engine

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
                "title": "Dynamic Heap Allocation & NULL Safety",
                "code": "books = (Book *)malloc(bookCount * sizeof(Book));\nif (books == NULL) {\n    printf(\"Memory allocation failed!\\n\");\n    return;\n}",
                "explanation": "malloc() requests contiguous heap memory for N book structs. Always verify books != NULL to prevent fatal segmentation faults when RAM is low."
            },
            {
                "title": "State Transition in issueBook() & returnBook()",
                "code": "if (books[pos].Availability_Status == 0) {\n    printf(\"Cannot issue: Already issued!\\n\");\n} else {\n    books[pos].Availability_Status = 0; // mark issued\n}",
                "explanation": "Availability status acts as a boolean flag (1 = Available, 0 = Issued) guarding against double-issuing or returning books not checked out."
            }
        ],
        "challenge": {
            "prompt": "How do you dynamically allocate heap memory for 'n' structures of type 'Book' to pointer 'books'?",
            "opts": [
                "[A] books = malloc(sizeof(Book));",
                "[B] books = (Book *)malloc(n * sizeof(Book));",
                "[C] books = (Book)malloc(n * sizeof(Book *));",
                "[D] books = malloc(n * Book);"
            ],
            "correct_opt": "B",
            "hint": "Multiply the count 'n' by sizeof(Book) and cast the returned void* pointer to (Book*).",
            "praise": "Spot on! You safely allocated heap memory for all N book structures.",
            "roast": "Careful! Option [A] only allocates space for 1 book instead of N, causing buffer overflows!"
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
                "title": "Metadata Header in Slot 0",
                "code": "a[0].r = rows; a[0].c = cols; a[0].v = count;",
                "explanation": "Slot 0 stores metadata: total rows (.r), total columns (.c), and total non-zero elements (.v). Indices 1..count store actual matrix data."
            },
            {
                "title": "Transposing Sparse Matrix Triplet",
                "code": "for (int col = 0; col < a[0].c; col++)\n    for (int i = 1; i <= a[0].v; i++)\n        if (a[i].c == col) {\n            t[k].r = a[i].c; t[k].c = a[i].r; t[k].v = a[i].v; k++;\n        }",
                "explanation": "Scans column by column from 0 to c-1 so the transposed triplets are automatically created in row-major sorted order."
            }
        ],
        "challenge": {
            "prompt": "In a 3-column triplet array where row 0 holds metadata, what condition verifies matrices A and B have matching dimensions for addition?",
            "opts": [
                "[A] a[0].r == b[0].r && a[0].c == b[0].c",
                "[B] a[0].v == b[0].v",
                "[C] a[1].r == b[1].r && a[1].c == b[1].c",
                "[D] a[0].r == b[0].c && a[0].c == b[0].r"
            ],
            "correct_opt": "A",
            "hint": "Slot 0 stores metadata: .r is total rows and .c is total columns. Both must match.",
            "praise": "Correct! Slot 0 metadata guards against invalid matrix addition.",
            "roast": "Remember that row 0 (.r and .c) stores rows and columns! Row 1 is already data."
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
                "title": "PUSH with Stack Overflow Guard",
                "code": "if (top == capacity - 1) {\n    printf(\"Stack Overflow! Cannot push.\\n\");\n    return;\n}\nstack[++top] = val;",
                "explanation": "Pre-increments top before storing. You must check top == capacity - 1 first, otherwise you will corrupt adjacent stack frame memory."
            },
            {
                "title": "POP with Stack Underflow Guard",
                "code": "if (top == -1) {\n    printf(\"Stack Underflow! Empty stack.\\n\");\n    return -1;\n}\nreturn stack[top--];",
                "explanation": "Checks top == -1 first. If elements exist, returns current top value and post-decrements top pointer back down."
            }
        ],
        "challenge": {
            "prompt": "To push 'val' into an array-based stack 'stack' with top pointer 'top', what is the correct sequence?",
            "opts": [
                "[A] top++; stack[top] = val;",
                "[B] stack[top] = val; top++;",
                "[C] stack[++val] = top;",
                "[D] stack[top--] = val;"
            ],
            "correct_opt": "A",
            "hint": "Pre-increment top first, then store the value at the new top index.",
            "praise": "Clean execution! Pre-incrementing top and then storing is classic LIFO push.",
            "roast": "If you store first and then increment (post-increment), top starts pointing to garbage!"
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
                "title": "Enqueue with Linear Queue Full Guard",
                "code": "if (rear == MAX - 1) {\n    printf(\"Queue Full! (Linear Queue Overflow)\\n\");\n    return;\n}\nif (front == -1) front = 0;\nqueue[++rear] = job;",
                "explanation": "When first item arrives, front moves from -1 to 0. rear increments to accommodate the incoming print job."
            },
            {
                "title": "Dequeue with Single-Job Reset Logic",
                "code": "int job = queue[front];\nif (front == rear) {\n    front = -1; rear = -1; // reset when last item leaves\n} else {\n    front++;\n}\nreturn job;",
                "explanation": "When front == rear, exactly one job remained. After dequeuing it, reset front = rear = -1 to allow fresh reuse of the buffer."
            }
        ],
        "challenge": {
            "prompt": "In a linear printer queue with pointers 'front' and 'rear', which condition indicates the queue is completely empty?",
            "opts": [
                "[A] front == MAX",
                "[B] front == -1 || front > rear",
                "[C] rear == -1 && front == 0",
                "[D] front == rear"
            ],
            "correct_opt": "B",
            "hint": "A linear queue is empty initially when front == -1, or after dequeuing all items when front surpasses rear.",
            "praise": "Spot on! front == -1 or front > rear signifies an empty linear queue.",
            "roast": "When all jobs are printed and removed, front increments past rear. Checking front == -1 alone misses depleted queues!"
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
                "title": "Circular Header Node Initialization",
                "code": "Node* head = (Node*)malloc(sizeof(Node));\nhead->next = head; // Points back to itself!",
                "explanation": "Header node points back to itself when empty. Traversal loops terminate cleanly when p->next returns back to head."
            },
            {
                "title": "Sorted Polynomial Term Insertion & Merging",
                "code": "if (p1->expo == p2->expo) {\n    int sumCoeff = p1->coeff + p2->coeff;\n    if (sumCoeff != 0) insertTerm(head3, sumCoeff, p1->expo);\n    p1 = p1->next; p2 = p2->next;\n}",
                "explanation": "Compares exponents: matching exponents add coefficients; non-matching exponents advance the higher degree term first."
            }
        ],
        "challenge": {
            "prompt": "When creating a Circular Linked List with a header node 'h', how do you make it point to itself initially?",
            "opts": [
                "[A] h->next = NULL;",
                "[B] h->next = h;",
                "[C] h = h->next;",
                "[D] h->next = &h;"
            ],
            "correct_opt": "B",
            "hint": "In a circular list, the last node links back to the header; when empty, the header's next points to itself.",
            "praise": "Perfect circular link! h->next = h makes list traversal loops terminate cleanly when returning to h.",
            "roast": "Setting h->next = NULL turns it into a standard linear list, breaking circular traversal!"
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
                "title": "Level-Order Traversal using Queue (BFS)",
                "code": "enqueue(root);\nwhile (!isQueueEmpty()) {\n    Node* curr = dequeue();\n    printf(\"%d \", curr->data);\n    if (curr->left) enqueue(curr->left);\n    if (curr->right) enqueue(curr->right);\n}",
                "explanation": "FIFO queue processes tree nodes horizontal slice by horizontal slice. Visiting parent schedules children for the next level."
            },
            {
                "title": "Recursive Inorder Traversal (DFS)",
                "code": "void inorder(Node* root) {\n    if (root == NULL) return;\n    inorder(root->left);\n    printf(\"%d \", root->data);\n    inorder(root->right);\n}",
                "explanation": "Left -> Root -> Right. Traverses deepest left subtrees first before printing current node and ascending up."
            }
        ],
        "challenge": {
            "prompt": "In standard binary tree traversals, what is the visit sequence for PREORDER traversal?",
            "opts": [
                "[A] Left -> Root -> Right",
                "[B] Root -> Left -> Right",
                "[C] Left -> Right -> Root",
                "[D] Level by level from top to bottom"
            ],
            "correct_opt": "B",
            "hint": "Pre = Before. The root is visited BEFORE its left and right subtrees.",
            "praise": "Spot on! Preorder is Root -> Left -> Right. Inorder is L->Root->R and Postorder is L->R->Root.",
            "roast": "Remember: Preorder visits the Root FIRST, then Left subtree, then Right subtree!"
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
                "title": "Stack-Based Bracket Validation",
                "code": "if (ch == '(' || ch == '{' || ch == '[') push(ch);\nelse if (ch == ')' || ch == '}' || ch == ']') {\n    if (isEmpty() || !isMatchingPair(pop(), ch)) return 0;\n}",
                "explanation": "Pushes opening brackets. Closing bracket must match the most recently pushed opening bracket popped off the LIFO stack."
            },
            {
                "title": "Operator Precedence & Conversion Loop",
                "code": "while (precedence(stack[top]) >= precedence(token)) {\n    postfix[k++] = pop();\n}\npush(token);",
                "explanation": "Higher or equal precedence operators must be popped to output before pushing the current operator onto the operator stack."
            }
        ],
        "challenge": {
            "prompt": "What is the correct postfix conversion for the infix expression: (A + B) * C ?",
            "opts": [
                "[A] A B + C *",
                "[B] A B C + *",
                "[C] * + A B C",
                "[D] A + B * C"
            ],
            "correct_opt": "A",
            "hint": "Parentheses force (A + B) to evaluate first into 'AB+', which is then multiplied by C giving 'AB+C*'.",
            "praise": "Flawless stack parsing! The parentheses bump '+' precedence above '*'.",
            "roast": "Parentheses force (A + B) to be converted to 'AB+' before multiplying with C!"
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
                "title": "Insert at Front of Singly Linked List",
                "code": "newNode->next = head;\nhead = newNode;",
                "explanation": "Connects newNode's next to old head first, then updates head to point to newNode. O(1) time complexity."
            },
            {
                "title": "Insert After Node 'p' (Preserve Chain)",
                "code": "newNode->next = p->next;\np->next = newNode;",
                "explanation": "CRITICAL ORDER: You must attach newNode to downstream list (p->next) BEFORE modifying p->next, otherwise downstream nodes are leaked!"
            }
        ],
        "challenge": {
            "prompt": "To insert a new node 'newNode' immediately after node 'p' in an SLL, what is the correct pointer assignment order?",
            "opts": [
                "[A] p->next = newNode; newNode->next = p->next;",
                "[B] newNode->next = p->next; p->next = newNode;",
                "[C] newNode = p->next; p = newNode->next;",
                "[D] p->next = newNode->next; newNode = p;"
            ],
            "correct_opt": "B",
            "hint": "Always connect the new node downstream first (newNode->next = p->next) before breaking p's current link!",
            "praise": "Golden rule of pointers! You connected downstream before overwriting p->next, preventing orphan memory leaks.",
            "roast": "DISASTER! If you assign p->next = newNode first, you lose the entire downstream list forever!"
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
                "title": "Modulo Hash Function & Direct Slot Probe",
                "code": "int index = partId % TABLE_SIZE;\nwhile (table[index].status == OCCUPIED) {\n    index = (index + 1) % TABLE_SIZE; // Linear probing\n}",
                "explanation": "Computes slot index in range [0, TABLE_SIZE-1]. If collision occurs, steps sequentially through subsequent slots using modulo wrap-around."
            },
            {
                "title": "Tombstone (DELETED) Slot Handling",
                "code": "table[index].status = DELETED; // Tombstone marker",
                "explanation": "Deleted entries cannot be set to EMPTY (-1) because that would prematurely stop search probe chains for keys inserted after collisions."
            }
        ],
        "challenge": {
            "prompt": "In linear probing with collision resolution, when does a search for key K conclude that K is NOT in the table?",
            "opts": [
                "[A] When it encounters an EMPTY slot (-1)",
                "[B] When it visits the table midpoint",
                "[C] Only after checking all slots in the entire table",
                "[D] When it encounters any OCCUPIED slot"
            ],
            "correct_opt": "A",
            "hint": "Because linear probing places keys into the first available slot, hitting a truly empty slot means the key was never inserted.",
            "praise": "Spot on! An EMPTY slot terminates the probe chain immediately with O(1) average time.",
            "roast": "If a key were in the table, it would have taken that empty slot! Encountering an empty slot proves it does not exist."
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
                "title": "Recursive BST Node Insertion",
                "code": "if (root == NULL) return createNode(val);\nif (val < root->data) root->left = insert(root->left, val);\nelse if (val > root->data) root->right = insert(root->right, val);\nreturn root;",
                "explanation": "Enforces BST invariant: smaller values route to left subtree, larger values route to right subtree. Duplicates are rejected."
            },
            {
                "title": "Inorder Traversal for Sorted Output",
                "code": "void inorder(BSTNode* root) {\n    if (root == NULL) return;\n    inorder(root->left);\n    printf(\"%d \", root->data);\n    inorder(root->right);\n}",
                "explanation": "Because Left < Root < Right in any valid BST, visiting Left then Root then Right yields elements in strictly ascending sorted order."
            }
        ],
        "challenge": {
            "prompt": "Which tree traversal on a Binary Search Tree (BST) is guaranteed to visit all elements in strictly ascending sorted order?",
            "opts": [
                "[A] Preorder Traversal",
                "[B] Inorder Traversal (Left -> Root -> Right)",
                "[C] Postorder Traversal",
                "[D] Level-Order Traversal"
            ],
            "correct_opt": "B",
            "hint": "BST property: Left < Root < Right. Visiting Left, then Root, then Right yields ascending order.",
            "praise": "Spot on! Inorder traversal of any valid BST always prints items in non-decreasing sorted order.",
            "roast": "By BST definition, Left < Root < Right, so visiting Left then Root then Right (Inorder) is the only sorted traversal!"
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
                "title": "Prime Table Size (17) Hash Calculation",
                "code": "int hashIndex = empId % 17;\nif (hashIndex < 0) hashIndex += 17;",
                "explanation": "Table size 17 is prime, which minimizes clustering when employee IDs share common factors or sequential increments."
            },
            {
                "title": "Linear Collision Resolution with Full-Table Guard",
                "code": "int count = 0;\nwhile (table[hashIndex].occupied && count < 17) {\n    hashIndex = (hashIndex + 1) % 17;\n    count++;\n}",
                "explanation": "Maintains a count of examined slots. If count reaches 17, the table is completely full and prevents infinite while loop freeze."
            }
        ],
        "challenge": {
            "prompt": "Using the division hash function h(key) = key % TABLE_SIZE with TABLE_SIZE = 17, what is the initial hash index for Employee ID 122?",
            "opts": [
                "[A] 122 % 17 = 3",
                "[B] 122 % 17 = 7",
                "[C] 122 % 17 = 11",
                "[D] 122 % 17 = 5"
            ],
            "correct_opt": "A",
            "hint": "17 * 7 = 119. So 122 - 119 = 3.",
            "praise": "Math wizard! 17 * 7 = 119, leaving a remainder of 3. Slot 3 is probed first.",
            "roast": "17 goes into 122 seven times (17 * 7 = 119), with remainder 3!"
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
                "title": "Adjacency Matrix Representation of Cities",
                "code": "int adj[MAX][MAX] = {0};\nadj[u][v] = 1; adj[v][u] = 1; // Bidirectional road",
                "explanation": "2D matrix stores direct connectivity. In an undirected road network, connecting city U to V automatically connects V back to U."
            },
            {
                "title": "Recursive DFS with Visited Array (Cycle Guard)",
                "code": "visited[u] = 1; // Mark current city\nfor (int v = 0; v < n; v++) {\n    if (adj[u][v] && !visited[v]) dfs(v);\n}",
                "explanation": "visited[u] = 1 tracks traversed cities. Without this mark, recursive DFS would bounce back and forth between adjacent cities forever."
            }
        ],
        "challenge": {
            "prompt": "Why is a boolean 'visited' array mandatory when performing Depth-First Search (DFS) on an undirected city graph?",
            "opts": [
                "[A] To calculate the shortest driving distance between cities",
                "[B] To prevent infinite recursion and stack overflow caused by cycles",
                "[C] To sort city names alphabetically",
                "[D] To count the number of edges in the graph"
            ],
            "correct_opt": "B",
            "hint": "In an undirected graph, city A connects to city B and B connects back to A. Without marking visited, DFS bounces infinitely.",
            "praise": "Bullseye! 'visited[city] = 1' breaks graph cycles and stops stack overflow crashes dead in their tracks.",
            "roast": "Undirected edges (A <-> B) form cycles! Without 'visited', your recursive DFS bounces back and forth until the call stack blows up."
        }
    }
]
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
                print(f"  {Color.DIM}Explanation: Array indices 0 to {cap-1} are occupied. Cannot insert without overwriting.{Color.RESET}")
                prompt_input("Press Enter to continue...")
            else:
                val = prompt_input("Enter integer to push: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    int_val = int(val)
                    print(f"\n  {Color.YELLOW}Step 1: Check boundary{Color.RESET} -> top < MAX-1 ({len(stack)-1} < {cap-1}) [OK]")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                    print(f"  {Color.YELLOW}Step 2: Advance pointer{Color.RESET} -> top = top + 1 (new top index: {len(stack)})")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                    print(f"  {Color.YELLOW}Step 3: Write memory{Color.RESET}   -> stack[{len(stack)}] = {int_val}")
                    stack.append(int_val)
                    time.sleep(0.4)
                else:
                    print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                    time.sleep(0.8)
        elif cmd == "2":
            if not stack:
                print(f"{Color.RED}🚨 STACK UNDERFLOW! Stack is empty.{Color.RESET}")
                print(f"  {Color.DIM}Explanation: top == -1. There are no elements in memory to pop.{Color.RESET}")
                prompt_input("Press Enter to continue...")
            else:
                popped = stack[-1]
                print(f"\n  {Color.YELLOW}Step 1: Check boundary{Color.RESET} -> top >= 0 ({len(stack)-1} >= 0) [OK]")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 2: Read data element{Color.RESET} -> item = stack[top] (retrieved: {popped})")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 3: Decrement pointer{Color.RESET} -> top = top - 1 (freed slot {len(stack)-1})")
                stack.pop()
                time.sleep(0.4)
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
                int_val = int(val)
                print(f"\n  {Color.YELLOW}Step 1: Allocate Heap Node{Color.RESET} -> new_node = malloc(sizeof(Node)); new_node->data = {int_val};")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 2: Wire next pointer{Color.RESET}  -> new_node->next = HEAD (points to previous first node)")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 3: Update HEAD{Color.RESET}        -> HEAD = new_node (new node is now the list entry point)")
                nodes.insert(0, int_val)
                time.sleep(0.4)
        elif cmd == "2":
            val = prompt_input("Enter integer for new node: ").strip()
            if val.isdigit():
                int_val = int(val)
                print(f"\n  {Color.YELLOW}Step 1: Allocate Heap Node{Color.RESET} -> new_node = malloc(sizeof(Node)); new_node->data = {int_val}; new_node->next = NULL;")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 2: Traverse to Tail{Color.RESET}   -> while (temp->next != NULL) temp = temp->next;")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 3: Attach to Tail{Color.RESET}     -> temp->next = new_node;")
                nodes.append(int_val)
                time.sleep(0.4)
        elif cmd == "3":
            if not nodes:
                print(f"{Color.RED}List is empty. Nothing to delete!{Color.RESET}")
                time.sleep(0.8)
            else:
                removed = nodes[0]
                print(f"\n  {Color.YELLOW}Step 1: Save Target Pointer{Color.RESET} -> temp = HEAD (storing address of node {removed})")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 2: Advance HEAD{Color.RESET}        -> HEAD = HEAD->next (moving list entry to 2nd node)")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"  {Color.YELLOW}Step 3: Reclaim Memory{Color.RESET}      -> free(temp) (deallocates heap memory, avoids memory leak!)")
                nodes.pop(0)
                time.sleep(0.4)
        elif cmd in ("0", "b", "exit"):
            break

# ==============================================================================
# EXPERIMENT RUNNER & CODE CHALLENGE ENGINE
# ==============================================================================

def mode_dsa_disaster():
    clear_screen()
    print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║        🚨 MODE: DSA LAB DISASTER RECOVERY (8 REAL EMERGENCIES)     ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_slow("These are actual bugs and pointer disasters students encounter in lab exams.", 0.012, Color.CYAN)
    print_slow("Identify the root cause and save your program before the system crashes!\n", 0.012)

    score = 0
    scenarios = list(DSA_DISASTER_SCENARIOS)
    random.shuffle(scenarios)
    for i, s in enumerate(scenarios, 1):
        clear_screen()
        print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║     🚨 DSA EMERGENCY {i}/{len(scenarios)}: EXAM DISASTER IN PROGRESS          ║")
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

        spinner("Analyzing heap state & pointer registers", duration=0.6, color=Color.RED)

        if pick == s["ans_idx"]:
            anim_correct()
            _award_xp(150, "disaster averted")
            _unlock_badge("dsa_doctor")
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
    print(f"  DSA Disaster Recovery Complete! Score: {score}/{len(scenarios)*150}")
    print(f"{'═'*51}{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def run_dsa_experiment_lab(exp):
    base_dir = PROJECT_ROOT
    source_path = os.path.join(base_dir, exp["file"])

    # Stage 1: The Big Picture & Intuition
    clear_screen()
    print()
    _show_session_header(subject="dsa")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  🌳 EXPERIMENT {exp['num']:02d} ({exp['part']}): {exp['title']:<52} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()
    print(f"{Color.YELLOW}{Color.BOLD}[Stage 1/4] 💡 THE BIG PICTURE & MENTAL MODEL:{Color.RESET}")
    print()
    print_slow(f"  {exp['concept']}", 0.008, Color.WHITE)
    print()
    print(f"{Color.CYAN}{Color.BOLD}🎯 VTU Lab Requirement:{Color.RESET}")
    print(f"  {exp['problem']}")
    print()
    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the complete C code first...{Color.RESET}")

    # Stage 2: Complete Source Code First
    clear_screen()
    print()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  📄 [Stage 2/4] COMPLETE VERIFIED C PROGRAM CODE                              ║")
    print(f"║  Source: {exp['file']:<68} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    funny_spinners = [
        "Consulting Stack Overflow (just kidding, we have the code)",
        "malloc()-ing your brain cells for maximum absorption",
        "Asking ChatGPT... nah, we wrote this ourselves",
        "Garbage collecting wrong assumptions",
        "Compiling elegance into your neurons",
    ]
    spinner(random.choice(funny_spinners), duration=0.5, color=Color.GREEN)
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
    _show_session_header(subject="dsa")

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
            "Analyzing your code selection",
            "Consulting the C standard committee",
            "Checking pointer arithmetic sanity",
            "Running valgrind on your answer",
        ]), duration=0.6, color=Color.CYAN)

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
    exp_id = f"DSA-{exp['num']}"
    if exp_id not in _SESSION["experiments_done"]:
        _SESSION["experiments_done"].append(exp_id)
        _save_to_local_db()

    print(f"{Color.DIM}File location: {exp['file']}{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to DSA Lab Studio...{Color.RESET}")


def mode_dsa_viva():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎓 DSA LAB VIVA PREP & CONCEPT MASTERY (1BCSL306) 🎓{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}\n")
    print("  Stress-free practice with Socratic hints and examiner expectations.\n")

    score = 0
    questions = list(DSA_VIVA_GAUNTLET)
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
                _award_xp(10, "viva correct")
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


def mode_dsa_studio():
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  🌳 DSA LAB STUDIO: 1BCSL306 (VTU 2025 Scheme — 12 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="dsa")
        print(f"  {Color.YELLOW}[V1]{Color.RESET} 📦 Interactive Stack Visualizer (Push, Pop, Overflow)")
        print(f"  {Color.YELLOW}[V2]{Color.RESET} 🔗 Interactive Linked List Visualizer (Pointers, Head, Traversal)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨 DSA Lab Disaster Recovery (8 Real Exam Emergencies)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 External Examiner DSA Viva Gauntlet (3 Lives)")
        print(f"  {Color.CYAN}{'─'*78}{Color.RESET}")
        print(f"  {Color.BOLD}PART A: FIXED EXPERIMENTS{Color.RESET}")
        for i in range(6):
            exp = DSA_EXPERIMENTS[i]
            done = "✅" if f"DSA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.BOLD}PART B: OPEN-ENDED EXPERIMENTS{Color.RESET}")
        for i in range(6, 12):
            exp = DSA_EXPERIMENTS[i]
            done = "✅" if f"DSA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        # Streak motivator
        streak = _SESSION["streak"]
        if streak >= 3:
            print(f"\n  {Color.RED}{Color.BOLD}🔥 You're on a {streak}-streak! Don't stop now!{Color.RESET}")
        elif streak >= 1:
            print(f"\n  {Color.YELLOW}⚡ Streak: {streak} — keep it going!{Color.RESET}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 12, V1, V2, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "V1":
            visualizer_stack()
        elif choice == "V2":
            visualizer_linked_list()
        elif choice == "DR":
            mode_dsa_disaster()
        elif choice == "VG":
            mode_dsa_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 12:
                run_dsa_experiment_lab(DSA_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)

