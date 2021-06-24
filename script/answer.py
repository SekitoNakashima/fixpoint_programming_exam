import pandas as pd
import numpy as np

class Answer:
    # 初期処理
    def __init__(self):
        self.folder_name = "security_log" # フォルダー名
        self.file_name = "log_1.txt" # ログのファイル名
        self.df_log = self.get_log() # ログを取得
        
    
    # ログの取得
    def get_log(self):
        return pd.read_table("../{0}/{1}".format(self.folder_name, self.file_name),
                            names=["date", "address", "response_time"],
                            sep=",")

    # 故障しているサーバのアドレスを取得
    def get_error_server_address(self):
        """ 重複の対処 """
        return self.df_log[self.df_log["response_time"] == "-"]["address"].unique()

    # 故障しているサーバのアドレスと期間を出力
    def output_error_data(self, address_list):
        # サーバごとにデータフレームをまとめる
        for address in address_list:
            # アドレス出力
            print("error_server_address: ", address)

            df_error_server = self.df_log[self.df_log["address"] == address].reset_index()
            # 故障したタイミングの行番号
            error_index_arr = df_error_server[df_error_server["response_time"] == "-"].index.values

            # 復旧したタイミングの行番号
            restore_index_arr = error_index_arr + 1

            # 重複要素を取得
            duplicate_index_list = np.intersect1d(error_index_arr, restore_index_arr)

            # 重複した番号を削除
            new_error_index_arr = np.setdiff1d(error_index_arr, duplicate_index_list)
            new_restore_index_arr = np.setdiff1d(restore_index_arr, duplicate_index_list)

            # 故障期間を出力
            self.output_error_time(new_error_index_arr, new_restore_index_arr, df_error_server)
        return 0
    
    # 故障期間を取得 (復旧時刻はないデータは考慮しない)
    def output_error_time(self, error_arr, restore_arr, df):
        for error_index, restore_index in zip(error_arr, restore_arr):
            print("error_time: ", df.at[df.index[error_index], "date"], " - ",
                df.at[df.index[restore_index], "date"], "\n")


test = Answer()
address = test.get_error_server_address()
test.output_error_data(address)

# import numpy as np
# length = 8
# a = np.array([1, 4, 5, 7])
# b = np.array([2, 5, 6, 7])
# print(np.intersect1d(a, b))

# print(np.setdiff1d(b, a))
# log = get_log()