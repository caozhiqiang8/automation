from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import sys,os
import sqlite3
from datetime import datetime
import traceback

def nowTime():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now

def log(type='err',msg=''):
    filePath = 'log.txt'
    fileSize = os.path.getsize(filePath)
    if fileSize > 1*1024*1024:
        with open(filePath, 'w',encoding='UTF-8-sig') as f:
            f.truncate(0)
    with open(filePath, 'a',encoding='UTF-8-sig') as f:
        f.write('\n' + '[{}]  '.format(nowTime()) + msg)
        if type =='err':
            traceback.print_exc(file=f)

def secretKey(cdk):
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
            runJs('没有权限，请联系作者：syy180806')
            sys.exit()
    else:
        runJs('没有权限，请联系作者：syy180806')
        sys.exit()
    cursor.close()
    conn.close()

def runJs(msg):
    page.run_js('alert(arguments[0]);', msg)

def getArticleUrl(cdk,navItem,scrollNum = 0):
    secretKey(cdk)
    page.get('https://www.toutiao.com/')
    login = page.ele('xpath://*[@id="root"]/div/div[3]/div[2]/a')
    if login:
        runJs('请先登录，并且重新运行程序')
        sys.exit()
    print('[{}] 开始自动采集 {} 文章......'.format(nowTime(),navItem))
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[9]/div[1]').click()
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul').ele('text:{}'.format(navItem)).click()
    page.wait(1)
    if scrollNum-1 > 0:
        for i in range(scrollNum):
            page.scroll.to_bottom()
            page.wait(3)
    refresh = page.ele('@class=feed-m-top-refresh')
    page.wait.ele_hidden(refresh)
    articleCard  = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]').children()
    articleUrlList = []
    for i in range(len(articleCard)):
        url = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div[{}]/div/div/a'.format(i+1)).link
        articleUrlList.append(url)
    return articleUrlList

def getArticle(cdk,url):
    secretKey(cdk)
    page.get(url)
    redirectUrl = page.url
    try:
        if 'https://www.toutiao.com' in redirectUrl :
            connect = page.ele('xpath://*[@id="root"]/div[2]/div[2]/div[1]/div/div/div/div/article').text
            title = page.ele('@class=article-content').ele('tag:h1').text
            img = page.ele('xpath://*[@id="root"]/div[2]/div[2]/div[1]/div/div/div/div/article').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.163.com/' in redirectUrl:
            connect = page.ele('xpath://*[@id="content"]/div[2]').text
            title = page.ele('@class=post_title').text
            img = page.ele('@class:post_body').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.sohu.com/' in redirectUrl :
            connect = page.ele('@id=mp-editor').text
            title = page.ele('@class=text-title').text
            img = page.ele('@id=mp-editor').eles('tag:img')
            imgList = []
            for i in img:
                imgurl = i.attr('src')
                if imgurl == None:
                    imgurl = i.attr('data-src')
                if 'https:' not in imgurl:
                    imgurl = r'https:' +imgurl
                imgList.append(imgurl)
        elif 'https://new.qq.com/' in redirectUrl  or 'https://view.inews.qq.com' in redirectUrl:
            connect = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').text
            title = page.ele('xpath://*[@id="dc-normal-body"]/div[3]/div[1]/div[1]/div[2]/h1').text
            img = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').eles('tag:img')
            imgList = img.get.links()
        elif 'https://a.mp.uc.cn/' in redirectUrl :
            connect = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').text
            title = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/h1').text
            img = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').eles('tag:img')
            imgList = img.get.links()
        elif 'https://www.360kuai.com/'in redirectUrl :
            connect = page.ele('@id=article__content').text
            title = page.ele('@class=article__title').text
            img = page.ele('@id=article__content').eles('tag:img')
            imgList = img.get.links()
        else:
            return 5,5,5
        return connect, title, imgList[:8]
    except Exception:
        log()
        return 5, 5, 5

