import nltk
import io, sys


stop_words = [line.rstrip('\n') for line in open('Stop_words.txt', encoding="utf8")]

lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]


# Number of document
count_of_document = len(lines)

docs = {}

# count number of each document type

puredFile = open('puredInput.txt', 'w', encoding="utf8")

for line in lines:
    delimiter = line.find('@@@@@@@@@@')+10
    puredFile.write(line[:delimiter+1])
    line = line[delimiter:]
    tokens = nltk.word_tokenize(line)
    for token in tokens:
        if token in stop_words:
            continue
        else:
            puredFile.write(token+" ")
    puredFile.write("\n")
puredFile.close()