from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import pandas
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import LabelBinarizer


def get_data_info(dta):
    print(dta.head())
    print(dta.info())
    print(dta.describe())
    print(dta.columns)
    print(dta.groupby('WH').describe())


def pre_process(dta):
    return pandas.get_dummies(dta)

pandas.set_option('max_rows', 7)
dta = pandas.read_csv('corpus/qclassifier_trainer.csv', sep='|')
# get_data_info(dta)

y = dta.pop('Class')
print(dta.info())
X_train = pre_process(dta)
print(X_train.shape)

dtree = DecisionTreeClassifier(random_state=0, max_depth=2)
dtree.fit(X_train, y)
export_graphviz(dtree, feature_names=X_train.columns)