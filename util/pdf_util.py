import logging
import os
import time

import pandas
from pdf2image import convert_from_path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='../logs/my.log',
                    filemode='a')
logger = logging.getLogger(__name__)


# pdf2image在windows电脑安装：https://pypi.org/project/pdf2image/
def pdf2image(pdf_path, output_folder, dpi=250, fmt='jpeg'):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    basename = os.path.basename(pdf_path)
    convert_from_path(pdf_path, dpi=dpi, output_folder=output_folder, fmt=fmt, paths_only=True,
                      thread_count=4, output_file=basename)


if __name__ == '__main__':
    start_time = time.time()
    root = "Z:\\格度产品录入"
    for catagory_name in os.listdir(root):
        catagory_path = os.path.join(root, catagory_name)
        if not os.path.isdir(catagory_path):
            logger.warning("跳过非文件夹路径 '{}'".format(catagory_path))
            continue
        if ['exe'].__contains__(catagory_name):
            logger.warning("跳过特定文件夹 '{}'".format(catagory_path))
            continue
        logger.info(catagory_path)

        # 读取分类目录下excel表
        excel_path = os.path.join(catagory_path, "out.xlsx")
        if not os.path.exists(excel_path):
            logger.warning("'{}' 路径下未找到Excel文件".format(catagory_path))
            continue
        dataframe = pandas.read_excel(excel_path, sheet_name=0, skiprows=0, usecols=['产品介绍'])
        for cur_row_pdf_str in dataframe['产品介绍']:
            if not cur_row_pdf_str:
                continue
            cur_row_pdfs = str(cur_row_pdf_str).split('|')

            for pdf in cur_row_pdfs:
                inner_start_time = time.time()
                logger.info("  dealing with pdf: '{}'".format(pdf))
                pdf = os.path.join(catagory_path, pdf)
                stem, suffix = os.path.splitext(pdf)
                if suffix != '.pdf':
                    logger.info("    跳过处理...")
                    continue
                pdf_image_folder = pdf.replace(suffix, '')
                if os.path.exists(pdf_image_folder):
                    logger.info("    跳过处理...")
                    continue
                try:
                    # 转换图片工具
                    pdf2image(pdf, pdf_image_folder, 150)
                    inner_end_time = time.time()
                    logger.info(
                        '  Successful dealing with conversion time: %.3f seconds\n' % (
                                    inner_end_time - inner_start_time))
                except Exception as e:
                    if os.path.exists(pdf_image_folder):
                        os.rmdir(pdf_image_folder)
                    inner_end_time = time.time()
                    logger.error(
                        '  Failed to deal with conversion time: %.3f seconds\n' % (inner_end_time - inner_start_time))
    end_time = time.time()
    logger.info('Conversion finished within %.3f seconds' % (end_time - start_time))
