import os
import logging
import pandas

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.sparse import csr_matrix

from qas.constants import CORPUS_DIR

logger = logging.getLogger(__name__)


def get_data_info(question_df):
    print(question_df.head())
    print(question_df.info())
    print(question_df.describe())
    print(question_df.columns)


def pre_process(question_df):
    return pandas.get_dummies(question_df)


def transform_data_matrix(df_question_train):

    # Generate Compressed Sparse Row matrix:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
    df_question_train = csr_matrix(df_question_train)

    return df_question_train


def naive_bayes_classifier(df_question_train, df_question_class):
    gnb = GaussianNB()
    gnb.fit(df_question_train, df_question_class)
    logger.info("Gaussian Naive Bayes: {0}".format(gnb))

    return gnb


def support_vector_machine(df_question_train, df_question_class):
    lin_clf = LinearSVC()
    lin_clf.fit(df_question_train, df_question_class)
    logger.info("Linear SVC: {0}".format(lin_clf))

    return lin_clf


def save_classifier_model(df_question_train, df_question_class, type="linearSVC"):

    classifier_model = None
    training_model_path = os.path.join(CORPUS_DIR, 'question_classifier.pkl')

    if type == "linearSVC":
        classifier_model = support_vector_machine(df_question_train, df_question_class)
    else:
        logger.error("Undefined Classifier")

    if classifier_model is not None:
        joblib.dump(classifier_model, training_model_path)
        logger.info("Model saved at {0}".format(training_model_path))
    else:
        logger.error("Model empty")


def remove_irrelevant_features(df_question):
    df_question_class = df_question.pop('Class')

    df_question.pop('Question')
    df_question.pop('WH-Bigram')

    return df_question_class


def train_question_classifier():
    """
    Question Classifier based on its feature.
    CSV: Training Data `qclassifier_trainer.csv`
        #Question|WH|WH-Bigram|WH-POS|WH-NBOR-POS|Root-POS|Class
    Using: Linear Support Vector Machine
    Model: Saved as Pickle `question_classifier.pkl`
    """

    training_data_path = os.path.join(CORPUS_DIR, 'qclassifier_trainer.csv')
    df_question = pandas.read_csv(training_data_path, sep='|', header=0)

    df_question_class = remove_irrelevant_features(df_question)

    df_question_train = pre_process(df_question)

    df_question_train = transform_data_matrix(df_question_train)

    save_classifier_model(df_question_train, df_question_class)


if __name__ == "__main__":

    from time import time

    logging.basicConfig(level=logging.DEBUG)
    start_time = time()

    train_question_classifier()

    end_time = time()
    logger.info("Total training time : {0}".format(end_time - start_time))
