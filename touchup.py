import os
import pandas as pd
import random

# Make 3 csvs 
# train + validate + test
def make_tvt_csvs(folder, shuffled, train_pc, validate_pc, test_pc, num_samples):
    x = int(train_pc*num_samples) # num train
    y = int(validate_pc*num_samples) # num validate
    z = int(test_pc*num_samples) # num test
    # train
    train = pd.DataFrame()
    train['filename'] = shuffled.loc[:, 'filename'].iloc[0:x]
    train['label'] = shuffled.loc[:, 'label'].iloc[0:x]
    train_path = os.path.join(folder, 'train.csv')
    train.to_csv(train_path, sep= ' ', header=False, index=False)
    # validate
    validate = pd.DataFrame()
    validate['filename'] = shuffled.loc[:, 'filename'].iloc[x:x+y]
    validate['label'] = shuffled.loc[:, 'label'].iloc[x:x+y]
    validate_path = os.path.join(folder, 'val.csv')
    validate.to_csv(validate_path, sep= ' ', header=False, index=False)
    # test
    test = pd.DataFrame()
    test['filename'] = shuffled.loc[:, 'filename'].iloc[x+y:x+y+z]
    test['label'] = shuffled.loc[:, 'label'].iloc[x+y:x+y+z]
    test_path = os.path.join(folder, 'test.csv')
    test.to_csv(test_path, sep= ' ', header=False, index=False)

    print(f'Generated CSVs \ntrain: {x}, validate: {y}, test: {z}, total: {x+y+z}')
    print(f'{train_path} \n{validate_path} \n{test_path}')


# take in file name of csv file
def final_touchup(video_dir, filename, train_pc, validate_pc, test_pc):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_video_dir = os.path.join(cur_dir, video_dir) # add this to each path

    csv_path = os.path.join(video_dir, filename) # all data
    data = pd.read_csv(csv_path)

    # New df to shuffle all samples
    shuffled = pd.DataFrame()
    shuffled['filename'] = data.loc[:, 'filename'].apply(lambda x: os.path.join(full_video_dir, x))
    shuffled['label'] = data.loc[:, 'label']
    shuffled = shuffled.sample(frac=1, random_state=random.randint(0, 10e8)) # randomly shuffle data

    num_samples = shuffled.shape[0]
    make_tvt_csvs('dataset', shuffled, train_pc, validate_pc, test_pc, num_samples)

    print('done BOZO') # FINISHED


###################### RUN on brown computer
# Make train/val/test csv files
train_pc = 0.70
validate_pc = 0.15
test_pc = 0.15
filename = 'uniform_timestamps.csv'
video_dir = os.path.join('dataset', 'uniform_dataset8')
final_touchup(video_dir, filename, train_pc, validate_pc, test_pc)


