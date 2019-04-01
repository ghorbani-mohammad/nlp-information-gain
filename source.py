from __future__ import unicode_literals
from hazm import *
import io, sys, nltk, math, operator, collections
from collections import OrderedDict
import numpy as np


def save_dict_to_file(dic):
    f = open('information_gain_calculated.txt', 'w', encoding="utf8")
    f.write(str(dic))
    f.close()


def load_dict_from_file():
    f = open('dict.txt', 'r', encoding="utf8")
    data=f.read()
    f.close()
    return eval(data)


lines = [line.rstrip('\n') for line in open('puredInput.txt', encoding="utf8")]

# Number of document
count_of_document = len(lines)

docs = {}

# count number of each document type
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    docs[doc_type] = docs.get(doc_type, 0) + 1


# print(docs.keys())
# print(docs.values())

term1 = 0
current_sum = 0
for key, value in docs.items():
    x = value/count_of_document
    term1 += x*(math.log2(x))
    current_sum += value
term1 = - term1
# print("term1_value: " + str(term1))


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

    term2_value = 0
    sum_of_docs_that_has__word = sum(word_docs_found.values())

    for key2, value2 in word_docs_found.items():
        x1 = value2 / sum_of_docs_that_has__word
        term2_value += x1 * (math.log2(x1))
    term2_value = (sum_of_docs_that_has__word / count_of_document) * term2_value

    term3_value = 0
    sum_of_docs_that_has_not_word = sum(word_docs_has_not_found.values())
    for key3, value3 in word_docs_has_not_found.items():
        x2 = value3 / sum_of_docs_that_has_not_word
        term3_value += x2 * (math.log2(x2))
    term3_value = (sum_of_docs_that_has_not_word / count_of_document) * term3_value

    # print("term3_value")
    # print(term3_value)
    return term2_value + term3_value


processed_words = {}
for line in lines[:]:
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


#sorting dict based on value
sorted_procceed_words = sorted(processed_words.items(), key=lambda kv: kv[1])
print(sorted_procceed_words)

save_dict_to_file(sorted_procceed_words)