import shutil
import os

for file in os.listdir("."):
    if file.endswith("_1.png"):
        filename = file
        src = os.path.join(".", filename)
        dest = os.path.join("sober", filename)
        shutil.move(src, dest)
    elif file.endswith("_2.png"):
        filename = file
        src = os.path.join(".", filename)
        dest = os.path.join("drunk1", filename)
        shutil.move(src, dest)
    elif file.endswith("_3.png"):
        filename = file
        src = os.path.join(".", filename)
        dest = os.path.join("drunk2", filename)
        shutil.move(src, dest)
    elif file.endswith("_4.png"):
        filename = file
        src = os.path.join(".", filename)
        dest = os.path.join("drunk3", filename)
        shutil.move(src, dest)
