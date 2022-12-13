import pandas as pd
import os


'''
Total vids: 2851, Total runtime (hours): 2.32
Num zero: 1987, % zero: 69.69, runtime zero: 1.62
Num one: 864, % one: 30.31, runtime one: 0.7
'''
def naive_prediction(uniform_csv):
    num_frames = 88 # per video
    fps = 30

    df = pd.read_csv(uniform_csv)
    counts = df.loc[:, 'label'].value_counts()

    n0 = counts.loc[0]
    n1 = counts.loc[1]
    total = n0 + n1
    pc0 = 100*round(n0/total, 4)
    pc1 = 100*round(n1/total, 4)
    print(f'Total vids: {total}, Total runtime (hours): {round(num_frames*total/(fps*60*60), 2)}')
    print(f'Num zero: {n0}, % zero: {pc0}, runtime zero: {round(num_frames*n0/(fps*60*60), 2)}')
    print(f'Num one: {n1}, % one: {pc1}, runtime one: {round(num_frames*n1/(fps*60*60), 2)}')


folder = os.path.join('dataset', 'uniform_dataset8')
filename = 'uniform_timestamps.csv'
uniform_csv = os.path.join(folder, filename)

naive_prediction(uniform_csv)