import neurokit2 as nk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

rand = 1

cracked_vibrations = pd.read_csv('./database/cracked_vibrations.csv')
fourier_vibrations = pd.read_csv('./database/vibrations_fourier.csv')

# Using the mean-vibration data as the feature
X = cracked_vibrations['mean_vibration'].values.reshape(-1, 1)
y = cracked_vibrations['is_cracked'].values

# Using the dominant frequency data as the feature
X_fourier = fourier_vibrations[['dominant_freq_50Hz', 'dominant_freq_100Hz', 'dominant_freq_150Hz']].values
y_fourier = fourier_vibrations['is_cracked'].values

# Splitting the mean data into training- and test-data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=rand)

# Splitting the fourier data into training- and test-data
X_train_fourier, X_test_fourier, y_train_fourier, y_test_fourier = train_test_split(X_fourier, y_fourier, test_size=0.3, random_state=rand)

#model = DecisionTreeClassifier()
#model_fourier = DecisionTreeClassifier()
model = KNeighborsClassifier(n_neighbors=3)
model_fourier = KNeighborsClassifier(n_neighbors=3)
#model = LogisticRegression()
#model_fourier = LogisticRegression()


model.fit(X_train, y_train)
model_fourier.fit(X_train_fourier, y_train_fourier)

y_pred = model.predict(X_test)
y_pred_fourier = model_fourier.predict(X_test_fourier)

cm = confusion_matrix(y_test, y_pred)
cm_fourier = confusion_matrix(y_test_fourier, y_pred_fourier)
print(cm)
print(cm_fourier)

f1_train = f1_score(y_train, model.predict(X_train))
f1_test = f1_score(y_test, y_pred)

f1_train_fourier = f1_score(y_train_fourier, model_fourier.predict(X_train_fourier))
f1_test_fourier = f1_score(y_test_fourier, y_pred_fourier)

print(f'F1 score on training set: {f1_train}')
print(f'F1 score on test set: {f1_test}')


print(y_train_fourier)
print(model_fourier.predict(X_train_fourier))

print(y_test_fourier)
print(y_pred_fourier)

print(f'F1 score on training set (Fourier): {f1_train_fourier}')
print(f'F1 score on test set (Fourier): {f1_test_fourier}')
