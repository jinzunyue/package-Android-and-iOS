#!/usr/bin/python
# coding:utf-8
import os
import shutil
import time

# 此脚本可以实现安卓自动打包，将包名修改为当前时间，并移动到指定的目录,还可以上传到蒲同英
# 使用时修改 android_project_path 和 apk_dest_path 这两个参数即可

# 安卓项目的目录
android_project_path = "/Users/xuqinchao/Projects/otc_client/android"

# app-releaes.apk 的目标路径
apk_dest_path = "/Users/xuqinchao/Desktop/apps"

# 将要上新的版本描述
updateDescription = "OTC 内部测试"

#蒲公英App_Key
pgy_appKey = 'a34e092c13743beba31d10cb07ad7cec'

os.chdir(android_project_path)
os.system("./gradlew assembleRelease")
app_src = android_project_path + "/app/build/outputs/apk/release/app-release.apk"
new_apk_name = time.strftime("%Y-%m-%d--%H:%M:%S", time.localtime()) + ".apk"
app_dest = app_src
if apk_dest_path:
    app_dest = apk_dest_path + new_apk_name
else:
    app_dest = app_dest.replace("app-release.apk", new_apk_name)
shutil.copy2(app_src, app_dest)
if pgy_appKey:
    res = (os.popen(
        "curl -F 'file=@%s' -F '_api_key=%s' -F'updateDescription=%s' https://www.pgyer.com/apiv2/app/upload" % (
        app_dest, pgy_appKey, updateDescription))).readlines()
    res_json = json.loads(res[0])
    f_result = open(apk_dest_path + "/Android 蒲公英上传结果.txt", "w")
    if res_json["code"] == 0:
        f_result.write("上传成功啦！！！  \r\n\r\n")
    else:
        f_result.write("上传失败了！！！  \r\n\r\n")
    f_result.write("服务器返回结果: \r\n" + str(res))
    print res