def aiRewrite(cdk,article,aiType):
    secretKey(cdk)
    try:
        if aiType == 'wenxin':
            page.get('https://yiyan.baidu.com/')
            login = page.ele('xpath://*[@id="root"]/div[1]/div[2]/div/div[2]/div/div')
            if login:
                runJs('请先登录，并且重新运行程序')
                sys.exit()
            page.ele('.yc-editor-paragraph').input(article)
            page.wait(1)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.wait(2)
            page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
            with open(r'AI指令.txt', 'r',encoding='UTF-8-sig') as file:
                aiPromat = file.read()
            page.ele('.yc-editor-paragraph').input(aiPromat)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
            page.ele('@id:chat-id-').eles('tag:span')[3].click()


        elif aiType =='tongyi':
            page.get('https://tongyi.aliyun.com/')
            login = page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[1]/div/div/div[3]/button')
            if login:
                runJs('请先登录，并且重新运行程序')
                sys.exit()
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(article)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]',timeout=120)
            with open(r'AI指令.txt', 'r',encoding='UTF-8-sig') as file:
                aiPromat = file.read()
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(aiPromat)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div[2]/div[2]/div[3]',timeout=120).click()
    except Exception:
        log()
        runJs('请先登录，并且重新运行程序')
        sys.exit()
def articleContrast(cdk,originalText,contrastType='meibp'):
    secretKey(cdk)
    try:
        if contrastType =='meibp':
            page.get('https://ai.meibp.com/diff.html')
            login = page.ele('xpath://*[@id="nav-container"]/div[2]/a')
            if  login:
                runJs('请先登录，并且重新运行程序')
                sys.exit()
            page.ele('xpath://*[@id="source2"]').click()
            ac.type(Keys.CTRL_V)
            page.ele('xpath://*[@id="source1"]').input(originalText)
            page.ele('xpath://*[@id="button"]').click()
            result = page.ele('xpath://*[@id="result"]/span').text
            result = float(result[5:-2])
            if result < 25.00:
                print('[{}] 检测结果：{}'.format(nowTime(), result))
                return 0
            elif result == 100.0:
                runJs('请检查检测网站是否正常')
                sys.exit()
            else:
                print('[{}] 检测结果：{}'.format(nowTime(), result))
                return 1

        elif contrastType =='wenpp':
            page.get('http://www.wenpipi.com/sim')
            updateBox = page.ele('@id=TurnOnScreenDialogBoxCloseId')
            if updateBox:
                updateBox.click()
            page.ele('@id=content2').click()
            ac.type(Keys.CTRL_V)
            page.ele('@id=content1').input(originalText)
            page.ele('@id=animation-container').click()
            page.wait(2)
            result = page.ele('xpath://*[@id="judgeDivId"]/font[2]/strong').text
            if result == '原创' or result =='模仿(伪原创)':
                print('[{}] 检测结果：{}'.format(nowTime(), result))
                return 0
            else:
                print('[{}] 检测结果：{}'.format(nowTime(), result))
                return 1
    except Exception:
        log()
        sys.exit()

