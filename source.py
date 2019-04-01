from __future__ import unicode_literals
from hazm import *
import io, sys, nltk, math


lines = [line.rstrip('\n') for line in open('puredInput.txt', encoding="utf8")]

# Number of document
count_of_document = len(lines)

docs = {}

# count number of each document type
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    docs[doc_type] = docs.get(doc_type, 0) + 1


print(docs.keys())
print(docs.values())

term1 = 0
current_sum = 0
for key, value in docs.items():
    x = value/count_of_document
    term1 += x*(math.log10(x))
    current_sum += value
print("term1_value: " + str(term1))


def calculation(word):
    number_of_doc_that_has_word = 0
    word_docs_found = {}
    word_docs_has_not_found = {}

    for line in lines[:]:
        delimiter2 = line.find('@@@@@@@@@@')
        doc_type2 = line[:delimiter2]
        if word in line:
            number_of_doc_that_has_word += 1
            word_docs_found[doc_type2] = word_docs_found.get(doc_type2, 0) + 1
        else:
            word_docs_has_not_found[doc_type2] = word_docs_has_not_found.get(doc_type2, 0) + 1

    # print(word)
    # print(number_of_doc_that_has_word)
    # print("Document That has:")
    # print(word_docs_found)

    term2_value = 0
    sum_of_docs_that_has__word = sum(word_docs_found.values())
    # print(sum_of_docs_that_has__word)

    for key2, value2 in word_docs_found.items():
        x1 = value2 / sum_of_docs_that_has__word
        term2_value += x1 * (math.log10(x1))
    term2_value = (sum_of_docs_that_has__word / count_of_document) * term2_value

    # print("term2_value")
    # print(term2_value)

    # print("Document That has not: ")
    # print(word_docs_has_not_found)

    term3_value = 0
    sum_of_docs_that_has_not_word = sum(word_docs_has_not_found.values())
    # print(sum_of_docs_that_has_not_word)
    for key3, value3 in word_docs_has_not_found.items():
        x2 = value3 / sum_of_docs_that_has_not_word
        term3_value += x2 * (math.log10(x2))
    term3_value = (sum_of_docs_that_has_not_word / count_of_document) * term3_value

    # print("term3_value")
    # print(term3_value)
    return term2_value + term3_value


processed_words = {}
for line in lines[:1]:
    delimiter = line.find('@@@@@@@@@@') + 10
    line = line[delimiter:]
    tokens = nltk.word_tokenize(line)
    for word in tokens:
        # print(word)
        if word in processed_words:
            continue
        else:
            # calculating score for each word
            processed_words[word] = term1 + calculation(word)

print(processed_words)