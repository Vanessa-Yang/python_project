import datetime
import json
import os
import time
import urllib.parse

import requests
from wand.image import Image

from util import utils
from util.utils import obs_client


# 图像压缩
def compress_image_util(image_path, resize_pix=700, resolution=300, quality=70, out_path='../images/'):
    img = Image(filename=image_path)
    time_stamp = str(int(datetime.datetime.now().timestamp() * 100000))
    img.resolution = resolution if min(img.resolution) > resolution else img.resolution
    name = image_path.split("/")[-1]
    img.compression_quality = quality if img.compression_quality > quality else img.compression_quality
    w, h = img.size
    if w <= resize_pix or h <= resize_pix:
        if img.length_of_bytes <= 3 * 1024 * 1024:
            # 小于3M不压缩
            img.close()
            return ""
        new_w, new_h = img.size
        new_file_path = out_path + f"{time_stamp}_{new_w}x{new_h}_{name}"
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
        os.makedirs(path)


def attempt_download(url, save_path):
    try:
        download_res = requests.get(url, stream=True)
    except Exception as e:
        return str(e)
    if download_res.status_code != 200:
        return "Download file failed."
    with open(save_path, 'wb') as file:
        for chunk in download_res.iter_content(chunk_size=1024):
            file.write(chunk)
    return None


def test_compress_image():
    env = "test"
    resize_pix = 2000
    resolution = 200
    quality = 80
    root_path = f"E:\\高清素材_压缩图\\bujue_{env}_{resize_pix}px_{resolution}dpi_{quality}qua\\"
    start_time = time.time()
    url_path_map = {}

    input_path = f"E:\\高清素材_压缩图\\{env}_imagesUrls.json"
    f = open(input_path, 'r', encoding='utf-8')
    f_data = f.read()
    f.close()
    urls = json.loads(f_data)
    size = len(urls)
    print("总图片数：", size, "开始压缩处理...")

    errorNo = []

    output_path = root_path + 'images\\'
    creat_dir_not_exist(output_path)

    i = 0
    for url in urls:
        i = i + 1
        if i < 1452:
            continue
        if not url.startswith('https://app-test.'):
            print("跳过", i, url)
            continue
        out_full_path = ""
        try:
            urlName = urllib.parse.unquote(url.split("/")[-1])
            save_path = "../images/" + urlName.replace("/", "_")
            attempt_download(url, save_path)

            out_full_path = compress_image_util(save_path, resize_pix, resolution, quality, output_path)
            if not out_full_path:
                print(i, "小图跳过处理")
                os.remove(save_path)
                continue
            os.remove(save_path)
            # 上传覆盖原图
            utils.upload_file_to_obs(obs_client, "obs.cn-east-2.myhuaweicloud.com", "app-test",
                                           urlName, out_full_path)
            os.remove(out_full_path)
        except Exception as ex:
            errorNo.append(i)
            if out_full_path:
                os.remove(out_full_path)
            url_path_map[url] = "error:" + str(ex)
            print(i, "error:", ex)

    with open(root_path + 'compress_result_map.json', 'w', encoding='utf-8') as fo:
        json.dump(url_path_map, fo)
        print("加载入文件完成...")

    cost_time = time.time() - start_time
    print("处理完毕，耗时(ms): ", cost_time, "errorNo:", errorNo)


if __name__ == '__main__':
    test_compress_image()
