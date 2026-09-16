# PART 2: CONTROL FLOW - IF/ELSE STATEMENTS

# Example 1: Simple If Statement
print("=== EXAMPLE 1: Simple If ===")
age = 18
if age >= 18:
    print("You are an adult!")

# Example 2: If-Else Statement
print("\n=== EXAMPLE 2: If-Else ===")
score = 45
if score >= 50:
    print("You passed!")
else:
    print("You failed. Try again!")

# Example 3: If-Elif-Else (Multiple Conditions)
print("\n=== EXAMPLE 3: If-Elif-Else ===")
grade = 85

if grade >= 90:
    print("Grade: A")
elif grade >= 80:
    print("Grade: B")
elif grade >= 70:
    print("Grade: C")
elif grade >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# Example 4: Logical Operators (and, or, not)
print("\n=== EXAMPLE 4: Logical Operators ===")
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive!")
else:
    print("You cannot drive!")

# Example 5: Using 'or' operator
print("\n=== EXAMPLE 5: OR Operator ===")
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
else:
    print("It's a weekday!")

# Example 6: Using 'not' operator
print("\n=== EXAMPLE 6: NOT Operator ===")
is_raining = False

if not is_raining:
    print("Let's go outside!")
else:
    print("Stay inside, it's raining!")
