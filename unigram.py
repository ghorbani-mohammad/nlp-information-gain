import collections, nltk

lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]

count_of_document = len(lines)


matrix = collections.defaultdict(lambda: 0)

# build matrix
word_counter = 0
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    line = line[delimiter+10:]
    tokens = nltk.word_tokenize(line)
    for word in tokens:
        matrix[doc_type, word] = matrix[doc_type, word] + 1
        matrix[doc_type] = matrix[doc_type] + 1
        word_counter += 1

docs = {}
# count number of each document type
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    docs[doc_type] = docs.get(doc_type, 0) + 1


print(docs.keys())
print(docs.values())
print(word_counter)

prior_probility = {}

for key, value in docs.items():
    x = value / count_of_document
    prior_probility[key] = x

print(prior_probility)


lines_test = [line.rstrip('\n') for line in open('HAM-Test.txt', encoding="utf8")]

deltas = [0.1, 0.3, 0.5]

for step in deltas:
    for line in lines_test[:1]:
        delimiter = line.find('@@@@@@@@@@')
        line = line[delimiter+10:]
        tokens = nltk.word_tokenize(line)
        for doc_type in docs.keys():
            not_zero_counter = 0
            term1 = []
            for token in tokens:
                print(doc_type)
                print(token)
                x = matrix[doc_type, token] - step
                if x < 0:
                    x = 0
                else:
                    not_zero_counter += 1
                x = x/matrix[doc_type]
                term1.append(x)
            a = (step/matrix[doc_type]) * not_zero_counter
            term2 = a * 1/word_counter
            multiple_accumulator = 1
            for word_score in term1:
                multiple_accumulator *= (word_score + term2)



    # docs[doc_type] = docs.get(doc_type, 0) + 1
    # print(line)