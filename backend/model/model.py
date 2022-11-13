import pandas as pd
import numpy as np
import pickle
df = pd.read_csv('fulldata.csv', delimiter='\t', index_col=0)

#print(df.shape)
#print(df.head())

df = df.iloc[1: , :]
df = df.rename(columns={'type': 'drunkTest'})
df['drunkTest'] = df['drunkTest'].map({'Drunk': 1, 'Sober': 0})
df = df[df['drunkTest'].notna()]


X = df.drop("drunkTest", axis = 1)
y = df["drunkTest"]

#print(X.shape)

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

model = RandomForestClassifier(n_estimators = 100, random_state = 24)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#print(X_train.shape)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
a = (f1_score(y_test, y_pred))
b = (accuracy_score(y_test, y_pred))
print("f1-score: ", np.mean(a))
print("average-score: ", np.mean(b))

filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(X_test)
#print(y_pred)
#print(y_test)
a = (f1_score(y_test, y_pred))
b = (accuracy_score(y_test, y_pred))
print("re calc f1-score: ", np.mean(a))
print("re calc average-score: ", np.mean(b))