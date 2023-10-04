import pandas as pd
import numpy as np
import tensorflow as tf
import json


# model = tf.keras.models.load_model('model-001')
#
# statuses = []
#
# with open('statuses.json') as file:
#     statuses = list(map(lambda x: x.rstrip(), file.readlines()))
#
# with open('z_scrores.json','r') as file:
#     z_scores = json.loads(file.read())
#
# print(z_scores)

# columns = []
# numeric_col = []
# symbolic_col = []
#
# with open('kddcup.names', 'r') as file:
#     file.readline()
#     data = file.readlines()
#     data = [x.strip().replace(':', '').replace('.', '') for x in data]
#     data = [tuple(x.split()) for x in data]
#     for column in data:
#         match column:
#
#             case (name, 'continuous'):
#                 columns.append(name)
#                 numeric_col.append(name)
#
#             case (name, 'symbolic'):
#                 columns.append(name)
#                 symbolic_col.append(name)
#
# symbolic_col.remove('is_host_login')
# symbolic_col.remove('is_guest_login')


with open('trafAld.list') as file:
    first_row = file.readline().split(',')[6:]
    first_row = list(map(lambda x: float(x) if x.count('.') == 1 else int(x) if x.rstrip().replace('.', '').isnumeric() else x, first_row))
    del first_row[3]
    df = pd.DataFrame({name: [value] for name, value in zip(columns, first_row)})
    print(first_row)
    for row in file.readlines():
        row = row.split(',')[6:]
        row = list(map(lambda x: float(x) if x.count('.') == 1 else int(x) if x.rstrip().replace('.', '').isnumeric() else x, row))
        del row[3]
        df.loc[len(df.index)] = {name: value for name, value in zip(columns, row)}



# def encode_numeric_zscore(df, name):
#     mean = z_scores[name]['mean']
#     sd = z_scores[name]['sd']
#     # Z-оценка
#     df[name] = (df[name] - mean) / sd
#
# def encode_text_dummy(df, name):
#     # Получаем фиктивные переменные
#     dummies = pd.get_dummies(df[name])
#     # Для каждой фиктивной переменной создаем новый столбец
#     for x in dummies.columns:
#         dummy_name = f"{name}-{x}"
#         df[dummy_name] = dummies[x]
#     # Удаляем оригинальный столбец
#     df.drop(name, axis=1, inplace=True)



# with open('column_names.json','r') as file:
#     dummies = json.loads(file.read())


for column in dummies:
    df[column] = False


for column_name in symbolic_col:
    encode_text_dummy(df, column_name)

for column_name in numeric_col:
    encode_numeric_zscore(df, column_name)

df = df.fillna(0.0)


print(df)

print(df.columns)
print(df.shape)


difference = set(df.columns).difference(dummies)

df = df.drop(difference,axis=1)
print(df.shape)

x = df.values
x = np.asarray(x).astype(np.float32)


predict = model.predict(x)

for row in predict:
    for index, num in enumerate(row):
        if num == np.float32(1):
            print(statuses[index])
            break

