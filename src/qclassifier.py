from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
import pandas
import spacy


def get_data_info(dta):
    print(dta.head())
    print(dta.info())
    print(dta.describe())
    print(dta.columns)
    print(dta.groupby('WH').describe())


def pre_process(dta):
    return pandas.get_dummies(dta)


def naive_bayes_classifier(X_train, y, X_predict):
    gnb = GaussianNB()
    gnb.fit(X_train, y)
    prediction = gnb.predict(X_predict)
    return prediction


def support_vector_machine(X_train, y, X_predict):
    lin_clf = LinearSVC()
    lin_clf.fit(X_train, y)
    prediction = lin_clf.predict(X_predict)
    return prediction


def get_question_predict_data(question, en_nlp, column_list):
    en_doc = en_nlp(u'' + question)
    sent_list = list(en_doc.sents)
    sent = sent_list[0]
    wh_bi_gram = []
    root_token = ""
    wh_pos = ""
    wh_nbor_pos = ""
    wh_word = ""
    for token in sent:
        if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            wh_pos = token.tag_
            wh_word = token.text
            wh_bi_gram.append(token.text)
            wh_bi_gram.append(str(en_doc[token.i + 1]))
            wh_nbor_pos = en_doc[token.i + 1].tag_
        if token.dep_ == "ROOT":
            root_token = token.tag_
    qdata_frame = [{'WH':wh_word, 'WH-POS':wh_pos, 'WH-NBOR-POS':wh_nbor_pos, 'Root-POS':root_token}]
    # qdata_list = [wh_word, wh_pos, wh_nbor_pos, root_token]
    # dta = pandas.DataFrame(qdata_list, columns=column_list)
    dta = pandas.DataFrame(qdata_frame)
    return dta


en_nlp = spacy.load("en")
pandas.set_option('max_rows', 7)
dta = pandas.read_csv('corpus/qclassifier_trainer.csv', sep='|')
# get_data_info(dta)

y = dta.pop('Class')
dta.pop('Question')
dta.pop('WH-Bigram')

X_train = pre_process(dta)

# print(X_train.shape)
column_list = list(X_train.columns)
# print(len(column_list))
question = 'Who is Linus Torvalds ?'
question_data = get_question_predict_data(question, en_nlp, column_list)
X_predict = pre_process(question_data)
print(X_predict)
print(X_train)

# print(naive_bayes_classifier(X_train, y, X_predict))
print(support_vector_machine(X_train, y, X_predict))

# ValueError: operands could not be broadcast together with shapes (1,4) (66,)
# ValueError: X has 4 features per sample; expecting 1228
# Training - [5452 rows x 66 columns]
# Predict - [1 rows x 4 columns]
