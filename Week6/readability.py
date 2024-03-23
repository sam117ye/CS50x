text = str(input("Text: "))

letter = 0

for i in range(len(text)):
    if text[i].isalpha():
        letter += 1

sentence = 0
word = 1

for i in range (len(text)):
    if text[i] == '?' or text[i] == '.' or text[i] == '!':
        sentence +=1
    elif text[i] == ' ':
         word += 1

L = (letter / word) * 100
S = (sentence / word) * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print(f"Before Grade 1")
elif 1 <= index <= 16:
     print(f"Grade {index}")
elif index > 16:
     print(f"Grade 16+")
