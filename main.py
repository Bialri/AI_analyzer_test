import numpy as np
import pandas as pd
import json

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten

df = pd.read_csv('kddcup.data.corrected', header=None)

z_scores = {}

columns = []
numeric_col = []
symbolic_col = []

with open('kddcup.names', 'r') as file:
    file.readline()
    data = file.readlines()
    data = [x.strip().replace(':', '').replace('.', '') for x in data]
    data = [tuple(x.split()) for x in data]
    for column in data:
        match column:

            case (name, 'continuous'):
                columns.append(name)
                numeric_col.append(name)

            case (name, 'symbolic'):
                columns.append(name)
                symbolic_col.append(name)

symbolic_col.remove('is_host_login')
symbolic_col.remove('is_guest_login')

df.columns = columns + ['outcome', ]

print(df)


def encode_numeric_zscore(df, name):
    mean = df[name].mean()  # Вычисляем среднее значение
    print(name + "(mean):" + str(mean))
    sd = df[name].std()  # Вычисляем среднеквадратическое отклонение
    print(name + "(sd):" + str(sd))
    z_scores[name] = {'mean': mean, 'sd': sd}
    # Z-оценка
    df[name] = (df[name] - mean) / sd


def encode_text_dummy(df, name):
    # Получаем фиктивные переменные
    dummies = pd.get_dummies(df[name])
    # Для каждой фиктивной переменной создаем новый столбец
    for x in dummies.columns:
        dummy_name = f"{name}-{x}"
        df[dummy_name] = dummies[x]
    # Удаляем оригинальный столбец
    df.drop(name, axis=1, inplace=True)


for column_name in numeric_col:
    encode_numeric_zscore(df, column_name)

with open('z_scrores.json','w') as file:
    json_z_scores = json.dumps(z_scores)
    file.write(json_z_scores)

for column_name in symbolic_col:
    encode_text_dummy(df, column_name)

# просмотр 5 строк
df.dropna(inplace=True, axis=1)
print(df.columns)
print(df.shape)

# df.to_csv('raw_model.csv', index=False)

with open('column_names.json', 'w') as file:
    out_columns = list(df.columns)
    out_columns.remove('outcome')
    json_out_columns = json.dumps(out_columns)
    file.write(json_out_columns)

df = df[:]

# конвертация данных
x_columns = df.columns.drop('outcome')  # Получаем все колонки кроме outcome
x = df[x_columns].values  # Получаем значения в колонках
dummies = pd.get_dummies(df['outcome'])  # Получаем фиктивные пере-менные
outcomes = dummies.columns  # Получаем названия фиктивных переменных
num_classes = len(outcomes)  # Получаем количество классов, по которым будет происходить классификация
y = dummies.values  # Получаем значения из выборки
df.groupby('outcome')['outcome'].count()  # Полуаем значение для каждой атаки

# Создаем данные для обучения и разделяем набор на тестовую и обуча-ющую выборку тестовая - 25%
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42)

print(df.columns)

# x_train = np.asarray(x_train).astype(np.float32)
# y_train = np.asarray(y_train).astype(np.float32)
# x_test = np.asarray(x_test).astype(np.float32)
# y_test = np.asarray(y_test).astype(np.float32)
#
#
# model = Sequential()  # Создаем модель
#
# model.add(Flatten(input_shape=(x.shape[1],)))  # Добавляем 1 скрытый слой
#
# model.add(Dense(128, kernel_initializer='normal', activation='relu'))  # Добавляем 2 скрытый слой
#
# model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))  # Добавляем выходной слой
# model.compile(loss='categorical_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])  # Компилируем модель
#
# model.fit(x_train, y_train, validation_data=(x_test, y_test), verbose=1,
#           epochs=25)  # Обучаем модель
#
#
# model.summary()  # Просмотр структуры сети
#
# model.save('model-001', overwrite=True, include_optimizer=True)
