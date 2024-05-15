import datetime
import math
import os
import time

import cv2
import numpy as np
from PIL import Image as PILImage, ImageFilter
from PIL import ImageFont, ImageDraw, ImageEnhance
from wand.image import Image

BLURRY = "Blurry"
NOT_BLURRY = "Not Blurry"


# 彩色图像转灰度图像
def color_to_grayscale():
    start_time = time.time()
    input_image = 'C:/Users/Administrator/Pictures/images_for_test/oyad_logo.png'
    # 大图压缩
    zip_image = compress_image_util(input_image, 300)
    # 读取彩色图片
    img_color = PILImage.open(zip_image)
    # 如果图片的模式不是RGBA，则转换为RGBA模式
    if img_color.mode != 'RGBA':
        img_color = img_color.convert('RGBA')
    # 创建一个白色背景图像
    white_bg = PILImage.new('RGBA', img_color.size, (255, 255, 255))
    # 将原始图片粘贴到白色背景上
    white_bg.paste(img_color, (0, 0), img_color)
    # 转换为灰度图像
    img_gray = white_bg.convert('L')
    # 保存原始灰度图片
    img_gray.save("../images/original_gray.png")

    # 加透明度参数并保存不同透明度的图片
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        transparent_img = img_gray.copy()
        transparent_img.putalpha(int(alpha * 255))
        transparent_img.save(f"../images/gray_with_alpha_{alpha}.png")
    end_time = time.time()
    print("耗时：", end_time - start_time)


# 图像压缩
def compress_image_util(image_path, resize_pix=700, resolution=300, quality=70, out_path='../images/'):
    img = Image(filename=image_path)
    time_stamp = str(int(datetime.datetime.now().timestamp() * 100000))
    img.resolution = resolution if min(img.resolution) > resolution else img.resolution
    name = image_path.split("/")[-1]
    img.compression_quality = quality if img.compression_quality > quality else img.compression_quality
    w, h = img.size
    if w < resize_pix or h < resize_pix:
        new_w, new_h = img.size
        new_file_path = out_path + f"{time_stamp}_{new_w}_{new_h}_{name}"
        img.save(filename=new_file_path)
        img.close()
        return new_file_path
    if w > h:
        img.transform(resize="x" + str(resize_pix))
    else:
        img.transform(resize=str(resize_pix))
    new_w, new_h = img.size
    new_file_path = out_path + f"{time_stamp}_{new_w}x{new_h}_{name}"
    img.save(filename=new_file_path)
    img.close()
    return new_file_path


def creat_dir_not_exist(path):
    if (not os.path.exists(path)):
        os.mkdir(path)


def test_compress_image():
    input_path = 'E:/高清素材/'
    input_folders = os.listdir(input_path)

    resize_pix = 2000
    resolution = 200
    quality = 90

    output_path = 'E:/高清素材_压缩图/' + f'_{resize_pix}px_{resolution}dpi_{quality}qua/'
    creat_dir_not_exist(output_path)

    for folder_level_1 in input_folders:
        print('\n')
        for file_name in os.listdir(input_path + folder_level_1 + "/"):
            file_path = input_path + folder_level_1 + '/' + file_name
            print("-> file_path: ", file_path)

            out_full_folder = output_path + folder_level_1 + '/'
            creat_dir_not_exist(out_full_folder)

            out_full_path = compress_image_util(file_path, resize_pix, resolution, quality, out_full_folder)
            print("-> out_file_path: ", out_full_path, '\n')


# 加文字水印
def add_watermark_util(text, font_size, opacity, rotate, space, image_path, out_path):
    img = Image(filename=image_path)
    img.resolution = 300 if min(img.resolution) > 300 else img.resolution
    # img.format = 'PNG'
    # img.alpha_channel = True
    img_width, img_height = img.size
    ratio = img_width / 1920
    space = space * ratio

    watermark_path = generate_water_mark_image(text, font_size, ratio, opacity, rotate)
    try:
        watermark = Image(filename=watermark_path)
        w_width, w_height = watermark.size
        left = math.ceil(img_width - w_width - space)
        top = math.ceil(img_height - w_height - space)
        img.composite(watermark, left=left, top=top, operator='over')
        img.save(filename=out_path)
        img.close()
        watermark.close()
    finally:
        os.remove(watermark_path)


def generate_water_mark_image(text, font_size, ratio, opacity, rotate):
    text = "不觉艺术空间" if not text else text
    font_size = ratio * (44 if not font_size else font_size)
    opacity = 1 if not opacity else opacity
    rotate = 0 if not rotate else rotate
    text_w = math.ceil(len(text) * font_size + 10)
    text_h = math.ceil(font_size * 2)
    blur_radius = 10 * ratio
    print(blur_radius)

    # 创建空白画布
    water_markimage = PILImage.new('RGBA', (text_w, text_h))
    draw_table = ImageDraw.Draw(water_markimage)
    font_file = ImageFont.truetype("../font/SourceHanSansSC-Regular.otf", font_size)
    text_coordinate = (0, 0)
    # 测定文本框边界
    w_left, w_top, w_right, w_bottom = draw_table.textbbox(text_coordinate, text=text, font=font_file)
    print(w_left, w_top, w_right, w_bottom)
    # 设置文本居于右下角
    text_coordinate = (text_w - w_right, text_h - w_bottom)

    # 文字阴影`
    # set_font_shadow(draw_table, text_coordinate, text, font_file, ratio)
    water_markimage.filter(ImageFilter.GaussianBlur)
    draw_table.text(text_coordinate, text=text, fill=(255, 255, 255, 255), font=font_file)

    # 设置水印图片透明度
    set_opacity(water_markimage, opacity)
    if rotate:
        # 水印图片角度翻转
        water_markimage = water_markimage.rotate(rotate)
    # 保存图片
    timestamp = str(int(datetime.datetime.now().timestamp() * 100000))
    save_path = "../images/watermark-" + text + timestamp + ".png"
    water_markimage.save(save_path)
    water_markimage.close()
    return save_path


