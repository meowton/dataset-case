import fuzzymatcher as fm
import pandas as pd


# Check if input file is a Pandas DataFrame
def isframe(file):
    return type(file) is pd.DataFrame


# Matches correlation between to data sets, scoring the
# results from how similar they are.The df1_path/df2_path
# parameters are for each corresponding data set, and
# arr1/arr2 for the columns to run the matching
class Matcher:
    def __init__(self, df1_path, df2_path, arr1, arr2):
        if isframe(df1_path) is True:
            self.df1 = df1_path
        else:
            self.df1 = pd.read_csv(df1_path)

        if isframe(df2_path) is True:
            self.df2 = df2_path
        else:
            self.df2 = pd.read_csv(df2_path)

        self.arr1 = arr1
        self.arr2 = arr2

    def dataset(self):
        return fm.link_table(self.df1, self.df2, self.arr1,
                             self.arr2, left_id_col='id', right_id_col='id')

    def dataset_filter(self):
        result = self.dataset()
        return result[result.match_score > 0]

    def dataset_index(self, arg, table_side):
        result = self.dataset_filter()
        return result[f'{arg}_{table_side}'].to_list()

    def export_to_csv(self, match_func, file_name):
        result = match_func
        compression = dict(method='zip',
                           archive_name=f'{file_name}.csv')
        return result.to_csv(f'{file_name}.zip',
                             index=False,
                             compression=compression)
