import os
import random
import hashlib

try:
    from qcloud_cos_v5 import CosConfig
    from qcloud_cos_v5 import CosS3Client
except:
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client

appid = os.environ.get('tencent_appid')
secret_id = os.environ.get('tencent_secret_id')
secret_key = os.environ.get('tencent_secret_key')
region = os.environ.get('region')
bucket = os.environ.get('cos_bucket').replace("-" + appid, "")

print(os.environ)

config = CosConfig(
    Secret_id=secret_id,
    Secret_key=secret_key,
    Region=region,
)
client = CosS3Client(config)


def getFileMd5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()


def getFileKey(md5):
    random_data = str(random.randint(0, 10000))
    m = hashlib.md5()
    m.update((md5 + random_data).encode())
    return m.hexdigest()


def getUrl(key):
    try:
        response = client.get_presigned_url(
            Method='GET',
            Bucket='{}-{}'.format(bucket, appid),
            Key=key
        )
        return response
    except:
        return "https://{}-{}.cos.{}.myqcloud.com/{}".format(bucket, appid, region, key)


def upload2Cos(file='/tmp/picture.png', type="png"):
    try:
        name = getFileKey(getFileMd5(file)) + "." + type
        path = "large/" + name
        response = client.put_object_from_local_file(
            Bucket='{}-{}'.format(bucket, appid),
            LocalFilePath=file,
            Key=path
        )
        print(response)
        return (path, name)
    except Exception as e:
        print(e)
        return False


def download2disk(file, download_path):
    response = client.get_object(Bucket='{}-{}'.format(bucket, appid), Key=file, )
    response['Body'].get_stream_to_file(download_path)
