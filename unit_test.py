import correct_functions


def main():
    done = False

    while not done:
        w = input("Please enter a word (enter -1 to end: ")
        if w == "-1":
            print("Exiting.")
            break
            done = True

        c = correct_functions.check_word(w)

        if c == True:
            print("The word is correctly spelled.")
        else:
            print("Suggested corrections are: ", c)
            f = input("Enter one of the words or your own correction: ")
            r = correct_functions.update_corrections(w,f)


main()
