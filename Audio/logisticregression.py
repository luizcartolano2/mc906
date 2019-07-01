import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv('features_2.csv', sep=';')
X = df.drop(['genre'], axis=1) 
Y = df[["genre"]]

scaler = StandardScaler()
X = scaler.fit_transform(X)

train_x, test_x, train_y, test_y = train_test_split(X,Y, train_size=0.7)

lr = linear_model.LogisticRegression()
lr.fit(train_x, train_y)
print ("Logistic regression multiclass Train Accuracy :: ", lr.score(train_x, train_y))
print ("Logistic regression multiclass Test Accuracy :: ", lr.score(test_x, test_y))

lr_mul = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)

print ("Multinomial Logistic regression Train Accuracy :: ", lr_mul.score(train_x, train_y))
print ("Multinomial Logistic regression Test Accuracy :: ", lr_mul.score(test_x, test_y))

song_a = X[0:5]
song_b = X[9000:9005]
song_c = X[10500:10600]

pred_a = lr.predict(song_a)
pred_b = lr.predict(song_b)
pred_c = lr.predict(song_c)

real_a = Y[0:5]
real_b = Y[9000:9005]
real_c = Y[10500:10600]
