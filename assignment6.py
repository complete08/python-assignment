# ================================
# FUNCTIONS
# ================================

def get_user_info():
    name = input("Enter your name: ")

    while True:
        try:
            age = int(input("Enter your age: "))
            break
        except ValueError:
            print("Invalid! Please enter a number for age.")

    with open("user_profile.txt", "w") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Age: {age}\n")

    print("Profile saved to user_profile.txt!")


def load_profile():
    try:
        with open("user_profile.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("No saved profile found. Please create one first.")


# ================================
# MENU
# ================================

print("Welcome to the Profile App!")

while True:
    print("\n1. Create new profile")
    print("2. Load existing profile")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        get_user_info()
    elif choice == "2":
        load_profile()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")