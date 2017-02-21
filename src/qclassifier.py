from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import pandas
from sklearn.preprocessing import LabelBinarizer


def get_data_info(dta):
    print(dta.head())
    print(dta.info())
    print(dta.describe())
    print(dta.columns)
    print(dta.groupby('WH').describe())


def pre_process(dta):
    X_train = pandas.get_dummies(dta)
    return X_train

pandas.set_option('max_rows', 7)
dta = pandas.read_csv('corpus/qclassifier_trainer.csv', sep='|')
# get_data_info(dta)

X_train = pre_process(dta)
print(X_train.shape)

