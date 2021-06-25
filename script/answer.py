import pandas as pd
import numpy as np

class LogAnalysis:
    # 初期処理
    def __init__(self, N, m, t):
        # フォルダ・ファイル名
        self.folder_name = "security_log"
        self.file_name = "log_1.txt"
        # パラメータ
        self.N = N
        self.m = m
        self.t = t
        # ログを取得
        self.df_log = self.get_log()
    
    # ログの取得
    def get_log(self):
        return pd.read_table("../{0}/{1}".format(self.folder_name, self.file_name),
                            names=["date", "address", "response_time"],
                            sep=",")

    # 全サーバのアドレスを取得
    def get_all_address(self):
        return self.df_log["address"].unique()

    # タイムアウトしたサーバのアドレスを取得
    def get_timeout_server_address(self):
        return self.df_log[self.df_log["response_time"] == "-"]["address"].unique()

    # 故障しているサーバのアドレスと期間を出力
    def output_error_data(self):

        # タイムアウトしたサーバのアドレス取得
        address_list = self.get_timeout_server_address()

        # サーバごとにデータフレームをまとめる
        for address in address_list:
            # アドレス出力
            print("error_server_address: ", address)

            # タイムアウトが発生したサーバのデータフレームを取得
            df_error_server = self.df_log[self.df_log["address"] == address].reset_index()
            # errorしたタイミングの行番号
            error_index_arr = df_error_server[df_error_server["response_time"] == "-"].index.values

            # 故障の判定 (故障の場合、故障時間の出力を無視)
            if self.is_failure(error_index_arr):
                print("fail")
                continue            

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
    

    
    # error期間を出力 (復旧時刻はないデータは考慮しない)
    def output_error_time(self, error_arr, restore_arr, df):
        for error_index, restore_index in zip(error_arr, restore_arr):
            print("error_time: ", df.at[df.index[error_index], "date"], " - ",
                df.at[df.index[restore_index], "date"], "\n")

    # 故障の判定
    def is_failure(self, error_index_arr):
        # タイムアウトの回数が上限値以下の場合
        if len(error_index_arr) <= self.N:
            return False
        
        # タイムアウトの連続値をカウントし故障かどうか判別
        if self.count_timeout(error_index_arr) > self.N:
            return True

    # タイムアウトの連続値をカウント
    def count_timeout(self, error_index_arr):
        count = 1
        prev_num = error_index_arr[0]
        for num in error_index_arr[1:]:
            if (prev_num + 1) == num:
                count += 1
            else:
                count = 1
            prev_num = num
        return count
    
    # サーバの過負荷をチェック
    def output_overload(self):
        # 全サーバを走査
        for address in self.get_all_address():
            df_one_server = self.df_log[self.df_log["address"] == address].reset_index()

            # 平均応答時間
            mean_response_time = self.get_mean_response_time(df_one_server)

            # 過負荷の判定
            if self.is_overload(mean_response_time):
                # サーバのアドレスを出力
                print("overload: {}".format(address))
        return None

    # 過負荷の判定
    def is_overload(self, mean_response_time):
        return mean_response_time > self.t

    # 直近m個のデータの平均応答時間を取得
    def get_mean_response_time(self, df):
        return df.iloc[-self.m:].mean()["response_time"]
        

# メイン処理
def main():
    # パラメータ
    N = 3   # 連続タイムアウトの上限
    m = 2   # 直近のデータ数
    t = 2   # 過負荷判定の基準となる応答時間[ミリ秒]

    la = LogAnalysis(N, m, t)
    # 設問1, 2
    la.output_error_data()
    # 設問3
    la.output_overload()

# おまじない(正しくファイルが実行されているかどうか)
if __name__ == "__main__":
    main()