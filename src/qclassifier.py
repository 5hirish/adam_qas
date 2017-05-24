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


def pre_process(dta):
    return pandas.get_dummies(dta)


def transform_data_matrix(X_train, X_predict):
    X_train_columns = list(X_train.columns)
    X_predict_columns = list(X_predict.columns)

    X_trans_columns = list(set(X_train_columns + X_predict_columns))
    # print(X_trans_columns, len(X_trans_columns))

    trans_data_train = {}

    for col in X_trans_columns:
        if col not in X_train:
            trans_data_train[col] = [0 * len(X_train.index)]
        else:
            trans_data_train[col] = list(X_train[col])

    XT_train = pandas.DataFrame(trans_data_train)
    # get_data_info(XT_train)

    trans_data_predict = {}

    for col in X_trans_columns:
        if col not in X_predict:
            trans_data_predict[col] = 0
        else:
            trans_data_predict[col] = list(X_predict[col])  # KeyError

    XT_predict = pandas.DataFrame(trans_data_predict)
    # get_data_info(XT_predict)

    return XT_train, XT_predict


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


def get_question_predict_data(en_doc):
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


def classify_question(en_doc):

    dta = pandas.read_csv('corpus/qclassifier_trainer.csv', sep='|')
    # get_data_info(dta)

    y = dta.pop('Class')
    dta.pop('Question')
    dta.pop('WH-Bigram')

    X_train = pre_process(dta)

    question_data = get_question_predict_data(en_doc)
    X_predict = pre_process(question_data)

    X_train, X_predict = transform_data_matrix(X_train, X_predict)

    return str(support_vector_machine(X_train, y, X_predict))

"""
en_nlp = spacy.load("en_core_web_md")
dta = pandas.read_csv('corpus/qclassifier_trainer.csv', sep='|')
# get_data_info(dta)

y = dta.pop('Class')
dta.pop('Question')
dta.pop('WH-Bigram')

X_train = pre_process(dta)

# print(X_train.shape)

# print(len(column_list))

question = 'Who is Linus Torvalds ?'
# question = 'What is the colour of apple ?'
en_doc = en_nlp(u'' + question)

question_data = get_question_predict_data(question, en_doc)
X_predict = pre_process(question_data)
# print(X_predict)
# print(X_train)

X_train, X_predict = transform_data_matrix(X_train, X_predict)

# print(naive_bayes_classifier(X_train, y, X_predict))
print(support_vector_machine(X_train, y, X_predict))
"""