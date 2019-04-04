import collections, nltk, math


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
# matrix for sum of words for each doc type
sum_of_words_for_each_type = collections.defaultdict(lambda: 0)

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
        matrix[doc_type, word] += 1
        sum_of_words_for_each_type[doc_type] += 1
        if prev != '':
            word_matrix[doc_type, prev, word] += 1
        prev = word

print("Finished build matrixes")

# exit()
# save_dict_to_file(matrix, 'word_each_doctype_matrix.txt')
# save_dict_to_file(word_matrix, 'currentWord_prevWord_matrix.txt')
# save_dict_to_file(doc_type_matrix, 'doc_type_counter_of_train_file_matrix.txt')

# matrix = load_dict_from_file('word_each_doctype_matrix.txt')
# word_matrix = load_dict_from_file('currentWord_prevWord_matrix.txt')
# doc_type_matrix = load_dict_from_file('doc_type_counter_of_train_file_matrix.txt')

# print(matrix)
# print(word_matrix)
# print(doc_type_matrix)
# print(sum_of_words_for_each_type)
# exit()



lines = [line.rstrip('\n') for line in open('HAM-Test.txt', encoding="utf8")]
all_test_documents = len(lines)

confusion_matrix = collections.defaultdict(lambda: 0)
fp_matrix = collections.defaultdict(lambda: 0)
fp_matrix2 = collections.defaultdict(lambda: 0)

deltas = [0.1, 0.3, 0.5]

for step in deltas:
    # print("delta is: " + str(step))
    for line in lines[:]:
        delimiter = line.find('@@@@@@@@@@')
        test_doc_type = line[:delimiter]
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
                # if word_matrix[doc_type, prev, word] == 0:
                #     print(prev)
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
            a = 0
            if not_zero_counter != 0:
                # deminator may become zero and will rise error
                try:
                    a = not_zero_counter * (step / matrix[doc_type, prev])
                except:
                    a = not_zero_counter * (step / sum_of_words_for_each_type[doc_type])
                    # continue
            # print(a)
            term2 = a * p_background
            # print(term2)
            multiple_accumulator = 1
            for word_score in term1:
                multiple_accumulator *= math.log2(word_score + term2)
                # print(multiple_accumulator)
            # print(multiple_accumulator)
            each_line_score[doc_type] = multiple_accumulator
        result = sorted(each_line_score.items(), key=lambda kv: kv[1])
        # print(result)
        label = result[0][0]
        real = test_doc_type
        if label == real:
            confusion_matrix[step, real, "tp"] += 1
        else:
            confusion_matrix[step, real, "fn"] += 1
            fp_matrix[step, label] += 1
            fp_matrix2[step, real, label] += 1
        # print(line[:delimiter])

# exit()

print("Confusion Matrix:")
print(confusion_matrix)
print()
print(fp_matrix2)
print()


precision = {}
recall = {}
# print(confusion_matrix)
# print(fp_matrix)
for step in deltas:
    for doc_type in doc_type_matrix.keys():
        try:
            precision[step, doc_type] = confusion_matrix[step, doc_type, "tp"]/(confusion_matrix[step, doc_type, "tp"] + fp_matrix[step, doc_type])
            recall[step, doc_type] = confusion_matrix[step, doc_type, "tp"]/(confusion_matrix[step, doc_type, "fn"] + fp_matrix[step, doc_type])
        except:
            print(doc_type)
            print(confusion_matrix[step, doc_type, "tp"])
            print(fp_matrix[step, doc_type])

print("Precision:")
print(precision)
print("")
print("Recall:")
print(recall)
print("")

f_measure = {}
for step in deltas:
    for doc_type in doc_type_matrix.keys():
        f_measure[step, doc_type] = (2 * precision[step, doc_type] * recall[step, doc_type]) / (precision[step, doc_type] + recall[step, doc_type])
print("F-measure:")
print(f_measure)
print("")
micro_averaged = collections.defaultdict(lambda: 0)
macro_averaged = {}

weight = {}
for step in deltas[:1]:
    for doc_type in doc_type_matrix.keys():
        weight[doc_type] = confusion_matrix[step, doc_type, "tp"] + confusion_matrix[step, doc_type, "fn"]
        # print(weight[doc_type])

sum_of_precisions = collections.defaultdict(lambda: 0)
sum_of_recalls = collections.defaultdict(lambda: 0)
sum_of_f_measure = collections.defaultdict(lambda: 0)
for step in deltas[:]:
    for doc_type in doc_type_matrix.keys():
        sum_of_precisions[step] += precision[step, doc_type]
        sum_of_recalls[step] += recall[step, doc_type]
        sum_of_f_measure[step] += f_measure[step, doc_type]
    macro_averaged[step, "Macro_precision"] = sum_of_precisions[step] / 5
    macro_averaged[step, "Macro_recalls"] = sum_of_recalls[step] / 5
    macro_averaged[step, "Macro_f_measure"] = sum_of_f_measure[step] / 5

print(macro_averaged)


for step in deltas[:]:
    for doc_type in doc_type_matrix.keys():
        micro_averaged[step, "Micro_precision"] += precision[step, doc_type] * (weight[doc_type] / all_test_documents)
        micro_averaged[step, "Micro_recalls"] += recall[step, doc_type] * (weight[doc_type] / all_test_documents)
        micro_averaged[step, "micro_f_measure"] += f_measure[step, doc_type] * (weight[doc_type] / all_test_documents)

print(micro_averaged)
