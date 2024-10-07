import os


version = 'V2.1.1'
command = "pyinstaller -F -i icon.ico --distpath=exe\{0}\dist --workpath=exe\{0}\work --name=自动化{0} toutiao.py".format(version)
exit_code = os.system(command)



# command = "pyinstaller -F -i icon.ico --distpath=exe\openurl\dist --workpath=exe\openurl\work --name=打开浏览器 openUrl.py"
# exit_code = os.system(command)

if exit_code == 0:
    print("打包完成")
else:
    print("An error occurred")