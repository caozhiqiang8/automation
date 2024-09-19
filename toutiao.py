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
    with open(r'cdk.txt', 'r', encoding='utf-8') as file:
        cdk = file.read()
    if cdk :
        hostname = os.popen('hostname').read().strip()
        conn = sqlite3.connect('automation.db')
        cursor = conn.cursor()
        sql = '''
          select * from host_key where  host='{}' and key = '{}'
            '''.format(hostname, cdk)
        result = cursor.execute(sql).fetchall()
        if result:
            return ''
        else:
            print('[{}] 没有权限，请联系作者：syy180806'.format(nowTime()))
            page.wait(10)
            sys.exit()
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
    try:
        if 'https://www.toutiao.com' in url :
            page.get(url)
            connect = page.ele('xpath://*[@id="root"]/div[2]/div[2]/div[1]/div/div/div/div/article').text
            title = page.ele('@class=article-content').ele('tag:h1').text
            img = page.ele('xpath://*[@id="root"]/div[2]/div[2]/div[1]/div/div/div/div/article').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.163.com/' in url:
            page.get(url)
            connect = page.ele('xpath://*[@id="content"]/div[2]').text
            title = page.ele('@class=post_title').text
            img = page.ele('@class:post_body').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.sohu.com/' in url :
            page.get(url)
            connect = page.ele('@id=mp-editor').text
            title = page.ele('@class=text-title').text
            img = page.ele('@id=mp-editor').eles('tag:img')
            imgList = []
            for i in img:
                imgurl = i.attr('src')
                if imgurl == None:
                    imgurl = r'https:' + i.attr('data-src')
                imgList.append(imgurl)
        elif 'https://new.qq.com/' in url:
            page.get(url)
            connect = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').text
            title = page.ele('xpath://*[@id="dc-normal-body"]/div[3]/div[1]/div[1]/div[2]/h1').text
            img = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').eles('tag:img')
            imgList = img.get.links()
        elif 'https://a.mp.uc.cn/' in url :
            page.get(url)
            connect = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').text
            title = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/h1').text
            img = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.360kuai.com/'in url :
            page.get(url)
            connect = page.ele('@id=article__content').text
            title = page.ele('@class=article__title').text
            img = page.ele('@id=article__content').eles('tag:img')
            imgList = img.get.links()
        else:
            return 5,5,5
        print('[{}] 文章标题、内容、图片获取成功'.format(nowTime()))
        return connect, title, imgList[:8]
    except:
        return 5, 5, 5

def aiRewrite(article,aiType='wenxin'):
    if aiType == 'wenxin':
        page.get('https://yiyan.baidu.com/')
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
        page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
        print('[{}] 开始输入AI指令......'.format(nowTime()))
        with open(r'AI指令.txt', 'r', encoding='utf-8') as file:
            aiPromat = file.read()
        page.ele('.yc-editor-paragraph').input(aiPromat)
        page.wait(1)
        ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
        page.wait(2)
        page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
        page.wait(1)
        page.ele('@id:chat-id-').eles('tag:span')[3].click()
        print('[{}] AI洗稿成功'.format(nowTime()))

    elif aiType =='tongyi':
        page.get('https://tongyi.aliyun.com/')
        login = page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[1]/div/div/div[3]/button')
        if login:
            print('[{}] 请先登录，并且重新运行程序'.format(nowTime()))
            page.wait(10)
            sys.exit()
        print('[{}] 开始AI改写......'.format(nowTime()))
        page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(article)
        page.wait(1)
        ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
        page.wait(2)
        page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]',timeout=120)
        print('[{}] 开始输入AI指令......'.format(nowTime()))
        with open(r'AI指令.txt', 'r', encoding='utf-8') as file:
            aiPromat = file.read()
        page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(aiPromat)
        page.wait(1)
        ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
        page.wait(2)
        page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div[2]/div[2]/div[3]',timeout=120).click()
        print('[{}] AI洗稿成功'.format(nowTime()))

def articleContrast(originalText,contrastType='meibp'):
    print('[{}] 开始文章检测......'.format(nowTime()))
    if contrastType =='meibp':
        page.get('https://ai.meibp.com/diff.html')
        login = page.ele('xpath://*[@id="nav-container"]/div[2]/a')
        if  login:
            print('[{}] 请先登录，并且重新运行程序'.format(nowTime()))
            page.wait(10)
            sys.exit()
        page.wait(1)
        page.ele('xpath://*[@id="source2"]').click()
        ac.type(Keys.CTRL_V)
        page.wait(1)
        page.ele('xpath://*[@id="source1"]').input(originalText)
        page.wait(1)
        page.ele('xpath://*[@id="button"]').click()
        page.wait(1)
        result = page.ele('xpath://*[@id="result"]/span').text
        result = float(result[5:-2])
        if result < 25.00:
            return 0
        else:
            return 1

    elif contrastType =='wenpp':
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
        if result == '原创' or result =='模仿(伪原创)':
            return 0
        else:
            return 1


if __name__=='__main__':
    secretKey()
    ac = Actions(page)
    page.set.window.max()
    lableLlist = {0:'自己输入文章链接',1:'热点',2:'娱乐',3:'体育',4:'军事',5:'历史',6:'财经'}
    print('[0]自己输入文章链接  [1]热点  [2]娱乐  [3]体育  [4]军事  [5]历史  [6]财经')
    inputLable = int(input('------->>>请选择:'))
    if inputLable > 6:
        inputLable = 1
    elif inputLable == 0 :
        with open(r'文章链接.txt', 'r', encoding='utf-8') as file:
            fileUrl = file.read()
        articleUrlList = fileUrl.splitlines()
    else:
        navItem = lableLlist[inputLable]
        articleUrlList = getArticleUrl(navItem = navItem)
    print(articleUrlList)

    successNum = 0
    contrastNum = 0
    for url in articleUrlList:
        article,title,imgList = getArticle(url)
        # print(title,article,imgList)
        page.wait(1)
        if article == 5:
            print('[{}] 链接暂时不支持，自动跳过'.format(nowTime()))
            continue
        aiRewrite(article,aiType='tongyi')
        page.wait(1)

        for i in range(3):
            firm = articleContrast(article,contrastType='meibp')
            if firm == 0 :
                print('[{}] 文章检测完成'.format(nowTime()))
                contrastNum = 0
                break
            contrastNum+=1
            page.wait(1)

        if contrastNum > 4:
            print('[{}] 文章3次未通过检测自动跳过'.format(nowTime()))
            contrastNum = 0
            continue

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
        imgNum = 4
        if len (imgList) >0:
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
        else:
            pass
        successNum += 1

        if  inputLable == 0:
            delUrl = fileUrl.replace(url,'')
            with open(r'文章链接.txt', 'w', encoding='utf-8') as file:
                file.write(delUrl)

        print('[{}] {}写入成功，共成功 {} 条'.format(url,nowTime(),successNum))
