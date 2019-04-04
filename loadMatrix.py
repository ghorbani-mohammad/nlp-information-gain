def load_dict_from_file(file):
    f = open(file, 'r', encoding="utf8")
    data = f.read()
    f.close()
    return eval(data)


print(load_dict_from_file("confusion_matrix_unigram_without_feature_selection.txt"))
