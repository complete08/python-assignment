# ================================
# BASE LEVEL
# ================================

def get_student_info():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    return name, age


def get_scores(num_subjects=3):
    scores = []
    for i in range(num_subjects):
        score = int(input(f"Enter score for Subject {i + 1}: "))
        scores.append(score)
    return scores


def calculate_average(scores):
    return sum(scores) / len(scores)


def get_grade(average):
    if average >= 70:
        return "A - Excellent"
    elif average >= 60:
        return "B - Very Good"
    elif average >= 50:
        return "C - Good"
    elif average >= 40:
        return "D - Pass"
    else:
        return "F - Fail"


# ================================
# STRETCH LEVEL
# ================================

def get_remark(grade):
    if grade.startswith("A"):
        return "Outstanding performance! Keep it up!"
    elif grade.startswith("B"):
        return "Great work! Push for that A next time."
    elif grade.startswith("C"):
        return "Good effort. A little more study will get you higher."
    elif grade.startswith("D"):
        return "You passed, but there's room for improvement."
    else:
        return "Don't give up! Talk to your teacher for extra help."


def print_report(name, age, scores, average, grade):
    remark = get_remark(grade)
    print("\n================================")
    print("     STUDENT REPORT CARD")
    print("================================")
    print(f"Name:    {name}")
    print(f"Age:     {age}")
    print()
    for i, score in enumerate(scores):
        print(f"Subject {i + 1}:  {score}")
    print()
    print(f"Average:    {average:.1f}")
    print(f"Grade:      {grade}")
    print(f"Remark:     {remark}")
    print("================================")


# ================================
# BOSS LEVEL
# ================================

all_students = []

while True:
    print("\n--- New Student Entry ---")
    name, age = get_student_info()

    num_subjects = int(input("How many subjects? "))
    scores = get_scores(num_subjects)

    average = calculate_average(scores)
    grade = get_grade(average)

    print_report(name, age, scores, average, grade)

    all_students.append({
        "name": name,
        "average": average,
        "grade": grade
    })

    again = input("\nAdd another student? (yes/no): ").strip().lower()
    if again != "yes":
        break

# ================================
# CLASS SUMMARY
# ================================

print("\n================================")
print("        CLASS SUMMARY")
print("================================")

class_average = sum(s["average"] for s in all_students) / len(all_students)
top_student = max(all_students, key=lambda s: s["average"])

for student in all_students:
    print(f"{student['name']:<15} Average: {student['average']:.1f}   Grade: {student['grade']}")

print(f"\nClass Average:   {class_average:.1f}")
print(f"Top Student:     {top_student['name']} ({top_student['average']:.1f})")
print("================================")