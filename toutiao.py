from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import sys,os
import sqlite3
from datetime import datetime

page = ChromiumPage()

def nowTime():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now

def secretKey():

    hostname = os.popen('hostname').read().strip()
    conn = sqlite3.connect('automation.db')
    cursor = conn.cursor()
    firstSql = '''
    select * from host_key where  host='{}' and user_key != ''
    '''.format(hostname)
    firstResult = cursor.execute(firstSql).fetchall()

    if firstResult:
        sql = '''
            select * from host_key where  host='{}' and key = user_key
            '''.format(hostname)
        result = cursor.execute(sql).fetchall()
        if result:
            return ''
        else:
            print('[{}] 没有权限，请联系作者：syy180806'.format(nowTime()))
            page.wait(10)
            sys.exit()
    else:
        card = input('请输入卡密:')
        sql = '''
            select * from host_key where  host='{}' and key = '{}'
                            '''.format(hostname,card)
        result = cursor.execute(sql).fetchall()
        if result:
            updateSql = '''
                    update host_key set user_key = '{}'  where host = '{}'
                    '''.format(card, hostname)
            cursor.execute(updateSql)
            conn.commit()
            return ''
        else:
            print('[{}] 没有权限，请联系作者：syy180806'.format(nowTime()))
            page.wait(10)
            sys.exit()

    cursor.close()
    conn.close()


def getArticleUrl(navItem,scrollNum = 0):
    page.get('https://www.toutiao.com/')
    page.wait(1)
    login = page.ele('xpath://*[@id="root"]/div/div[3]/div[2]/a')
    if login:
        print('[{}] 请先登录，并且重新运行程序'.format(nowTime()))
        page.wait(10)
        sys.exit()
    print('[{}] 开始自动采集 {} 文章......'.format(nowTime(),navItem))
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[9]/div[1]').click()
    page.wait(1)
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul').ele('text:{}'.format(navItem)).click()
    page.wait(1)
    if scrollNum > 0:
        for i in range(scrollNum):
            page.scroll.to_bottom()
            page.wait(1)
    articleCard  = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]').children()
    articleUrlList = []
    for i in range(len(articleCard)):
        url = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div[{}]/div/div/a'.format(i+1)).link
        articleUrlList.append(url)
        page.wait(1)
    print('[{}] {} 文章共采集了 {} 条'.format(nowTime(),navItem,(scrollNum+1)*15))
    return articleUrlList

def getArticle(url):
    print('[{}] 开始获取文章内容......'.format(nowTime()))
    page.get(url)
    page.wait(1)
    connect = page.ele('tag:article').text
    page.wait(1)
    title = page.ele('@class=article-content').ele('tag:h1').text
    page.wait(1)
    img = page.ele('tag:article').eles('tag:img')
    page.wait(1)
    imgList = img.get.links()
    print('[{}] 文章标题、内容、图片获取成功'.format(nowTime()))
    return connect,title,imgList[:8]

def aiRewrite(article):
    page.get('https://yiyan.baidu.com/')
    page.set.load_mode.normal()
    login = page.ele('xpath://*[@id="root"]/div[1]/div[2]/div/div[2]/div/div')
    if login:
        print('[{}] 请先登录，并且重新运行程序'.format(nowTime()))
        page.wait(10)
        sys.exit()
    print('[{}] 开始AI改写......'.format(nowTime()))
    page.ele('.yc-editor-paragraph').input(article)
    page.wait(1)
    ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
    page.wait(2)
    page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=1200)
    page.wait(1)
    print('[{}] 开始输入AI指令......'.format(nowTime()))
    with open(r'AI指令.txt', 'r', encoding='utf-8') as file:
        aiPromat = file.read()
    page.ele('.yc-editor-paragraph').input(aiPromat)
    page.wait(1)
    ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
    page.wait(2)
    page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=1200)
    page.wait(1)
    page.ele('@id:chat-id-').eles('tag:span')[3].click()
    print('[{}] AI洗稿成功'.format(nowTime()))

def articleContrast(originalText):
    print('[{}] 开始文章检测......'.format(nowTime()))
    page.get('http://www.wenpipi.com/sim')
    updateBox = page.ele('@id=TurnOnScreenDialogBoxCloseId')
    if updateBox:
        updateBox.click()
    page.wait(1)
    page.ele('@id=content2').click()
    ac.type(Keys.CTRL_V)
    page.wait(1)
    page.ele('@id=content1').input(originalText)
    page.wait(1)
    page.ele('@id=animation-container').click()
    page.wait(1)
    result = page.ele('xpath://*[@id="judgeDivId"]/font[2]/strong').text

    return result

if __name__=='__main__':

    secretKey()
    ac = Actions(page)
    page.set.window.max()

    lableLlist = {0:'自己输入文章链接',1:'热点',2:'娱乐',3:'体育',4:'军事',5:'历史',6:'财经'}
    print('[0]自己输入文章链接  [1]热点  [2]娱乐  [3]体育  [4]军事  [5]历史  [6]财经')
    inputLable = int(input('请选择需要采集的文章领域(输入数字,如果不输入默认热点)：'))
    if inputLable > 6:
        inputLable = 1
    elif inputLable == 0 :
        pass
    navItem = lableLlist[inputLable]
    articleUrlList = getArticleUrl(navItem = navItem)
    successNum = 0
    for url in articleUrlList:
        article,title,imgList = getArticle(url)
        page.wait(1)
        aiRewrite(article)
        page.wait(1)

        for i in range(3):
            firm = articleContrast(article)
            if firm == '原创' or firm =='模仿(伪原创)':
                print('[{}] 文章检测完成'.format(nowTime()))
                break
            page.wait(1)

        print('[{}] 开始头条写入文章......'.format(nowTime()))
        page.wait(1)
        page.get('https://mp.toutiao.com/profile_v4/index')
        page.wait(1)
        login = page.ele('xpath://*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button')
        if login:
            print('[{}] 请先登录，并且重新运行程序'.format(nowTime()))
            page.wait(10)
            sys.exit()
        page.ele('@class=byte-menu-item').click()
        page.wait(1)
        page.ele('@class=ProseMirror').click()
        ac.type(Keys.CTRL_V)
        page.wait(1)
        page.ele('@class=feedback-wrapper feedback-questions').click()
        page.wait(1)
        page.ele('xpath://*[@id="root"]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div/div/div/textarea').input(title)
        print('[{}] 开始插入图片......'.format(nowTime()))
        imgNum=4
        for img in imgList:
            newpage = page.new_tab(img)
            newpage.wait(1)
            newpage.ele('tag:img').click()
            new_ac = Actions(newpage)
            new_ac.type(Keys.CTRL_C)
            newpage.wait(1)
            newpage.close()
            newpage.wait(1)
            if imgNum > len(page.ele('@class:ProseMirror').children()):
                imgNum = len(page.ele('@class:ProseMirror').children())
            page.ele('@class:ProseMirror').child(imgNum).click.at(0,0)
            ac.key_down(Keys.HOME).key_up(Keys.HOME)
            page.wait(1)
            ac.type(Keys.CTRL_V)
            page.wait(1)
            imgNum = imgNum + 3
        successNum = successNum + 1
        print('[{}] 头条成功写入: {} 条'.format(nowTime(),successNum))
