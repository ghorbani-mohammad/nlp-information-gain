import nltk
import io, sys


stop_words = [line.rstrip('\n') for line in open('Stop_words.txt', encoding="utf8")]


lines = [line.rstrip('\n') for line in open('HAM-Train.txt', encoding="utf8")]


# Number of document
count_of_document=len(lines)

docs = {}

# count number of each document type
for line in lines[:]:
    delimiter = line.find('@@@@@@@@@@')
    doc_type = line[:delimiter]
    docs[doc_type] = docs.get(doc_type, 0) + 1
    # print(line)


print(docs.keys())
print(docs.values())
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


