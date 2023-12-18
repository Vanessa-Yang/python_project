import os
import datetime

from wand.image import Image


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
    if(not os.path.exists(path)):
        os.mkdir(path)

if __name__ == '__main__':
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
