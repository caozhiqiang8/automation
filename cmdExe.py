import os


version = 'V2.1'
command = "pyinstaller -F -i icon.ico --distpath=exe\{0}\dist --workpath=exe\{0}\work --name=自动化{0} toutiao.py".format(version)
exit_code = os.system(command)


if exit_code == 0:
    print("输入完成")
else:
    print("An error occurred")