def set_font_shadow(draw_table, text_coordinate, text, font_file, ratio):
    gap = max(ratio * 2.5, 0.1)
    print("ratio:", ratio, "gap:", gap)
    draw_table.text((text_coordinate[0] + gap, text_coordinate[1] + gap), text, font=font_file,
                    fill=(128, 128, 128, 255))


def set_opacity(im, opacity):
    """
    设置水印透明度
    """
    assert 0 <= opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return


def test_add_watermark():
    image_paths = [
        # "C:\\Users\\Administrator\\Pictures\\images_for_test\\segment2.png",
        # "C:\\Users\\Administrator\\Pictures\\images_for_test\\big_image_20000×20000.png",
        "C:\\Users\\Administrator\\Pictures\\images_for_test\\mini_img.png",
        # "C:\\Users\\Administrator\\Pictures\\images_for_test\\rotate.jpeg",
        # "C:\\Users\\Administrator\\Downloads\\mini_pic.png"
    ]
    for image_path in image_paths:
        name = image_path.split('\\')[-1]
        out_path = "C:\\Users\\Administrator\\Downloads\\textmark2_" + name
        add_watermark_util("来源：盘子设计团队", 44, 1, 0, 24, image_path, out_path)
    print("水印添加完成")


# 判断是否为模糊图像
def blurry_detect(image_path, threshold=1500, shape=(1080, 1920)):
    if threshold < 1:
        threshold = 1500
    # 灰度化
    img = cv2.imread(image_path)
    h,w = img.shape[0], img.shape[1]
    resize_ratio = min(shape[1] / w, shape[0] / h)

    img = cv2.resize(img,  (int(w * resize_ratio), int(h * resize_ratio)))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray_img.shape)

    # 计算灰度图的边缘方差
    fm = laplacian_var(gray_img)
    text = 'Not Blurry'

    # 设置输出文字
    if fm < threshold:
        text = "Blurry"
    else:
        # 局部模糊检测
        is_burry = local_blur_detect(fm, gray_img, img, threshold)
        if is_burry:
            text = "Local Blurry"

    # 显示结果
    cv2.putText(img, "{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyWindow('Image')


# 局部模糊检测
def local_blur_detect(fm, gray_img, img, threshold):
    # 分四个区域再次检测，模糊区域两个及以上则视为模糊
    blur_count = 0
    sep_count = 2 if fm < 1000 else 3
    h, w = gray_img.shape
    mid_x, mid_y = int(w // 2), int(h // 2)
    error_x, error_y = w % 2, h % 2
    _img = img.copy()
    img1 = _img[0:(mid_y + error_y), 0:(mid_x + error_x)]
    img2 = _img[0:(mid_y + error_y), mid_x: w]
    img3 = _img[mid_y: h, 0:(mid_x + error_x)]
    img4 = _img[mid_y: h, mid_x:w]
    fm1 = laplacian_var(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
    fm2 = laplacian_var(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY))
    fm3 = laplacian_var(cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY))
    fm4 = laplacian_var(cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY))
    blur_count += 1 if fm1 < threshold else 0
    blur_count += 1 if fm2 < threshold else 0
    blur_count += 1 if fm3 < threshold else 0
    blur_count += 1 if fm4 < threshold else 0
    local_text1 = BLURRY if fm1 < threshold else NOT_BLURRY
    local_text2 = BLURRY if fm2 < threshold else NOT_BLURRY
    local_text3 = BLURRY if fm3 < threshold else NOT_BLURRY
    local_text4 = BLURRY if fm4 < threshold else NOT_BLURRY
    # 展示多个
    cv2.putText(img1, "{}: {:.2f}".format(local_text1, fm1), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                2)
    cv2.putText(img2, "{}: {:.2f}".format(local_text2, fm2), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                2)
    cv2.putText(img3, "{}: {:.2f}".format(local_text3, fm3), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                2)
    cv2.putText(img4, "{}: {:.2f}".format(local_text4, fm4), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                2)
    # 图集
    imgs = np.hstack((img1, img2, img3, img4))
    cv2.imshow('local_images_of_4', imgs)
    cv2.waitKey(0)
    cv2.destroyWindow('local_images_of_4')

    return blur_count >= sep_count


# 拉普拉斯变换，求取方差 —— 边缘检测值，值越大，认为图片越清晰；反之，越模糊
def laplacian_var(gray_img):
    # 拉普拉斯变换
    gray_lap = cv2.Laplacian(gray_img, cv2.CV_64F)
    dst = cv2.convertScaleAbs(gray_lap)
    # 求取方差
    fm = dst.var()
    return fm


if __name__ == '__main__':
    # test_compress_image()
    # test_add_watermark()
    # color_to_grayscale()

    # 遍历目录下每一张图片
    folder_path = 'C:\\Users\\Administrator\\Pictures\\opencv'
    for image_name in os.listdir(folder_path):
        _image_path = os.path.join(folder_path, image_name)
        print(_image_path)
        blurry_detect(_image_path, 100, (1080, 1920))
