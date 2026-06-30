# --- Step 1: Create the menu ---
menu = {
    "burger": 1500,
    "fries": 800,
    "soda": 500,
    "pizza": 3000,
    "ice cream": 1000
}

# --- Step 2: Display the menu ---
print("=== WELCOME TO PYTHON BITES ===\n")
print("--- Menu ---")
for item, price in menu.items():
    print(f"{item}: {price}")

# --- Step 3: Create an empty cart ---
cart = []

# --- Step 4: Ordering loop ---
while True:
    order = input("\nWhat would you like to order? (type 'done' to finish): ")
    
    if order == "done":
        break
    
    if order in menu:
        quantity = int(input("How many? "))
        for _ in range(quantity):
            cart.append(order)
        print(f"Added {quantity} x {order} to your cart!")
    else:
        print("Sorry, that's not on the menu.")

# --- Step 5: Calculate the total ---
total = 0
for item in cart:
    total += menu[item]

# --- Step 6: Print the receipt ---
print("\n=== YOUR RECEIPT ===")
print(cart)
print(f"Total: {total}")

# --- STRETCH: Discount ---
if total > 5000:
    discount_amount = total * 10 / 100
    total -= discount_amount
    print(f"You got a 10% discount: -{discount_amount}")
    print(f"New total: {total}")

print("Thank you for shopping at Python Bites!")