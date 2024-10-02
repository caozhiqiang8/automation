from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import pyautogui


# page = ChromiumPage()
# ac = Actions(page)
# page.get('https://www.baidu.com')
# page.wait(1)


# pyautogui.hotkey('shift', 'ctrl','m')
# pyautogui.hotkey('down')
# pyautogui.hotkey('enter')
# page.close()
# new = page.latest_tab
# new.get('https://www.hao123.com')
# pyautogui.alert(text='结束', title='title', button='alert')

from DrissionPage import ChromiumPage, ChromiumOptions

# 创建多个配置对象，每个指定不同的端口号和用户文件夹路径

localList = {
    'local_port':[9111,9222],
    'user_data_path' : [r'D:\userData_9111',r'D:\userData_9222'],
}
do = ChromiumOptions().set_paths(local_port=localList['local_port'][0], user_data_path=localList['user_data_path'][0])
page = ChromiumPage(addr_or_opts=do)
page.get('https://www.baidu.com')

page.close()
do = ChromiumOptions().set_paths(local_port=localList['local_port'][0], user_data_path=localList['user_data_path'][0])
page = ChromiumPage(addr_or_opts=do)

page.get('http://www.163.com')