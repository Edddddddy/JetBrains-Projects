import random
wordList = ["python", "java", "kotlin", "javascript"]
hiddenWord = list(wordList[random.randint(0, 3)])
lines = list("-" * len(hiddenWord))
chances = 8
previousLetters = []
playing = True
print("H A N G M A N")
while playing:
    print('Type "play" to play the game, "exit" to quit: ', end="")
    selection = input()
    if selection == "play":
        while chances > 0:
            print("")
            print("".join(lines))
            if "".join(lines) == "".join(hiddenWord):
                print("You guessed the word {}!".format("".join(hiddenWord)))
                print("You survived!", end="\n")
                break
            print("Input a letter: ", end="")
            letter = input()
            if letter in previousLetters:
                print("You already typed this letter")
                continue
            if letter == "" or len(letter) > 1:
                print("You should input a single letter")
                continue
            if not letter.islower() or not letter.isascii():
                print("It is not an ASCII lowercase letter")
                continue
            previousLetters.append(letter)
            if letter in lines:
                print("No improvements")
                chances -= 1
                continue
            elif letter in hiddenWord:
                for i, v in enumerate(hiddenWord):
                    if v == letter:
                        lines[i] = letter
                continue
            else:
                print("No such letter in the word")
                chances -= 1
        else:
            print("You are hanged!", end="\n")
    if selection == "exit":
        break
    else:
        continue
