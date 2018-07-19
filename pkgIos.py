#! /usr/bin/python
# coding:utf-8
import os
import time
import json

#######################  须用户配置   ##############################


#将要上新的版本描述
updateDescription = 'test autopkg'

# 项目路径
projectPath = '/Users/xuqinchao/Projects/otc_client/ios'

# 项目名称
projectName = 'bitaneOTC'

# 打包路径
IPASavePath = '/Users/xuqinchao/Desktop/apps'

# exportOptionPlist文件路径
exportOptionPlistPath = projectPath + '/ExportOptions.plist'


#蒲公英App_Key
pgy_appKey = 'a34e092c13743beba31d10cb07ad7cec'

##################################################################
time_str = time.strftime("%Y-%m-%d--%H:%M:%S", time.localtime())


# 清屏
os.system('clear')
# 进入工程目录
os.chdir(projectPath)
# clean 项目
os.system("xcodebuild clean -project " + projectName + ".xcodeproj -scheme " + projectName + " -configuration Release")
# 生成archive文件
xcarchive_path = IPASavePath + "/" + projectName + ".xcarchive"
# os.system('xcodebuild archive -workspace %s.xcworkspace -scheme %s -configuration Release -archivePath %s'%(projectName,projectName,archivePath))
os.system("xcodebuild archive -project " + projectName + ".xcodeproj -scheme " + projectName + " -archivePath " + xcarchive_path)
# # 生成iPa包
os.system("xcodebuild -exportArchive -archivePath " + xcarchive_path + " -exportPath " + IPASavePath + " -exportOptionsPlist " + exportOptionPlistPath + " -allowProvisioningUpdates")
IpaPath_src = IPASavePath + "/" + projectName + ".ipa"
IpaPath_des = IpaPath_src.replace(projectName+".ipa", time_str + ".ipa")
os.rename(IpaPath_src, IpaPath_des)
if pgy_appKey:
    res = (os.popen("curl -F 'file=@%s' -F '_api_key=%s' -F'updateDescription=%s' https://www.pgyer.com/apiv2/app/upload"%(IpaPath_des,pgy_appKey,updateDescription))).readlines()
    res_json = json.loads(res[0])
    f_result = open(IPASavePath + "/iOS 蒲公英上传结果.txt", "w")
    if res_json["code"] == 0:
        f_result.write("上传成功啦！！！  \r\n\r\n")
    else:
        f_result.write("上传失败了！！！  \r\n\r\n")
    f_result.write("服务器返回结果: \r\n" + str(res))
    print res
