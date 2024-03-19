# 华为云 Obs 存储中心
from urllib.parse import quote

from obs import ObsClient

# TODO 推送代码前：必须注释，临时使用，用完即删
AK = "W2QOGAAHZZCIPHSA6BME"
SK = "KKXCGoPSnZta4odeSvg3DN6D1KybYLQN6Lg07E8d"
OBS_ADDR = "obs.cn-east-2.myhuaweicloud.com"

# AK = ""
# SK = ""
# OBS_ADDR = ""

def upload_file_to_obs(client, obs_address, bucket, obj_name, file):
    resp = client.putFile(bucket, obj_name, file)
    if resp.status >= 300:
        print(
            "   上传 %s 失败，状态码： %d 。" % (
                file.split("/", 2)[-1], resp.status))
        return ""
    else:
        print("   上传 %s 成功。" % obj_name)
        # url = "https://" + bucket + "." + obs_address + quote(obj_name)
        # res = requests.get(url)
        # if res.status_code != 200:
        url = "https://" + bucket + "." + obs_address + "/" + quote(obj_name)
        return url


# 连接obs
def new_obs_client(ak, sk, obs_server):
    return ObsClient(access_key_id=ak, secret_access_key=sk, server=obs_server,
                     path_style=True, ssl_verify=False, max_retry_count=5, timeout=20)


obs_client = new_obs_client(AK, SK, OBS_ADDR)