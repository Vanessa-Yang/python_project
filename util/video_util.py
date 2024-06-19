# 视频处理工具
import logging
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compress_video(video_path, output_path):
    fp_size = os.path.getsize(video_path) / 1024 / 1024
    # 超过3M则压缩视频
    if fp_size > 3:
        compress = (
            "ffmpeg -i {} -r 24 -c:v libx264 -crf 45 -acodec aac {}"
            .format(video_path, output_path))
        is_run = os.system(compress)
        if is_run != 0:
            logger.error("is_run = {}, 没有安装ffmpeg".format(is_run))
            return False
        return True
    return True


if __name__ == '__main__':
    start = time.time()
    compress_video('C:\\Users\\Administrator\\Videos\\MP4测试.MP4',
                   'C:\\Users\\Administrator\\Videos\\MP4测试_compression.MP4')
    end = time.time()
    logger.info("Video compression time: {}".format(end - start))
