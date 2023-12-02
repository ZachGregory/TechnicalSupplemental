import sqlite3
import random

# Create SQLite database
conn = sqlite3.connect('scav.db')
cursor = conn.cursor()

if cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='Users' ''').fetchone() is None:
    # Create Users table
    cursor.execute('''CREATE TABLE Users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

if cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='Scavenger' ''').fetchone() is None:
    # Create Scavenger table
    cursor.execute('''CREATE TABLE Scavenger
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    answer TEXT)''')

if cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='UserQuestions' ''').fetchone() is None:
    # Create Association table
    cursor.execute('''CREATE TABLE UserQuestions
                    (user_id INTEGER,
                    question_id INTEGER)''')

# Insert random users into Users table
users = [('Buster Biggs',), ('Kyra Yelland',), ('Riley Rogers',)]
cursor.executemany('INSERT INTO Users (name) VALUES (?)', users)

# Insert random questions into Scavenger table
questions = [('What is the tallest building on earth?', 'Dunton Tower'),
                ('?!', 'Ollies?!'),
                ('What is the best place to hang out?', "Leo's Lounge"),
                ('EngFrosh?', 'BestFrosh!'),
                ('Dont get bored, dont get lost, ', 'dont get dead')]

cursor.executemany('INSERT INTO Scavenger (question, answer) VALUES (?, ?)', questions)

# Associate users with random questions
user_questions = []
for user_id in range(1, 4):
    question_ids = random.sample(range(1, 6), 3)
    for question_id in question_ids:
        user_questions.append((user_id, question_id))
cursor.executemany('INSERT INTO UserQuestions (user_id, question_id) VALUES (?, ?)', user_questions)

# Output Users table
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print("Users:")
for user in users:
    print(user)

# Output Scavenger table
cursor.execute('SELECT * FROM Scavenger')
scavenger = cursor.fetchall()
print("\nScavenger Questions:")
for question in scavenger:
    print(question)

# Output user's name and answers to completed questions
cursor.execute('''SELECT Users.name, Scavenger.answer
                    FROM Users
                    JOIN UserQuestions ON Users.id = UserQuestions.user_id
                    JOIN Scavenger ON UserQuestions.question_id = Scavenger.id
                    ORDER BY Users.id''')
user_answers = cursor.fetchall()

print("\nUser Answers:")

if user_answers[0][0] is not None:
    print(user_answers[0][0]+":")
person = user_answers[0][0]
for user_answer in user_answers:
    if user_answer[0] != person:
        print(user_answer[0]+":")
        person = user_answer[0]
    person = user_answer[0]
    print("\t" + user_answer[1])

# Close the database connection
conn.close()
