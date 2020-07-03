import fuzzymatcher as fm
import pandas as pd


class Matcher:
    def __init__(self, df1_path, df2_path, arr1, arr2):
        self.df1 = pd.read_csv(df1_path)
        self.df2 = pd.read_csv(df2_path)
        self.arr1 = arr1
        self.arr2 = arr2

    def dataset(self):
        return fm.link_table(self.df1, self.df2, self.arr1,
                             self.arr2, left_id_col='id', right_id_col='id')

    def dataset_filter(self):
        result = self.dataset()
        return result[result.match_score > 0]

    def dataset_index(self, table_side):
        result = self.dataset_filter()
        return result[f'__id_{table_side}'].to_list()

    def read_filtered_dataset(self):
        return self.df1.iloc[self.dataset_index('left')]

    def export_to_csv(self, match_func, file_name):
        result = match_func
        compression = dict(method='zip', archive_name=f'{file_name}.csv')
        return result.to_csv(f'{file_name}.zip', index=False, compression=compression)
