# 图像分割方法
import cv2

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

image_path = 'C:\\Users\\Administrator\\Pictures\\images_for_test\\segment2.png'

# 获取图片
def getimg():
    return Image.open(image_path)


def showimg(img, isgray=False):
    plt.axis("off")
    if isgray == True:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)
    plt.show()


im5 = getimg()
im5 = np.array(im5.convert('L'))
im5 = np.where(im5[..., :] < 165, 0, 255)  # 根据设置的阈值来进行黑白分类
image = Image.fromarray(im5)
# showimg(image, True)
image.close()
image.save("../images/segment2.png")
