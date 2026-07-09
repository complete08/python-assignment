#bug 1
# broken
"Burger" = 1500,

# fixed
"Burger": 1500,

#bug2
# broken
for item in cart

# fixed
for item in cart:


#bug3
# broken
price = menu(item)

# fixed
price = menu[item]



#bug4
# broken
print("Subtotal: N" + total)

# fixed
print(f"Subtotal: N{total}")


#bug5
# broken
def apply_discount(amount, percent)

# fixed
def apply_discount(amount, percent):


#bug6
# broken — defined but never used
def apply_discount(amount, percent):
    discounted = amount - (amount * percent / 100)
    return discounted

# fixed — call it where the discount logic is needed
if total >= 5000:
    total = apply_discount(total, 10)
    print("Discount applied!")


#full corrected code
def apply_discount(amount, percent):
    discounted = amount - (amount * percent / 100)
    return discounted

menu = {
    "Burger": 1500,       # BUG 1 fixed — : instead of =
    "Fries": 500,
    "Drink": 400,
}

cart = ["Burger", "Fries", "Drink", "Fries"]
total = 0

for item in cart:         # BUG 2 fixed — added :
    price = menu[item]    # BUG 3 fixed — [] instead of ()
    total = total + price

print(f"Subtotal: N{total}")  # BUG 4 fixed — f-string instead of +

if total >= 5000:
    total = apply_discount(total, 10)   # BUG 6 fixed — function now called
    print("Discount applied!")

print(f"Total: N{total}")