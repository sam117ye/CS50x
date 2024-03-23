while True:
    try:
        height = int(input("height: "))
        if 1 <= height <= 8:
            break
        else:
            print("Height must be between 1 and 8,")
    except ValueError:
        print("Invalid input.")

for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")
    for k in range(i + 1):
        print("#", end="")
    print()
