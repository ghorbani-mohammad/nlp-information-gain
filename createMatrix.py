from hazm import *
import io, sys, nltk, math
import collections


lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]

# Number of document
count_of_document = len(lines)

matrix = collections.defaultdict(lambda:0)

# count number of each document type
for line in lines[:5]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    line = line[delimiter+10:]
    # print(line)
    tokens = nltk.word_tokenize(line)
    for word in tokens:
        matrix[doc_type, word] = matrix[doc_type, word] + 1
        matrix[doc_type] = matrix[doc_type] + 1

print(matrix)
# print(matrix['اقتصاد','کالاهای'])
print(matrix['اقتصاد'])
print(matrix['سیاسی'])