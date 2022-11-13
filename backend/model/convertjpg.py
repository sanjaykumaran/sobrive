from pathlib import Path
from PIL import Image

folder_dir = 'drunkImages'
images = Path(folder_dir).glob('*.webp')
i = 0 
for image in images:
    print(image)
    #im = Image.open(image).convert("RGB")
    #title = "pic" + str(i) + ".jpg"
    #im.save(title, "jpeg")
    #i = i + 1