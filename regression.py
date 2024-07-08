import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# read data from X.csv to predict
test_data = pd.read_csv('./database/X.csv', index_col=0)
#print(test_data.head())

# Read data to train on
data = pd.read_csv('./database/combined.csv')

X = data.drop(['bottle', 'final_weight'], axis=1)
y = data['final_weight']
print(X.head())


test_data = test_data.drop(['temperature_mean_C'], axis=1)
test_data = test_data.rename(columns={'vibration-index_red_vibration':'vibration-index_red',
                                      'vibration-index_blue_vibration':'vibration-index_blue',
                                      'vibration-index_green_vibration':'vibration-index_green'})
test_data = test_data.reindex(columns=['fill_level_grams_red', 'fill_level_grams_blue', 'fill_level_grams_green', 'vibration-index_red', 'vibration-index_blue', 'vibration-index_green'])
print(test_data.head())


#-------------Excluding the fill levels for the different colors----------------
#X = X.drop(['fill_level_grams_red', 'fill_level_grams_blue', 'fill_level_grams_green'], axis=1)

#-------------Excluding vibration data----------------
#X = X.drop(['vibration-index_red', 'vibration-index_blue', 'vibration-index_green'], axis=1)
#print(X.head())


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lin_model = LinearRegression()
lin_model.fit(X_train, y_train)

lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)

ridge_model = Ridge(alpha=0.1)
ridge_model.fit(X_train, y_train)

#poly_model = make_pipeline(PolynomialFeatures(2), LinearRegression())
#poly_model.fit(X_train, y_train)

models = [lin_model, lasso_model, ridge_model]

for model in models:
    print(F"Model: {model}")
    #print(F"Regression Coefficients: {model.coef_}")
    y_predict = model.predict(X_test)

    print(F"Mean Squared Error Testing of {model}: {mean_squared_error(y_test, y_predict)}")
    print(F"Mean Squared Error Training of {model}: {mean_squared_error(y_train, model.predict(X_train))}")
    print("\n")

test_data_predict = lin_model.predict(test_data)
#test_predicted_df = pd.DataFrame(test_data_predict, columns=['Flaschen ID','y_hat'])
test_predicted_df = pd.DataFrame({'Flaschen ID': test_data.index+1, 'y_hat': test_data_predict})
test_predicted_df.to_csv('./database/52216067-62200066-61901292.csv', index=False)

print(lin_model.coef_)
print(lin_model.intercept_)