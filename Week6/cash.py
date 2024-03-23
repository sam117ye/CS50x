
while True:
     dollar = float(input("Change: "))
     if dollar > 0:
         break

dollar = round(dollar * 100)

quarter = 0
while dollar >= 25:
    dollar -= 25
    quarter += 1

dimes = 0
while dollar >= 10:
    dollar -= 10
    dimes += 1

nickels = 0
while dollar >= 5:
    dollar -= 5
    nickels += 1

pennies = 0
while dollar >= 1:
    dollar -= 1
    pennies += 1

total = float(quarter + dimes + nickels + pennies)

print(f"Total: {total}")
