"""
arcade.dsa.experiments_data — 12 VTU DSA Lab Experiments (1BCSL306, 2025 Scheme).
Each experiment features detailed 3-part structured block breakdowns:
  1) Block Purpose & Role
  2) Inside the Block (Components, Variables & Logic)
  3) Step-by-Step Execution Flow
"""

DSA_EXPERIMENTS = [
    {
        "num": 1,
        "part": "A",
        "title": "Library Book Management (Structures & Dynamic Memory)",
        "file": "dsa-lab/programs/lab01_library_management.c",
        "concept": "Dynamic heap allocation using malloc(N * sizeof(Book)). Pointers allow allocating exact bytes at runtime rather than fixed array sizes.",
        "problem": "Define Book structure (Book_ID, Title, Author, Price, Status). Dynamically allocate memory for N books on the heap using malloc(). Implement create(), display(), search(), issueBook(), and returnBook().",
        "blocks": [
            {
                "title": "Book Structure & Dynamic Heap Allocation",
                "code": "typedef struct {\n    int Book_ID;\n    char Title[50];\n    char Author[50];\n    float Price;\n    int Availability_Status; // 1 = Available, 0 = Issued\n} Book;\n\nbooks = (Book *)malloc(bookCount * sizeof(Book));\nif (books == NULL) {\n    printf(\"Memory allocation failed!\\n\");\n    return;\n}",
                "purpose": "Defines the user-defined Book entity type and requests contiguous heap RAM for N book structs at runtime.",
                "inside": [
                    "`struct Book`: Bundles heterogeneous attributes (integer ID, string Title/Author, float Price, and boolean Availability flag) into a single memory block.",
                    "`malloc(bookCount * sizeof(Book))`: Requests `bookCount * sizeof(Book)` bytes from the OS Heap. Cast `(Book *)` converts void* pointer to Book pointer.",
                    "`if (books == NULL)`: Critical NULL safety guard. If the operating system runs out of RAM, malloc returns NULL. Dereferencing NULL causes an immediate OS Segmentation Fault (SIGSEGV)."
                ],
                "flow": [
                    "Step 1: User specifies number of books (`bookCount`).",
                    "Step 2: `sizeof(Book)` calculates total byte footprint of one struct.",
                    "Step 3: `malloc()` requests memory block on the heap and assigns address to pointer `books`.",
                    "Step 4: Pointer checked against NULL to verify OS allocation succeeded."
                ]
            },
            {
                "title": "Linear Search & Status Mutation (issueBook & returnBook)",
                "code": "int found = 0;\nfor (int i = 0; i < bookCount; i++) {\n    if (books[i].Book_ID == searchID) {\n        found = 1;\n        if (books[i].Availability_Status == 0) {\n            printf(\"Book already issued!\\n\");\n        } else {\n            books[i].Availability_Status = 0;\n            printf(\"Book %d successfully issued!\\n\", searchID);\n        }\n        break;\n    }\n}",
                "purpose": "Searches the heap array for a matching Book_ID and atomically mutates its boolean availability flag.",
                "inside": [
                    "`for loop`: Sequentially inspects each struct index from 0 to `bookCount - 1` with O(N) complexity.",
                    "`books[i].Book_ID == searchID`: Direct member access via array indexing offset `*(books + i)`.",
                    "`Availability_Status = 0`: State transition indicating the book is checked out. Guards against double-issuing.",
                    "`break`: Halts search loop immediately once target book is located, saving CPU cycles."
                ],
                "flow": [
                    "Step 1: Loop reads index `i` and compares `books[i].Book_ID` with target `searchID`.",
                    "Step 2: If found, checks current status flag: 1 (Available) or 0 (Issued).",
                    "Step 3: If 1, flips flag to 0 and logs confirmation; if 0, notifies user book is unavailable.",
                    "Step 4: Exits loop immediately via `break`."
                ]
            },
            {
                "title": "Safe Deallocation & Memory Leak Prevention",
                "code": "free(books);\nbooks = NULL;",
                "purpose": "Releases the allocated heap memory back to the operating system when the program terminates or resets.",
                "inside": [
                    "`free(books)`: Informs the OS memory manager that the heap chunk pointed to by `books` is no longer needed.",
                    "`books = NULL`: Critical safety measure! Calling free does NOT erase the address stored in `books`. Setting `books = NULL` prevents Dangling Pointer dereference bugs."
                ],
                "flow": [
                    "Step 1: `free(books)` releases heap block.",
                    "Step 2: Pointer variable `books` set to NULL (0x0) so any subsequent access fails safely."
                ]
            }
        ],
        "challenge": {
            "prompt": "What catastrophic bug happens if you call free(books) but later write 'printf(\"%s\", books[0].Title)'?",
            "opts": [
                "A) It compiles and runs fine because free() is only a suggestion to the CPU.",
                "B) Use-After-Free (Dangling Pointer) undefined behavior — reading deallocated RAM can cause crashes or security exploits.",
                "C) Stack overflow error.",
                "D) The operating system automatically re-allocates the memory."
            ],
            "correct_opt": "B",
            "hint": "free() marks RAM as available to other programs. Reading it after free is undefined behavior.",
            "praise": "Exactly right! Always set pointers to NULL after freeing to eliminate dangling pointers.",
            "roast": "Incorrect. Calling free releases memory to the OS. Accessing it afterward is a Dangling Pointer bug!"
        }
    },
    {
        "num": 2,
        "part": "A",
        "title": "Sparse Matrix Triplet Representation, Addition & Transpose",
        "file": "dsa-lab/programs/lab02_sparse_matrix.c",
        "concept": "A sparse matrix is one where most elements are zero. Triplet representation stores only non-zero elements as (row, col, value), reducing space from O(M*N) to O(non_zeros).",
        "problem": "Represent two sparse matrices in triplet form (row, column, value) where element [0] stores matrix metadata (rows, columns, total non-zeros). Perform addition and transpose.",
        "blocks": [
            {
                "title": "Triplet Structure & Header Metadata",
                "code": "typedef struct {\n    int row;\n    int col;\n    int val;\n} Term;\n\nTerm a[MAX], b[MAX], c[MAX];\n// a[0] stores: a[0].row = total_rows, a[0].col = total_cols, a[0].val = total_non_zeros",
                "purpose": "Defines the 3-tuple structure and uses the 0th element as a header storing matrix dimensions and count of non-zero entries.",
                "inside": [
                    "`struct Term`: Stores coordinate `(row, col)` and the non-zero integer `val`.",
                    "`a[0] Header`: Self-describing convention. `a[0].row` = rows in original matrix, `a[0].col` = cols in original matrix, `a[0].val` = number of non-zero terms stored from `a[1]` to `a[k]`."
                ],
                "flow": [
                    "Step 1: Original matrix dimensions entered into `a[0].row` and `a[0].col`.",
                    "Step 2: Non-zero values entered into subsequent indices `a[1]`, `a[2]`, ...",
                    "Step 3: Total non-zero count saved in `a[0].val`."
                ]
            },
            {
                "title": "Two-Pointer Triplet Addition Comparison",
                "code": "int i = 1, j = 1, k = 1;\nwhile (i <= a[0].val && j <= b[0].val) {\n    if (a[i].row == b[j].row && a[i].col == b[j].col) {\n        c[k] = a[i];\n        c[k].val = a[i].val + b[j].val;\n        i++; j++; k++;\n    } else if (a[i].row < b[j].row || (a[i].row == b[j].row && a[i].col < b[j].col)) {\n        c[k++] = a[i++];\n    } else {\n        c[k++] = b[j++];\n    }\n}",
                "purpose": "Merges two sorted triplet arrays into a sum triplet array in O(non-zero A + non-zero B) time.",
                "inside": [
                    "`i, j, k`: Pointer indices for matrix A, matrix B, and Result matrix C.",
                    "`Same coordinate check`: If `row` and `col` match, sum the values (`a[i].val + b[j].val`) into `c[k]` and advance both `i` and `j`.",
                    "`Lexicographical order comparison`: If `a[i]` precedes `b[j]` in row-major order, copy `a[i]` and advance `i`; otherwise copy `b[j]` and advance `j`."
                ],
                "flow": [
                    "Step 1: Compare coordinates of `a[i]` and `b[j]`.",
                    "Step 2: If identical coordinate, add values into `c[k]` and increment both pointers.",
                    "Step 3: If different, insert the term with smaller `(row, col)` into `c[k]`.",
                    "Step 4: Copy any remaining terms from A or B after loop ends."
                ]
            }
        ],
        "challenge": {
            "prompt": "In standard VTU sparse matrix triplet format, what does the 0th element (matrix[0]) store?",
            "opts": [
                "A) The first non-zero element of the matrix.",
                "B) Total rows, total columns, and total count of non-zero elements.",
                "C) The determinant of the matrix.",
                "D) The memory address of the operating system."
            ],
            "correct_opt": "B",
            "hint": "matrix[0].row = M, matrix[0].col = N, matrix[0].val = non-zero count.",
            "praise": "Spot on! The 0th entry is the self-describing header element.",
            "roast": "matrix[0] is the header storing total rows, columns, and non-zero count!"
        }
    },
    {
        "num": 3,
        "part": "A",
        "title": "Stack Operations Using an Array (PUSH, POP, PEEK)",
        "file": "dsa-lab/programs/lab03_stack_operations.c",
        "concept": "LIFO (Last-In, First-Out) linear data structure. All insertions (push) and deletions (pop) occur at a single end called 'top'.",
        "problem": "Implement a Stack of integers using a 1D array of fixed size MAX. Support PUSH, POP, PEEK, and DISPLAY operations with boundary overflow and underflow checks.",
        "blocks": [
            {
                "title": "PUSH Operation & Overflow Boundary Check",
                "code": "void push(int val) {\n    if (top == MAX - 1) {\n        printf(\"Stack Overflow! Cannot push %d\\n\", val);\n        return;\n    }\n    top = top + 1;\n    stack[top] = val;\n    printf(\"%d pushed to stack\\n\", val);\n}",
                "purpose": "Inserts an element onto the top of the stack after verifying capacity remains.",
                "inside": [
                    "`if (top == MAX - 1)`: Overflow condition check. In a 0-indexed array of size MAX, the highest valid index is `MAX - 1`. Pushing when `top == MAX - 1` corrupts adjacent RAM.",
                    "`top = top + 1`: Pre-increments pointer to claim the next available memory slot.",
                    "`stack[top] = val`: Writes value into newly claimed slot."
                ],
                "flow": [
                    "Step 1: Check boundary condition (`top == MAX - 1`). If true, abort.",
                    "Step 2: Advance pointer: `top = top + 1`.",
                    "Step 3: Assign value: `stack[top] = val`."
                ]
            },
            {
                "title": "POP Operation & Underflow Boundary Check",
                "code": "int pop() {\n    if (top == -1) {\n        printf(\"Stack Underflow! Stack is empty\\n\");\n        return -1;\n    }\n    int item = stack[top];\n    top = top - 1;\n    return item;\n}",
                "purpose": "Removes and returns the most recently inserted element from the stack.",
                "inside": [
                    "`if (top == -1)`: Underflow condition check. When stack has 0 elements, `top` is initialized to -1. Popping at -1 leads to out-of-bounds negative indexing `stack[-1]`.",
                    "`item = stack[top]`: Reads data element currently at the top of the stack.",
                    "`top = top - 1`: Decrements top pointer, logically freeing the slot."
                ],
                "flow": [
                    "Step 1: Check boundary condition (`top == -1`). If true, abort.",
                    "Step 2: Store value at `stack[top]` in local variable `item`.",
                    "Step 3: Decrement pointer: `top = top - 1`.",
                    "Step 4: Return `item`."
                ]
            }
        ],
        "challenge": {
            "prompt": "What is the initial value of 'top' in a 0-indexed array stack when it is empty?",
            "opts": [
                "A) 0",
                "B) -1",
                "C) MAX",
                "D) NULL"
            ],
            "correct_opt": "B",
            "hint": "Since index 0 is a valid slot, empty is represented by -1 so that top+1 becomes index 0.",
            "praise": "Correct! top = -1 represents an empty stack.",
            "roast": "In a 0-indexed array, index 0 is valid! Therefore empty MUST be top = -1."
        }
    },
    {
        "num": 4,
        "part": "A",
        "title": "Printer Queue Simulation Using an Array",
        "file": "dsa-lab/programs/lab04_printer_queue.c",
        "concept": "FIFO (First-In, First-Out) linear structure. Elements are inserted at REAR and removed from FRONT. Circular queues resolve the 'false overflow' limitation of linear arrays.",
        "problem": "Simulate a printer job queue using a Circular Queue of size MAX. Implement insert (enqueue), delete (dequeue), and display using modulo wrap-around arithmetic.",
        "blocks": [
            {
                "title": "Modulo Ring Enqueue & Circular Full Check",
                "code": "void enqueue(int job_id) {\n    if ((rear + 1) % MAX == front) {\n        printf(\"Queue Full! (Circular Overflow)\\n\");\n        return;\n    }\n    if (front == -1) {\n        front = 0;\n    }\n    rear = (rear + 1) % MAX;\n    queue[rear] = job_id;\n}",
                "purpose": "Inserts a print job at the next circular rear index using modulo arithmetic.",
                "inside": [
                    "`(rear + 1) % MAX == front`: The circular queue full condition. If incrementing rear lands on front, the ring is full.",
                    "`front == -1`: First element insertion case. Sets `front = 0`.",
                    "`rear = (rear + 1) % MAX`: Modulo operator wraps index from `MAX - 1` back to `0`, reusing slots freed by dequeues."
                ],
                "flow": [
                    "Step 1: Check if `(rear + 1) % MAX == front`. If true, queue is full.",
                    "Step 2: If queue was empty (`front == -1`), set `front = 0`.",
                    "Step 3: Advance rear circularly: `rear = (rear + 1) % MAX`.",
                    "Step 4: Store `job_id` at `queue[rear]`."
                ]
            },
            {
                "title": "Modulo Ring Dequeue & Reset Condition",
                "code": "int dequeue() {\n    if (front == -1) {\n        printf(\"Queue Empty! (Underflow)\\n\");\n        return -1;\n    }\n    int job = queue[front];\n    if (front == rear) {\n        // Last remaining element consumed\n        front = -1;\n        rear = -1;\n    } else {\n        front = (front + 1) % MAX;\n    }\n    return job;\n}",
                "purpose": "Removes and returns the print job at the front of the queue, resetting pointers when empty.",
                "inside": [
                    "`front == -1`: Underflow check indicating no jobs waiting.",
                    "`front == rear`: Critical boundary check. When front equals rear, exactly one job remains. After removing it, reset both `front = -1` and `rear = -1`.",
                    "`front = (front + 1) % MAX`: Circularly advances front to the next job in line."
                ],
                "flow": [
                    "Step 1: Check if `front == -1`. If true, underflow.",
                    "Step 2: Read job at `queue[front]` into `job`.",
                    "Step 3: If `front == rear`, queue becomes empty -> set `front = rear = -1`.",
                    "Step 4: Else, advance front circularly: `front = (front + 1) % MAX`.",
                    "Step 5: Return `job`."
                ]
            }
        ],
        "challenge": {
            "prompt": "What formula checks if a circular queue of size MAX is completely full?",
            "opts": [
                "A) rear == MAX - 1",
                "B) (rear + 1) % MAX == front",
                "C) front == rear + 1",
                "D) front + rear == MAX"
            ],
            "correct_opt": "B",
            "hint": "Modulo wraps rear around: if advancing rear hits front, the ring is full.",
            "praise": "Correct! (rear + 1) % MAX == front is the canonical circular queue full check.",
            "roast": "In a circular queue, wrap-around means full condition is `(rear + 1) % MAX == front`!"
        }
    },
    {
        "num": 5,
        "part": "A",
        "title": "Polynomial Addition Using Circular Linked List with Header",
        "file": "dsa-lab/programs/lab05_polynomial_addition.c",
        "concept": "Polynomials represented as linked lists of terms (coeff, exp). A circular header node (exp = -1) eliminates NULL pointer edge-case checks and keeps the list cyclic.",
        "problem": "Represent two multivariate or single-variable polynomials using circular singly linked lists with a header node. Implement polynomial addition and display the resulting polynomial.",
        "blocks": [
            {
                "title": "Polynomial Node & Circular Header Initialization",
                "code": "typedef struct Node {\n    int coeff;\n    int exp;\n    struct Node *next;\n} Node;\n\nNode* create_header() {\n    Node *head = (Node *)malloc(sizeof(Node));\n    head->coeff = 0;\n    head->exp = -1; // Dummy sentinel exponent\n    head->next = head; // Points to itself circularly\n    return head;\n}",
                "purpose": "Creates a sentinel header node whose next pointer initially points to itself.",
                "inside": [
                    "`head->exp = -1`: Dummy sentinel exponent smaller than any valid term (powers >= 0).",
                    "`head->next = head`: Establishes circularity. Even an empty list is a closed circular ring."
                ],
                "flow": [
                    "Step 1: Allocate node on heap using `malloc()`.",
                    "Step 2: Assign dummy value `exp = -1`.",
                    "Step 3: Point `next` to `head` (self-loop).",
                    "Step 4: Return header pointer."
                ]
            },
            {
                "title": "The 3-Case Polynomial Addition Algorithm",
                "code": "Node *p1 = head1->next;\nNode *p2 = head2->next;\nwhile (p1 != head1 || p2 != head2) {\n    if (p1->exp == p2->exp) {\n        int sum = p1->coeff + p2->coeff;\n        if (sum != 0) attach(sum, p1->exp, res);\n        p1 = p1->next; p2 = p2->next;\n    } else if (p1->exp > p2->exp) {\n        attach(p1->coeff, p1->exp, res);\n        p1 = p1->next;\n    } else {\n        attach(p2->coeff, p2->exp, res);\n        p2 = p2->next;\n    }\n}",
                "purpose": "Traverses two sorted circular polynomial lists, adding matching exponents and inserting terms in descending exponent order.",
                "inside": [
                    "`p1 != head1 || p2 != head2`: Loop continues until both circular lists return to their header nodes.",
                    "`Case 1 (p1->exp == p2->exp)`: Like terms! Add coefficients, advance both pointers.",
                    "`Case 2 (p1->exp > p2->exp)`: Term 1 has higher power; copy term 1 to result and advance `p1`.",
                    "`Case 3 (p1->exp < p2->exp)`: Term 2 has higher power; copy term 2 to result and advance `p2`."
                ],
                "flow": [
                    "Step 1: Pointers start at first real terms (`head->next`).",
                    "Step 2: Compare exponents of current nodes.",
                    "Step 3: Branch to Case 1, 2, or 3 and attach term to result list.",
                    "Step 4: Terminate when both pointers cycle back to their respective header nodes."
                ]
            }
        ],
        "challenge": {
            "prompt": "Why is the header node exponent set to -1 in circular polynomial lists?",
            "opts": [
                "A) To save memory on 32-bit systems.",
                "B) As a sentinel value indicating the end of real terms (since valid exponents are >= 0), terminating traversal without NULL checks.",
                "C) To invert the sign of the polynomial.",
                "D) Required by the C preprocessor."
            ],
            "correct_opt": "B",
            "hint": "Valid exponents are non-negative. -1 guarantees the header is distinguishable from real terms.",
            "praise": "Exactly right! It acts as a sentinel boundary marker.",
            "roast": "Sentinel value -1 distinguishes the dummy header from valid non-negative exponent terms."
        }
    },
    {
        "num": 6,
        "part": "A",
        "title": "Binary Tree Creation & Traversals (Level-Order via Queue)",
        "file": "dsa-lab/programs/lab06_binary_tree_traversals.c",
        "concept": "Non-linear hierarchical data structure. Each node has at most two children (left and right). Level-order traversal uses a FIFO queue to visit nodes level by level.",
        "problem": "Create a Binary Tree dynamically. Implement recursive Inorder, Preorder, Postorder traversals, and Breadth-First Level-Order traversal using an auxiliary Queue.",
        "blocks": [
            {
                "title": "Recursive Depth-First Traversals (DFS)",
                "code": "void inorder(Node *root) {\n    if (root == NULL) return;\n    inorder(root->left);         // L: Left Subtree\n    printf(\"%d \", root->data);   // V: Visit Root Node\n    inorder(root->right);        // R: Right Subtree\n}",
                "purpose": "Traverses the tree recursively using the system call stack in Left-Root-Right order.",
                "inside": [
                    "`if (root == NULL) return`: Base case terminating recursion at leaf branches.",
                    "`inorder(root->left)`: Recursively descends to leftmost child.",
                    "`printf(...)`: Action taken when node is visited.",
                    "`inorder(root->right)`: Recursively visits right subtree."
                ],
                "flow": [
                    "Step 1: Check if current pointer is NULL. If so, return.",
                    "Step 2: Call `inorder(root->left)` recursively.",
                    "Step 3: Print current node `root->data`.",
                    "Step 4: Call `inorder(root->right)` recursively."
                ]
            },
            {
                "title": "Level-Order Breadth-First Traversal (BFS) using Queue",
                "code": "void level_order(Node *root) {\n    if (root == NULL) return;\n    enqueue(root);\n    while (!is_empty()) {\n        Node *curr = dequeue();\n        printf(\"%d \", curr->data);\n        if (curr->left != NULL) enqueue(curr->left);\n        if (curr->right != NULL) enqueue(curr->right);\n    }\n}",
                "purpose": "Visits all nodes horizontally level by level from root down to deepest leaves using a FIFO queue.",
                "inside": [
                    "`enqueue(root)`: Seeds queue with tree root.",
                    "`while (!is_empty())`: Processes nodes in strict FIFO arrival order.",
                    "`enqueue(curr->left) / enqueue(curr->right)`: Enqueues children so they are visited after current level completes."
                ],
                "flow": [
                    "Step 1: Insert root into queue.",
                    "Step 2: While queue has items, dequeue front node `curr`.",
                    "Step 3: Print `curr->data`.",
                    "Step 4: If left child exists, enqueue it; if right child exists, enqueue it.",
                    "Step 5: Repeat until queue is exhausted."
                ]
            }
        ],
        "challenge": {
            "prompt": "Which data structure is required to implement Level-Order (Breadth-First) traversal of a tree iteratively?",
            "opts": [
                "A) Stack",
                "B) Queue",
                "C) Hash Table",
                "D) Circular Linked List"
            ],
            "correct_opt": "B",
            "hint": "Breadth-First Search requires FIFO order to visit nodes level-by-level.",
            "praise": "Correct! A FIFO Queue is mandatory for Level-Order traversal.",
            "roast": "Level-order traversal visits nodes level by level (FIFO), requiring a Queue!"
        }
    },
    {
        "num": 7,
        "part": "B",
        "title": "Infix-to-Postfix Conversion with Bracket Validation",
        "file": "dsa-lab/programs/lab07_infix_to_postfix.c",
        "concept": "Translates human-readable infix expressions (A + B) into parenthesis-free postfix expressions (A B +) using Dijkstra's Shunting-Yard operator stack algorithm.",
        "problem": "Convert an infix expression containing operators (+, -, *, /, ^) and parentheses into postfix form using a character Stack, validating matching brackets.",
        "blocks": [
            {
                "title": "Operator Precedence & Associativity Evaluation",
                "code": "int precedence(char op) {\n    switch (op) {\n        case '^': return 3;\n        case '*':\n        case '/':\n        case '%': return 2;\n        case '+':\n        case '-': return 1;\n        default:  return 0;\n    }\n}",
                "purpose": "Defines arithmetic hierarchy so higher precedence operations bind before lower precedence ones.",
                "inside": [
                    "`^` (Exponentiation): Highest precedence (3).",
                    "`*`, `/`, `%` (Multiplicative): Precedence 2.",
                    "`+`, `-` (Additive): Precedence 1.",
                    "`default`: Returns 0 for non-operators and parentheses."
                ],
                "flow": [
                    "Step 1: Character operator passed in.",
                    "Step 2: Switch statement maps symbol to integer rank.",
                    "Step 3: Returns numeric priority."
                ]
            },
            {
                "title": "Shunting-Yard Infix to Postfix Conversion Loop",
                "code": "for (int i = 0; infix[i] != '\\0'; i++) {\n    char ch = infix[i];\n    if (isalnum(ch)) {\n        postfix[k++] = ch; // Operands directly to output\n    } else if (ch == '(') {\n        push(ch);\n    } else if (ch == ')') {\n        while (top != -1 && stack[top] != '(') {\n            postfix[k++] = pop();\n        }\n        pop(); // Discard matching '('\n    } else {\n        while (top != -1 && precedence(stack[top]) >= precedence(ch)) {\n            postfix[k++] = pop();\n        }\n        push(ch);\n    }\n}",
                "purpose": "Iterates through infix tokens, sending operands directly to output and managing operator stack precedence.",
                "inside": [
                    "`isalnum(ch)`: Operands (variables/digits) bypass the stack and go directly to `postfix` string.",
                    "`ch == '('`: Pushed unconditionally to mark subexpression boundary.",
                    "`ch == ')'`: Pops all operators into postfix until matching `(` is encountered.",
                    "`precedence(stack[top]) >= precedence(ch)`: Pops higher or equal precedence operators before pushing current operator."
                ],
                "flow": [
                    "Step 1: Scan token `ch`.",
                    "Step 2: If operand -> append to `postfix`.",
                    "Step 3: If `(` -> push to stack.",
                    "Step 4: If `)` -> pop to `postfix` until `(`, then discard `(`.",
                    "Step 5: If operator -> pop higher/equal precedence operators, then push `ch`.",
                    "Step 6: Drain remaining stack operators at string end."
                ]
            }
        ],
        "challenge": {
            "prompt": "What is the postfix form of the infix expression: (A + B) * C?",
            "opts": [
                "A) A B + C *",
                "B) A B C + *",
                "C) * + A B C",
                "D) A + B C *"
            ],
            "correct_opt": "A",
            "hint": "(A + B) evaluates first due to parentheses, yielding AB+, then multiplied by C giving AB+C*.",
            "praise": "Spot on! (A + B) becomes AB+, which when multiplied by C yields AB+C*.",
            "roast": "(A + B) * C -> Parentheses force AB+ first, then * C -> AB+C*!"
        }
    },
    {
        "num": 8,
        "part": "B",
        "title": "Student Record Management Using Singly Linked List (SLL)",
        "file": "dsa-lab/programs/lab08_student_sll.c",
        "concept": "Dynamic linear chain of nodes connected by forward pointers. Memory is allocated on the heap per node, enabling dynamic sizing without pre-allocating fixed arrays.",
        "problem": "Create a Singly Linked List of Student nodes (USN, Name, Branch, Sem, Phone). Implement insert front, insert end, delete front, delete end, and display with node count.",
        "blocks": [
            {
                "title": "Student Node Definition & Insert at Front",
                "code": "typedef struct Student {\n    char usn[20];\n    char name[50];\n    char branch[10];\n    int sem;\n    char phno[15];\n    struct Student *next;\n} Student;\n\nStudent* insert_front(Student *head) {\n    Student *newNode = (Student *)malloc(sizeof(Student));\n    // read student details...\n    newNode->next = head; // Link new node to old head\n    head = newNode;       // New node becomes the new head\n    return head;\n}",
                "purpose": "Inserts a student node at the beginning of the list in O(1) constant time.",
                "inside": [
                    "`struct Student *next`: Self-referential pointer storing the 64-bit RAM address of the succeeding node.",
                    "`newNode->next = head`: Wires the new node's next pointer to point to the current first node.",
                    "`head = newNode`: Updates head pointer to designate new node as the list entry point."
                ],
                "flow": [
                    "Step 1: Allocate new node on heap using `malloc()`.",
                    "Step 2: Read student data into `newNode` fields.",
                    "Step 3: Point `newNode->next` to current `head`.",
                    "Step 4: Return `newNode` as the updated `head`."
                ]
            },
            {
                "title": "Delete from End & Memory Leak Prevention",
                "code": "Student* delete_end(Student *head) {\n    if (head == NULL) return NULL;\n    if (head->next == NULL) {\n        free(head);\n        return NULL;\n    }\n    Student *curr = head;\n    while (curr->next->next != NULL) {\n        curr = curr->next; // Stop at second-to-last node\n    }\n    free(curr->next);      // Deallocate tail node\n    curr->next = NULL;     // Terminate list\n    return head;\n}",
                "purpose": "Traverses to the second-to-last node, frees the tail node, and terminates the list safely.",
                "inside": [
                    "`curr->next->next != NULL`: Lookahead condition. Stops `curr` at the second-to-last node so it can sever the tail link.",
                    "`free(curr->next)`: Releases tail node memory back to OS heap.",
                    "`curr->next = NULL`: Sets new tail's pointer to NULL so traversal algorithms terminate properly."
                ],
                "flow": [
                    "Step 1: Check if list is empty or single-node. Handle edge cases.",
                    "Step 2: Loop `curr` until `curr->next->next == NULL`.",
                    "Step 3: `free(curr->next)` deallocates tail node.",
                    "Step 4: Set `curr->next = NULL`."
                ]
            }
        ],
        "challenge": {
            "prompt": "What happens if you run 'while (curr->next->next != NULL)' on a single-node list?",
            "opts": [
                "A) It deletes the node normally.",
                "B) Segmentation fault (crash), because curr->next is NULL, and dereferencing NULL->next is illegal memory access.",
                "C) It loops infinitely.",
                "D) The operating system prints a warning."
            ],
            "correct_opt": "B",
            "hint": "On a 1-node list, head->next is NULL. Dereferencing NULL->next causes an instant SIGSEGV segfault.",
            "praise": "Critical exam catch! Always check if head->next is NULL before accessing curr->next->next.",
            "roast": "In a 1-node list, curr->next is NULL. Accessing curr->next->next dereferences NULL, triggering a crash!"
        }
    },
    {
        "num": 9,
        "part": "B",
        "title": "Manufacturing Parts Inventory Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab09_parts_hash_table.c",
        "concept": "Direct addressing using a hash function (key % TABLE_SIZE) provides O(1) average lookup. Collisions (two keys hashing to the same bucket) are resolved via Linear Probing.",
        "problem": "Create a Hash Table of size M to store manufacturing part records (Part_ID, Part_Name). Implement division hash function and linear probing collision resolution.",
        "blocks": [
            {
                "title": "Hash Function & Linear Probing Insertion",
                "code": "void insert(int part_id, char *name) {\n    int index = part_id % TABLE_SIZE;\n    int start = index;\n    while (table[index].occupied == 1) {\n        if (table[index].part_id == part_id) {\n            printf(\"Duplicate Key!\\n\");\n            return;\n        }\n        index = (index + 1) % TABLE_SIZE; // Linear probing\n        if (index == start) {\n            printf(\"Hash Table is FULL!\\n\");\n            return;\n        }\n    }\n    table[index].part_id = part_id;\n    strcpy(table[index].name, name);\n    table[index].occupied = 1;\n}",
                "purpose": "Computes home bucket and sequentially searches adjacent slots modulo TABLE_SIZE until an empty slot is found.",
                "inside": [
                    "`part_id % TABLE_SIZE`: Division method hash function mapping large keys to array range `[0..TABLE_SIZE-1]`.",
                    "`(index + 1) % TABLE_SIZE`: Linear probing probe step. Checks the next contiguous slot circularly.",
                    "`index == start`: Full cycle detection. If probing wraps around back to `start`, table is completely full."
                ],
                "flow": [
                    "Step 1: Calculate initial hash index `part_id % TABLE_SIZE`.",
                    "Step 2: If slot occupied, probe `(index + 1) % TABLE_SIZE`.",
                    "Step 3: Repeat until empty slot found or table verified full.",
                    "Step 4: Store record and mark `occupied = 1`."
                ]
            }
        ],
        "challenge": {
            "prompt": "What is the primary drawback of Linear Probing in Hash Tables?",
            "opts": [
                "A) Memory cannot be freed.",
                "B) Primary Clustering — occupied slots form long contiguous chains, degrading lookup from O(1) toward O(N).",
                "C) It only works with negative numbers.",
                "D) Keys must be strings only."
            ],
            "correct_opt": "B",
            "hint": "Adjacent occupied slots clump together, making subsequent collisions even more likely.",
            "praise": "Examiner favorite! Primary clustering is the signature drawback of linear probing.",
            "roast": "Linear probing suffers from Primary Clustering, where contiguous blocks of filled slots degrade search performance."
        }
    },
    {
        "num": 10,
        "part": "B",
        "title": "Hierarchical Numeric Data Using Binary Search Tree (BST)",
        "file": "dsa-lab/programs/lab10_bst_numeric.c",
        "concept": "Binary Search Tree property: for every node, all values in its Left Subtree are smaller, and all values in its Right Subtree are greater. Inorder traversal produces sorted output.",
        "problem": "Construct a Binary Search Tree of integers dynamically. Implement iterative/recursive insert, inorder traversal (sorted order), and search for a given key.",
        "blocks": [
            {
                "title": "Recursive BST Insertion Algorithm",
                "code": "Node* insert(Node *root, int val) {\n    if (root == NULL) {\n        Node *newNode = (Node *)malloc(sizeof(Node));\n        newNode->data = val;\n        newNode->left = newNode->right = NULL;\n        return newNode;\n    }\n    if (val < root->data) {\n        root->left = insert(root->left, val);   // Branch Left\n    } else if (val > root->data) {\n        root->right = insert(root->right, val); // Branch Right\n    }\n    // If val == root->data, duplicate ignored\n    return root;\n}",
                "purpose": "Inserts a new value into its correct mathematical location in the BST.",
                "inside": [
                    "`root == NULL`: Base insertion case. Reached an empty leaf branch, allocates new node.",
                    "`val < root->data`: Value is smaller than current node -> recursively branches to Left Subtree.",
                    "`val > root->data`: Value is larger than current node -> recursively branches to Right Subtree."
                ],
                "flow": [
                    "Step 1: If current root is NULL, allocate and return new node.",
                    "Step 2: If `val < root->data`, recurse on `root->left`.",
                    "Step 3: If `val > root->data`, recurse on `root->right`.",
                    "Step 4: Return `root` pointer up the call stack."
                ]
            },
            {
                "title": "Binary Search Algorithm in BST",
                "code": "Node* search(Node *root, int key) {\n    if (root == NULL || root->data == key) {\n        return root;\n    }\n    if (key < root->data) {\n        return search(root->left, key);  // Search Left\n    }\n    return search(root->right, key);     // Search Right\n}",
                "purpose": "Searches for target key by halving the search space at each level in O(log N) average time.",
                "inside": [
                    "`root == NULL`: Key does not exist in tree.",
                    "`root->data == key`: Key found at current node.",
                    "`key < root->data`: Key must be in left subtree; discard entire right subtree.",
                    "`key > root->data`: Key must be in right subtree; discard entire left subtree."
                ],
                "flow": [
                    "Step 1: Check if root is NULL or equals key.",
                    "Step 2: If `key < root->data`, branch left.",
                    "Step 3: If `key > root->data`, branch right.",
                    "Step 4: Returns pointer to matching node or NULL."
                ]
            }
        ],
        "challenge": {
            "prompt": "What traversal of a Binary Search Tree ALWAYS produces keys in sorted ascending order?",
            "opts": [
                "A) Preorder (Root-Left-Right)",
                "B) Inorder (Left-Root-Right)",
                "C) Postorder (Left-Right-Root)",
                "D) Level-Order (Breadth-First)"
            ],
            "correct_opt": "B",
            "hint": "Left (< Root) then Root then Right (> Root) produces sorted output.",
            "praise": "Golden rule of BSTs! Inorder traversal always yields sorted output.",
            "roast": "Inorder traversal (Left -> Root -> Right) always produces sorted ascending sequence in a BST!"
        }
    },
    {
        "num": 11,
        "part": "B",
        "title": "Employee Record Management Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab11_employee_hash_table.c",
        "concept": "Hash Table implementation storing structured multi-field records. Demonstrates primary key hashing and collision handling.",
        "problem": "Create a Hash Table to manage Employee records (Emp_ID, Name, Salary). Implement division hash function, linear probing for collisions, and search by Emp_ID.",
        "blocks": [
            {
                "title": "Employee Record Structure & Division Hashing",
                "code": "typedef struct {\n    int emp_id;\n    char name[50];\n    float salary;\n    int is_occupied;\n} Employee;\n\nEmployee emp_table[MAX_SIZE];\n\nint hash(int key) {\n    return key % MAX_SIZE;\n}",
                "purpose": "Defines the fixed array hash table and maps 4-digit employee IDs to table indices.",
                "inside": [
                    "`is_occupied`: Boolean status flag (1 = slot contains active record, 0 = slot empty).",
                    "`key % MAX_SIZE`: Hashes key into valid index range `[0..MAX_SIZE-1]`."
                ],
                "flow": [
                    "Step 1: Table initialized with all `is_occupied = 0`.",
                    "Step 2: `hash(key)` returns initial probe index."
                ]
            }
        ],
        "challenge": {
            "prompt": "If TABLE_SIZE is 10, what is the initial hash index for an employee with ID 4127?",
            "opts": [
                "A) 4",
                "B) 7",
                "C) 2",
                "D) 1"
            ],
            "correct_opt": "B",
            "hint": "4127 % 10 = 7.",
            "praise": "Correct! 4127 % 10 = 7.",
            "roast": "Modulo arithmetic: 4127 % 10 = 7!"
        }
    },
    {
        "num": 12,
        "part": "B",
        "title": "City Connectivity Using Graphs & Depth-First Search (DFS)",
        "file": "dsa-lab/programs/lab12_city_connectivity.c",
        "concept": "Graph traversal using an Adjacency Matrix. DFS explores as deep as possible along each branch before backtracking, determining connected components and reachability.",
        "problem": "Represent city road networks as a Graph using an Adjacency Matrix. Implement Depth-First Search (DFS) to determine if all cities are reachable from a starting city.",
        "blocks": [
            {
                "title": "Adjacency Matrix & Visited Array Setup",
                "code": "int adj[MAX][MAX];     // adj[i][j] = 1 if road exists between city i and j\nint visited[MAX] = {0}; // visited[i] = 1 once city i is reached\nint n;                  // Total number of cities",
                "purpose": "Models graph edges as a 2D boolean grid and tracks visited state to avoid infinite cycles.",
                "inside": [
                    "`adj[i][j]`: 1 indicates direct road connects city `i` to city `j`; 0 indicates no direct connection.",
                    "`visited[MAX]`: Prevents revisiting nodes in cyclic graphs. Eliminates infinite recursion loops."
                ],
                "flow": [
                    "Step 1: Input number of cities `n`.",
                    "Step 2: Read adjacency matrix values.",
                    "Step 3: Clear `visited` array to all 0s."
                ]
            },
            {
                "title": "Recursive Depth-First Search (DFS) Traversal",
                "code": "void dfs(int u) {\n    visited[u] = 1;\n    printf(\"Visited City %d\\n\", u);\n    for (int v = 0; v < n; v++) {\n        if (adj[u][v] == 1 && !visited[v]) {\n            dfs(v); // Recursively explore unvisited neighbor\n        }\n    }\n}",
                "purpose": "Explores as deeply as possible from vertex `u` before backtracking.",
                "inside": [
                    "`visited[u] = 1`: Marks current city visited as soon as it is entered.",
                    "`adj[u][v] == 1 && !visited[v]`: Checks two criteria: 1) direct road exists, 2) destination city has not yet been visited.",
                    "`dfs(v)`: Recursive call pushes new call frame onto system stack."
                ],
                "flow": [
                    "Step 1: Mark city `u` as visited.",
                    "Step 2: Loop through all candidate cities `v`.",
                    "Step 3: If road exists and city `v` unvisited, call `dfs(v)` recursively.",
                    "Step 4: When all neighbors visited, backtrack to caller."
                ]
            }
        ],
        "challenge": {
            "prompt": "How do you check if an entire graph of N vertices is fully connected after running dfs(start)?",
            "opts": [
                "A) Check if the adjacency matrix has no zeros.",
                "B) Check if every element in the visited array (visited[0] to visited[N-1]) is equal to 1.",
                "C) Check if the number of edges equals N.",
                "D) Count the number of recursive calls."
            ],
            "correct_opt": "B",
            "hint": "If every vertex was reached, every visited[i] will be 1.",
            "praise": "Precisely! If any visited[i] == 0, that city was unreachable from the start node.",
            "roast": "A graph is fully connected if every single node was reached (visited[i] == 1 for all i)!"
        }
    }
]
