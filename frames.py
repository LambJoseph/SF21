from timeit import default_timer as timer
import cv2
import pandas as pd
import numpy as np
import click

score = np.load("../sf21/testset/numpy/anomaly_scores.npy").tolist()
round_score = [round(value, 3) for value in score]
start = timer()



source = "../testset/source/testset_3.mp4"
cap = cv2.VideoCapture('source/%s' % source)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


copy = frame_count


data = { 'frame': [], 'score': round_score, 'path': []}
count = 0

with click.progressbar(length=frame_count, show_pos=True, fill_char="//", label="Extracting frames", show_percent=True) as bar:
    for i in bar:
        ret, frame = cap.read()
        if ret:
            path = "../sf21/testset/frames/"
            name = f"frame{count}.png"
            data['frame'].append(f"frame{count}")
            data['path'].append(path + name)
            cv2.imwrite(path + name, frame)
        else:
            cap.release()
            break
        count += 1

df = pd.DataFrame(data, columns = ['frame', 'score', 'path'], dtype=float)
print(df)
df.to_csv('data.csv')


end = timer()
print(f"FRAMES: {count}")
print(f"ELAPSED TIME: {int(end - start)} seconds")

f = open("log.txt", "a")
f.write(f"FRAMES: {count}\n")
f.write(f"ELAPSED TIME: {int(end - start)}\n")
f.close()


