from pathlib import Path
import cv2
from PIL import Image

folder_dir = ''
images = Path(folder_dir).glob('*.jpg')





# cv2.imshow("Top Left Corner", topLeft)
# cv2.imshow("Top Right Corner", topRight)
# cv2.imshow("Bottom Right Corner", bottomLeft)
# cv2.imshow("Bottom Left Corner", bottomRight)
# cv2.waitKey(0)

i = 0 
for image in images:
    path = str(image).split('\\')[0]
    print(path)
    im = cv2.imread(path)

    (h, w) = im.shape[:2]
 
    # compute the center coordinate of the image
    (cX, cY) = (w // 2, h // 2)

    # crop the image into four parts which will be labelled as
    # top left, top right, bottom left, and bottom right.
    topLeft = im[0:cY, 0:cX]
    p1 = path + "_1.png"
    cv2.imwrite(p1, topLeft)
    topRight = im[0:cY, cX:w]
    p2 = path + "_2.png"
    cv2.imwrite(p2, topRight)
    bottomLeft = im[cY:h, 0:cX]
    p3 = path + "_3.png"
    cv2.imwrite(p3, bottomLeft)
    bottomRight = im[cY:h, cX:w]
    p4 = path + "_4.png"
    cv2.imwrite(p4, bottomRight)
    
    #img = cv2.imread(path)
    #for r in range(0,img.shape[0],2):
    #    for c in range(0,img.shape[1],2):
    #        cv2.imwrite(f"img{r}_{c}.png",img[r:r+2, c:c+2,:])

