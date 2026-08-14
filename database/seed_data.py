"""
Seed / reference content for CareerBoost AI.

Kept separate from models/db.py so the (large) content banks are easy to
scan, extend and maintain independently of the data-access layer.

    QUIZ_QUESTIONS        -> 110 aptitude MCQs  (Quantitative / Logical / Verbal / Technical)
    INTERVIEW_QUESTIONS   -> 100 technical + HR interview Q&A
    CODING_PROBLEMS       -> coding problems across Python, JavaScript, C, C++, Java
                             (auto-graded) and HTML/CSS (live-preview, ungraded)
    COMPANIES             -> placement drive company directory
"""

import json

# ======================================================================
#  APTITUDE QUIZ  —  (category, difficulty, question, A, B, C, D, correct)
# ======================================================================
QUIZ_QUESTIONS = [
    # ---------------- QUANTITATIVE — Easy (10) ----------------
    ("Quantitative", "Easy", "What is 20% of 150?", "20", "30", "40", "50", "B"),
    ("Quantitative", "Easy", "A shopkeeper sells an item for Rs.550 that cost Rs.500. What is the profit percentage?", "5%", "10%", "15%", "20%", "B"),
    ("Quantitative", "Easy", "If a train travels 60 km in 1.5 hours, what is its speed?", "30 km/h", "40 km/h", "45 km/h", "50 km/h", "B"),
    ("Quantitative", "Easy", "Simplify: 12 + 8 × 2 = ?", "40", "28", "20", "32", "B"),
    ("Quantitative", "Easy", "What is the LCM of 4 and 6?", "8", "12", "16", "24", "B"),
    ("Quantitative", "Easy", "What is the HCF of 18 and 24?", "3", "6", "9", "12", "B"),
    ("Quantitative", "Easy", "A sum of Rs.2000 is divided between two people in the ratio 3:2. Find the smaller share.", "Rs.800", "Rs.900", "Rs.1000", "Rs.750", "A"),
    ("Quantitative", "Easy", "Convert 0.75 to a fraction in lowest terms.", "3/4", "7/10", "3/5", "5/6", "A"),
    ("Quantitative", "Easy", "What is the average of 10, 20, 30 and 40?", "20", "25", "30", "35", "B"),
    ("Quantitative", "Easy", "A car covers 150 km using 10 litres of fuel. What is its mileage?", "10 km/l", "12 km/l", "15 km/l", "18 km/l", "C"),
    # ---------------- QUANTITATIVE — Medium (10) ----------------
    ("Quantitative", "Medium", "If the cost price of 20 articles equals the selling price of 16 articles, find the profit %.", "20%", "25%", "16%", "30%", "B"),
    ("Quantitative", "Medium", "Simple interest on Rs.5000 at 8% p.a. for 3 years is:", "Rs.1000", "Rs.1100", "Rs.1200", "Rs.1400", "C"),
    ("Quantitative", "Medium", "A man's age is 3 times his son's age. After 5 years he will be 2.5 times his son's age. Find the son's current age.", "8", "10", "12", "15", "D"),
    ("Quantitative", "Medium", "Two pipes can fill a tank in 12 and 15 hours respectively. Working together, how long will they take to fill it?", "6 hr 40 min", "7 hr", "6 hr", "8 hr", "A"),
    ("Quantitative", "Medium", "A sum becomes double itself in 8 years at simple interest. Find the rate of interest.", "10%", "12.5%", "15%", "8%", "B"),
    ("Quantitative", "Medium", "A student scored 75% and got 30 marks more than the passing marks of 50%. Find the maximum marks.", "100", "120", "150", "200", "B"),
    ("Quantitative", "Medium", "The ratio of two numbers is 4:5 and their LCM is 180. Find the numbers.", "36, 45", "40, 50", "44, 55", "32, 40", "A"),
    ("Quantitative", "Medium", "A boat travels 30 km downstream in 2 hours and returns upstream in 3 hours. Find the boat's speed in still water.", "10 km/h", "11 km/h", "12.5 km/h", "15 km/h", "C"),
    ("Quantitative", "Medium", "Find the compound interest on Rs.10,000 at 10% p.a. for 2 years, compounded annually.", "Rs.2000", "Rs.2100", "Rs.2200", "Rs.1900", "B"),
    ("Quantitative", "Medium", "The average of 5 consecutive even numbers is 24. Find the largest number.", "26", "28", "30", "32", "B"),
    # ---------------- QUANTITATIVE — Hard (10) ----------------
    ("Quantitative", "Hard", "A can complete a work in 12 days and B in 15 days. They work together for 4 days, then A leaves. In how many more days will B finish the remaining work?", "5", "6", "7", "8", "B"),
    ("Quantitative", "Hard", "Two trains 150m and 100m long run towards each other at 54 km/h and 36 km/h. In how many seconds will they cross each other?", "8", "9", "10", "11", "C"),
    ("Quantitative", "Hard", "The present ages of A and B are in ratio 5:6. After 4 years the ratio becomes 6:7. Find A's present age.", "15", "18", "20", "25", "C"),
    ("Quantitative", "Hard", "A sum amounts to Rs.4840 in 2 years and Rs.5324 in 3 years at compound interest. Find the rate of interest.", "8%", "9%", "10%", "12%", "C"),
    ("Quantitative", "Hard", "A, B and C can do a job in 18, 24 and 36 days respectively. Working together they earn Rs.3300. Find B's share.", "Rs.900", "Rs.1000", "Rs.1100", "Rs.1200", "C"),
    ("Quantitative", "Hard", "A 60-litre mixture has milk and water in ratio 2:1. How much water must be added to make the ratio 1:2?", "60 litres", "80 litres", "90 litres", "100 litres", "A"),
    ("Quantitative", "Hard", "A shopkeeper marks up goods by 40% and then gives a 20% discount. Find his overall profit percentage.", "8%", "10%", "12%", "15%", "C"),
    ("Quantitative", "Hard", "If x:y = 3:4, find (2x+3y):(3x+4y).", "18:25", "17:23", "16:22", "19:26", "A"),
    ("Quantitative", "Hard", "A can finish a job in 10 days, B in 15 days. Working together for 5 days, what fraction of the work is left?", "1/6", "1/4", "1/3", "1/2", "A"),
    ("Quantitative", "Hard", "A town's population grows 10% annually. If it is currently 22,000, what was it 2 years ago?", "18,000", "18,182", "20,000", "19,800", "B"),

    # ---------------- LOGICAL — Easy (10) ----------------
    ("Logical", "Easy", "Find the odd one out: Apple, Banana, Carrot, Mango.", "Apple", "Banana", "Carrot", "Mango", "C"),
    ("Logical", "Easy", "Complete the series: 2, 4, 6, 8, ?", "9", "10", "11", "12", "B"),
    ("Logical", "Easy", "If Monday is the 1st day, what day is the 10th?", "Tuesday", "Wednesday", "Thursday", "Friday", "B"),
    ("Logical", "Easy", "Which word does NOT belong: Circle, Square, Triangle, Sphere?", "Circle", "Square", "Triangle", "Sphere", "D"),
    ("Logical", "Easy", "Find the missing number: 5, 10, 15, 20, ?", "22", "24", "25", "30", "C"),
    ("Logical", "Easy", "A is taller than B. C is shorter than B. Who is the shortest?", "A", "B", "C", "Cannot be determined", "C"),
    ("Logical", "Easy", "All Roses are Flowers. Some Flowers fade quickly. Which is definitely true?", "All Roses fade quickly", "Some Roses may fade quickly", "No Roses fade quickly", "All Flowers are Roses", "B"),
    ("Logical", "Easy", "Complete the analogy: Hand is to Glove as Foot is to ?", "Sock", "Shoe", "Sandal", "Both A and B", "D"),
    ("Logical", "Easy", "Find the odd pair: (2,4), (3,9), (4,16), (5,20)", "(2,4)", "(3,9)", "(4,16)", "(5,20)", "D"),
    ("Logical", "Easy", "What comes next in the pattern: A, C, E, G, ?", "H", "I", "J", "K", "B"),
    # ---------------- LOGICAL — Medium (10) ----------------
    ("Logical", "Medium", "If CAT is coded as 3120 (C=3, A=1, T=20), how is DOG coded?", "4157", "4715", "4175", "4517", "A"),
    ("Logical", "Medium", "Complete the series: 3, 6, 12, 24, ?", "36", "48", "44", "40", "B"),
    ("Logical", "Medium", "Pointing to a photo, a man says 'She is the daughter of my grandfather's only son.' How is she related to him (assume he is the only son)?", "Sister", "Mother", "Aunt", "Cousin", "A"),
    ("Logical", "Medium", "In a code, RIVER is written as SJWFS (each letter +1). How is STONE written?", "TUPOF", "TUPPF", "UTQPG", "TUPOG", "A"),
    ("Logical", "Medium", "Five friends sit in a row: R is left of Q, Q is left of P, P is left of T, T is left of S. Who is leftmost?", "P", "Q", "R", "S", "C"),
    ("Logical", "Medium", "All pens are books. All books are tables. Conclusion: All pens are tables. Is this valid?", "True", "False", "Cannot be determined", "Partially true", "A"),
    ("Logical", "Medium", "If the day before yesterday was Saturday, what day will it be tomorrow?", "Tuesday", "Wednesday", "Thursday", "Monday", "A"),
    ("Logical", "Medium", "Find the next term: 1, 4, 9, 16, 25, ?", "30", "36", "32", "49", "B"),
    ("Logical", "Medium", "A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?", "Uncle", "Father", "Grandfather", "Brother", "A"),
    ("Logical", "Medium", "In a row of children, Raj is 7th from the left and 12th from the right. How many children are in the row?", "18", "19", "20", "17", "A"),
    # ---------------- LOGICAL — Hard (10) ----------------
    ("Logical", "Hard", "Pointing to a man, a woman says 'His mother is the only daughter of my mother.' How is the woman related to the man?", "Mother", "Sister", "Aunt", "Grandmother", "A"),
    ("Logical", "Hard", "If '+' means '÷', '−' means '×', '×' means '−', and '÷' means '+', evaluate: 8 × 4 ÷ 2 − 3 + 6", "5", "7", "3", "9", "A"),
    ("Logical", "Hard", "A cube is painted red on all faces and cut into 27 equal smaller cubes. How many have exactly 2 faces painted?", "8", "12", "6", "4", "B"),
    ("Logical", "Hard", "In a code, TRUST is written as SQTRS (each letter −1). How is FAITH written?", "EZHSG", "FZHSG", "EZGSG", "EYHSG", "A"),
    ("Logical", "Hard", "P is the son of Q. Q and R are siblings. S is R's mother. How is S related to P?", "Grandmother", "Mother", "Aunt", "Sister", "A"),
    ("Logical", "Hard", "A father is 4 times as old as his son. After 20 years he will be twice as old as his son. Find the father's current age.", "40", "36", "44", "48", "A"),
    ("Logical", "Hard", "No cats are dogs. All dogs are animals. Conclusion I: No cats are animals. Conclusion II: Some animals are dogs. Which follows?", "Only I follows", "Only II follows", "Both follow", "Neither follows", "B"),
    ("Logical", "Hard", "If south-east becomes north and north-east becomes west (rotate 135° anticlockwise), what does south become?", "North-west", "North-east", "South-east", "East", "B"),
    ("Logical", "Hard", "A is twice as good a worker as B; together they finish a job in 14 days. In how many days can A alone finish it?", "18", "21", "24", "20", "B"),
    ("Logical", "Hard", "Complete the number series: 7, 26, 63, 124, 215, ?", "342", "330", "320", "350", "A"),

    # ---------------- VERBAL — Easy (8) ----------------
    ("Verbal", "Easy", "Choose the synonym of 'Happy'.", "Sad", "Joyful", "Angry", "Tired", "B"),
    ("Verbal", "Easy", "Choose the antonym of 'Brave'.", "Courageous", "Bold", "Cowardly", "Fearless", "C"),
    ("Verbal", "Easy", "Fill in the blank: She ___ to school every day.", "go", "goes", "going", "gone", "B"),
    ("Verbal", "Easy", "Choose the correctly spelled word.", "Recieve", "Receive", "Receeve", "Receve", "B"),
    ("Verbal", "Easy", "Identify the plural of 'Child'.", "Childs", "Childes", "Children", "Childrens", "C"),
    ("Verbal", "Easy", "Choose the correct article: I saw ___ elephant at the zoo.", "a", "an", "the", "no article", "B"),
    ("Verbal", "Easy", "Choose the synonym of 'Abundant'.", "Scarce", "Plentiful", "Limited", "Rare", "B"),
    ("Verbal", "Easy", "Choose the antonym of 'Ancient'.", "Old", "Modern", "Historic", "Aged", "B"),
    # ---------------- VERBAL — Medium (9) ----------------
    ("Verbal", "Medium", "Choose the correctly punctuated sentence.", "Its a nice day", "It's a nice day.", "Its' a nice day", "It is a nice day,", "B"),
    ("Verbal", "Medium", "Identify the part of speech of 'beautifully' in: She sings beautifully.", "Noun", "Verb", "Adverb", "Adjective", "C"),
    ("Verbal", "Medium", "Choose the correct passive voice of: 'The chef cooks the meal.'", "The meal cooks the chef.", "The meal is cooked by the chef.", "The meal was cooked by the chef.", "The meal cooking by chef.", "B"),
    ("Verbal", "Medium", "Choose the correct word: Despite the rain, the match ___ not cancelled.", "was", "is", "were", "be", "A"),
    ("Verbal", "Medium", "Choose the idiom meaning 'to reveal a secret'.", "Break a leg", "Spill the beans", "Hit the sack", "Under the weather", "B"),
    ("Verbal", "Medium", "Identify the error: 'Neither of the students have submitted their assignment.'", "Neither", "have", "their", "No error", "B"),
    ("Verbal", "Medium", "Choose the word closest in meaning to 'Meticulous'.", "Careless", "Careful", "Quick", "Lazy", "B"),
    ("Verbal", "Medium", "Choose the correct preposition: He is good ___ mathematics.", "in", "at", "on", "with", "B"),
    ("Verbal", "Medium", "Rearrange to form a meaningful sentence: 'the / rises / sun / east / in / the'", "The sun rises in the east", "The east rises in sun the", "In the sun rises east", "Rises the sun in east", "A"),
    # ---------------- VERBAL — Hard (8) ----------------
    ("Verbal", "Hard", "Choose the sentence with correct subject-verb agreement.", "Each of the boys have a pen.", "Each of the boys has a pen.", "Each of the boy has a pen.", "Each of boys have a pen.", "B"),
    ("Verbal", "Hard", "Identify the figure of speech: 'The wind whispered through the trees.'", "Simile", "Metaphor", "Personification", "Hyperbole", "C"),
    ("Verbal", "Hard", "Choose the correct meaning of the idiom 'to bite the bullet'.", "To eat quickly", "To face a difficult situation bravely", "To avoid responsibility", "To argue fiercely", "B"),
    ("Verbal", "Hard", "Choose the correctly structured conditional sentence.", "If I will study, I pass the exam.", "If I studied, I will pass the exam.", "If I study, I will pass the exam.", "If I study, I passed the exam.", "C"),
    ("Verbal", "Hard", "Choose the word that is a homophone of 'Peace'.", "Piece", "Peas", "Piace", "Peaceful", "A"),
    ("Verbal", "Hard", "Identify the correct indirect speech for: He said, 'I am going home.'", "He said that he is going home.", "He said that he was going home.", "He says that he was going home.", "He said that he is went home.", "B"),
    ("Verbal", "Hard", "Choose the sentence that uses 'affect' and 'effect' correctly.", "The medicine had a positive affect on him.", "The medicine will effect his health.", "The medicine had a positive effect on him.", "The medicine will affected him.", "C"),
    ("Verbal", "Hard", "Choose the meaning of the phrase 'a blessing in disguise'.", "A hidden curse", "Something good that seemed bad at first", "A disguised gift", "An obvious benefit", "B"),

    # ---------------- TECHNICAL — Easy (8) ----------------
    ("Technical", "Easy", "Which data structure uses FIFO order?", "Stack", "Queue", "Tree", "Graph", "B"),
    ("Technical", "Easy", "What does CPU stand for?", "Central Process Unit", "Central Processing Unit", "Computer Processing Unit", "Central Processor Utility", "B"),
    ("Technical", "Easy", "Which of these is NOT a programming language?", "Python", "Java", "C++", "HTTP", "D"),
    ("Technical", "Easy", "What is the binary equivalent of decimal 10?", "1000", "1010", "1100", "1001", "B"),
    ("Technical", "Easy", "Which symbol is used for single-line comments in Python?", "//", "/* */", "#", "<!-- -->", "C"),
    ("Technical", "Easy", "What does SQL stand for?", "Structured Query Language", "Simple Query Language", "Sequential Query Language", "Standard Query Language", "A"),
    ("Technical", "Easy", "Which of the following is a valid variable name?", "2value", "value_2", "value-2", "value 2", "B"),
    ("Technical", "Easy", "What is the time complexity of accessing an array element by index?", "O(1)", "O(n)", "O(log n)", "O(n^2)", "A"),
    # ---------------- TECHNICAL — Medium (9) ----------------
    ("Technical", "Medium", "Which sorting algorithm has the best average-case time complexity?", "Bubble Sort", "Merge Sort", "Selection Sort", "Insertion Sort", "B"),
    ("Technical", "Medium", "What is the output of 5 // 2 in Python?", "2.5", "2", "3", "2.0", "B"),
    ("Technical", "Medium", "Which HTTP method is used to update an existing resource in REST APIs?", "GET", "POST", "PUT", "DELETE", "C"),
    ("Technical", "Medium", "In OOP, which concept lets a child class use methods of a parent class?", "Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "B"),
    ("Technical", "Medium", "What is a primary key constraint used for?", "Allow duplicate values", "Uniquely identify each record", "Sort table data", "Enforce foreign key relations", "B"),
    ("Technical", "Medium", "Which data structure is used to implement recursion internally?", "Queue", "Stack", "Array", "Heap", "B"),
    ("Technical", "Medium", "What does 'git commit' do?", "Uploads code to GitHub", "Saves a snapshot of staged changes locally", "Creates a new branch", "Deletes the repository", "B"),
    ("Technical", "Medium", "What is the time complexity of binary search on a sorted array of n elements?", "O(n)", "O(n log n)", "O(log n)", "O(1)", "C"),
    ("Technical", "Medium", "Which of these is a NoSQL database?", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "C"),
    # ---------------- TECHNICAL — Hard (8) ----------------
    ("Technical", "Hard", "What is the space complexity of a recursive Fibonacci function (no memoization)?", "O(1)", "O(n)", "O(2^n)", "O(n^2)", "B"),
    ("Technical", "Hard", "Which collision-handling technique stores multiple elements at the same hash index using a linked list?", "Open addressing", "Chaining", "Linear probing", "Double hashing", "B"),
    ("Technical", "Hard", "Which normal form removes transitive dependency in a relational database?", "1NF", "2NF", "3NF", "BCNF", "C"),
    ("Technical", "Hard", "What is the worst-case time complexity of QuickSort?", "O(n log n)", "O(n)", "O(n^2)", "O(log n)", "C"),
    ("Technical", "Hard", "Which design pattern ensures a class has only one instance?", "Factory", "Singleton", "Observer", "Builder", "B"),
    ("Technical", "Hard", "What does a 'deadlock' mean in operating systems?", "Fast process execution", "Processes waiting indefinitely for each other's resources", "Memory overflow", "CPU idle state", "B"),
    ("Technical", "Hard", "Which algorithm finds the shortest path in a weighted graph with no negative edges?", "DFS", "BFS", "Dijkstra's Algorithm", "Kruskal's Algorithm", "C"),
    ("Technical", "Hard", "What does the 'Isolation' property in ACID ensure?", "Transactions are permanent", "Concurrent transactions don't interfere with each other", "Data is always consistent", "All operations complete or none do", "B"),
]


# ======================================================================
#  INTERVIEW QUESTIONS  —  (category, difficulty, question, answer)
# ======================================================================
INTERVIEW_QUESTIONS = [
    # ---------------- Python (10) ----------------
    ("Python", "Easy", "What are Python's key features?", "Python is interpreted, dynamically typed, has automatic memory management, a huge standard library, and supports procedural, object-oriented and functional programming styles."),
    ("Python", "Easy", "Differentiate between list and tuple.", "Lists are mutable and defined with [], while tuples are immutable and defined with (). Tuples are generally faster and are used for fixed collections of data."),
    ("Python", "Easy", "What is the difference between '==' and 'is' in Python?", "'==' compares values for equality, while 'is' checks whether two references point to the exact same object in memory."),
    ("Python", "Medium", "What is a decorator in Python?", "A decorator is a function that wraps another function to extend or modify its behaviour without changing its source code, commonly used for logging, timing, caching and access control."),
    ("Python", "Medium", "Explain list comprehension with an example.", "List comprehension is a concise way to build lists, e.g. [x*x for x in range(5)] creates [0,1,4,9,16] in a single readable line instead of a manual loop."),
    ("Python", "Medium", "What is the difference between deep copy and shallow copy?", "A shallow copy creates a new object but inserts references to the same nested objects, while a deep copy recursively copies every nested object so the two structures share no references."),
    ("Python", "Medium", "What are *args and **kwargs used for?", "*args lets a function accept any number of positional arguments as a tuple, and **kwargs lets it accept any number of keyword arguments as a dictionary."),
    ("Python", "Hard", "Explain the Global Interpreter Lock (GIL) and its impact.", "The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, which limits true parallelism for CPU-bound multi-threaded code but doesn't affect multi-processing or I/O-bound concurrency."),
    ("Python", "Hard", "What are Python generators and why are they memory-efficient?", "Generators are functions that use 'yield' to produce values lazily, one at a time, instead of building the whole sequence in memory, which makes them ideal for processing large or infinite data streams."),
    ("Python", "Hard", "How does Python's garbage collection work?", "Python primarily uses reference counting to free objects as soon as their reference count hits zero, plus a generational cyclic garbage collector that periodically detects and cleans up reference cycles that counting alone can't catch."),

    # ---------------- OOP (10) ----------------
    ("OOP", "Easy", "Explain the four pillars of OOP.", "Encapsulation (bundling data and methods), Abstraction (hiding implementation detail), Inheritance (reusing behaviour from a parent class), and Polymorphism (same interface, different implementations)."),
    ("OOP", "Easy", "What is a class and what is an object?", "A class is a blueprint that defines attributes and behaviours, while an object is a concrete instance of that class created in memory at runtime."),
    ("OOP", "Easy", "What is encapsulation?", "Encapsulation means bundling data and the methods that operate on it inside a class, and restricting direct access to internal state using access modifiers to protect the object's integrity."),
    ("OOP", "Medium", "What is the difference between overloading and overriding?", "Overloading is defining multiple methods with the same name but different parameters in the same class; overriding is redefining a parent class method in a child class with an identical signature."),
    ("OOP", "Medium", "What is an abstract class and how does it differ from an interface?", "An abstract class can have both implemented and unimplemented methods and can hold state, while an interface (in most languages) only declares method signatures with no implementation or state."),
    ("OOP", "Medium", "Explain polymorphism with an example.", "Polymorphism lets objects of different classes respond to the same method call in their own way — e.g. calling speak() on a Dog and a Cat object produces different sounds through the same interface."),
    ("OOP", "Medium", "What is method resolution order (MRO)?", "MRO is the order in which a language looks up methods across a chain of inherited classes, especially important in multiple inheritance to resolve which parent's method is actually called."),
    ("OOP", "Hard", "What is the difference between composition and inheritance, and when would you prefer one?", "Inheritance models an 'is-a' relationship by extending a base class, while composition models a 'has-a' relationship by including other objects as fields; composition is generally preferred because it's more flexible and avoids tight coupling to a rigid class hierarchy."),
    ("OOP", "Hard", "Explain the SOLID principles briefly.", "SOLID stands for Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation and Dependency Inversion — five design guidelines that make object-oriented code easier to maintain, extend and test."),
    ("OOP", "Hard", "What is the diamond problem in multiple inheritance and how is it resolved?", "The diamond problem occurs when a class inherits from two classes that both inherit from a common base, creating ambiguity about which inherited method to use; languages resolve it via a linearized method resolution order (like C3 linearization in Python) or by disallowing multiple inheritance entirely."),

    # ---------------- DBMS (10) ----------------
    ("DBMS", "Easy", "What is a database and what is a DBMS?", "A database is an organized collection of structured data, and a DBMS (Database Management System) is the software that lets users create, read, update, delete and manage that data efficiently and securely."),
    ("DBMS", "Easy", "What is a primary key?", "A primary key is a column (or set of columns) that uniquely identifies every row in a table and cannot contain NULL values."),
    ("DBMS", "Easy", "What is the difference between a primary key and a foreign key?", "A primary key uniquely identifies rows within its own table, while a foreign key is a column that references the primary key of another table to establish a relationship between the two."),
    ("DBMS", "Medium", "What is normalization?", "Normalization is the process of organizing database tables to reduce redundancy and improve data integrity, typically progressing through 1NF, 2NF, 3NF and BCNF."),
    ("DBMS", "Medium", "Explain ACID properties.", "Atomicity, Consistency, Isolation and Durability are properties that guarantee reliable processing of database transactions, even in the presence of errors or concurrent access."),
    ("DBMS", "Medium", "What is the difference between DELETE, TRUNCATE and DROP?", "DELETE removes specific rows and can be rolled back, TRUNCATE removes all rows quickly and resets identity counters, while DROP removes the entire table structure from the database."),
    ("DBMS", "Medium", "What is an index and why is it useful?", "An index is a data structure (usually a B-tree) built on one or more columns that speeds up data retrieval at the cost of extra storage and slower writes, similar to an index in a book."),
    ("DBMS", "Hard", "What is the difference between clustered and non-clustered indexes?", "A clustered index determines the physical storage order of table rows and a table can have only one, while a non-clustered index is a separate structure that stores pointers back to the actual rows, and a table can have many."),
    ("DBMS", "Hard", "Explain database deadlocks and how they can be prevented.", "A deadlock occurs when two or more transactions each hold a lock the other needs and wait indefinitely; it can be mitigated by acquiring locks in a consistent order, using timeouts, or letting the DBMS detect and abort one of the transactions."),
    ("DBMS", "Hard", "What is the CAP theorem?", "The CAP theorem states that a distributed data store can only guarantee two of three properties at once — Consistency, Availability and Partition tolerance — forcing architects to make explicit trade-offs during network partitions."),

    # ---------------- SQL (10) ----------------
    ("SQL", "Easy", "What is the difference between WHERE and HAVING clauses?", "WHERE filters individual rows before any grouping happens, while HAVING filters groups after a GROUP BY aggregation has been applied."),
    ("SQL", "Easy", "What does the SELECT DISTINCT statement do?", "SELECT DISTINCT removes duplicate rows from the result set, returning only unique combinations of the selected columns."),
    ("SQL", "Easy", "What is a JOIN in SQL?", "A JOIN combines rows from two or more tables based on a related column, commonly using INNER, LEFT, RIGHT or FULL join types depending on which unmatched rows should be kept."),
    ("SQL", "Medium", "Explain the difference between INNER JOIN and LEFT JOIN.", "INNER JOIN returns only rows that have matching values in both tables, while LEFT JOIN returns all rows from the left table plus matching rows from the right table, filling unmatched columns with NULL."),
    ("SQL", "Medium", "What is a subquery and give an example use case.", "A subquery is a query nested inside another query, often used to filter results based on an aggregate, e.g. selecting employees whose salary is above the department's average salary computed in a subquery."),
    ("SQL", "Medium", "What is the difference between UNION and UNION ALL?", "UNION combines the results of two queries and removes duplicate rows, while UNION ALL combines them and keeps duplicates, making it faster since no de-duplication step is needed."),
    ("SQL", "Medium", "What are aggregate functions? Name a few.", "Aggregate functions compute a single summary value from multiple rows, such as COUNT(), SUM(), AVG(), MIN() and MAX(), and are commonly paired with GROUP BY."),
    ("SQL", "Hard", "How would you find the second-highest salary in an Employees table?", "One common approach is: SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees); another is using ORDER BY salary DESC with LIMIT/OFFSET or the window function DENSE_RANK()."),
    ("SQL", "Hard", "What is a window function and how does it differ from a normal aggregate?", "A window function performs a calculation across a set of related rows (a 'window') without collapsing them into a single row, unlike GROUP BY aggregates, e.g. RANK() OVER (PARTITION BY dept ORDER BY salary DESC) ranks employees within each department while still returning every row."),
    ("SQL", "Hard", "What is SQL injection and how do you prevent it?", "SQL injection is an attack where untrusted input is concatenated directly into a query to alter its logic; it's prevented by always using parameterized queries or prepared statements instead of building SQL strings via string concatenation."),

    # ---------------- CS Fundamentals / DSA (10) ----------------
    ("CS Fundamentals", "Easy", "What is the difference between a stack and a queue?", "A stack follows Last-In-First-Out (LIFO) ordering, while a queue follows First-In-First-Out (FIFO) ordering."),
    ("CS Fundamentals", "Easy", "What is Big-O notation used for?", "Big-O notation describes how an algorithm's running time or space requirement grows relative to the size of its input, focusing on the worst-case upper bound."),
    ("CS Fundamentals", "Easy", "What is a linked list and how does it differ from an array?", "A linked list is a sequence of nodes where each node points to the next, allowing O(1) insertion/deletion at known positions but only O(n) random access, unlike arrays which offer O(1) indexed access but costly insertions."),
    ("CS Fundamentals", "Medium", "Explain the time complexity of binary search.", "Binary search runs in O(log n) time because it halves the remaining search space at every step on a sorted array."),
    ("CS Fundamentals", "Medium", "What is a hash table and how does it achieve O(1) average lookup?", "A hash table maps keys to array indices using a hash function, so on average it can locate, insert or delete a value in constant time; collisions are handled via chaining or open addressing."),
    ("CS Fundamentals", "Medium", "What is the difference between BFS and DFS traversal?", "BFS (Breadth-First Search) explores a graph level by level using a queue, useful for shortest paths in unweighted graphs, while DFS (Depth-First Search) explores as deep as possible along each branch using a stack or recursion, useful for cycle detection and topological sorting."),
    ("CS Fundamentals", "Medium", "What is dynamic programming?", "Dynamic programming solves complex problems by breaking them into overlapping subproblems, solving each subproblem once and storing (memoizing) the result to avoid redundant recomputation."),
    ("CS Fundamentals", "Hard", "What is the difference between process and thread?", "A process is an independent program in execution with its own isolated memory space; a thread is a lightweight unit of execution within a process that shares memory with other threads of the same process, making communication cheaper but requiring careful synchronization."),
    ("CS Fundamentals", "Hard", "Explain the difference between a greedy algorithm and dynamic programming.", "A greedy algorithm makes the locally optimal choice at each step and never reconsiders it, which is fast but only guarantees a global optimum for certain problem structures; dynamic programming explores overlapping subproblems more thoroughly and guarantees optimality for a wider class of problems at the cost of more memory/time."),
    ("CS Fundamentals", "Hard", "What is amortized time complexity? Give an example.", "Amortized complexity averages the cost of an operation over a sequence of operations rather than looking at any single worst case, e.g. appending to a dynamic array is O(1) amortized even though occasional resizes cost O(n), because those resizes happen rarely enough to average out."),

    # ---------------- Operating Systems (10) ----------------
    ("Operating Systems", "Easy", "What is an operating system?", "An operating system is system software that manages hardware resources (CPU, memory, storage, I/O) and provides common services so applications can run without dealing with hardware directly."),
    ("Operating Systems", "Easy", "What is the difference between a process and a program?", "A program is passive code stored on disk, while a process is that program actively loaded into memory and being executed, with its own state, resources and program counter."),
    ("Operating Systems", "Easy", "What is virtual memory?", "Virtual memory is a technique that gives each process the illusion of a large, contiguous private address space by mapping it to physical memory and disk, enabling multitasking beyond physical RAM limits."),
    ("Operating Systems", "Medium", "What is a deadlock and what are its four necessary conditions?", "A deadlock is a state where processes wait indefinitely for resources held by each other; it requires mutual exclusion, hold-and-wait, no preemption and circular wait to all be present simultaneously."),
    ("Operating Systems", "Medium", "What is the difference between paging and segmentation?", "Paging divides memory into fixed-size pages that map to physical frames, avoiding external fragmentation; segmentation divides a program into variable-size logical segments (code, stack, heap) that map more naturally to program structure but can suffer external fragmentation."),
    ("Operating Systems", "Medium", "Explain the difference between preemptive and non-preemptive scheduling.", "In preemptive scheduling the OS can interrupt a running process to give the CPU to another, enabling better responsiveness; in non-preemptive scheduling a process keeps the CPU until it voluntarily finishes or blocks."),
    ("Operating Systems", "Medium", "What is a semaphore and how does it differ from a mutex?", "A semaphore is a counter-based synchronization primitive that can allow multiple threads access up to a limit, while a mutex is a binary lock owned by exactly one thread at a time, typically used to protect a single critical section."),
    ("Operating Systems", "Hard", "What is thrashing and how can it be avoided?", "Thrashing happens when a system spends more time swapping pages in and out of memory than doing useful work because processes don't have enough frames; it can be avoided with proper working-set based allocation, limiting the degree of multiprogramming, or adding more RAM."),
    ("Operating Systems", "Hard", "Explain the Banker's Algorithm.", "The Banker's Algorithm is a deadlock-avoidance strategy that simulates resource allocation before actually granting it, only approving a request if the resulting state is 'safe' — meaning there's still some order in which all processes could finish without deadlock."),
    ("Operating Systems", "Hard", "What is the difference between a monolithic kernel and a microkernel?", "A monolithic kernel runs most OS services (drivers, file systems, scheduling) in a single privileged address space for speed, while a microkernel keeps only the bare minimum (IPC, scheduling, basic memory management) in kernel space and runs other services as user-space processes for better isolation and stability."),

    # ---------------- Computer Networks (10) ----------------
    ("Computer Networks", "Easy", "What is the OSI model?", "The OSI model is a 7-layer conceptual framework (Physical, Data Link, Network, Transport, Session, Presentation, Application) that standardizes how different networking systems communicate."),
    ("Computer Networks", "Easy", "What is the difference between TCP and UDP?", "TCP is connection-oriented, reliable and ordered, using handshakes and acknowledgements, while UDP is connectionless and faster but offers no delivery or ordering guarantees, making it suited to real-time applications like video streaming."),
    ("Computer Networks", "Easy", "What is an IP address?", "An IP address is a unique numerical label assigned to each device on a network that allows it to be located and communicated with, following either the IPv4 or IPv6 addressing scheme."),
    ("Computer Networks", "Medium", "What happens when you type a URL into a browser and press Enter?", "The browser resolves the domain via DNS to an IP address, establishes a TCP connection (with a TLS handshake for HTTPS), sends an HTTP request, receives the response, and then renders the returned HTML/CSS/JS."),
    ("Computer Networks", "Medium", "What is DNS and why is it needed?", "DNS (Domain Name System) translates human-readable domain names into IP addresses, acting like the internet's phonebook so users don't have to memorize numeric addresses."),
    ("Computer Networks", "Medium", "Explain the three-way TCP handshake.", "The client sends a SYN packet, the server responds with a SYN-ACK, and the client replies with an ACK — after this exchange both sides agree on initial sequence numbers and a reliable connection is established."),
    ("Computer Networks", "Medium", "What is the difference between a hub, a switch and a router?", "A hub broadcasts incoming data to all ports blindly, a switch intelligently forwards data only to the correct port using MAC addresses, and a router forwards data between different networks using IP addresses."),
    ("Computer Networks", "Hard", "What is the difference between HTTP/1.1, HTTP/2 and HTTP/3?", "HTTP/1.1 sends one request per connection at a time (or with limited pipelining), HTTP/2 introduces multiplexing over a single TCP connection to avoid head-of-line blocking at the app layer, and HTTP/3 replaces TCP with QUIC (built on UDP) to also eliminate transport-level head-of-line blocking and speed up connection setup."),
    ("Computer Networks", "Hard", "What is NAT and why is it used?", "NAT (Network Address Translation) lets multiple devices on a private network share a single public IP address by rewriting packet headers at the router, which conserves IPv4 addresses and adds a layer of obscurity from the outside network."),
    ("Computer Networks", "Hard", "Explain how HTTPS ensures secure communication.", "HTTPS wraps HTTP inside a TLS layer that performs a handshake to authenticate the server (via certificates), negotiate a shared symmetric session key, and then encrypts all subsequent traffic, guaranteeing confidentiality, integrity and authenticity."),

    # ---------------- Web Development (10) ----------------
    ("Web Development", "Easy", "What is the difference between HTML, CSS and JavaScript?", "HTML defines the structure and content of a web page, CSS controls its visual styling and layout, and JavaScript adds interactivity and dynamic behaviour."),
    ("Web Development", "Easy", "What is the DOM?", "The DOM (Document Object Model) is a tree-like, in-memory representation of an HTML page that JavaScript can read and manipulate to dynamically change content, structure and styling."),
    ("Web Development", "Easy", "What is the difference between GET and POST HTTP methods?", "GET requests retrieve data and append parameters to the URL, making them cacheable and bookmarkable, while POST requests send data in the request body, are not cached, and are typically used to create or modify resources."),
    ("Web Development", "Medium", "What is REST and what makes an API RESTful?", "REST is an architectural style for APIs built around stateless requests, resource-based URLs, and standard HTTP verbs (GET/POST/PUT/DELETE); a RESTful API exposes resources as URLs and uses these verbs consistently rather than exposing custom RPC-style actions."),
    ("Web Development", "Medium", "What is the difference between localStorage, sessionStorage and cookies?", "localStorage persists data with no expiration until explicitly cleared, sessionStorage persists only for the browser tab's session, and cookies are smaller, sent with every HTTP request, and can carry an explicit expiry — making them the only option usable server-side."),
    ("Web Development", "Medium", "What is CORS and why does it exist?", "CORS (Cross-Origin Resource Sharing) is a browser security mechanism that blocks a web page from making requests to a different origin unless that origin's server explicitly allows it via response headers, preventing malicious cross-site data access."),
    ("Web Development", "Medium", "What is the difference between server-side rendering (SSR) and client-side rendering (CSR)?", "SSR renders the full HTML on the server for each request, giving faster first paint and better SEO, while CSR ships a mostly empty HTML shell and lets JavaScript render content in the browser, giving richer interactivity after the initial load."),
    ("Web Development", "Hard", "Explain how session-based authentication differs from token-based (JWT) authentication.", "Session-based auth stores user state on the server and identifies the client via a session ID cookie, requiring server-side lookups on every request; token-based auth issues a signed, self-contained JWT that the server can verify statelessly without a database lookup, which scales better horizontally but makes revoking a token harder."),
    ("Web Development", "Hard", "What is the critical rendering path?", "The critical rendering path is the sequence of steps a browser takes to convert HTML, CSS and JS into pixels on screen — parsing the DOM and CSSOM, building the render tree, computing layout, and finally painting — and optimizing it (e.g. minimizing render-blocking resources) improves perceived page load speed."),
    ("Web Development", "Hard", "What are Web Sockets and how do they differ from traditional HTTP polling?", "WebSockets establish a single persistent, full-duplex connection between client and server that both sides can push messages over at any time, whereas traditional polling repeatedly opens new HTTP requests to check for updates, which is far less efficient for real-time features like chat."),

    # ---------------- Java (10) ----------------
    ("Java", "Easy", "What is the difference between JDK, JRE and JVM?", "JDK is the full development kit (compiler + tools + JRE) used to build Java applications, JRE is the runtime environment needed to run them, and JVM is the virtual machine that actually executes the compiled bytecode."),
    ("Java", "Easy", "What is the difference between '==' and '.equals()' in Java?", "'==' compares object references (memory addresses) for primitives and objects, while '.equals()' compares the actual logical content of objects when properly overridden, as String and most wrapper classes do."),
    ("Java", "Easy", "What are the main pillars of Java's platform independence?", "Java source code is compiled into bytecode which any JVM can interpret, so the same compiled .class file can run unmodified on any platform that has a compatible JVM — 'write once, run anywhere.'"),
    ("Java", "Medium", "What is the difference between an abstract class and an interface in Java?", "An abstract class can hold state and both abstract and concrete methods but supports only single inheritance, while an interface traditionally holds only method signatures (plus default/static methods since Java 8) and a class can implement multiple interfaces."),
    ("Java", "Medium", "Explain checked vs unchecked exceptions.", "Checked exceptions (like IOException) must be declared or caught at compile time because they represent recoverable external conditions, while unchecked exceptions (like NullPointerException, extending RuntimeException) aren't enforced by the compiler and usually indicate programming bugs."),
    ("Java", "Medium", "What is the purpose of the 'final' keyword?", "'final' on a variable makes it a constant that can't be reassigned, on a method prevents it from being overridden, and on a class prevents it from being subclassed."),
    ("Java", "Medium", "What is garbage collection in Java?", "Garbage collection is the JVM's automatic process of identifying and reclaiming memory used by objects that are no longer reachable from any active reference, freeing developers from manual memory management."),
    ("Java", "Hard", "What is the difference between HashMap, LinkedHashMap and TreeMap?", "HashMap offers O(1) average access with no ordering guarantee, LinkedHashMap preserves insertion order using a backing linked list, and TreeMap keeps keys sorted by using a red-black tree, giving O(log n) operations."),
    ("Java", "Hard", "Explain how the JVM's memory is organized (heap, stack, metaspace).", "The heap stores objects and is shared across threads (managed by the garbage collector), the stack stores per-thread method call frames and local primitive variables, and metaspace (replacing PermGen since Java 8) stores class metadata."),
    ("Java", "Hard", "What is the difference between synchronized methods and using a ReentrantLock?", "'synchronized' is a simpler, JVM-managed intrinsic lock acquired and released automatically around a block or method, while ReentrantLock is an explicit, more flexible lock from java.util.concurrent that supports timed/interruptible acquisition, fairness policies, and multiple condition variables at the cost of requiring manual unlock in a finally block."),

    # ---------------- HR / Behavioral (10) ----------------
    ("HR", "Easy", "Tell me about yourself.", "Give a concise 60-90 second summary of your academic background, key technical skills, one standout project or achievement, and what kind of role you're looking for — keep it focused and relevant to the job."),
    ("HR", "Easy", "Why should we hire you?", "Connect your specific skills and project experience directly to the requirements of the role, backed by one concrete example of impact, and show genuine enthusiasm for what the company does."),
    ("HR", "Easy", "What are your strengths and weaknesses?", "Pick strengths genuinely relevant to the role with a quick example, and for weaknesses choose something real but non-critical, paired with what you're actively doing to improve it."),
    ("HR", "Medium", "Where do you see yourself in 5 years?", "Describe realistic growth within the field — deepening technical expertise, taking on more ownership or mentoring others — while showing that growing with this company specifically fits into that plan."),
    ("HR", "Medium", "Describe a time you faced a conflict in a team project and how you resolved it.", "Use the STAR method (Situation, Task, Action, Result): briefly set the scene, explain the disagreement, describe the concrete steps you took to communicate and compromise, and end with the positive outcome."),
    ("HR", "Medium", "Why do you want to work at this company?", "Show you've researched the company's products, values or recent work, and connect specific things you admire about them to your own skills and career goals rather than giving a generic answer."),
    ("HR", "Medium", "How do you handle tight deadlines or pressure?", "Explain your practical approach — prioritizing tasks, breaking work into milestones, communicating early if a deadline is at risk — ideally with a real example of delivering successfully under pressure."),
    ("HR", "Hard", "Tell me about a time you failed. What did you learn?", "Choose a genuine failure, own it honestly without over-explaining or blaming others, then focus most of the answer on the specific lesson learned and how you've applied it since — interviewers care more about the growth than the mistake."),
    ("HR", "Hard", "How do you handle receiving critical feedback from a manager?", "Show that you listen without getting defensive, ask clarifying questions to fully understand the concern, and describe a real example of turning feedback into a concrete change in your work."),
    ("HR", "Hard", "Why did you leave (or are leaving) your previous role/internship?", "Keep the answer forward-looking and professional — focus on what you're moving toward (growth, scope, technology) rather than complaining about the previous employer, even if the real reasons were negative."),
]


# ======================================================================
#  CODING PROBLEMS  —  wired to a real Python judge (see routes/coding.py)
#
#  Each entry: (title, difficulty, topic, description, sample_input,
#               sample_output, function_name, starter_code,
#               test_cases[json], hints[json])
# ======================================================================

def _tc(cases):
    return json.dumps(cases)


def _hints(hints):
    return json.dumps(hints)


def _tc_stdio(cases):
    """Test cases for stdin/stdout-judged (C / C++ / Java) problems.
    Each case is [stdin_text, expected_stdout_text] — stdout is compared
    after stripping trailing whitespace on each line."""
    return json.dumps(cases)


_PYTHON_PROBLEMS = [
    # ---------------- EASY (12) ----------------
    (
        "Two Sum", "Easy", "Arrays",
        "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to target. Return the indices sorted ascending.",
        "nums=[2,7,11,15], target=9", "[0, 1]",
        "two_sum",
        "def two_sum(nums, target):\n    # Return a list of the two indices whose values add up to target\n    pass\n",
        _tc([[[[2, 7, 11, 15], 9], [0, 1]], [[[3, 2, 4], 6], [1, 2]], [[[3, 3], 6], [0, 1]]]),
        _hints(["A brute-force O(n^2) double loop works but is slow for large inputs.",
                "Use a hash map to store each value's index as you scan once through the array.",
                "For each number, check if (target - number) has already been seen in the map."]),
    ),
    (
        "Reverse a String", "Easy", "Strings",
        "Write a function that reverses a string and returns the reversed version.",
        "s='hello'", "'olleh'",
        "reverse_string",
        "def reverse_string(s):\n    # Return the reverse of s\n    pass\n",
        _tc([[["hello"], "olleh"], [["Python"], "nohtyP"], [[""], ""]]),
        _hints(["Python slicing can reverse a sequence in one line.", "s[::-1] reverses a string.", "Return s[::-1]."]),
    ),
    (
        "Valid Parentheses", "Easy", "Stack",
        "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid (every bracket is closed by the same type in the correct order).",
        "s=\"()[]{}\"", "True",
        "is_valid_parentheses",
        "def is_valid_parentheses(s):\n    # Return True if brackets are balanced and correctly nested\n    pass\n",
        _tc([[["()[]{}"], True], [["(]"], False], [["{[]}"], True], [["("], False]]),
        _hints(["A stack is the natural fit for matching nested pairs.", "Push opening brackets; when you see a closer, pop and check it matches.", "At the end the stack must be empty for the string to be valid."]),
    ),
    (
        "FizzBuzz", "Easy", "Basics",
        "Return a list of strings for numbers 1 to n: 'Fizz' for multiples of 3, 'Buzz' for multiples of 5, 'FizzBuzz' for multiples of both, otherwise the number itself as a string.",
        "n=5", "['1','2','Fizz','4','Buzz']",
        "fizzbuzz",
        "def fizzbuzz(n):\n    # Return a list of length n following the FizzBuzz rules\n    pass\n",
        _tc([[[5], ["1", "2", "Fizz", "4", "Buzz"]], [[15], ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]]]),
        _hints(["Loop from 1 to n inclusive.", "Check divisibility by 15 first (both 3 and 5) before checking 3 or 5 individually.", "Use the modulo operator % to test divisibility."]),
    ),
    (
        "Palindrome Check", "Easy", "Strings",
        "Write a function that checks whether a given string is a palindrome (reads the same forwards and backwards).",
        "s='madam'", "True",
        "is_palindrome",
        "def is_palindrome(s):\n    # Return True if s reads the same forwards and backwards\n    pass\n",
        _tc([[["madam"], True], [["hello"], False], [["racecar"], True]]),
        _hints(["Compare the string with its reverse.", "s == s[::-1] gives you the answer directly."]),
    ),
    (
        "Factorial", "Easy", "Math",
        "Write a function that computes n! (the factorial of a non-negative integer n).",
        "n=5", "120",
        "factorial",
        "def factorial(n):\n    # Return n! (n factorial)\n    pass\n",
        _tc([[[5], 120], [[0], 1], [[7], 5040]]),
        _hints(["Factorial can be computed iteratively or recursively.", "0! is defined as 1 — handle that base case.", "Multiply numbers from 1 up to n."]),
    ),
    (
        "Find the Maximum", "Easy", "Arrays",
        "Given a list of integers, return the maximum value without using the built-in max() function.",
        "nums=[3,1,4,1,5,9,2,6]", "9",
        "find_max",
        "def find_max(nums):\n    # Return the largest value in nums (do not use max())\n    pass\n",
        _tc([[[[3, 1, 4, 1, 5, 9, 2, 6]], 9], [[[-5, -1, -10]], -1], [[[42]], 42]]),
        _hints(["Keep a running 'best so far' variable initialized to the first element.", "Loop through the rest of the list and update whenever you find something larger."]),
    ),
    (
        "Count Vowels", "Easy", "Strings",
        "Write a function that counts the number of vowels (a, e, i, o, u — case-insensitive) in a string.",
        "s='Programming'", "3",
        "count_vowels",
        "def count_vowels(s):\n    # Return the number of vowels (case-insensitive) in s\n    pass\n",
        _tc([[["Programming"], 3], [["AEIOU"], 5], [["xyz"], 0]]),
        _hints(["Convert the string to lowercase first to simplify comparison.", "Loop through each character and check membership in the set {'a','e','i','o','u'}."]),
    ),
    (
        "Sum of Digits", "Easy", "Math",
        "Write a function that returns the sum of the digits of a non-negative integer.",
        "n=12345", "15",
        "digit_sum",
        "def digit_sum(n):\n    # Return the sum of the digits of n\n    pass\n",
        _tc([[[12345], 15], [[0], 0], [[9], 9]]),
        _hints(["Convert the number to a string to iterate over its digits easily.", "Or repeatedly use n % 10 and n // 10 to peel off digits."]),
    ),
    (
        "Nth Fibonacci Number", "Easy", "Math",
        "Write a function that returns the nth Fibonacci number (0-indexed: fibonacci(0)=0, fibonacci(1)=1).",
        "n=6", "8",
        "fibonacci",
        "def fibonacci(n):\n    # Return the nth Fibonacci number (0-indexed)\n    pass\n",
        _tc([[[0], 0], [[1], 1], [[6], 8], [[10], 55]]),
        _hints(["An iterative approach avoids the exponential blowup of naive recursion.", "Keep two running variables representing the previous two Fibonacci numbers and update them in a loop."]),
    ),
    (
        "Missing Number", "Easy", "Arrays",
        "Given an array containing n distinct numbers taken from the range 0 to n (inclusive), find the one number that is missing from the array.",
        "nums=[3,0,1]", "2",
        "missing_number",
        "def missing_number(nums):\n    # nums has n distinct numbers from range 0..n with exactly one missing\n    pass\n",
        _tc([[[[3, 0, 1]], 2], [[[0, 1]], 2], [[[9,6,4,2,3,5,7,0,1]], 8]]),
        _hints(["The expected sum of 0..n can be computed with the formula n*(n+1)/2.", "Subtract the actual sum of the array from the expected sum to get the missing number."]),
    ),
    (
        "Anagram Check", "Easy", "Strings",
        "Write a function that checks whether two strings are anagrams of each other (contain exactly the same letters, possibly in a different order).",
        "s1='listen', s2='silent'", "True",
        "is_anagram",
        "def is_anagram(s1, s2):\n    # Return True if s1 and s2 are anagrams of each other\n    pass\n",
        _tc([[["listen", "silent"], True], [["rat", "car"], False], [["Dormitory", "Dirtyroom"], True]]),
        _hints(["If two strings are anagrams, sorting their characters produces identical results.", "sorted(s1) == sorted(s2) is a clean one-line check (remember case sensitivity)."]),
    ),

    # ---------------- MEDIUM (12) ----------------
    (
        "Longest Substring Without Repeating Characters", "Medium", "Strings",
        "Given a string s, find the length of the longest substring without repeating characters.",
        "s=\"abcabcbb\"", "3",
        "length_of_longest_substring",
        "def length_of_longest_substring(s):\n    # Return the length of the longest substring of s with no repeated characters\n    pass\n",
        _tc([[["abcabcbb"], 3], [["bbbbb"], 1], [["pwwkew"], 3], [[""], 0]]),
        _hints(["Use a sliding window with two pointers marking the current substring.", "Keep a dictionary mapping each character to the last index it was seen at.", "When you see a repeat inside the window, move the window's start just past its previous occurrence."]),
    ),
    (
        "Kth Largest Element", "Medium", "Heap",
        "Find the kth largest element in an unsorted array (1st largest is the maximum).",
        "nums=[3,2,1,5,6,4], k=2", "5",
        "kth_largest",
        "def kth_largest(nums, k):\n    # Return the k-th largest element in nums\n    pass\n",
        _tc([[[[3, 2, 1, 5, 6, 4], 2], 5], [[[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], 4]]),
        _hints(["Sorting the array descending and indexing works but is O(n log n).", "A min-heap of size k gives an O(n log k) approach for large inputs.", "For this exercise, sorted(nums, reverse=True)[k-1] is a perfectly valid solution."]),
    ),
    (
        "Word Break", "Medium", "Dynamic Programming",
        "Given a string s and a list of words word_dict, determine if s can be segmented into a space-separated sequence of one or more dictionary words.",
        "s='leetcode', word_dict=['leet','code']", "True",
        "word_break",
        "def word_break(s, word_dict):\n    # Return True if s can be fully segmented using words from word_dict\n    pass\n",
        _tc([[["leetcode", ["leet", "code"]], True], [["catsandog", ["cats", "dog", "sand", "and", "cat"]], False], [["applepenapple", ["apple", "pen"]], True]]),
        _hints(["This is a classic dynamic programming problem over string prefixes.", "Let dp[i] mean 's[:i]' can be segmented; dp[0] = True is your base case.", "dp[i] is True if there's some j < i where dp[j] is True and s[j:i] is in the dictionary."]),
    ),
    (
        "Container With Most Water", "Medium", "Two Pointers",
        "Given an array `heights` where heights[i] is the height of a vertical line at position i, find two lines that together with the x-axis form a container holding the most water. Return the max area.",
        "heights=[1,8,6,2,5,4,8,3,7]", "49",
        "max_area",
        "def max_area(heights):\n    # Return the maximum water area two lines can hold\n    pass\n",
        _tc([[[[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49], [[[1, 1]], 1]]),
        _hints(["A brute-force check of every pair is O(n^2) — there's a faster way.", "Use two pointers starting at both ends of the array, moving the shorter one inward.", "Area = min(height[left], height[right]) * (right - left); track the best seen."]),
    ),
    (
        "Subarray Sum Equals K", "Medium", "Hashing",
        "Given an array of integers nums and an integer k, return the total number of contiguous subarrays whose sum equals k.",
        "nums=[1,1,1], k=2", "2",
        "subarray_sum",
        "def subarray_sum(nums, k):\n    # Return the count of contiguous subarrays that sum to k\n    pass\n",
        _tc([[[[1, 1, 1], 2], 2], [[[1, 2, 3], 3], 2]]),
        _hints(["A brute-force nested loop is O(n^2) — a hash map can get you to O(n).", "Track a running prefix sum and store how many times each prefix sum value has occurred.", "For each running sum, check if (running_sum - k) has been seen before — that count is how many new subarrays end here."]),
    ),
    (
        "Rotate Array", "Medium", "Arrays",
        "Given an array, rotate it to the right by k steps and return the rotated array.",
        "nums=[1,2,3,4,5,6,7], k=3", "[5, 6, 7, 1, 2, 3, 4]",
        "rotate_array",
        "def rotate_array(nums, k):\n    # Return nums rotated right by k positions\n    pass\n",
        _tc([[[[1, 2, 3, 4, 5, 6, 7], 3], [5, 6, 7, 1, 2, 3, 4]], [[[1, 2], 1], [2, 1]]]),
        _hints(["k can be larger than len(nums) — reduce it first with k % len(nums).", "Python slicing makes this a one-liner: the last k elements followed by everything else."]),
    ),
    (
        "Triplet Sum to Zero", "Medium", "Two Pointers",
        "Given an array of integers, determine whether there exist three numbers that sum to zero.",
        "nums=[-1,0,1,2,-1,-4]", "True",
        "has_triplet_sum_zero",
        "def has_triplet_sum_zero(nums):\n    # Return True if any three numbers in nums sum to 0\n    pass\n",
        _tc([[[[-1, 0, 1, 2, -1, -4]], True], [[[1, 2, 3]], False]]),
        _hints(["Sort the array first — this makes a two-pointer scan possible.", "Fix one number, then use two pointers on the rest of the (sorted) array to find a pair that sums to its negative."]),
    ),
    (
        "Longest Common Prefix", "Medium", "Strings",
        "Write a function that finds the longest common prefix string among a list of strings. If there is none, return an empty string.",
        "strs=['flower','flow','flight']", "'fl'",
        "longest_common_prefix",
        "def longest_common_prefix(strs):\n    # Return the longest common prefix shared by all strings in strs\n    pass\n",
        _tc([[[["flower", "flow", "flight"]], "fl"], [[["dog", "racecar", "car"]], ""]]),
        _hints(["Start by assuming the first string is the whole prefix, then shrink it.", "For each subsequent string, trim the prefix from the end until the string actually starts with it."]),
    ),
    (
        "Move Zeroes", "Medium", "Arrays",
        "Given an array, move all zeroes to the end while maintaining the relative order of the non-zero elements. Return the resulting array.",
        "nums=[0,1,0,3,12]", "[1, 3, 12, 0, 0]",
        "move_zeroes",
        "def move_zeroes(nums):\n    # Return nums with all zeroes moved to the end, order of non-zeros preserved\n    pass\n",
        _tc([[[[0, 1, 0, 3, 12]], [1, 3, 12, 0, 0]], [[[0, 0, 1]], [1, 0, 0]]]),
        _hints(["Collect all non-zero elements first, preserving their order.", "Pad the result with the right number of zeroes to match the original length."]),
    ),
    (
        "Product of Array Except Self", "Medium", "Arrays",
        "Given an array nums, return an array where each element is the product of all other elements except itself, without using division.",
        "nums=[1,2,3,4]", "[24, 12, 8, 6]",
        "product_except_self",
        "def product_except_self(nums):\n    # Return array where result[i] = product of all nums except nums[i]\n    pass\n",
        _tc([[[[1, 2, 3, 4]], [24, 12, 8, 6]], [[[2, 3]], [3, 2]]]),
        _hints(["Do it in two passes: first compute the running product of everything to the left of each index.", "Then do a second pass right-to-left multiplying in the running product of everything to the right."]),
    ),
    (
        "First Non-Repeating Character", "Medium", "Hashing",
        "Given a string s, find the index of the first character that does not repeat. Return -1 if every character repeats.",
        "s='leetcode'", "0",
        "first_unique_char",
        "def first_unique_char(s):\n    # Return the index of the first non-repeating character, or -1\n    pass\n",
        _tc([[["leetcode"], 0], [["aabb"], -1]]),
        _hints(["First pass: count the frequency of every character.", "Second pass: return the index of the first character whose count is exactly 1."]),
    ),
    (
        "Course Schedule", "Medium", "Graph",
        "Given num_courses and a list of prerequisite pairs [a, b] meaning course a requires course b first, determine if it's possible to finish all courses (i.e. the prerequisite graph has no cycle).",
        "num_courses=2, prerequisites=[[1,0]]", "True",
        "can_finish",
        "def can_finish(num_courses, prerequisites):\n    # Return True if all courses can be finished (no cycle in the prerequisite graph)\n    pass\n",
        _tc([[[2, [[1, 0]]], True], [[2, [[1, 0], [0, 1]]], False]]),
        _hints(["This is a cycle-detection problem on a directed graph.", "Kahn's algorithm (topological sort via in-degree + queue) works well here.", "If you can process all nodes via BFS/topological sort, there's no cycle; if some nodes are left stuck, there is one."]),
    ),

    # ---------------- HARD (6) ----------------
    (
        "Trapping Rain Water", "Hard", "Two Pointers",
        "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "heights=[0,1,0,2,1,0,1,3,2,1,2,1]", "6",
        "trap_rain_water",
        "def trap_rain_water(heights):\n    # Return the total units of rain water trapped\n    pass\n",
        _tc([[[[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6], [[[4, 2, 0, 3, 2, 5]], 9]]),
        _hints(["Water trapped above any bar depends on the tallest bar to its left AND to its right.", "A two-pointer approach from both ends can track the running max on each side in a single pass.", "Move the pointer on the side with the smaller max, adding (that max - current height) to the total."]),
    ),
    (
        "Median of Two Sorted Arrays", "Hard", "Arrays",
        "Given two sorted arrays, return the median of the combined dataset.",
        "a=[1,3], b=[2]", "2.0",
        "find_median_sorted_arrays",
        "def find_median_sorted_arrays(a, b):\n    # Return the median (a float) of the merged sorted arrays a and b\n    pass\n",
        _tc([[[[1, 3], [2]], 2.0], [[[1, 2], [3, 4]], 2.5]]),
        _hints(["The direct O(n log n) approach: merge and sort both arrays, then pick the middle value(s).", "For an optimal O(log(min(m,n))) solution, use a binary search on the partition point of the smaller array — but merging is perfectly fine for this exercise."]),
    ),
    (
        "Longest Increasing Subsequence", "Hard", "Dynamic Programming",
        "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "nums=[10,9,2,5,3,7,101,18]", "4",
        "length_of_lis",
        "def length_of_lis(nums):\n    # Return the length of the longest strictly increasing subsequence\n    pass\n",
        _tc([[[[10, 9, 2, 5, 3, 7, 101, 18]], 4], [[[0, 1, 0, 3, 2, 3]], 4]]),
        _hints(["Let dp[i] be the length of the longest increasing subsequence ending exactly at index i.", "dp[i] = 1 + max(dp[j]) for every j < i where nums[j] < nums[i] (or 1 if none qualify).", "The answer is the maximum value across the whole dp array. This gives an O(n^2) solution; an O(n log n) patience-sorting approach also exists."]),
    ),
    (
        "N-Queens Count", "Hard", "Backtracking",
        "Given an integer n, return the number of distinct ways to place n queens on an n x n chessboard so that no two queens attack each other.",
        "n=4", "2",
        "total_n_queens",
        "def total_n_queens(n):\n    # Return the number of valid n-queens placements\n    pass\n",
        _tc([[[4], 2], [[1], 1], [[5], 10]]),
        _hints(["Place queens one row at a time using backtracking.", "Track which columns and which diagonals (row-col and row+col) are already occupied.", "Backtrack whenever a column or either diagonal is already taken; count successful placements when you reach the last row."]),
    ),
    (
        "Edit Distance", "Hard", "Dynamic Programming",
        "Given two strings word1 and word2, return the minimum number of single-character insertions, deletions or substitutions required to convert word1 into word2.",
        "word1='horse', word2='ros'", "3",
        "min_distance",
        "def min_distance(word1, word2):\n    # Return the minimum edit distance between word1 and word2\n    pass\n",
        _tc([[["horse", "ros"], 3], [["intention", "execution"], 5]]),
        _hints(["This is the classic Levenshtein distance dynamic programming problem.", "Build a 2D dp table where dp[i][j] is the edit distance between word1[:i] and word2[:j].", "If the current characters match, dp[i][j] = dp[i-1][j-1]; otherwise it's 1 + the minimum of insert, delete and substitute options."]),
    ),
    (
        "Group Anagrams Count", "Hard", "Hashing",
        "Given a list of strings, return the number of distinct anagram groups (i.e. how many unique 'letter signatures' exist across all the words).",
        "words=['eat','tea','tan','ate','nat','bat']", "3",
        "count_anagram_groups",
        "def count_anagram_groups(words):\n    # Return the number of distinct anagram groups among words\n    pass\n",
        _tc([[[["eat", "tea", "tan", "ate", "nat", "bat"]], 3], [[["a"]], 1]]),
        _hints(["Two words are anagrams if their sorted letters are identical.", "Build a set of the sorted-letter 'signature' for every word.", "The number of distinct signatures is the number of groups."]),
    ),
]

# ======================================================================
#  JAVASCRIPT  — function-based, judged the same way as Python
#  (each starter function is called directly and the return value is
#   compared to the expected result, so these use the [args, expected]
#   test-case format via _tc)
# ======================================================================
_JAVASCRIPT_PROBLEMS = [
    (
        "Sum of an Array", "Easy", "Arrays",
        "Write a function `sumArray(nums)` that returns the sum of all numbers in the array.",
        "nums=[1,2,3,4]", "10",
        "sumArray",
        "function sumArray(nums) {\n  // Return the sum of all numbers in nums\n}\n",
        _tc([[[[1, 2, 3, 4]], 10], [[[]], 0], [[[-1, 5, 2]], 6]]),
        _hints(["Use Array.prototype.reduce, or a simple for loop with a running total.", "reduce((acc, n) => acc + n, 0) does it in one line."]),
    ),
    (
        "Reverse a String", "Easy", "Strings",
        "Write a function `reverseString(s)` that returns the string reversed.",
        "s='hello'", "'olleh'",
        "reverseString",
        "function reverseString(s) {\n  // Return the reverse of s\n}\n",
        _tc([[["hello"], "olleh"], [["JS"], "SJ"], [[""], ""]]),
        _hints(["Split the string into characters, reverse the array, and join it back.", "s.split('').reverse().join('') works well in JS."]),
    ),
    (
        "Find the Maximum", "Easy", "Arrays",
        "Write a function `findMax(nums)` that returns the largest number in a non-empty array.",
        "nums=[3,9,2,7]", "9",
        "findMax",
        "function findMax(nums) {\n  // Return the largest number in nums\n}\n",
        _tc([[[[3, 9, 2, 7]], 9], [[[-5, -1, -9]], -1], [[[4]], 4]]),
        _hints(["Math.max(...nums) spreads the array as arguments to Math.max.", "Or track a running maximum with a for loop."]),
    ),
    (
        "Count Vowels", "Easy", "Strings",
        "Write a function `countVowels(s)` that returns how many vowels (a, e, i, o, u — case-insensitive) appear in the string.",
        "s='Hello World'", "3",
        "countVowels",
        "function countVowels(s) {\n  // Return the count of vowels in s\n}\n",
        _tc([[["Hello World"], 3], [["xyz"], 0], [["AEIOUaeiou"], 10]]),
        _hints(["Lower-case the string first so you only check one case.", "Loop through the characters and test membership in 'aeiou'."]),
    ),
    (
        "FizzBuzz", "Easy", "Basics",
        "Write a function `fizzBuzz(n)` returning an array of strings for 1..n: 'Fizz' for multiples of 3, 'Buzz' for multiples of 5, 'FizzBuzz' for both, else the number as a string.",
        "n=5", "['1','2','Fizz','4','Buzz']",
        "fizzBuzz",
        "function fizzBuzz(n) {\n  // Return an array of length n following the FizzBuzz rules\n}\n",
        _tc([[[5], ["1", "2", "Fizz", "4", "Buzz"]], [[15], ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]]]),
        _hints(["Loop from 1 to n inclusive with a for loop.", "Check divisibility by 15 before checking 3 or 5 individually.", "n % 3 === 0 tests divisibility by 3 in JS."]),
    ),
    (
        "Check for Palindrome", "Medium", "Strings",
        "Write a function `isPalindrome(s)` that returns true if s reads the same forwards and backwards.",
        "s='racecar'", "true",
        "isPalindrome",
        "function isPalindrome(s) {\n  // Return true if s is a palindrome\n}\n",
        _tc([[["racecar"], True], [["hello"], False], [["a"], True]]),
        _hints(["Compare the string to its reverse.", "s === s.split('').reverse().join('') gives the answer directly."]),
    ),
]

# ======================================================================
#  C / C++ / JAVA  — stdio-judged: the learner writes a *full program*
#  that reads input from stdin and prints the answer to stdout. The
#  judge compiles the program and compares its printed output (trimmed
#  per line) against the expected text for each test case.
# ======================================================================
_C_PROBLEMS = [
    (
        "Sum of Two Numbers", "Easy", "Basics",
        "Read two integers a and b from standard input (space or newline separated) and print their sum.",
        "5 7", "12",
        None,
        "#include <stdio.h>\n\nint main(void) {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n    // TODO: print a + b\n    return 0;\n}\n",
        _tc_stdio([["5 7", "12"], ["-3 10", "7"], ["0 0", "0"]]),
        _hints(["scanf(\"%d %d\", &a, &b) reads two space-separated integers.", "printf(\"%d\\n\", a + b) prints the sum."]),
    ),
    (
        "Reverse a String", "Easy", "Strings",
        "Read a single line of text and print it reversed.",
        "hello", "olleh",
        None,
        "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char s[1000];\n    fgets(s, sizeof(s), stdin);\n    s[strcspn(s, \"\\n\")] = 0;\n    // TODO: print s reversed\n    return 0;\n}\n",
        _tc_stdio([["hello", "olleh"], ["C programming", "gnimmargorp C"], ["a", "a"]]),
        _hints(["Find the string length with strlen, then print characters from the last index down to 0.", "for (int i = strlen(s) - 1; i >= 0; i--) putchar(s[i]);"]),
    ),
    (
        "Factorial", "Easy", "Math",
        "Read a non-negative integer n and print n! (n factorial).",
        "5", "120",
        None,
        "#include <stdio.h>\n\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    // TODO: compute and print n!\n    return 0;\n}\n",
        _tc_stdio([["5", "120"], ["0", "1"], ["7", "5040"]]),
        _hints(["Use a long or long long accumulator, factorials grow fast.", "Multiply a running total by i for i from 1 to n."]),
    ),
    (
        "Check Prime", "Medium", "Math",
        "Read an integer n and print \"Prime\" if it is a prime number, otherwise print \"Not Prime\".",
        "13", "Prime",
        None,
        "#include <stdio.h>\n\nint main(void) {\n    int n;\n    scanf(\"%d\", &n);\n    // TODO: print \"Prime\" or \"Not Prime\"\n    return 0;\n}\n",
        _tc_stdio([["13", "Prime"], ["12", "Not Prime"], ["1", "Not Prime"], ["2", "Prime"]]),
        _hints(["Numbers less than 2 are never prime.", "You only need to test divisors up to sqrt(n) for efficiency."]),
    ),
]

_CPP_PROBLEMS = [
    (
        "Sum of an Array", "Easy", "Arrays",
        "Read an integer n, then n integers, and print their sum.",
        "n=4, then: 1 2 3 4", "10",
        None,
        "#include <iostream>\nusing namespace std;\n\nint main() {\n    int n;\n    cin >> n;\n    int sum = 0;\n    for (int i = 0; i < n; i++) {\n        int x;\n        cin >> x;\n        // TODO: accumulate into sum\n    }\n    cout << sum << endl;\n    return 0;\n}\n",
        _tc_stdio([["4\n1 2 3 4", "10"], ["3\n-1 -2 -3", "-6"], ["1\n0", "0"]]),
        _hints(["Add each number to `sum` as you read it inside the loop.", "cout << sum << endl; prints the final total."]),
    ),
    (
        "Palindrome Check", "Easy", "Strings",
        "Read a single word and print \"Yes\" if it's a palindrome, otherwise print \"No\".",
        "madam", "Yes",
        None,
        "#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s;\n    cin >> s;\n    // TODO: print \"Yes\" or \"No\"\n    return 0;\n}\n",
        _tc_stdio([["madam", "Yes"], ["hello", "No"], ["a", "Yes"]]),
        _hints(["Build the reverse of s with std::reverse or a manual loop and compare.", "string r(s.rbegin(), s.rend()); then compare r == s."]),
    ),
    (
        "Nth Fibonacci Number", "Medium", "Math",
        "Read an integer n (0-indexed, fib(0)=0, fib(1)=1) and print the nth Fibonacci number.",
        "7", "13",
        None,
        "#include <iostream>\nusing namespace std;\n\nint main() {\n    int n;\n    cin >> n;\n    // TODO: compute and print fib(n)\n    return 0;\n}\n",
        _tc_stdio([["7", "13"], ["0", "0"], ["1", "1"], ["10", "55"]]),
        _hints(["Build it iteratively with two running variables instead of plain recursion — it's much faster.", "Swap a, b = b, a + b in a loop n times, starting from a=0, b=1."]),
    ),
    (
        "Count Vowels", "Easy", "Strings",
        "Read a line of text and print how many vowels (a, e, i, o, u, case-insensitive) it contains.",
        "Hello World", "3",
        None,
        "#include <iostream>\n#include <string>\n#include <cctype>\nusing namespace std;\n\nint main() {\n    string s;\n    getline(cin, s);\n    // TODO: count and print the number of vowels\n    return 0;\n}\n",
        _tc_stdio([["Hello World", "3"], ["xyz", "0"], ["AEIOUaeiou", "10"]]),
        _hints(["Lower-case each character with tolower() before checking.", "Check membership against the string \"aeiou\"."]),
    ),
]

_JAVA_PROBLEMS = [
    (
        "Add Two Numbers", "Easy", "Basics",
        "Read two integers a and b (space or newline separated) and print their sum. The public class must be named `Main`.",
        "5 7", "12",
        None,
        "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int a = sc.nextInt();\n        int b = sc.nextInt();\n        // TODO: print a + b\n    }\n}\n",
        _tc_stdio([["5 7", "12"], ["-3 10", "7"], ["0 0", "0"]]),
        _hints(["Scanner.nextInt() reads one integer at a time.", "System.out.println(a + b); prints the sum."]),
    ),
    (
        "Reverse a String", "Easy", "Strings",
        "Read a line of text and print it reversed. The public class must be named `Main`.",
        "hello", "olleh",
        None,
        "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.nextLine();\n        // TODO: print s reversed\n    }\n}\n",
        _tc_stdio([["hello", "olleh"], ["Java rocks", "skcor avaJ"], ["a", "a"]]),
        _hints(["new StringBuilder(s).reverse().toString() reverses a string in one line.", "Print the result with System.out.println."]),
    ),
    (
        "Largest of Three", "Easy", "Basics",
        "Read three integers and print the largest one. The public class must be named `Main`.",
        "4 9 2", "9",
        None,
        "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int a = sc.nextInt(), b = sc.nextInt(), c = sc.nextInt();\n        // TODO: print the largest of a, b, c\n    }\n}\n",
        _tc_stdio([["4 9 2", "9"], ["-1 -5 -2", "-1"], ["7 7 7", "7"]]),
        _hints(["Math.max(a, Math.max(b, c)) finds the largest of three values."]),
    ),
    (
        "Check Prime", "Medium", "Math",
        "Read an integer n and print \"Prime\" if it is prime, otherwise print \"Not Prime\". The public class must be named `Main`.",
        "13", "Prime",
        None,
        "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        // TODO: print \"Prime\" or \"Not Prime\"\n    }\n}\n",
        _tc_stdio([["13", "Prime"], ["12", "Not Prime"], ["1", "Not Prime"], ["2", "Prime"]]),
        _hints(["Numbers less than 2 are never prime.", "Only test divisors up to Math.sqrt(n)."]),
    ),
]

# ======================================================================
#  HTML / CSS  — live-preview practice (not auto-graded). The learner
#  edits one combined HTML+CSS file and sees an instant rendered
#  preview instead of pass/fail test cases — the right fit for markup
#  and styling, which has no single "correct return value" to check.
# ======================================================================
_WEB_PROBLEMS = [
    (
        "Build a Profile Card", "Easy", "Layout",
        "Build a simple profile card: a rounded container with an avatar circle, a name, a short bio line, and a 'Follow' button. Use the live preview to check your layout as you go.",
        "—", "A styled card matching the description",
        None,
        "<!-- Edit the HTML and CSS below, the preview updates as you type -->\n<div class=\"card\">\n  <div class=\"avatar\"></div>\n  <h3>Your Name</h3>\n  <p>A short one-line bio goes here.</p>\n  <button>Follow</button>\n</div>\n\n<style>\n.card {\n  /* TODO: give the card a max-width, padding, rounded corners and a subtle shadow */\n}\n.avatar {\n  width: 80px;\n  height: 80px;\n  border-radius: 50%;\n  background: #cbd5e1;\n  margin: 0 auto 12px;\n}\n</style>\n",
        None,
        _hints(["border-radius: 50% turns a square div into a perfect circle for the avatar.", "box-shadow: 0 4px 12px rgba(0,0,0,0.1) gives a subtle card shadow.", "text-align: center on the card keeps everything neatly centered."]),
    ),
    (
        "Build a Responsive Navbar", "Medium", "Layout",
        "Build a horizontal navbar with a logo on the left and 3-4 nav links on the right, spaced evenly using Flexbox.",
        "—", "A horizontal navbar with logo + links",
        None,
        "<nav class=\"navbar\">\n  <div class=\"logo\">Brand</div>\n  <ul class=\"nav-links\">\n    <li><a href=\"#\">Home</a></li>\n    <li><a href=\"#\">About</a></li>\n    <li><a href=\"#\">Contact</a></li>\n  </ul>\n</nav>\n\n<style>\n.navbar {\n  /* TODO: use display: flex and justify-content to place logo left, links right */\n}\n.nav-links {\n  list-style: none;\n  display: flex;\n  gap: 20px;\n}\n</style>\n",
        None,
        _hints(["display: flex plus justify-content: space-between spreads the logo and links to opposite ends.", "align-items: center vertically centers everything in the bar."]),
    ),
    (
        "Center a Div (Classic Challenge)", "Easy", "Layout",
        "Perfectly center a single box both horizontally and vertically inside its full-height container — the classic CSS interview challenge.",
        "—", "A box centered both ways on the page",
        None,
        "<div class=\"container\">\n  <div class=\"box\">Centered!</div>\n</div>\n\n<style>\n.container {\n  height: 100vh;\n  /* TODO: center .box both horizontally and vertically */\n}\n.box {\n  width: 120px;\n  height: 120px;\n  background: #6366f1;\n  color: white;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n</style>\n",
        None,
        _hints(["Flexbox on the parent makes this a two-line fix.", "display: flex; align-items: center; justify-content: center; on .container centers the child both ways."]),
    ),
    (
        "Build a Pricing Card Group", "Medium", "Layout",
        "Build three pricing cards side by side (Basic / Pro / Premium), each with a plan name, a price, and a list of 3 features, laid out in a row with even spacing.",
        "—", "Three side-by-side pricing cards",
        None,
        "<div class=\"pricing\">\n  <div class=\"plan\"><h4>Basic</h4><p class=\"price\">$9/mo</p></div>\n  <div class=\"plan\"><h4>Pro</h4><p class=\"price\">$19/mo</p></div>\n  <div class=\"plan\"><h4>Premium</h4><p class=\"price\">$39/mo</p></div>\n</div>\n\n<style>\n.pricing {\n  /* TODO: lay the .plan cards out in a row with gap and centering */\n}\n.plan {\n  border: 1px solid #e2e8f0;\n  border-radius: 12px;\n  padding: 20px;\n  width: 180px;\n  text-align: center;\n}\n</style>\n",
        None,
        _hints(["display: flex with a gap on .pricing spaces the cards evenly.", "justify-content: center centers the whole row if it doesn't fill the width."]),
    ),
]

CODING_PROBLEMS = (
    [t + ("python", "function") for t in _PYTHON_PROBLEMS]
    + [t + ("javascript", "function") for t in _JAVASCRIPT_PROBLEMS]
    + [t + ("c", "stdio") for t in _C_PROBLEMS]
    + [t + ("cpp", "stdio") for t in _CPP_PROBLEMS]
    + [t + ("java", "stdio") for t in _JAVA_PROBLEMS]
    + [t + ("html_css", "preview") for t in _WEB_PROBLEMS]
)


# ======================================================================
#  COMPANIES
# ======================================================================
COMPANIES = [
    ("TCS", "IT Services", "Software Engineer Trainee", "3.5-7 LPA", "Pan India", "60% in 10th, 12th & Degree, no active backlogs", "bi-building"),
    ("Infosys", "IT Services", "Systems Engineer", "3.6-8 LPA", "Pan India", "65% throughout academics", "bi-building-fill"),
    ("Wipro", "IT Services", "Project Engineer", "3.5-6.5 LPA", "Pan India", "60% aggregate, no standing arrears", "bi-buildings"),
    ("Amazon", "E-commerce / Cloud", "SDE-1", "18-28 LPA", "Bengaluru, Hyderabad", "Strong DSA & CS fundamentals", "bi-bag-check"),
    ("Google", "Product / Cloud", "Software Engineer", "25-45 LPA", "Bengaluru, Hyderabad", "Excellent CS fundamentals, DSA, System Design", "bi-google"),
    ("Microsoft", "Product / Cloud", "SDE", "22-40 LPA", "Hyderabad, Bengaluru", "Strong problem solving & CS core", "bi-microsoft"),
    ("Accenture", "IT Consulting", "Associate Software Engineer", "4.5-7 LPA", "Pan India", "65% throughout, no backlogs", "bi-diagram-3"),
    ("Cognizant", "IT Services", "Programmer Analyst", "4-6.5 LPA", "Pan India", "60% aggregate", "bi-cpu"),
    ("Zoho", "Product", "Member Technical Staff", "4.5-8 LPA", "Chennai", "Strong coding & aptitude, own selection test", "bi-code-square"),
    ("Deloitte", "Consulting", "Analyst", "4.5-7.5 LPA", "Pan India", "60% throughout academics", "bi-graph-up-arrow"),
]

# ======================================================================
#  GROUP DISCUSSION TOPICS  —  (category, title, difficulty, description)
# ======================================================================
GD_TOPICS = [
    # ---------------- Technology ----------------
    ("Technology", "Artificial Intelligence: Opportunity or Threat to Jobs?", "Medium",
     "Discuss whether AI adoption will create more jobs than it displaces, and how students should prepare."),
    ("Technology", "Should Generative AI Tools Be Allowed in Academic Work?", "Medium",
     "Debate the role of tools like ChatGPT/Gemini in assignments, learning, and academic integrity."),
    ("Technology", "Cybersecurity: Is India Prepared for the Next Big Cyber Attack?", "Hard",
     "Discuss India's cybersecurity readiness across government, banking, and personal data."),
    ("Technology", "Social Media: Connecting the World or Isolating It?", "Easy",
     "Discuss the dual impact of social media on real-world relationships and mental health."),
    ("Technology", "Automation and the Future of Blue-Collar Jobs", "Medium",
     "Discuss how automation and robotics are reshaping manufacturing and manual labor jobs."),
    ("Technology", "Is the Future of Software Development Low-Code/No-Code?", "Medium",
     "Debate whether traditional programming skills will remain essential as low-code tools grow."),
    ("Technology", "Digital Transformation in Government Services", "Medium",
     "Discuss the benefits and challenges of digitizing public services in India."),
    ("Technology", "Should Self-Driving Cars Be Allowed on Indian Roads?", "Hard",
     "Discuss readiness of infrastructure, law, and safety for autonomous vehicles in India."),

    # ---------------- Education ----------------
    ("Education", "Online Education vs Traditional Classroom Learning", "Easy",
     "Compare effectiveness, accessibility, and engagement of online vs offline education."),
    ("Education", "Role of AI in Personalized Education", "Medium",
     "Discuss how AI-driven tools could adapt learning to individual student needs."),
    ("Education", "Skill-Based Education vs Degree-Based Education", "Medium",
     "Debate whether certifications and skills should matter more than traditional degrees."),
    ("Education", "Is College Education Still Relevant for a Tech Career?", "Medium",
     "Discuss whether a formal degree is necessary given the rise of self-taught developers."),
    ("Education", "Should Coding Be a Mandatory School Subject?", "Easy",
     "Discuss the case for and against introducing programming from school level."),
    ("Education", "Examination Reforms: Are Marks the Right Measure of Learning?", "Medium",
     "Discuss alternatives to traditional exam-based evaluation systems."),

    # ---------------- Society ----------------
    ("Society", "Impact of Social Media on Mental Health of Youth", "Medium",
     "Discuss the psychological effects of constant social media use among students."),
    ("Society", "Work-Life Balance in the Age of Hustle Culture", "Easy",
     "Discuss whether hustle culture is sustainable or harmful to long-term wellbeing."),
    ("Society", "Digital Addiction: A Growing Concern for Gen Z", "Medium",
     "Discuss screen-time habits and their effects on productivity and relationships."),
    ("Society", "Youth and Technology: Empowerment or Dependency?", "Medium",
     "Discuss whether growing up with constant tech access empowers or weakens young people."),
    ("Society", "Gender Diversity in the Tech Industry", "Medium",
     "Discuss barriers to and benefits of improving gender balance in tech workplaces."),
    ("Society", "Urban vs Rural: Should IT Companies Set Up in Tier-2 Cities?", "Easy",
     "Discuss the impact of decentralizing tech jobs beyond metro cities."),

    # ---------------- Business ----------------
    ("Business", "Startups vs Corporate Jobs: What Should Freshers Choose?", "Easy",
     "Compare stability, growth, and learning between joining a startup or a large company."),
    ("Business", "Entrepreneurship: Is India's Startup Boom Sustainable?", "Hard",
     "Discuss funding trends, failure rates, and long-term viability of India's startup ecosystem."),
    ("Business", "Remote Work: The Future of the Workplace?", "Medium",
     "Discuss whether remote/hybrid work will remain standard post-pandemic."),
    ("Business", "What Makes a Good Leader in a Tech Team?", "Easy",
     "Discuss qualities of effective leadership in fast-moving technology teams."),
    ("Business", "Innovation vs Execution: Which Matters More for a Startup?", "Medium",
     "Debate whether breakthrough ideas or disciplined execution drives startup success."),
    ("Business", "Should Freshers Negotiate Their First Salary?", "Easy",
     "Discuss whether and how entry-level candidates should approach salary negotiation."),

    # ---------------- Abstract ----------------
    ("Abstract", "What Does Success Really Mean?", "Easy",
     "An open-ended discussion on defining and measuring personal success."),
    ("Abstract", "Is Failure Necessary for Growth?", "Easy",
     "Discuss the role failure plays in personal and professional development."),
    ("Abstract", "Time: Our Most Valuable Resource?", "Medium",
     "An abstract discussion on time management and prioritization in life and career."),
    ("Abstract", "Change Is the Only Constant — Do You Agree?", "Medium",
     "Discuss how individuals and organizations should respond to constant change."),
    ("Abstract", "Knowledge vs Wisdom: What Matters More?", "Hard",
     "An abstract discussion distinguishing information/knowledge from applied wisdom."),
    ("Abstract", "Opportunity Knocks Only Once — True or False?", "Easy",
     "Discuss whether missed opportunities can truly be recovered or recreated."),
]
