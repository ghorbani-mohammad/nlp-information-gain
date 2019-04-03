import collections, nltk


def save_dict_to_file(dic, file):
    f = open(file, 'w', encoding="utf8")
    f.write(str(dic))
    f.close()


def load_dict_from_file(file):
    f = open(file, 'r', encoding="utf8")
    data = f.read()
    f.close()
    return eval(data)


# for simplicity we assume one for p_background
p_background = 1

lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]
count_of_document = len(lines)
# print(count_of_document)

# matrix for   [doctype, word] pair
matrix = collections.defaultdict(lambda: 0)
# matrix for   [doctype, prev_word, current_word] pair
word_matrix = collections.defaultdict(lambda: 0)
# matrix for number of document for each doc_type
doc_type_matrix = collections.defaultdict(lambda: 0)

# build matrix
word_counter = 0
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    doc_type_matrix[doc_type] += 1
    line = line[delimiter+10:]
    tokens = nltk.word_tokenize(line)
    prev = ''
    for word in tokens:
        word_counter += 1
        matrix[doc_type, word] = matrix[doc_type, word] + 1
        if prev != '':
            word_matrix[doc_type, prev, word] += 1
        prev = word


# save_dict_to_file(matrix, 'word_each_doctype_matrix.txt')
# save_dict_to_file(word_matrix, 'currentWord_prevWord_matrix.txt')
# save_dict_to_file(doc_type_matrix, 'doc_type_counter_of_train_file_matrix.txt')

# matrix = load_dict_from_file('word_each_doctype_matrix.txt')
# word_matrix = load_dict_from_file('currentWord_prevWord_matrix.txt')
# doc_type_matrix = load_dict_from_file('doc_type_counter_of_train_file_matrix.txt')


lines = [line.rstrip('\n') for line in open('HAM-Test.txt', encoding="utf8")]


deltas = [0.1, 0.3, 0.5]

for step in deltas:
    print("delta is: " + str(step))
    for line in lines[:1]:
        delimiter = line.find('@@@@@@@@@@')
        line = line[delimiter+10:]
        tokens = nltk.word_tokenize(line)
        each_line_score = {}
        for doc_type in doc_type_matrix.keys():
            not_zero_counter = 0
            term1 = []
            prev = ''
            for word in tokens:
                if prev == '':
                    prev = word
                    continue
                # print(str(word_matrix[doc_type, prev, word]) + " - " + str(step))
                x = word_matrix[doc_type, prev, word] - step
                if x < 0:
                    x = 0
                else:
                    not_zero_counter += 1
                if x != 0:
                    x = x/matrix[doc_type, prev]
                term1.append(x)
                prev = word
            # print(not_zero_counter)
            if not_zero_counter != 0:
                a = not_zero_counter * (step/matrix[doc_type, prev])
            else:
                a = 0
            # print(a)
            term2 = a * p_background
            # print(term2)
            multiple_accumulator = 1.0
            for word_score in term1:
                multiple_accumulator *= (word_score + term2)
                # print(multiple_accumulator)
            # print(multiple_accumulator)
            each_line_score[doc_type] = multiple_accumulator
        print(each_line_score)
        # print(line[:delimiter])
