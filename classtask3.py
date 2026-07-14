#part 1
def check_password_strength(password):
    has_number = False
    for char in password:
        if char.isdigit():
            has_number = True

    if len(password) >= 8 and has_number:
        return "Strong"
    elif len(password) >= 6:
        return "Medium"
    else:
        return "Weak"


print("=== PASSWORD STRENGTH CHECKER ===")
print("Testing passwords...")
print(f'"abc" -> {check_password_strength("abc")}')
print(f'"abcdef" -> {check_password_strength("abcdef")}')
print(f'"python2024" -> {check_password_strength("python2024")}')
print(f'"12345678" -> {check_password_strength("12345678")}')
print(f'"short1" -> {check_password_strength("short1")}')

print("Now try your own!")
user_password = input("Enter a password: ")
print(f"Your password strength: {check_password_strength(user_password)}")


#part 2
def check_password_strength(password):
    has_number = False
    for char in password:
        if char.isdigit():
            has_number = True

    if len(password) >= 8 and has_number:
        return "Strong"
    elif len(password) >= 6:
        return "Medium"
    else:
        return "Weak"


def display_strength(password):
    strength = check_password_strength(password)
    print(f"Password: {password}")
    print(f"Strength: {strength}")

    if strength == "Strong":
        print("[##########] Your password is strong!")
    elif strength == "Medium":
        print("[######----] Your password is medium. Consider adding numbers or more length.")
    else:
        print("[###-------] Your password is weak. Try adding numbers and more characters.")

    if strength == "Weak":
        print("Tip: Make your password at least 6 characters long.")
    elif strength == "Medium":
        print("Tip: Add numbers to make your password stronger.")


# Upgrade C: Multiple Password Checker
test_passwords = ["cat", "python", "Secure2024", "ab", "hello123"]

print("=== CHECKING MULTIPLE PASSWORDS ===")
for pw in test_passwords:
    display_strength(pw)
    print()  # blank line between entries for readability