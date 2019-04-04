import collections, nltk, math

# Fetching impactful words
def load_dict_from_file():
    f = open('information_gain_calculated.txt', 'r', encoding="utf8")
    data = f.read()
    f.close()
    return eval(data)


dic = load_dict_from_file()
best_words = []
counter = 1
while counter <= 200:
    # print(str(counter) + " " + str(dic[-counter]))
    best_words.append(dic[-counter][0])
    counter += 1

# print(best_words)

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


# print(docs.keys())
# print(docs.values())
# print(word_counter)

prior_probility = {}

for key, value in docs.items():
    x = value / count_of_document
    prior_probility[key] = x

# print(prior_probility)


lines_test = [line.rstrip('\n') for line in open('HAM-Test.txt', encoding="utf8")]
all_test_documents = len(lines_test)

deltas = [0.1, 0.3, 0.5]

confusion_matrix = collections.defaultdict(lambda: 0)
fp_matrix = collections.defaultdict(lambda: 0)
fp_matrix2 = collections.defaultdict(lambda: 0)

for line in lines_test[:]:
    # print(line)
    delimiter = line.find('@@@@@@@@@@')
    test_doc_type = line[:delimiter]
    line = line[delimiter+10:]
    for step in deltas:
        each_line_score = {}
        tokens = nltk.word_tokenize(line)
        for doc_type in docs.keys():
            not_zero_counter = 0
            term1 = []
            for token in tokens:
                if token not in best_words:
                    continue
                x = matrix[doc_type, token] - step
                if x < 0:
                    x = 0
                else:
                    not_zero_counter += 1
                x = x/matrix[doc_type]
                y = matrix[doc_type]
                term1.append(x)
            a = (step/matrix[doc_type]) * not_zero_counter
            # term2 = a * 1/word_counter
            term2 = a * 1/len(tokens)
            # print(term2)
            multiple_accumulator = 1
            for word_score in term1:
                multiple_accumulator *= math.log2((word_score + term2))
                # print(multiple_accumulator)
            each_line_score[doc_type] = multiple_accumulator
        result = sorted(each_line_score.items(), key=lambda kv: kv[1])
        label = result[0][0]
        real = test_doc_type
        if label == real:
            confusion_matrix[step, real, "tp"] += 1
        else:
            confusion_matrix[step, real, "fn"] += 1
            fp_matrix[step, label] += 1
            fp_matrix2[step, real, label] += 1

# print(confusion_matrix)
# save_dict_to_file(confusion_matrix, "confusion_matrix_unigram_without_feature_selection.txt")

print("Confusion Matrix:")
print(confusion_matrix)
print()
print(fp_matrix2)
print()

precision = {}
recall = {}

for step in deltas:
    for doc_type in docs.keys():
        precision[step, doc_type] = confusion_matrix[step, doc_type, "tp"]/(confusion_matrix[step, doc_type, "tp"] + fp_matrix[step, doc_type])
        recall[step, doc_type] = confusion_matrix[step, doc_type, "tp"]/(confusion_matrix[step, doc_type, "fn"] + fp_matrix[step, doc_type])

print("Precision:")
print(precision)
print("")
print("Recall:")
print(recall)
print("")

f_measure = {}
for step in deltas:
    for doc_type in docs.keys():
        f_measure[step, doc_type] = (2 * precision[step, doc_type] * recall[step, doc_type]) / (precision[step, doc_type] + recall[step, doc_type])
print("F-measure:")
print(f_measure)
print("")
micro_averaged = collections.defaultdict(lambda: 0)
macro_averaged = {}

weight = {}
for step in deltas[:1]:
    for doc_type in docs.keys():
        weight[doc_type] = confusion_matrix[step, doc_type, "tp"] + confusion_matrix[step, doc_type, "fn"]
        # print(weight[doc_type])

sum_of_precisions = collections.defaultdict(lambda: 0)
sum_of_recalls = collections.defaultdict(lambda: 0)
sum_of_f_measure = collections.defaultdict(lambda: 0)
for step in deltas[:]:
    for doc_type in docs.keys():
        sum_of_precisions[step] += precision[step, doc_type]
        sum_of_recalls[step] += recall[step, doc_type]
        sum_of_f_measure[step] += f_measure[step, doc_type]
    macro_averaged[step, "Macro_precision"] = sum_of_precisions[step] / 5
    macro_averaged[step, "Macro_recalls"] = sum_of_recalls[step] / 5
    macro_averaged[step, "Macro_f_measure"] = sum_of_f_measure[step] / 5

print(macro_averaged)


for step in deltas[:]:
    for doc_type in docs.keys():
        micro_averaged[step, "Micro_precision"] += precision[step, doc_type] * (weight[doc_type] / all_test_documents)
        micro_averaged[step, "Micro_recalls"] += recall[step, doc_type] * (weight[doc_type] / all_test_documents)
        micro_averaged[step, "micro_f_measure"] += f_measure[step, doc_type] * (weight[doc_type] / all_test_documents)

print(micro_averaged)