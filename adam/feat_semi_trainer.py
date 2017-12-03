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
            trans_data_train[col] = [0 for i in range(len(X_train.index))]
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


def get_feat_predict_data(token, qclass):

    feat = token.text
    feat_pos = token.tag_
    feat_dep = token.dep_
    feat_ent_label = token.ent_type_
    feat_shape = token.shape_

    if feat_ent_label == "":
        feat_ent_label = "NON"

    fdata_frame = [{'QType': qclass, 'F-POS': feat_pos, 'F-DEP': feat_dep, 'F-ENT': feat_ent_label, 'F-SHAPE': feat_shape}]

    dta = pandas.DataFrame(fdata_frame)
    return dta


def classify_question(en_doc):

    dta = pandas.read_csv('corpus/semi_feature_trainer.csv', sep='|')
    # get_data_info(dta)

    y = dta.pop('Class')
    dta.pop('Question')
    dta.pop('F-TXT')

    X_train = pre_process(dta)

    question_data = get_feat_predict_data(en_doc)
    X_predict = pre_process(question_data)

    X_train, X_predict = transform_data_matrix(X_train, X_predict)

    return str(support_vector_machine(X_train, y, X_predict))


en_nlp = spacy.load("en_core_web_md")
dta = pandas.read_csv('corpus/semi_feature_trainer.csv', sep='|')
# get_data_info(dta)

y = dta.pop('Class')
dta.pop('#Question')
dta.pop('F-TXT')

X_train = pre_process(dta)

# print(X_train.shape)

question = "What South American city has the world's highest commercial landing field ?"
qclass = "LOC"
en_doc = en_nlp(u'' + question)
sent_list = list(en_doc.sents)
sent = sent_list[0]

for token in sent:
    feat_data = get_feat_predict_data(token, qclass)

    X_predict = pre_process(feat_data)
    # print(X_predict)
    # print(X_train)

    X_train, X_predict = transform_data_matrix(X_train, X_predict)

    # print(naive_bayes_classifier(X_train, y, X_predict))
    print(token.text, support_vector_machine(X_train, y, X_predict))