import tensorflow as tf
import pandas as pd
import numpy as np

new_model = tf.keras.models.load_model('model-001')

df = pd.read_csv('raw_model.csv')

df = df[:]

x_columns = df.columns.drop('outcome')  # Получаем все колонки кроме outcome
x = df[x_columns].values  # Получаем значения в колонках

dummies = pd.get_dummies(df['outcome'])  # Получаем фиктивные пере-менные
outcomes = dummies.columns  # Получаем названия фиктивных переменных
num_classes = len(outcomes)  # Получаем количество классов, по которым будет происходить классификация
y = dummies.values  # Получаем значения из выборки
df.groupby('outcome')['outcome'].count()

x = np.asarray(x).astype(np.float32)
y = np.asarray(y).astype(np.float32)

print(dummies.columns)
print(y[1000000])

xtrain = tf.expand_dims(x, axis=1)


predict = new_model.predict(xtrain[1000000])[0]

for index, num in enumerate(predict):
    if num == np.float32(1):
        print(dummies.columns[index])
        break

with open('4.json', 'w') as file:
    for x in dummies.columns:
        file.write(str(x)+'\n')

