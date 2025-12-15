import random as r
import sys as s
import os
import time

print("\n╭───────────────────────╮")
print("│█▄█ █▀█ ███ █▀▄ █   ██▀│")
print("│███ █▄█ █▀▄ █▄▀ █▄▄ █▄▄│")
print("╰IN A PINCH─────────────╯")


def print_result(guesses_in_emojis: list, real_word: str, duration: float):
    for i in guesses_in_emojis:
        print(i)
    print("WORD: " + real_word)
    print("TIME: " + str(duration) + " seconds")


def print_keyboard(badLetters: list):
    firstrow = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
    firsttext = ""
    for i in firstrow:
        if i in badLetters:
            firsttext = firsttext + "\033[91m" + i + "\033[0m" + " "
        else:
            firsttext = firsttext + i + " "
    secrow = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
    sectext = " "
    for i in secrow:
        if i in badLetters:
            sectext = sectext + "\033[91m" + i + "\033[0m" + " "
        else:
            sectext = sectext + i + " "
    thirdrow = ["z", "x", "c", "v", "b", "n", "m"]
    thirdtext = "   "
    for i in thirdrow:
        if i in badLetters:
            thirdtext = thirdtext + "\033[91m" + i + "\033[0m" + " "
        else:
            thirdtext = thirdtext + i + " "
    print(firsttext)
    print(sectext)
    print(thirdtext)


def play_wordle():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_words = os.path.join(current_dir, "words.txt")
    with open(path_to_words, "r") as file:
        words = file.readlines()
    word = r.choice(words)
    word = word.strip()
    temp1 = list(word)
    letter_list = []
    for i in temp1:  # Make set of letters
        if i in letter_list:
            continue
        else:
            letter_list.append(i)
    correct = False
    guesses = 6
    letterQuantities = {}
    for i in letter_list:
        numLetters = 0
        for n in temp1:
            if n == i:
                numLetters += 1
        letterQuantities[i] = numLetters
    guessQuantities = {}
    guessHistory = []
    badletters = []
    lines_in_emojis = []
    beginning = time.time()

    while not correct:
        output = []
        if guesses == 0:
            print(f"You ran out of guesses!\n")
            end = time.time()
            print_result(lines_in_emojis, word, round(end - beginning, 2))
            break
        guess = input("\nGuess: > ").lower()
        guess = list(guess)
        if len(guess) > 5 or len(guess) < 5:
            print("Only guess a five-letter word!")
            continue
        else:
            guessHistory.append("")
        if "".join(guess) != word:
            guesses -= 1
        index = 0
        guessQuantities = {}
        for i in guess:
            if i in guessQuantities:
                guessQuantities[i] += 1
            else:
                guessQuantities[i] = 1
        line_in_emojis = ""
        for i in guess:
            if temp1[index] != i and not i in temp1:
                guessHistory[-1] = guessHistory[-1] + "\033[90m" + i + "\033[0m"
                output.append("_")
                line_in_emojis += "⬛️"
            elif (
                i in temp1
                and temp1[index] != i
                and guessQuantities[i] <= letterQuantities[i]
            ):
                guessHistory[-1] = (
                    guessHistory[-1] + "\033[93m" + "\033[4m" + i + "\033[0m"
                )
                output.append(i)
                output.append("*")
                line_in_emojis += "🟨"
            elif temp1[index] == i and i in temp1:
                guessHistory[-1] = (
                    guessHistory[-1] + "\033[92m" + "\033[4m" + i + "\033[0m"
                )
                output.append(i)
                line_in_emojis += "🟩"
            else:
                guessHistory[-1] = guessHistory[-1] + "\033[90m" + i + "\033[0m"
                output.append("_")
                line_in_emojis += "⬛️"
            if i not in temp1:
                badletters.append(i)
            index += 1
        lines_in_emojis.append(line_in_emojis)
        if not "*" in output and not "_" in output:
            print(f"\nCongrats, you guessed the word correctly!\n")
            end = time.time()
            print_result(lines_in_emojis, word, round(end - beginning, 2))
            break
        else:
            print("")
            print_keyboard(badletters)
            print("")
            for guess in guessHistory:
                print(guess)
            if not (guesses == 0):
                print(f"\nYou have {guesses} guesses left.")
            else:
                print("")


play_wordle()
while True:
    print("\nType 'play' to keep playing. Type 'quit' to quit.")
    command = input("> ")
    if command == "play":
        play_wordle()
    elif command == "quit":
        s.exit()
    else:
        print("unrecognised command")
