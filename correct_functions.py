import csv
"""
==================================
Name: Bruk Zewdie
UNI: bbz2103
Homework3
================================== """

def correct_matches(possibleMatches, correctWords):
    ##Accepts two lists where every word in possibleMatches is compared
    ##against every word in correctWords. The matching words are appended
    ## in the correctly spelled word list.
    correctly_spelled = []
    for word in possibleMatches:
        if word in correctWords:
            correctly_spelled.append(word)
    return correctly_spelled


def split_pair_matches(possibleMatches, correctWords):
    ## Similar to correct_matches except that the possibleMatches parameter 
    ## of this function is split into two words, of which both are compared with
    ## the correctly spelled word list. Considered valid if both words in the pair 
    ## are correctly spelled words.
    correctly_spelled = []
    for word in possibleMatches:
        word_pair = word.split()
        if (word_pair[0] in correctWords) and (word_pair[1] in correctWords):
            correctly_spelled.append(word)
    return correctly_spelled



def is_correctly_spelled(word):
    ## matches the word with the first column in the dictionary.
    found = False
    my_list = simple_read()
    for row in my_list:
        if row[0]==word:
            found = True  ##if the word has a match return True
    return found
            

def simple_read(): ## default location of the file needs to be changed.
    with open("dictionary.csv","r")as dictionary:
        my_list = []
        reader = csv.reader(dictionary)
        for line in reader:
            my_list.append(line)
        return my_list
            


def each_letter_removed(word):
    ## returns a list of possible corrections by removing each
    ## letter in the word. 
    word_list=[]
    for i in range (len(word)):        
        temp_word = word[:i]+word[i+1:] #make a temporary word with the one letter removed.
        word_list.append(temp_word)        
    return word_list



def insert_space(word):
    ## returns a list of possible corrections by inserting space
    ## between each adjacent letters of the word.
    word_list = []
    for i in range(len(word)-1): ##we don't want to insert space after the last
                                 ## letter, thus len(word)-1
        temp_word = word[:i+1]+" "+word[i+1:]
        word_list.append(temp_word);
    return word_list


def previously_entered_correction(word,dictionary_list):
    word_list = []
    for row in dictionary_list:
        if row[5]==word:
            word_list.append(row[0])
    return word_list

def insert_all_alphabets(word):
    word_list = []
    for i in range(len(word)+1):
        ##inserts an alphabet adjacent to every letter
        ## in the word without replacing any letter
        for alphabet in "abcdefghijklmnopqrstuvwxyz":
            temp_word = word[:i]+alphabet+word[i:]
            word_list.append(temp_word)

            
    for i in range(len(word)):
        ##replaces every letter of the word by all the
         ##English alphabets. 
        for alphabet in "abcdefghijklmnopqrstuvwxyz":
            temp_word = word[:i]+alphabet+word[i+1:]
            word_list.append(temp_word)
    return word_list
                           

def generate_transposes(word):
    ##According to piazza, Professor Ferguson said that
    ##we can use his generate_transposes function.
    result = []
    for i in range(0,len(word)-1):
        l = word[:i]
        c1 = word[i]
        c2 = word[i+1]
        r = word[i+2:]
        n = l + c2 + c1 + r
        result.append(n)
    return result


def increment_selected(selected_word, my_list):
    ## To be used in update_corrections function.
    ## If the correction selected by the user is already
    ## in the dictionary increment the times_selected entry by 1.
        for row in my_list:
            if row[0]==selected_word:
                temp = eval(row[3])+1
                row[3]= str(temp)
        return my_list

def add_as_user_created(old_word, new_word, my_list):
    ## If the correction entered by the user was not already in the
    ## dictionary, append the new_word as a possible correction of the
    ## previous misspell.
        found=False
        for row in my_list:
            if row[0]==new_word:
                found=True  ## The word is in the correctly spelled word list
                            ## thus the function will just return the initial list
                            ## which is the one returned by simple_read().
        if found==False: ##if the new_word is not in the correctly spelled word list
                         ## append the new_word to my_list
            my_list.append([new_word,"0","True","0","0",old_word])
            ## NOTE I just inserted "0" for relative frequencey and total frequency.
            ## Because it says so on piazza.
        return my_list


def check_word(word_input):
        ## if the user just hits enter without entering a word,
        ## request for a word until the length of the input is > 0
    while len(word_input)==0:
        word_input = input("You have to enter a word, please enter a word.")
       
        
    word = word_input.strip()
    ##remove white spaces  at the beginning and the end of the word.
    ## Otherwise malicious input like  "the  " or "  the" will make it crash.
    
    word = word.lower() ##convert all the characters into lower case letters.
    my_list = simple_read()
    ##print(my_list)
    correct_words = [row[0] for row in my_list]
    if (is_correctly_spelled(word)):
        return True
    else:
        suggestion_list=[]
        letter_removed = correct_matches(each_letter_removed(word),correct_words)
        alphabet_inserted = correct_matches(insert_all_alphabets(word),correct_words)
        transposed = correct_matches(generate_transposes(word), correct_words)
        prior_corrections = previously_entered_correction(word,my_list)
        split_pair = split_pair_matches(insert_space(word),correct_words)
        
                
        ##Concatenate all the lists of the CORRECT generated suggestions into 
        ## a single suggestions list. 
        
        suggestion_list += letter_removed
        suggestion_list += alphabet_inserted
        suggestion_list += transposed
        suggestion_list += prior_corrections
        suggestion_list += split_pair
     
        ##The following block makes sure that there aren't any repeated words
        ## in the list. Since a set does not allow repetition of values, I cast
        ## the list into sets and then back to lists again. By doing this all repeated
        ## words will be removed.
        suggestion_list = set(suggestion_list)
        suggestion_list = list(suggestion_list)


        """The following block makes sure that the suggestion_list doesn't contain
         a previously user generated correction for words other than the one
         to which the correction was made for.
         E.g. if user inputs "ly", the suggested corrections are ['by','my']. But,
         when prompted, if the user selects as his/her own correction "cy", 
         then "cy" should only appear as a suggestion only for the initial
         misspell "ly" and not for "dy", "ty" or "gy".
         """
##        for row in my_list:
##            for each_word in suggestion_list:
##                if (row[0]==each_word) and (row[2]=="True") and row[5]!=word:
##                    ## if each_word (the word in the suggestion list) is previously user generated
##                    ## and the word is not a previous misspell then remove (each_word) from the
##                    ## suggestion list
##                    suggestion_list.remove(each_word)
                    
        return suggestion_list
    
def update_corrections(old_input_word, new_input_word):
        ## if the user just hits enter without entering a word,
        ## request for a word until the length of the input is > 0
    while len(old_input_word)==0:
        old_input_word = input("You have to enter a word, please enter a word.")
    while len(new_input_word)==0:
        new_input_word=input("You have to enter a word, please enter a word.")
    new_word = new_input_word.lower()  ## Since the user inputs this word, convert to lower case.
    old_word = old_input_word.lower()
    my_list = simple_read()
    my_list = increment_selected(new_word, my_list)
    my_list = add_as_user_created(old_word, new_word, my_list)
    with open ("dictionary.csv","w", newline='') as dictionary:
        writer = csv.writer(dictionary)
        for row in my_list:
            writer.writerow(row)







