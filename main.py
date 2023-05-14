#!/usr/bin/env python
# coding: utf-8

# ラベル付き(csvファイル)画像データセット（１つのフォルダにまとめている）をTrain-ValとTestに分割する.
# これにおいては、画像ファイル群をランダムに分割する。方法をここでは取る。
# なお、ここでのラベルは、連続値を前提としているが、離散値（よくあるクラス分類）でも問題ないだろう。
# 単に分けるだけでなく、あらためてディレクトリにリストファイル（ラベル、属性値のcsvファイル）も作成する。

# 処理にはPandasを使います。

# # データセットの準備
# csvファイルと画像フォルダは同じ階層に置く。
# csvファイルのフォーマットは以下の通り。
# Filename	Valence	Arousal
# Animals_001_h.jpg	2.57	6.44
# Animals_002_v.jpg	6.24	6.68
# Animals_003_h.jpg	5.24	5.52
# Animals_004_v.jpg	4.50	7.02
# Animals_005_h.jpg	5.31	5.82
# Animals_006_v.jpg	5.13	6.23
# Animals_007_h.jpg	4.76	7.06
# Animals_008_v.jpg	2.63	6.80
# 
# Filenameは画像ファイル名、ValenceとArousalはラベル値（連続値）。
# 画像フォルダには、Filenameと同じ名前の画像ファイルがあること。が望ましい。
# ここでは、K-fold交差検証のために、Train-ValとTestに分割する前提。もちろん、応用すれば、Train,Val,Testに分割することも可能。

# In[25]:


import os
import csv
import shutil
import random
import pandas as pd


#specify root directory
root_dir= '/mnt/c/Users/survey/Desktop/NAPS'
#Specify the directory containing the original images
image_original_dir= '/mnt/c/Users/survey/Desktop/NAPS/naps_l'


# os.listdir()を使って、ディレクトリ内の全てのファイル名を取得
files_in_directory = os.listdir(image_original_dir)
# 結果を表示
for file in files_in_directory:
    print(file)

# specify the save directory
Train_Val_dir= '/mnt/c/Users/survey/Desktop/NAPS/Train_Val'
Test_dir= '/mnt/c/Users/survey/Desktop/NAPS/Test'


# もとのデータ・セットのファイル名をシャッフル
random.shuffle(files_in_directory)


#割合を指定
Train_Val_P=0.9
Test_P=0.1

#いったんファイル名だけ分割
num_train = int(Train_Val_P * len(files_in_directory))
train_files = files_in_directory[:num_train]
val_files = files_in_directory[num_train:]

# ファイルを新しいディレクトリにコピー
for file in train_files:
    shutil.copy(os.path.join(image_original_dir, file), Train_Val_dir)

for file in val_files:
    shutil.copy(os.path.join(image_original_dir, file), Test_dir)


# # それぞれのディレクトリにあるファイル名を取得し、そのファイル名に紐づくラベルを取得し、csvファイルを作成する。

# もとのCSVファイル
label_file= '/mnt/c/Users/survey/Desktop/NAPS/NAPS.csv'

# CSVファイルを開く
with open(label_file, 'r') as csvfile:
    # CSVリーダーを作成
    reader = csv.reader(csvfile)

    # CSVファイルの内容を1行ずつ読み込み、表示
    for row in reader:
        print(row)


current_working_directory = os.getcwd()
print(current_working_directory)


list_of_files = os.listdir()
print(list_of_files)


# フォルダAとフォルダBのファイル名を取得
file_names_A = os.listdir(Train_Val_dir)
file_names_B = os.listdir(Test_dir)
# 元のCSVファイルを読み込む
df = pd.read_csv(label_file)  # 必要に応じてパスを修正

#ファイル名をたよりに、ラベルを取得
# フォルダAとフォルダBのファイル名に対応する行だけを抽出
df_A = df[df['Filename'].isin(file_names_A)]
df_B = df[df['Filename'].isin(file_names_B)]

print(df_A)
print(df_B)

result_A_path = os.path.join(root_dir, "Train_Val.csv")
result_B_path = os.path.join(root_dir, "Test.csv")
print(result_A_path)
print(result_B_path)
#保存する
df_A.to_csv(result_A_path, index=False)
df_B.to_csv(result_B_path, index=False)

