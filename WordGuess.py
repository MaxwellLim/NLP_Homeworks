import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from random import seed
from random import randint
seed(1234)



#main function
def main():
    #read words from the file
    f = open('anat19.txt','r')
    raw_text = f.read()

    #Tokenize the text
    unprocessed_tokens = word_tokenize(raw_text)

    #Use set to get rid of duplicate entries
    unique_tokens = set(unprocessed_tokens)

    #calculate percent of unique words
    print ("Lexical diversity: %.2f" %(len(unique_tokens)/ len(unprocessed_tokens)))

    #apply processing to the tokens
    tokens, nouns = preprocess(unprocessed_tokens)

    game_words = make_dict(tokens, nouns)
    start_game(game_words)
    

#preprocessing function 
def preprocess(unprocessed_tokens):
    stop_words = set(stopwords.words('english'))
    tokens = []
    lemmatizer = WordNetLemmatizer()
    #Removing tokens which are not words, that are stop words or are less than 5 letters long
    for x in unprocessed_tokens:
        if x.isalpha():
            if x not in stop_words: 
                if len(x) > 5:
                    tokens.append(x.lower())
    #lemmatizing the raw text
    lemmatized = [lemmatizer.lemmatize(x) for x in tokens]
    unique_lemmas = set(lemmatized)
    #adding the lemmas to a set to removed duplicated lemmas
    pos = nltk.pos_tag(unique_lemmas)
    #printing out the first 20 unque lemmas
    for x in range(1,21):
        print(pos[x])
    nouns = []
    #making a list of only nouns
    for x in pos:
        if 'NN' in x[1]:
            nouns.append(x[0])
    #printing out the number of tokens and nouns
    print(f"Number of tokens: {len(tokens)}")
    print(f"Number of nouns: {len(nouns)}")
    return tokens, nouns

#Count the occurences of each noun and return the 50 most common
def make_dict(tokens, nouns):
    dictionary = {}
    word_dict = []
    #trys to increase the count of the word in the dictionary if it exist and adds it to the dictionary if it doesnt
    for x in tokens:
        if x in nouns:
            try:
                dictionary[x] +=1
            except KeyError:
                dictionary.update({x: 1})
    #sorts the dictionary in descending order by count
    sorted_dictionary = sorted(dictionary.items(), key=lambda x:x[1], reverse = True)
    #prints out the first 50 tokens and adds them to a list
    for x in range(0,50):
        print(f"{sorted_dictionary[x]}")
        word_dict.append(sorted_dictionary[x][0])
    return word_dict


#Guessing game
def start_game(words):
    score = 5
    print("Let's play a word guessing game!")
    
    #Game Loop
    while score > 0:
        #Setup
        word = words[randint(0,49)]
        word_tracker = []
        word_guess = []
        for x in word:
            word_tracker.append(x)
            word_guess.append('_')
        guess = ""
        #Word Loop
        while True:
            #Print out underscores and guessed letters
            for x in word_guess:
                print(f"{x} ", end = '')
            print("")

            #Ask for them to guess a letter
            guess = input("Guess a letter:")
            #check and validate input
            if guess == '!':
                return
            if not check_input(guess):
                continue
            
            #Check to see if the letter is in the word and increment or decrement the score 
            correct, word_guess, word_tracker = check_guess(guess.lower(), word_guess, word_tracker)
            if correct:
                print(f"Right! Score is {score}")
                score+=1
            else:
                score-=1
                if score > 0:
                    print(f"Sorry, guess again. Score is {score}")
                else:
                    print(f"You have run out of points.\nThe word was {word}")
                    return
            
            #check if the full word has been guessed
            complete = True
            for x in word_guess:
                if x == "_":
                    complete=False
            if complete:
                print(f"You solved it\n\nCurrent Score: 3\n\nGuess another word")
                break
    return
            

#checks to see if the input is a single letter
def check_input(letter):
    if not letter.isalpha():
        print("Guess must be a letter")
        return False
    elif len(letter) > 1:
        print("Guess must be a singular letter")
        return False
    return True

#Checks each letter in the word to see if it matches and update both the word to remove the letter occurences and update the word output to correctly show where the letters are
def check_guess(letter, word_guess, word):
    if letter not in word:
        return False, word_guess, word
    for x in range(0,len(word)):
        if word[x] == letter:
            word[x] = "_"
            word_guess[x] = letter
    return True, word_guess, word

    

if __name__ == '__main__':
    main()