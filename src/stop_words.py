import os
from collections import Counter

path = os.path.dirname(os.path.realpath(__file__))
path = path.replace("/src", "/corpus/")
fp = open(path+"linus_torvalds.txt", "r")
fpw = open(path+"stop_words.txt", "w")

stop_words = Counter()
for line in fp:
    line = line.lower()
    stop_words.update(line.split())
for word, count in stop_words.most_common(20):
    print (word, count)
    fpw.write(word+" : "+str(count)+"\n")

fp.close()
fpw.close()
