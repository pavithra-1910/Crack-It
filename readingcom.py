import firebase_admin  # ✅ Add this line!
from firebase_admin import credentials, db

# Firebase Initialization
cred = credentials.Certificate("crackit-8371d-firebase-adminsdk-fbsvc-ce1f4e8eb4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com'
})

critical_reasoning_data = [
    {
        "question": "If all cats are animals, and all animals have fur, what can be concluded?",
        "options": ["Cats have fur.", "Cats are animals.", "All animals are cats.", "Some animals do not have fur."],
        "answer": "Cats have fur.",
        "type": "Critical Reasoning"
    },
    {
        "question": "John is taller than Sarah, and Sarah is taller than Emily. Who is the shortest?",
        "options": ["John", "Sarah", "Emily", "Cannot be determined"],
        "answer": "Emily",
        "type": "Critical Reasoning"
    },
    {
        "question": "If some A's are B's and all B's are C's, can it be concluded that some A's are C's?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "If the weather is rainy, then the ground is wet. The ground is wet. Can we conclude that the weather was rainy?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "No",
        "type": "Critical Reasoning"
    },
    {
        "question": "If all students are required to submit their assignments by Friday, and John is a student, when must John submit his assignment?",
        "options": ["By Friday", "By Thursday", "Anytime", "None of the above"],
        "answer": "By Friday",
        "type": "Critical Reasoning"
    },
    {
        "question": "No birds are mammals. Can we conclude that no mammals are birds?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "If Jane studies every day, she will pass the exam. Jane has been studying every day. What can be concluded?",
        "options": ["Jane will pass the exam.", "Jane may pass the exam.", "Jane will fail the exam.", "None of the above"],
        "answer": "Jane may pass the exam.",
        "type": "Critical Reasoning"
    },
    {
        "question": "If you are allergic to peanuts, you should avoid peanuts. John eats peanuts regularly. What can be concluded about John?",
        "options": ["John is not allergic to peanuts.", "John is allergic to peanuts.", "John may or may not be allergic to peanuts.", "None of the above"],
        "answer": "John may or may not be allergic to peanuts.",
        "type": "Critical Reasoning"
    },
    {
        "question": "All dogs are animals. Some animals are friendly. Can it be concluded that some dogs are friendly?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Cannot be determined",
        "type": "Critical Reasoning"
    },
    {
        "question": "The book is on the table. If the book is not on the table, where can it be?",
        "options": ["On the floor", "On a shelf", "On the chair", "All of the above"],
        "answer": "All of the above",
        "type": "Critical Reasoning"
    },
    {
        "question": "If it rains, the ground will be wet. It is not raining. Can the ground still be wet?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "A man is taller than his brother, but shorter than his father. Who is the tallest?",
        "options": ["The man", "The brother", "The father", "Cannot be determined"],
        "answer": "The father",
        "type": "Critical Reasoning"
    },
    {
        "question": "Some oranges are sweet. Can we conclude that all oranges are sweet?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "No",
        "type": "Critical Reasoning"
    },
    {
        "question": "Some people like chocolate, and all chocolate is sweet. Can we conclude that all people who like chocolate like sweet things?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "If I eat pizza, I will feel happy. I am feeling happy. Can we conclude that I ate pizza?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "No",
        "type": "Critical Reasoning"
    },
    {
        "question": "The sky is blue. If the sky is blue, we will go for a walk. What is the logical conclusion?",
        "options": ["We will go for a walk.", "We will not go for a walk.", "The sky is blue.", "None of the above"],
        "answer": "We will go for a walk.",
        "type": "Critical Reasoning"
    },
    {
        "question": "If a person works hard, they will succeed. John worked hard. What can we conclude?",
        "options": ["John will succeed.", "John may succeed.", "John will not succeed.", "None of the above"],
        "answer": "John may succeed.",
        "type": "Critical Reasoning"
    },
    {
        "question": "If all the books are on the shelf, and some books are old, can we conclude that some old books are on the shelf?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "All fruit is healthy. Apples are fruit. Are apples healthy?",
        "options": ["Yes", "No", "Cannot be determined", "None of the above"],
        "answer": "Yes",
        "type": "Critical Reasoning"
    },
    {
        "question": "If it is sunny outside, I will go swimming. It is sunny outside. What is the logical conclusion?",
        "options": ["I will go swimming.", "I will not go swimming.", "I am already swimming.", "None of the above"],
        "answer": "I will go swimming.",
        "type": "Critical Reasoning"
    }
]

# question to Firebase
ref = db.reference('critical_reasoning')
for item in critical_reasoning_data:
    ref.push(item)

print("✅ All Critical Reasoning questions uploaded to Firebase successfully!")


