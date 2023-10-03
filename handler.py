import pathlib

import tensorflow as tf
from pathlib import Path, PosixPath
import pandas as pd
import json
import numpy as np


class Handler:

    def __init__(self, model_directory: PosixPath):
        self.model = tf.keras.models.load_model(model_directory)
        self.statuses = None
        self.z_scores = None
        self.model_columns = None
        self.columns = []
        self.numeric_col = []
        self.symbolic_col = []

    def load_statuses(self, status_list_file: PosixPath):
        with open(status_list_file, 'r') as file:
            self.statuses = json.loads(file.read())

    def load_z_scores(self, z_score_file: PosixPath):
        with open(z_score_file, 'r') as file:
            self.z_scores = json.loads(file.read())

    def load_model_columns(self, model_columns_file: PosixPath):
        with open(model_columns_file, 'r') as file:
            self.model_columns = json.loads(file.read())

    def load_column_names(self, column_names_file: PosixPath):
        with open(column_names_file, 'r') as file:
            file.readline()
            data = file.readlines()
            data = [x.strip().replace(':', '').replace('.', '') for x in data]
            data = [tuple(x.split()) for x in data]
            for column in data:
                match column:

                    case (name, 'continuous'):
                        self.columns.append(name)
                        self.numeric_col.append(name)

                    case (name, 'symbolic'):
                        self.columns.append(name)
                        self.symbolic_col.append(name)

        self.symbolic_col.remove('is_host_login')
        self.symbolic_col.remove('is_guest_login')

    def encode_numeric_zscore(self, df, name):
        mean = self.z_scores[name]['mean']
        sd = self.z_scores[name]['sd']
        # Z-оценка
        df[name] = (df[name] - mean) / sd

    @staticmethod
    def encode_text_dummy(df, name):
        # Получаем фиктивные переменные
        dummies = pd.get_dummies(df[name])
        # Для каждой фиктивной переменной создаем новый столбец
        for x in dummies.columns:
            dummy_name = f"{name}-{x}"
            df[dummy_name] = dummies[x]
        # Удаляем оригинальный столбец
        df.drop(name, axis=1, inplace=True)

    def convert_input_dataframe(self, df):
        for column in self.model_columns:
            df[column] = False

        for column_name in self.symbolic_col:
            self.encode_text_dummy(df, column_name)

        for column_name in self.numeric_col:
            self.encode_numeric_zscore(df, column_name)

        df = df.fillna(0.0)
        difference = set(df.columns).difference(self.model_columns)
        df = df.drop(difference, axis=1)

        return df

    def load_raw_data(self, list_file: PosixPath):
        with open(list_file) as file:
            first_row = file.readline().split(',')[6:]
            first_row = list(map(lambda x: float(x) if x.count('.') == 1 else int(x) if x.rstrip().replace('.',
                                                                                                           '').isnumeric() else x,
                                 first_row))
            del first_row[3]
            df = pd.DataFrame({name: [value] for name, value in zip(self.columns, first_row)})
            print(first_row)
            for row in file.readlines():
                row = row.split(',')[6:]
                row = list(map(lambda x: float(x) if x.count('.') == 1 else int(x) if x.rstrip().replace('.',
                                                                                                         '').isnumeric() else x,
                               row))
                del row[3]
                df.loc[len(df.index)] = {name: value for name, value in zip(self.columns, row)}
            return df

    def predict_data(self, df):
        x = df.values
        x = np.asarray(x).astype(np.float32)

        predict = self.model.predict(x)

        for row in predict:
            for index, num in enumerate(row):
                if num == np.float32(1):
                    print(self.statuses[index])
                    break


model_directory1 = pathlib.Path.cwd().joinpath('model-001')

handler = Handler(model_directory1)
statuses_file = pathlib.Path.cwd().joinpath('4.json')
z_score_file = pathlib.Path.cwd().joinpath('z_scrores.json')
model_columns_file = pathlib.Path.cwd().joinpath('column_names.json')
column_names_file = pathlib.Path.cwd().joinpath('kddcup.names')
list_files = pathlib.Path.cwd().joinpath('trafAld.list')

handler.load_column_names(column_names_file)
handler.load_statuses(statuses_file)
handler.load_model_columns(model_columns_file)
handler.load_z_scores(z_score_file)
df = handler.load_raw_data(list_files)
df = handler.convert_input_dataframe(df)
handler.predict_data(df)
