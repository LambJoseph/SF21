import os
import glob


count = 0
my_dir = glob.glob("../sf21/testset/frames/*.png")
file_count = len(my_dir)

for file in my_dir:
    os.remove(file)
