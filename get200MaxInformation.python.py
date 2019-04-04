def load_dict_from_file():
    f = open('information_gain_calculated.txt', 'r', encoding="utf8")
    data = f.read()
    f.close()
    return eval(data)


dic = load_dict_from_file()
best_words = []
counter = 1
while counter <= 200:
    print(str(counter) + " " + str(dic[-counter]))
    best_words.append(dic[-counter][0])
    counter += 1

print(best_words)



