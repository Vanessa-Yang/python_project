import datetime
import itertools
import math
import os

from PIL import Image as PILImage
from PIL import ImageFont, ImageDraw, ImageEnhance
from wand.image import Image


# 图像压缩
def compress_image_util(image_path, resize_pix=700, resolution=300, quality=70, out_path='./data/images/'):
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
    set_font_shadow(draw_table, text_coordinate, text, font_file, ratio)
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
    shadow_color = (0, 0, 0, 77)
    layer1 = max(math.ceil(ratio * 3), 1)
    print("raio:", ratio, "layer1:", layer1)
    for i, j in itertools.product((-1 * layer1, 0, layer1), (-1 * layer1, 0, layer1)):
        draw_table.text((text_coordinate[0] + i, text_coordinate[1] + j), text, font=font_file, fill=shadow_color)


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
        "C:\\Users\\Administrator\\Pictures\\images_for_test\\segment2.png",
        "C:\\Users\\Administrator\\Pictures\\images_for_test\\big_image_20000×20000.png",
        "C:\\Users\\Administrator\\Pictures\\images_for_test\\mini_img.png",
        "C:\\Users\\Administrator\\Pictures\\images_for_test\\rotate.jpeg"
    ]
    for image_path in image_paths:
        name = image_path.split('\\')[-1]
        out_path = "C:\\Users\\Administrator\\Downloads\\textmark_" + name
        add_watermark_util("来源：盘子设计团队", 44, 1, 0, 24, image_path, out_path)
    print("水印添加完成")


if __name__ == '__main__':
    # test_compress_image()
    test_add_watermark()
