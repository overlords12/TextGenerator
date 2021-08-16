from nltk.tokenize import WhitespaceTokenizer
from random import choices
from random import choice


#  Construction of the Bigrams:%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

script = open(r'C:\Users\Asesor Virtual\PycharmProjects\Text Generator2\Text Generator\task\text_generator\corpus.txt',
              "r", encoding="utf-8")
script_list = script.read()
script.close()

tk = WhitespaceTokenizer()  # Create a reference variable for Class WhitespaceTokenizer
corpus_break = tk.tokenize(script_list)

trigram = [[corpus_break[i] + " " + corpus_break[i + 1], corpus_break[i + 2]] for i in range(0, len(corpus_break) - 2)]
heads_dict = {word for word in set(corpus_break[:-2])}  # [:-1] last word can't be a head
markov = {}
upper_markov = {}
# for every element in the bigram create a empty dict, for every bigram with head A create a key B
# Look for repeated values and count it
for element in trigram:
    #  Create 2 dict, for the first word with upper case
    #  the last dict is for the corpus with all non upper and final punctutation words
    if element[0][0].isupper() and element[0].split()[0][-1] not in [".", "!", "?"]:
        upper_markov.setdefault(element[0], {})
        upper_markov[element[0]].setdefault(element[1], 0)
        upper_markov[element[0]][element[1]] += 1

    markov.setdefault(element[0], {})
    markov[element[0]].setdefault(element[1], 0)
    markov[element[0]][element[1]] += 1

# Markov is now ready call it with markov[element]


# Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def phrase_maker():
    global markov
    global upper_markov
    word = choice(list(upper_markov.keys())).split()
    phrase = [word[0], word[1]]
    while True:  # Select random word from the bigrams, prob of each word is freq in de data
        word = phrase[-2] + " " + phrase[-1]
        word = choices(list(markov[word]), weights=list(markov[word].values()), k=1)[0]  # is a list
        phrase.append(word)
        if len(phrase) >= 5 and phrase[-1][-1] in [".", "!", "?"]:
            return " ".join(phrase)


# Menu %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


while True:
    index = input()
    if index == 'exit':
        break
    elif index == 'stats':
        #  Statics:
        print('Statistics:')
        print('All tokens: ', len(corpus_break))
        print('Unique tokens: ', len(set(corpus_break)))
        print('Number of bigrams: ', len(trigram))

    elif index == 'Structure':  # Show bigrams dict structure, the dict was so easy to work with
        while True:
            input_ = input()
            if input_ == 'exit':
                exit()
            try:
                print('Head:', input_)
                for i in sorted(markov[input_], key=markov[input_].get, reverse=True):
                    print('Tail: ', i, ' Count: ', markov[input_][i])
            except KeyError:
                print('Key Error. The requested word is not in the model. Please input another word.')

    elif index == 'test/corpus.txt':
        for i in range(10):
            print(phrase_maker())
        exit()
    else:
        try:
            print('Head: ', trigram[int(index)][0], 'Tail: ', trigram[int(index)][1])
        except IndexError:
            print('Index Error. Please input an integer that is in the range of the corpus.')
        except ValueError:
            print('Type Error. Please input an integer.')
