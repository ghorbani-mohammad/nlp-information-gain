from __future__ import unicode_literals
from hazm import *
import io, sys, nltk, math





stop_words = [line.rstrip('\n') for line in open('Stop_words.txt', encoding="utf8")]


lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]


# Number of document
count_of_document = len(lines)

docs = {}

# count number of each document type
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    docs[doc_type] = docs.get(doc_type, 0) + 1
    # print(word_tokenize(line))


print(docs.keys())
print(docs.values())

term1 = 0
current_sum = 0
# print(count_of_document)
for key, value in docs.items():
    x = value/count_of_document
    # print(x)
    # print(x*(math.log10(x)))
    term1 += x*(math.log10(x))
    current_sum += value
    # print(current_sum)
print("term1_value:")
print(term1)

words = [' است', ' بود']
processed_words = {}


for word in words:
    number_of_doc_that_has_word = 0
    word_docs_found = {}
    word_docs_notFound = {}
    if word in processed_words:
        continue
    else:
        processed_words[word] = 0
        for line in lines[:]:
            delimiter = line.find('@@@@@@@@@@')
            doc_type = line[:delimiter]
            if word in line:
                number_of_doc_that_has_word += 1
                word_docs_found[doc_type] = word_docs_found.get(doc_type, 0) + 1
                # print(line)
                # input('Choose a number')
                # number_of_doc_that_has_word[word] = number_of_doc_that_has_word.get(word, 0) + 1
            else:
                word_docs_notFound[doc_type] = word_docs_notFound.get(doc_type, 0) + 1
           #     print("Not found")

    print(word)
    print(number_of_doc_that_has_word)
    print("Document That has:")
    print(word_docs_found)

    term2_value = 0
    sum_of_docs_that_has__word = sum(word_docs_found.values())
    print(sum_of_docs_that_has__word)

    for key, value in word_docs_found.items():
        x = value / sum_of_docs_that_has__word
        term2_value += x * (math.log10(x))
    term2_value = (sum_of_docs_that_has__word / count_of_document)*term2_value

    print("term2_value")
    print(term2_value)

    print("Document That has not: ")
    print(word_docs_notFound)

    term3_value = 0
    sum_of_docs_that_has_not_word = sum(word_docs_notFound.values())
    print(sum_of_docs_that_has_not_word)
    for key, value in word_docs_notFound.items():
        x = value / sum_of_docs_that_has_not_word
        term3_value += x * (math.log10(x))
    term3_value = (sum_of_docs_that_has_not_word / count_of_document) * term3_value

    print("term3_value")
    print(term3_value)







# print(processed_words)
# print(lines[:10])
# print(number_of_doc_that_has_word)
# print("Document That has:")
# print(word_docs_found)
# print("Document That has not: ")
# print(word_docs_notFound)
sys.exit()






# # Read in the file
# with open('test.txt', encoding="utf8", mode='r') as file :
#   filedata = file.read()
#
#
# print(filedata)
#
# # Replace the target string
#
# for word in stop_words[:20]:
#     print(word)
#     filedata = filedata.replace(word, '')
#
# filedata = filedata.replace('است', '')
# print(filedata)
# sys.exit()

# Write the file out again
with open('file.txt', 'w') as file:
  file.write(filedata)






infile = "test.txt"
outfile = "cleaned_test.txt"

fin = open(infile, encoding="utf8")
fout = open(outfile, mode="w+", encoding="utf8")
for line in fin:
    print(line)
    for stop_word in stop_words:
        print()
        print(stop_word)
        print()
        line = line.replace(stop_word, "")
        print(line)
    fout.write(line)
fin.close()
fout.close()

sys.exit()

with open('Stop_words.txt', encoding="utf8") as f:
    print(f.readlines())

exit()

stop_words = open('Stop_words.txt', encoding="utf8")
line = stop_words.read()
words = line.split()
for w in words:
    print(w)

exit()



file = open('test.txt', encoding="utf8")
line = file.read()
words = line.split()
for r in words:
    print(r)