if __name__=='__main__':
    page = ChromiumPage(timeout=100)
    try:
        with open(r'config.txt', 'r', encoding='UTF-8-sig') as file:
            file = file.readlines()
        config = {}
        for i in file:
            key, value = i.strip().split('：')
            config[key] = value
        cdk = config['卡密']
        aiType = config['AI源(1代表文心一言，2代表通义千问)']
        if  aiType == '1':
            aiType ='wenxin'
        elif aiType == '2':
            aiType = 'tongyi'
        contrastType = config['文章检测(不要动)']
        if  contrastType == '1':
            contrastType ='meibp'
        elif contrastType == '2':
            contrastType = 'wenpp'
        articleType = int(config['选文方式【0自己选文】【1热点】【2娱乐】【3体育】【4军事】【5历史】'])
        timOut = config['timeout']
        # scrollNum = int(config['自动采集文章次数(1次采集15条，2次30条，依次类推)'])
        scrollNum = 1
    except Exception:
        log()
        runJs('配置文件加载失败，请联系作者：syy180806')
        sys.exit()

    page.set.timeouts(int(timOut))

    secretKey(cdk)
    ac = Actions(page)
    page.set.window.max()
    lableLlist = {0:'自己输入文章链接',1:'热点',2:'娱乐',3:'体育',4:'军事',5:'历史',6:'财经'}
    # scrollNum = 1
    if articleType > 6:
        articleType = 0
    elif articleType == 0 :
        with open(r'文章链接.txt', 'r', encoding='UTF-8-sig') as file:
            fileUrl = file.read()
        articleUrlList = fileUrl.splitlines()
    else:
        navItem = lableLlist[articleType]
        articleUrlList = getArticleUrl(cdk=cdk,navItem = navItem,scrollNum=scrollNum)
        print('[{}] {} 文章共采集了 {} 条'.format(nowTime(), navItem, len(articleUrlList)))

    successNum = 0
    contrastNum = 0
    for url in articleUrlList:
        print('[{}] 开始获取文章内容......'.format(nowTime()))
        article,title,imgList = getArticle(cdk,url)
        # print(article,title,imgList)
        if article == 5:
            print('[{}] 链接暂时不支持，自动跳过'.format(nowTime()))
            continue
        elif len(article) < 50:
            print('[{}] 链接暂时不支持，自动跳过'.format(nowTime()))
            continue
        elif len(article) > 2000:
            article=article[:2000]
        print('[{}] 文章标题、内容、图片获取成功'.format(nowTime()))
        for i in range(3):
            print('[{}] 开始AI改写......'.format(nowTime()))
            aiRewrite(cdk=cdk,article=article, aiType=aiType)
            print('[{}] AI洗稿成功'.format(nowTime()))
            print('[{}] 开始文章检测......'.format(nowTime()))
            firm = articleContrast(cdk=cdk,originalText=article,contrastType=contrastType)
            if firm == 0 :
                print('[{}] 文章检测完成'.format(nowTime()))
                contrastNum = 0
                break
            contrastNum+=1

        if contrastNum > 2:
            print('[{}] 文章3次未通过检测自动跳过'.format(nowTime()))
            contrastNum = 0
            continue

        print('[{}] 开始头条写入文章......'.format(nowTime()))
        page.get('https://mp.toutiao.com/profile_v4/index')
        login = page.ele('xpath://*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button')
        if login:
            runJs('请先登录，并且重新运行程序')
            sys.exit()
        try:
            page.ele('@class=byte-menu-item').click()
            page.wait(1)
            prose = page.ele('@class=ProseMirror')
            prose.click()
            ac.type(Keys.CTRL_V)
            page.wait(1)
            proseHr = prose.eles('tag:hr')
            for i in range(len(proseHr)):
                page.remove_ele(prose.ele('tag:hr'))
            proseStrong = prose.eles('tag:strong')
            for i in range(len(proseStrong)):
                page.remove_ele(prose.ele('tag:strong').parent())
            page.wait(1)
            page.scroll.to_top()
            page.wait(1)
            page.ele('xpath://*[@id="root"]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div/div/div/textarea').input(title)
            page.wait(1)
            print('[{}] 开始插入图片......'.format(nowTime()))
            imgNum = 3
            if len(imgList) >0:
                for img in imgList:
                    newpage = page.new_tab(img)
                    newpage.wait(1)
                    newpage.ele('tag:img').click()
                    new_ac = Actions(newpage)
                    new_ac.type(Keys.CTRL_C)
                    newpage.wait(1)
                    newpage.close()
                    newpage.wait(1)
                    lenProse = page.ele('@class:ProseMirror')
                    if imgNum > len(lenProse.children()):
                        imgNum = len(lenProse.children())
                    lenProse.child(imgNum).click.at(0,0)
                    page.wait(1)
                    ac.key_down(Keys.HOME).key_up(Keys.HOME)
                    page.wait(1)
                    ac.type(Keys.CTRL_V)
                    imgNum = imgNum + 2
            else:
                pass
            saveProse = page.ele('xpath://*[@id="root"]/div/div[1]/div/div[3]/div/div[1]/span[2]').text
            page.wait(3)
            successNum += 1
            logStr = '[{}] {}写入成功，共成功 {} 条'.format(nowTime(),url,successNum)
            log(type='log',msg=logStr)
            print(logStr)
            if articleType == 0:
                with open(r'文章链接.txt', 'r', encoding='UTF-8-sig') as file:
                    fileUrl = file.read()
                delUrl = fileUrl.replace(url,'')
                with open('文章链接.txt', 'w', encoding='UTF-8-sig') as file:
                    file.write(delUrl)

        except Exception:
            log()
            print('[{}] 写入失败，网络加载太慢'.format(nowTime()))
    runJs('程序运行完毕，一共洗稿 {} 条'.format(successNum))
