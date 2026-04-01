# NameAge.py
# This program asks the user for their name and age,
# then calculates and displays their birth year.

from datetime import datetime

# Get current year
current_year = datetime.now().year

# Ask for user input
name = input("What is your name? ")
age = int(input("How old are you? "))

# Calculate birth year
birth_year = current_year - age

# Display result
print("\nHello", name + "!", "You were born in", birth_year, ".")