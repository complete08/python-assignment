# --- Step 1: Import the module ---
import grade_tools

# --- Step 2: Get student info ---
print("=== STUDENT REPORT CARD ===\n")

name = input("Enter your name: ")

# STRETCH: get age for birth year
age = int(input("Enter your age: "))

scores = []
for i in range(3):
    score = int(input(f"Enter score for Subject {i + 1}: "))
    scores.append(score)

# --- Step 3: Use module functions ---
average = grade_tools.calculate_average(scores)
grade = grade_tools.get_grade(average)
letter = grade[0]                        # extracts "A" from "A - Excellent"
remark = grade_tools.get_remark(letter)

# STRETCH: birth year via lambda
birth_year = grade_tools.get_birth_year(age)

# --- Step 4: Print the report card ---
print("\n================================")
print("      STUDENT REPORT CARD")
print("================================")
print(f"Name:       {name}")
print(f"Birth Year: {birth_year}")
print()
for i, score in enumerate(scores):
    print(f"Subject {i + 1}:  {score}")
print()
print(f"Average:    {average:.1f}")
print(f"Grade:      {grade}")
print(f"Remark:     {remark}")
print("================================")

# --- STRETCH: Sort multiple students ---
all_students = [
    {"name": "Amina",  "average": 75.0},
    {"name": "Tunde",  "average": 88.5},
    {"name": "Chidi",  "average": 62.0},
    {"name": "Ngozi",  "average": 91.0},
    {"name": "Emeka",  "average": 55.5}
]

ranked = sorted(all_students, key=lambda s: s["average"], reverse=True)

print("\n=== CLASS RANKING ===")
for position, student in enumerate(ranked, start=1):
    print(f"{position}. {student['name']:<10} Average: {student['average']:.1f}")