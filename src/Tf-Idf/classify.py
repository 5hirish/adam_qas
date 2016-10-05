from math import sqrt
from math import log
from collections import Counter
from operator import itemgetter

'''
TF: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is often divided by the document length (aka. the total number of terms in the document) as a way of normalization: 
TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

IDF: Inverse Document Frequency, which measures how important a term is. While computing TF, all terms are considered equally important. However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance. Thus we need to weigh down the frequent terms while scale up the rare ones, by computing the following: 
IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
'''



def tf(kt,doc):											#Term Frequency
 return (doc.count(kt))

def idf(kt,all_docs):										#Inverse Document Frequency
 num=0 
 for x in all_docs:
  if kt in x:
   num=num+1
 if num>0:
  return round(float(log(float(len(all_docs))/float(num))),3)
 else:
  return 0

def tfidf(kt,doc):										#Total Tf-Idf
 return (tf(kt,doc)*idf(kt,all_docs))

def cos_sim(infile,docs,ktrms):								#Cosine Similarity Function
 a=0
 for x in ktrms:
  a=a+tfidf(x,infile)*tfidf(x,docs)
 b=doclen(infile,ktrms)*doclen(docs,ktrms)
 if not b:
  return 0
 else:
  return (round((a/b),3))

def doclen(doc,ktrms):									#length of the doc
 val=0
 for x in ktrms:
  val=val+pow(tfidf(x,doc),2)
 return sqrt(val)

files=[]
all_docs=[]
key_terms=[]

documents=['doc1.txt','doc2.txt','doc3.txt','doc4.txt']
result=[['doc1.txt','animals'],['doc2.txt','animals'],['doc3.txt','sports'],['doc4.txt','sports']]

for x in documents:
 files.append(open(x,'r').read())

for x in files:
 all_docs.append(x.lower().rstrip('\n'))

'''
def SentTokenizer(text):
    result = text
    result = result.replace('.', ' . ')
    result = result.replace(' .  .  . ', ' ... ')
    result = result.replace(',', ' , ')
    result = result.replace(':', ' : ')
    result = result.replace(';', ' ; ')
    result = result.replace('!', ' ! ')
    result = result.replace('?', ' ? ')
    result = result.replace('\"', ' \" ')
    result = result.replace('\'', ' \' ')
    result = result.replace('(', ' ( ')
    result = result.replace(')', ' ) ')
    result = result.replace('  ', ' ')
    result = result.strip()
    result = result.split(' ')
    return result
'''


for x in all_docs:
 key_terms=key_terms+x.split()
key_terms=set(key_terms)
key_terms=list(key_terms)

filename=raw_input("file: ")
inputfile=open(filename,'r').readline().lower()

cnt=0
for x in all_docs:
 result[cnt]=result[cnt]+[cos_sim(inputfile,x,key_terms)]
 cnt=cnt+1
print result
print ""

k=3
sortedresult=sorted(result,key=itemgetter(2),reverse=True)
top_k=sortedresult[:k]
top_k[:]=(x for x in top_k if x[2]!=0)
if len(top_k)==0:
 print "Does not match"
else:
 class_count=Counter(category for (document,category,value) in top_k)
 print class_count,
 classification=max(class_count,key=lambda cls:class_count[cls])
 print "Type of file: ",classification


