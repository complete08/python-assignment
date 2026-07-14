questions = [
    "What is the capital of Nigeria?",
    "How many continents are there?",
    "What does CPU stand for?",
    "In what year did Nigeria gain independence?",
    "What planet is closest to the sun?"
]

answers = ["abuja", "7", "central processing unit", "1960", "mercury"]

score = 0

print("=== PYTHON QUIZ GAME ===")

for i in range(len(questions)):
    print(f"Question {i + 1}: {questions[i]}")
    player_answer = input("Your answer: ").lower()

    if player_answer == answers[i]:
        score += 1
        print("Correct!")
    else:
        print(f"Wrong! The answer is: {answers[i]}")

print("=== RESULTS ===")
print(f"Your score: {score} / {len(questions)}")

if score == 5:
    print("Perfect score! You're a genius!")
elif score >= 3:
    print("Good job! Almost there!")
elif score >= 1:
    print("Keep studying, you'll get there!")
else:
    print("Oops! Better luck next time!")




quiz = {
    "What is the capital of Nigeria?": "abuja",
    "How many continents are there?": "7",
    "What does CPU stand for?": "central processing unit",
    "In what year did Nigeria gain independence?": "1960",
    "What planet is closest to the sun?": "mercury"
}

while True:
    score = 0
    total_questions = len(quiz)

    print("=== PYTHON QUIZ GAME ===")

    question_number = 1
    for question, correct_answer in quiz.items():
        print(f"Question {question_number}: {question}")
        player_answer = input("Your answer: ").lower()

        if player_answer == correct_answer:
            score += 1
            print("Correct!")
        else:
            print(f"Wrong! The answer is: {correct_answer}")

        question_number += 1

    print("=== RESULTS ===")
    print(f"Your score: {score} / {total_questions}")

    percentage = (score / total_questions) * 100
    print(f"You scored {percentage}%")

    if score == total_questions:
        print("Perfect score! You're a genius!")
    elif score >= 3:
        print("Good job! Almost there!")
    elif score >= 1:
        print("Keep studying, you'll get there!")
    else:
        print("Oops! Better luck next time!")

    play_again = input("Play again? (yes/no): ").lower()
    if play_again == "no":
        print("Thanks for playing!")
        break