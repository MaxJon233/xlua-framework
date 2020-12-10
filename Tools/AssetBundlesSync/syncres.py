#!/usr/bin/python
# -*- coding: UTF-8 -*-
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
import  sys
import logging
if len(sys.argv) < 4:
    print("param error：sample python xx.py E:/Tmp/Android/AssetBundles  server-rrot(week1) platform(iOS/Android)")
    exit(-1)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#pip install pyopenssl ndg-httpsclient pyasn1
secret_id = 'AKIDWrwlJbAMyOaYGjuzlHciZHkxve7K7Fp8'      # 替换为用户的 secretId
secret_key = 'B7mALGwOaXJrACyThjUzDArITNUMPFp9'      # 替换为用户的 secretKey
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
Bucketname='zhj-1253729609'  # Bucket由bucketname-appid组成

# with open('test.txt', 'rb') as fp:
#     response = client.put_object(
#         Bucket=Bucketname,  # Bucket由bucketname-appid组成
#         Body=fp,
#         Key=file_name,
#         StorageClass='STANDARD',
#         ContentType='text/html; charset=utf-8'
#     )
#     print(response['ETag'])
#首先定义部分本地文件名，不需要比价必须更新的
resversion = 'res_version.bytes'
appversion = 'app_version.bytes'
update_md5='update_md5.bytes'
audiobasepath='Audio/GeneratedSoundBanks/Android/'
localrespath=sys.argv[1]
serverroot=sys.argv[2]
platform = sys.argv[3]
audiobasepath=u"Audio/GeneratedSoundBanks/{Plat}".format(Plat=platform)
serverrespath=u"{root}/{Plat}/{Plat1}/AssetBundles".format(root=serverroot,Plat=platform,Plat1=platform)
audiopath=u"{path}/{name}".format(path=serverrespath, name=audiobasepath)
server_update_md5file=u"{path}/{name}".format(path=serverrespath, name=update_md5)
local_update_md5file=u"{path}/{name}".format(path=localrespath, name=update_md5)
#读取本地文件数组
localfilelist = []
#需要上传的本地文件数组
Uplocalfilelist = []
#需要更新到
updatefilelist = []
print localrespath
print serverroot
print platform
# 打开文件
def UploadFile(localfile,serverfile):
    try:
        response = client.put_object_from_local_file(
            Bucket=Bucketname,
            LocalFilePath=localfile,
            Key=serverfile,
        )
        return 1
    except CosServiceError as e:
        print(e.get_origin_msg())
        print(e.get_digest_msg())
        print(e.get_status_code())
        print(e.get_error_code())
        print(e.get_error_msg())
        print(e.get_resource_location())
        print(e.get_trace_id())
        print(e.get_request_id())
        print("------------error------------------upload faild:{path}".format(path=localfile))
    return 0

def CompareLocalAndServerFile(serverfile,_localfilelist,updatefilelist):
    downcode = 0
    dicServerFiles = {}
    try:
        response = client.get_object(
            Bucket=Bucketname,
            Key=serverfile,
        )
        file = u"{file}.bak".format(file=update_md5)
        response['Body'].get_stream_to_file(file)
        fp = open(file, "r")
        #吧服务器数据存储到本地字典中便于查询
        for serverfile in fp.readlines():  # 依次读取本地每行
            serverfile = serverfile.strip()  # 去掉每行头尾空白
            tmp = serverfile.split(',')
            dicServerFiles[tmp[0]] = tmp[2]
    except CosServiceError as e:
        print(e.get_origin_msg())
        print(e.get_digest_msg())
        print(e.get_status_code())
        print(e.get_error_code())
        print(e.get_error_msg())
        print(e.get_resource_location())
        print(e.get_trace_id())
        print(e.get_request_id())
        downcode = e.get_status_code()
    # 准备比较找出所有需要更新的文件
    if downcode != 0:
        print "server data is no,need to update all file"
        for linelocal in _localfilelist:
            filelocal = linelocal.split(',')
            if int(filelocal[3]) == 2:
                file = "{path}/{name}".format(path=audiobasepath, name=filelocal[0])
                updatefilelist.append(file)
            else:
                file = filelocal[0]
                updatefilelist.append(file)

    else:
        #遍历本地文件逐个和服务器文件对比
        for localline in localfilelist:  # 依次读取本地每行
            localline = localline.strip()  # 去掉每行头尾空白
            localfileinfo = localline.split(',')
            if localfileinfo[0] in dicServerFiles:
                if localfileinfo[2] != dicServerFiles[localfileinfo[0]] :
                    if int(localfileinfo[3]) == 2:
                        file = "{path}/{name}".format(path=audiobasepath, name=localfileinfo[0])
                        updatefilelist.append(file)
                    else:
                        file = localfileinfo[0]
                        updatefilelist.append(file)
            else:
                if int(localfileinfo[3]) == 2:
                    file = "{path}/{name}".format(path=audiobasepath, name=localfileinfo[0])
                    updatefilelist.append(file)
                else:
                    file = localfileinfo[0]
                    updatefilelist.append(file)

#首先读取本地文件数据
localfo = open(local_update_md5file, "r")
print "local md5 filename: ", localfo.name
localfilelist=localfo.readlines()
# for line in localfilelist:  # 依次读取每行
#     line = line.strip()  # 去掉每行头尾空白
#     print "读取的数据为: %s" % (line)
#下载服务器文件
# 文件下载 获取文件流
print(server_update_md5file)
CompareLocalAndServerFile(server_update_md5file,localfilelist,updatefilelist)
updatefilelist.append(resversion)
updatefilelist.append(appversion)
updatefilelist.append(update_md5)
print "begin upload"
for file in updatefilelist:
    locafile= "{path}/{name}".format(path=localrespath, name=file)
    serfile = "{path}/{name}".format(path=serverrespath, name=file)
    UploadFile(locafile,serfile)
 #开始上传必须文件

   # print "读取的数据为: %s" % (strsplit[0])

#首先下载服务器更新地址对应的update文件