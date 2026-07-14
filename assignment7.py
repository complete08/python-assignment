import re

# ================================
# VALIDATION FUNCTIONS
# ================================

def get_valid_name():
    while True:
        name = input("Enter your name: ").strip()
        if name:
            # re.sub cleans multiple spaces between words
            clean_name = re.sub(r"\s+", " ", name)
            return clean_name
        print("Name cannot be empty. Try again.")


def get_valid_email():
    pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"
    while True:
        email = input("Enter your email: ").strip()
        if re.fullmatch(pattern, email):
            print("✓")
            return email
        print("Invalid email format! Try again.")


def get_valid_phone():
    pattern = r"\d{4}-\d{3}-\d{4}"
    while True:
        phone = input("Enter your phone (e.g., 0801-234-5678): ").strip()
        if re.fullmatch(pattern, phone):
            print("✓")
            return phone
        print("Invalid phone format! Try again.")


def get_bio_tokens():
    bio = input("Write a short bio about yourself: ").strip()
    tokens = re.findall(r"\w+", bio.lower())
    print(f"Your bio contains {len(tokens)} words: {tokens}")
    return bio, tokens


def save_profile(name, email, phone, bio, token_count):
    with open("user_profile.txt", "w") as f:
        f.write(f"Name:        {name}\n")
        f.write(f"Email:       {email}\n")
        f.write(f"Phone:       {phone}\n")
        f.write(f"Bio:         {bio}\n")
        f.write(f"Word Count:  {token_count}\n")
    print("Profile saved successfully!")


def load_profile():
    try:
        with open("user_profile.txt", "r") as f:
            print("\n=== SAVED PROFILE ===")
            print(f.read())
    except FileNotFoundError:
        print("No saved profile found. Please create one first.")


# ================================
# MENU
# ================================

print("=== SMART PROFILE VALIDATOR ===\n")

while True:
    print("\n1. Create new profile")
    print("2. Load existing profile")
    print("3. Exit")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        name       = get_valid_name()
        email      = get_valid_email()
        phone      = get_valid_phone()
        bio, tokens = get_bio_tokens()
        save_profile(name, email, phone, bio, len(tokens))

    elif choice == "2":
        load_profile()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")