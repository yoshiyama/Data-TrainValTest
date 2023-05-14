# python dataset_split.py --root_dir /mnt/c/Users/survey/Desktop/NAPS --image_original_dir_name naps_l --label_file_name NAPS.csv --key_index Filename --Train_Val_P 0.9 --Test_P 0.1


import os
import csv
import shutil
import random
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Dataset Split')
    parser.add_argument('--root_dir', type=str, help='Root directory')
    parser.add_argument('--image_original_dir_name', type=str, help='Directory containing the original images')
    parser.add_argument('--label_file_name', type=str, help='CSV file containing the labels')
    parser.add_argument('--key_index', type=str, help='Column name for file names in the CSV')
    parser.add_argument('--Train_Val_P', type=float, help='Percentage for Train-Val split')
    parser.add_argument('--Test_P', type=float, help='Percentage for Test split')
    args = parser.parse_args()

    root_dir = args.root_dir
    image_original_dir_name = args.image_original_dir_name
    label_file_name = args.label_file_name
    key_index = args.key_index
    Train_Val_P = args.Train_Val_P
    Test_P = args.Test_P

    image_original_dir = os.path.join(root_dir, image_original_dir_name)
    label_file = os.path.join(root_dir, label_file_name)
    Train_Val_dir = os.path.join(root_dir, 'Train_Val')
    Test_dir = os.path.join(root_dir, 'Test')
    Train_Val_csv = 'Train_Val.csv'
    Test_csv = 'Test.csv'

    # Create Train_Val and Test directories
    os.makedirs(Train_Val_dir, exist_ok=True)
    os.makedirs(Test_dir, exist_ok=True)

    # Get file names in the original image directory
    files_in_directory = os.listdir(image_original_dir)
    random.shuffle(files_in_directory)

    num_train = int(Train_Val_P * len(files_in_directory))
    train_files = files_in_directory[:num_train]
    val_files = files_in_directory[num_train:]

    # Copy files to Train_Val and Test directories
    for file in train_files:
        shutil.copy(os.path.join(image_original_dir, file), Train_Val_dir)

    for file in val_files:
        shutil.copy(os.path.join(image_original_dir, file), Test_dir)

    # Read the label CSV file
    df = pd.read_csv(label_file)

    # Filter the rows based on file names in Train_Val and Test directories
    train_val_files = os.listdir(Train_Val_dir)
    test_files = os.listdir(Test_dir)
    df_Train_Val = df[df[key_index].isin(train_val_files)]
    df_Test = df[df[key_index].isin(test_files)]

    # Save Train_Val and Test CSV files
    result_Train_Val_path = os.path.join(root_dir, Train_Val_csv)
    result_Test_path = os.path.join(root_dir, Test_csv)
    df_Train_Val.to_csv(result_Train_Val_path, index=False)
    df_Test.to_csv(result_Test_path, index=False)

if __name__ == '__main__':
    main()