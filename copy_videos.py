import os
import shutil
from tqdm import tqdm
import pandas as pd

# Copies files from source to dest
# run locally to upload to brown computer
# copies videos into directory
def copy_folder(source, dest):
  source_files = os.listdir(source) # list of all files in source
  for file in tqdm(source_files, desc='Copying Files'):
    shutil.copy(os.path.join(source, file), dest)


# Checks number of files in dirs are same
def validate_copy(source, dest):
    num_source = len(os.listdir(source))
    num_dest = len(os.listdir(dest))
    print('Num files source:', num_source)
    print('Num files dest:', num_dest)


# Identify/delete files that are not in source
def purge_randos(source, dest):
    source_files = os.listdir(source)
    dest_files = os.listdir(dest)
    truth = {}
    for file in source_files:
        truth[file] = 1
    
    num_removed = 0
    for file in dest_files:
        if file not in truth:
            os.remove(file)
            print(f'Removed {file}')
            num_removed += 1

    print(f'Removed {num_removed} files')


# Compare csv files with videos in folder
def check_csv_files(source, csv_file):
    df = pd.read_csv(csv_file)
    for file in tqdm(df.loc[:, 'filename']):
        path = os.path.join(source, file)
        if not os.path.exists(path):
            print(f'{path} doesnt exist')


# delete contents of a directory
def delete_dir(dir):
    files = os.listdir(dir)
    counter = 0
    for file in tqdm(files):
        fpath = os.path.join(dir, file)
        os.remove(fpath)
        counter += 1
    print(f'Removed {counter} files from {dir}')


# move single file
def move_file(filename, source, dest):
    source = os.path.join(source, filename)
    dest = os.path.join(dest, filename)
    shutil.copy(source, dest)


# source = '/Users/seanyamamoto/workspace2/trans/data/dataset/uniform_dataset8/'
# dest = '/Users/seanyamamoto/browncs/course/robust_fp/data/dataset/uniform_dataset8'
# csv_file = os.path.join(dest, 'uniform_timestamps.csv')

filename = 'checkpoint_epoch_00015.pyth'
source = '/Users/seanyamamoto/browncs/checkpoints'
dest = '/Users/seanyamamoto/browncs/course/robust_fp/TimeSformer/checkpoints'

move_file(filename, source, dest)

# - conda activate /Users/seanyamamoto/opt/anaconda3/envs/timesformer

# copy_folder(source, dest)
# validate_copy(source, dest)
# purge_randos(source, dest)
# check_csv_files(source, csv_file)

# shit = '/Users/seanyamamoto/browncs/course/robust_fp/data/dataset/uniform_trash_deletethis'
# delete_dir(shit)/

print('FINISHED SUCCESFULLY')