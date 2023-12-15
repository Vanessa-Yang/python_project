from wand.image import Image

def compress_image_util(image_path, resize_pix=700, resolution = 300):
    img = Image(filename=image_path)
    time_stamp = str(int(datetime.datetime.now().timestamp() * 100000))
    img.resolution = resolution if min(img.resolution) > resolution else img.resolution
    name = image_path.split("/")[-1]
    img.compression_quality = 70 if img.compression_quality > 70 else img.compression_quality
    w, h = img.size
    if w < resize_pix or h < resize_pix:
        new_w, new_h = img.size
        new_file_path = "./images/" + f"{time_stamp}_{new_w}_{new_h}_{name}"
        img.save(filename=new_file_path)
        img.close()
        return new_file_path
    if w > h:
        img.transform(resize="x" + str(resize_pix))
    else:
        img.transform(resize=str(resize_pix))
    new_w, new_h = img.size
    new_file_path = "./images/" + f"{time_stamp}_{new_w}x{new_h}_{name}"
    img.save(filename=new_file_path)
    img.close()
    return new_file_path