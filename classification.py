import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

rand = 1
test_sz = 0.3

cracked_vibrations = pd.read_csv('./database/cracked_vibrations.csv') # mean vibrations and is_cracked
fourier_vibrations = pd.read_csv('./database/vibrations_fourier.csv') # dominant frequencies and is_cracked
both_features_df = pd.merge(cracked_vibrations.drop(['is_cracked'], axis=1), fourier_vibrations, on='bottle')


# Using only the mean-vibration data as the feature
X = cracked_vibrations['mean_vibration'].values.reshape(-1, 1)
y = cracked_vibrations['is_cracked'].values

# Using only the dominant frequency data as the feature
X_fourier = fourier_vibrations[['dominant_freq_50Hz', 'dominant_freq_100Hz', 'dominant_freq_150Hz']].values
y_fourier = fourier_vibrations['is_cracked'].values

# Using both features
X_both = both_features_df[['mean_vibration', 'dominant_freq_50Hz', 'dominant_freq_100Hz', 'dominant_freq_150Hz']].values
y_both = both_features_df['is_cracked'].values

#-------------------------------------------------------------------------------------------------------------------#

# Splitting the mean data into training- and test-data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_sz, random_state=rand)

# Splitting the fourier data into training- and test-data
X_train_fourier, X_test_fourier, y_train_fourier, y_test_fourier = train_test_split(X_fourier, y_fourier, test_size=test_sz, random_state=rand)

# Splitting the combined data into training- and test-data
X_train_both, X_test_both, y_train_both, y_test_both = train_test_split(X_both, y_both, test_size=test_sz, random_state=rand)

#-------------------------------------------------------------------------------------------------------------------#

#model = DecisionTreeClassifier()
#model_fourier = DecisionTreeClassifier()
#model_both = DecisionTreeClassifier()

model = KNeighborsClassifier(n_neighbors=3)
model_fourier = KNeighborsClassifier(n_neighbors=3)
model_both = KNeighborsClassifier(n_neighbors=3)

#model = LogisticRegression()
#model_fourier = LogisticRegression()
#model_both = LogisticRegression()

#-------------------------------------------------------------------------------------------------------------------#

model.fit(X_train, y_train)
model_fourier.fit(X_train_fourier, y_train_fourier)
model_both.fit(X_train_both, y_train_both)

y_pred = model.predict(X_test)
y_pred_fourier = model_fourier.predict(X_test_fourier)
y_pred_both = model_both.predict(X_test_both)

cm = confusion_matrix(y_test, y_pred)
cm_fourier = confusion_matrix(y_test_fourier, y_pred_fourier)
cm_both = confusion_matrix(y_test_both, y_pred_both)
print(cm)
print(cm_fourier)
print(cm_both)

f1_train = f1_score(y_train, model.predict(X_train))
f1_test = f1_score(y_test, y_pred)

f1_train_fourier = f1_score(y_train_fourier, model_fourier.predict(X_train_fourier))
f1_test_fourier = f1_score(y_test_fourier, y_pred_fourier)

f1_train_both = f1_score(y_train_both, model_both.predict(X_train_both))
f1_test_both = f1_score(y_test_both, y_pred_both)

print(f'F1 score on training set (Mean): {f1_train}')
print(f'F1 score on test set (Mean): {f1_test}')

print(f'F1 score on training set (Fourier): {f1_train_fourier}')
print(f'F1 score on test set (Fourier): {f1_test_fourier}')

print(f'F1 score on training set (Both): {f1_train_both}')
print(f'F1 score on test set (Both): {f1_test_both}')