import os
import time
import cv2


# 微信二维码引擎 + opencv 实现 “二维码解析”
def decode_qrcode(filename=""):
    img = cv2.imread(filename)
    # cv2.imshow('original image', img)
    # cv2.waitKey(0)

    # use after execute 'pip install opencv-contrib-python'
    WechatQRmodel = cv2.wechat_qrcode_WeChatQRCode('./imports/opencv_3rdparty/detect.prototxt',
                                                   './imports/opencv_3rdparty/detect.caffemodel',
                                                   './imports/opencv_3rdparty/sr.prototxt',
                                                   './imports/opencv_3rdparty/sr.caffemodel')
    start = time.time()
    # 解码
    codeinfo, pts = WechatQRmodel.detectAndDecode(img)
    if not pts:
        # 灰度化
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        codeinfo, pts = WechatQRmodel.detectAndDecode(img)
    if not pts:
        # 反色
        img = cv2.bitwise_not(img)
        codeinfo, pts = WechatQRmodel.detectAndDecode(img)

    end = time.time()
    print(filename, codeinfo[0], "time cost(ms):", (end - start) * 1000)
    # cv2.drawContours(img, [np.int32(pts)], -1, (0, 0, 255), 2)
    # cv2.imshow('QR' + filename, img)
    # cv2.waitKey(0)


if __name__ == '__main__':
    path = "./logo"
    dir_list = os.listdir(path)
    print(dir_list)

    for filename in dir_list:
        try:
            # Name of the QR Code Image file
            filename = path + '/' + filename
            # filename = "logo/xiaohongshu.JPG"
            decode_qrcode(filename)
        except Exception as e:
            print("error", e)
