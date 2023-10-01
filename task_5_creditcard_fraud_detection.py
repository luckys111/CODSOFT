# -*- coding: utf-8 -*-
"""Task_5: CreditCard Fraud Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oNq6QJt4JLEXrilP62lji4QZCPd85Ef-

Task_5: CreditCard Fraud Detection

Importing Important Libraries
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

pd.set_option('display.max_columns',None)

#calling the dataset
df = pd.read_csv("creditcard.csv")
df.head()

"""Exploration on dataset"""

# dimensions of the dataset
df.shape

#datatypes
df.dtypes

# checking for the null values
df.isnull().sum()

# checking the balance of the dataset
fraud_count = df["Class"].value_counts()
fraud_rate = 100*fraud_count/df.shape[0]
fraud_data = pd.concat([fraud_count,fraud_rate],axis = 1).reset_index()
fraud_data.columns = ['Class','Count','Percentage']
fraud_data

"""Data Preparation"""

# handling imbalance
df_fraud = df[df['Class']==1]
df_not_fraud = df[df['Class']==0]
df_not_fraud_sampled =df_not_fraud.sample(df_fraud.shape[0],replace= False,random_state=101)
df_balanced = pd.concat([df_not_fraud_sampled,df_fraud],axis=0).sample(frac=1,replace=False,random_state=101).reset_index().drop('index',axis=1)
df_balanced

# checking the balance of the dataset
fraud_count = df_balanced["Class"].value_counts()
fraud_rate = 100*fraud_count/df.shape[0]
fraud_data = pd.concat([fraud_count,fraud_rate],axis = 1).reset_index()
fraud_data.columns = ['Class','Count','Percentage']
fraud_data

# train_test_split
x_train,x_test,y_train,y_test = train_test_split(df_balanced.drop('Class',axis=1),df_balanced['Class'],test_size=0.2,random_state=101)
print(f'''x_train:{x_train.shape}
x_test:{x_test.shape}
y_train:{y_train.shape}
y_test:{y_test.shape}''')

from sklearn.pipeline import Pipeline

"""Fitting a Random Forest mode"""

# logistic model pipe
randomForestModel = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier',RandomForestClassifier())
])
randomForestModel.fit(x_train,y_train)

# PREDICTION
y_pred_logis= randomForestModel.predict(x_test)
y_pred_logis

#classification report
cr = classification_report(y_test,y_pred_logis)
print(cr)

# saving model
with open('./model.pkl','wb')as fp:
    pickle.dump(randomForestModel,fp)