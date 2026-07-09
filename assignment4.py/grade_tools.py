

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


def get_remark(letter):
    remarks = {
        "A": "Outstanding performance! Keep it up!",
        "B": "Great work! Push for that A next time.",
        "C": "Good effort. A little more study will get you higher.",
        "D": "You passed, but there's room for improvement.",
        "F": "Don't give up! Talk to your teacher for extra help."
    }
    return remarks[letter]


# STRETCH: lambda stored in a variable
get_birth_year = lambda age: 2026 - age