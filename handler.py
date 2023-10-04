import pathlib

import tensorflow as tf
from pathlib import Path, PosixPath
import pandas as pd
import json
import numpy as np


class Handler:

    def __init__(self, model_directory: PosixPath, statuses_list_file: PosixPath, z_score_file: PosixPath,
                 model_columns_file: PosixPath, column_names_file: PosixPath):
        self.model = tf.keras.models.load_model(model_directory)
        self.statuses = self._parse_json_file(statuses_list_file)
        self.z_scores = self._parse_json_file(z_score_file)
        self.model_columns = self._parse_json_file(model_columns_file)

        self.columns = []
        self.numeric_col = []
        self.symbolic_col = []
        self._load_column_names(column_names_file)

    @staticmethod
    def _parse_json_file(json_file: PosixPath):
        with open(json_file, 'r') as file:
            return json.loads(file.read())

    def _load_column_names(self, column_names_file: PosixPath):
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

    def _load_raw_data(self, list_file: PosixPath):
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

    def _encode_numeric_zscore(self, df, name):
        mean = self.z_scores[name]['mean']
        sd = self.z_scores[name]['sd']
        # Z-оценка
        df[name] = (df[name] - mean) / sd

    @staticmethod
    def _encode_text_dummy(df, name):
        # Получаем фиктивные переменные
        dummies = pd.get_dummies(df[name])
        # Для каждой фиктивной переменной создаем новый столбец
        for x in dummies.columns:
            dummy_name = f"{name}-{x}"
            df[dummy_name] = dummies[x]
        # Удаляем оригинальный столбец
        df.drop(name, axis=1, inplace=True)

    def _convert_input_dataframe(self, df):
        for column in self.model_columns:
            df[column] = False

        for column_name in self.symbolic_col:
            self._encode_text_dummy(df, column_name)

        for column_name in self.numeric_col:
            self._encode_numeric_zscore(df, column_name)

        df = df.fillna(0.0)
        difference = set(df.columns).difference(self.model_columns)
        df = df.drop(difference, axis=1)

        return df

    def _predict_data(self, df):
        x = df.values
        x = np.asarray(x).astype(np.float32)

        return self.model.predict(x)

    def _represent_data(self, data):
        output = []
        for row in data:
            for index, num in enumerate(row):
                if num == np.float32(1):
                    output.append(self.statuses[index])
                    break
        return output

    def handle_data(self, file_path):
        data = self._load_raw_data(file_path)
        converted_data = self._convert_input_dataframe(data)
        predict = self._predict_data(converted_data)
        return self._represent_data(predict)



if __name__ == '__main__':
    model_directory1 = pathlib.Path.cwd().joinpath('model-001')
    statuses_file = pathlib.Path.cwd().joinpath('columns/statuses.json')
    z_score_file = pathlib.Path.cwd().joinpath('columns/z_scrores.json')
    model_columns_file = pathlib.Path.cwd().joinpath('columns/column_names.json')
    column_names_file = pathlib.Path.cwd().joinpath('columns/kddcup.names')
    list_files = pathlib.Path.cwd().joinpath('trafAld.list')

    handler = Handler(model_directory1, statuses_file, z_score_file, model_columns_file, column_names_file)

    print(handler.handle_data(list_files))
