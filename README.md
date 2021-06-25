# fixpoint_rogramming_exam

## 環境

- Python 3.8.3

### 動作確認

||PC 1|
|---|---|
|OS|Windows 10 Home|
|CPU|Intel Core i5-7200 2.50GHz|
|メモリ|8.00GB DDR4|

## 使用手順

### 実行ファイルから使用

- 

## 関数

## 大まかな処理の流れ

1. シミュレータ起動
2. SimulationManagerが時間を一時停止
3. SettingManagerがユーザの入力を待機
4. ユーザからの入力に合わせてSettingManagerがシミュレータに設定を反映
5. ユーザからシミュレーション開始命令を受け取ると、SimulationManagerがシミュレーションを開始
6. HistoryManagerはシミュレーション中に指定した時間間隔でログを記録
7. SimulationManagerはシミュレーション中にドローンの状態を監視
8. 全てのドローンが飛行を終了するとSimulationManagerがシミュレーションを終了

## ディレクトリ構造

### script

- 要求に対する解答のプログラム

### security_log

- ログデータ
