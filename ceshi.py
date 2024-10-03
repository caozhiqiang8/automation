from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import pyautogui


page = ChromiumPage()
ac = Actions(page)

chuangzuo = page.ele('xpath://*[@id="app"]/div[2]/div[3]/div[2]/div')
for i in chuangzuo.children():
    if i.text == '图文消息':
        i.click()
        break
    else:
        print('meizhaodao')
