import os
import logging
import pandas

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.sparse import csr_matrix

from qas.constants import CORPUS_DIR, EN_MODEL_MD
from qas.corpus.data import QUESTION_CLASSIFICATION_TRAINING_DATA, QUESTION_CLASSIFICATION_MODEL

logger = logging.getLogger(__name__)


def pre_process(dta):
    return pandas.get_dummies(dta)


def remove_irrelevant_features(df_question):
    df_question_class = df_question.pop('Class')

    df_question.pop('Question')
    df_question.pop('WH-Bigram')

    return df_question_class


def transform_data_matrix(df_question_train, df_question_predict):

    df_question_train_columns = list(df_question_train.columns)
    df_question_predict_columns = list(df_question_predict.columns)

    df_question_trans_columns = list(set(df_question_train_columns + df_question_predict_columns))

    trans_data_train = {}

    for feature in df_question_trans_columns:
        if feature not in df_question_train:
            trans_data_train[feature] = [0 for i in range(len(df_question_train.index))]
        else:
            trans_data_train[feature] = list(df_question_train[feature])

    df_question_train = pandas.DataFrame(trans_data_train)
    df_question_train = csr_matrix(df_question_train)

    trans_data_predict = {}

    for feature in trans_data_train:
        if feature not in df_question_predict:
            trans_data_predict[feature] = 0
        else:
            trans_data_predict[feature] = list(df_question_predict[feature])  # KeyError

    df_question_predict = pandas.DataFrame(trans_data_predict)
    df_question_predict = csr_matrix(df_question_predict)

    return df_question_train, df_question_predict


def naive_bayes_classifier(X_train, y, X_predict):
    gnb = GaussianNB()
    gnb.fit(X_train, y)
    prediction = gnb.predict(X_predict)
    return prediction


def support_vector_machine(question_clf, X_predict):
    return question_clf.predict(X_predict)


def load_classifier_model(model_type="linearSVC"):

    training_model_path = os.path.join(CORPUS_DIR, QUESTION_CLASSIFICATION_MODEL)

    if model_type == "linearSVC":
        return joblib.load(training_model_path)


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
    qdata_frame = [{'WH': wh_word, 'WH-POS': wh_pos, 'WH-NBOR-POS': wh_nbor_pos, 'Root-POS': root_token}]
    # qdata_list = [wh_word, wh_pos, wh_nbor_pos, root_token]
    # dta = pandas.DataFrame(qdata_list, columns=column_list)
    dta = pandas.DataFrame(qdata_frame)
    return dta


def classify_question(en_doc):
    """ Determine whether this is a who, what, when, where or why question """

    training_data_path = os.path.join(CORPUS_DIR, QUESTION_CLASSIFICATION_TRAINING_DATA)
    df_question = pandas.read_csv(training_data_path, sep='|', header=0)

    df_question_class = remove_irrelevant_features(df_question)
    question_data = get_question_predict_data(en_doc)

    df_question_train = pre_process(df_question)
    df_question_predict = pre_process(question_data)

    df_question_train, df_question_predict = transform_data_matrix(df_question_train, df_question_predict)

    question_clf = load_classifier_model()

    predicted_class = support_vector_machine(question_clf, df_question_predict)

    return str(predicted_class)


if __name__ == "__main__":

    import spacy
    from time import time

    logging.basicConfig(level=logging.DEBUG)
    start_time = time()
    en_nlp = spacy.load(EN_MODEL_MD)

    question = 'Who is Linus Torvalds ?'
    en_doc_l = en_nlp(u'' + question)

    question_class = classify_question(en_doc_l)

    logger.info("Class: {0}".format(question_class))

    end_time = time()
    logger.info("Total training time : {0}".format(end_time - start_time))
