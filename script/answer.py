import pandas as pd

# ログの取得
def Get_log():
    return pd.read_table("../security_log/log_1.txt",
                        names=["date", "IP_address", "responce_result"],
                        sep=",")

# 故障しているサーバのアドレスを取得
def Get_error_server_address(log):
    """ 重複の対処 """
    return log[log["responce_result"] == "-"]["IP_address"].values

# 故障しているサーバのアドレスと期間を出力
def Output_error_time(error_addres):
    # サーバごとにデータフレームをまとめる
    
    # 故障

    # 復帰

    # 
    return 0

log = Get_log()
error_address = Get_error_server_address(log)
print(error_address)