from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import Actions,Keys
import sys,os
import sqlite3
from datetime import datetime
import traceback
import base64
import pyautogui
import re

def nowTime():
    now = datetime.strptime((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
    return now

def fileOperate(fileName, fileType,readType, msg=''):
    if fileType == 'r':
        with open(fileName, 'r', encoding='UTF-8-sig') as file:
            if readType == 'read':
                return  file.read()
            elif readType == 'readlines':
                return  file.readlines()

    elif fileType == 'w':
        with open(fileName, 'w', encoding='UTF-8-sig') as file:
            if readType == 'truncate':
                file.truncate(0)
            elif readType == 'write':
                file.write(msg)

    elif fileType == 'a':
        with open(fileName, 'a', encoding='UTF-8-sig') as file:
            if readType == 'write':
                file.write('\n' + '[{}]  '.format(nowTime()) + msg + '  ')
                if msg == '':
                    traceback.print_exc(file=file)

def baseKey(data,type):
    data = data.encode('utf-8')
    if type == 'encode':
        res = base64.b64encode(data).decode()
        return  res
    elif type == 'decode':
        res = base64.b64decode(data).decode()
        return res

def secretKey(cdk):
    if cdk :
        conn = sqlite3.connect('automation.db')
        cursor = conn.cursor()
        etimeSql = '''
        SELECT c_time FROM host_key LIMIT 1
        '''
        etime = (cursor.execute(etimeSql).fetchall())[0][0]

        hostname = os.popen('hostname').read().strip()
        for i in range(3):
            hostname = baseKey(data=hostname, type='encode')
            cdk = baseKey(data=cdk, type='encode')
            etime = baseKey(data=etime, type='decode')
        etime = datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        sql = '''
          SELECT * FROM host_key WHERE  host='{}' and key = '{}'
            '''.format(hostname, cdk)
        result = cursor.execute(sql).fetchall()
        if result:
            if etime < nowTime():
                pyautogui.alert(text='没有权限，请联系作者：syy180806', title='警告', button='我知道了')
                sys.exit()
        else:
            pyautogui.alert(text='没有权限，请联系作者：syy180806', title='警告', button='我知道了')
            sys.exit()
    else:
        pyautogui.alert(text='没有权限，请联系作者：syy180806', title='警告', button='我知道了')
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
        pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
        sys.exit()
    print('[{}] 开始自动采集 {} 文章......'.format(nowTime(),navItem))
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[9]/div[1]').click()
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul').ele('text:{}'.format(navItem)).click()
    page.wait(1)
    if scrollNum-1 > 0:
        for i in range(scrollNum):
            page.wait(2)
            page.scroll.to_bottom()
    page.wait(3)
    articleCard  = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]').children()
    articleUrlList = []
    for i in range(len(articleCard)):
        url = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div[{}]/div/div/a'.format(i+1)).link
        articleUrlList.append(url)
    return articleUrlList

def getArticle(cdk,url):
    secretKey(cdk)
    try:
        page.get(url)
        redirectUrl = page.url
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
        elif 'https://new.qq.com/' in redirectUrl  :
            connect = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').text
            title = page.ele('xpath://*[@id="dc-normal-body"]/div[3]/div[1]/div[1]/div[2]/h1').text
            img = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').eles('tag:img')
            imgList = img.get.links()
        elif 'https://view.inews.qq.com/' in redirectUrl:
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
        fileOperate(fileName=r'log.txt',fileType='a',readType='write')
        return 5, 5, 5

def aiRewrite(cdk,article,aiType):
    secretKey(cdk)
    try:
        aiPromat = fileOperate(fileName='AI指令.txt', fileType='r',readType='read')
        if len(aiPromat) < 5:
            pyautogui.alert(text='请检查指令是否正确，字符数必须大于5', title='警告', button='我知道了')
            sys.exit()
        if aiType == 'wenxin':
            page.get('https://yiyan.baidu.com/')
            login = page.ele('xpath://*[@id="root"]/div[1]/div[2]/div/div[2]/div/div')
            if login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                sys.exit()
            page.ele('.yc-editor-paragraph').input(article)
            page.wait(1)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.wait(2)
            page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
            page.ele('.yc-editor-paragraph').input(aiPromat)
            ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=120)
            page.ele('@id:chat-id-').eles('tag:span')[3].click()

        elif aiType =='tongyi':
            page.get('https://tongyi.aliyun.com/')
            login = page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[1]/div/div/div[3]/button')
            if login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                sys.exit()
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(article)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[2]/span',timeout=120).click()
            # ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]',timeout=120)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea').input(aiPromat)
            # ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[2]/span',timeout=120).click()
            page.ele('xpath://*[@id="tongyiPageLayout"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div[2]/div[2]/div[3]',timeout=120).click()
    except Exception:
        fileOperate(fileName=r'log.txt',fileType='a',readType='write')
        pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
        sys.exit()

def articleContrast(cdk,originalText,contrastType='meibp'):
    secretKey(cdk)
    try:
        if contrastType =='meibp':
            page.get('https://ai.meibp.com/diff.html')
            login = page.ele('xpath://*[@id="nav-container"]/div[2]/a')
            if  login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
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
                pyautogui.alert(text='请检查检测网站是否正常', title='警告', button='我知道了')
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
        fileOperate(fileName=r'log.txt',fileType='a',readType='write')
        sys.exit()

if __name__=='__main__':
    fileOperate(fileName='log.txt', fileType='w',readType='truncate')
    
    try:
        fileLines = fileOperate(fileName=r'config.txt', fileType='r',readType='readlines')
        config = {}
        for i in fileLines:
            key, value = i.strip().split('：')
            config[key] = value
        cdk = config['卡密']
        timOut = config['timeout']
        articleType = config['选文方式【0自己选文】【1自动采集】']
        domainType = int(config['自动采集领域(自动采集才生效)【0热点】【1娱乐】【2体育】【3军事】【4历史】'])
        scrollNum = int(config['自动采集文章次数(1次采集15条文章)']) -1
        releaseType = config['自动发布【0是】【1否】(请谨慎选择1)']
        publishType = config['发布平台【0头条】【1公众号】【2百家号】']
        aiType = config['AI源【0文心一言】【1通义千问】']
        if  aiType == '0':
            aiType ='wenxin'
        elif aiType == '1':
            aiType = 'tongyi'
        else:
            aiType = 'wenxin'
        contrastType = config['文章检测(不要动)']
        if  contrastType == '0':
            contrastType ='meibp'
        elif contrastType == '1':
            contrastType = 'wenpp'
        else:
            contrastType = 'meibp'
            
        if 'dataPath' in config:
            dataPath = config['dataPath']
        if 'localPort' in config:
            localPort = config['localPort']
            localPort = re.split(',',localPort) 

        
    except Exception:
        fileOperate(fileName=r'log.txt',fileType='a',readType='write')
        pyautogui.alert(text='配置文件加载失败，请联系作者：syy180806', title='警告', button='我知道了')
        sys.exit()
        
    page = ChromiumPage(timeout=100)
    page.set.timeouts(int(timOut))
    secretKey(cdk)
    ac = Actions(page)
    page.set.window.max()

    lableLlist = ['热点','娱乐','体育','军事','历史']
    if articleType == '1':
        if domainType not in [0,1,2,3,4]:
            domainType = 0
        navItem = lableLlist[domainType]
        articleUrlList = getArticleUrl(cdk=cdk, navItem=navItem, scrollNum=scrollNum)
        print('[{}] {} 文章共采集了 {} 条'.format(nowTime(), navItem, len(articleUrlList)))
    else:
        fileUrl = fileOperate(fileName=r'文章链接.txt', fileType='r',readType='read')
        articleUrlList = fileUrl.splitlines()

    successNum = 0
    contrastNum = 0
    for url in articleUrlList:
        if url == '---头条---':
            print('切换到头条')
            publishType ='0'
        elif url == '---公众号---':
            print('切换到公众号')
            publishType ='1'    
        elif url == '---百家号---':
            print('切换到百家')
            publishType ='2'
        elif '切换' in url:
            switchProject = int((url.replace('-','')).replace('切换',''))
            print('切换帐号到 ｛｝'.format(switchProject))
            if switchProject not in localPort:
                pyautogui.alert(text='切换帐号失败，请检查配置是否正确', title='警告', button='我知道了')
                sys.exit()
            publishType = config['发布平台【0头条】【1公众号】【2百家号】']
            page.wait(1)
            page.close()
            do = ChromiumOptions().set_paths(local_port=switchProject, user_data_path='{}:\\userData\\userData_{}'.format(dataPath,switchProject))
            page = ChromiumPage(addr_or_opts=do)
            page.set.timeouts(int(timOut))
            secretKey(cdk)
            ac = Actions(page)
            page.set.window.max()
            switchProjectNum +=1
            
        print('[{}] 开始获取文章内容......'.format(nowTime()))
        article, title, imgList = getArticle(cdk, url)
        # print(article,title,imgList)
        if article == 5:
            print('[{}] 链接暂时不支持，自动跳过'.format(nowTime()))
            continue
        elif len(article) < 50:
            print('[{}] 链接暂时不支持，自动跳过'.format(nowTime()))
            continue
        elif len(article) > 2000:
            article = article[:2000]
        print('[{}] 文章标题、内容、图片获取成功'.format(nowTime()))
        for i in range(3):
            
            print('[{}] 开始AI改写......'.format(nowTime()))
            aiRewrite(cdk=cdk, article=article, aiType=aiType)
            print('[{}] AI洗稿成功'.format(nowTime()))
            print('[{}] 开始文章检测......'.format(nowTime()))
            firm = articleContrast(cdk=cdk, originalText=article, contrastType=contrastType)
            if firm == 0:
                contrastNum = 0
                break
            contrastNum += 1
        if contrastNum > 2:
            print('[{}] 文章3次未通过检测自动跳过'.format(nowTime()))
            contrastNum = 0
            continue
        if publishType =='0':
            print('[{}] 头条写入文章......'.format(nowTime()))
            page.get('https://mp.toutiao.com/profile_v4/index')
            login = page.ele('xpath://*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button')
            if login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
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
                        if newpage.url =='about:blank':
                            newpage.close()
                            continue
                        newpage.ele('tag:img').click()
                        new_ac = Actions(newpage)
                        newpage.wait(1)
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
            except Exception:
                fileOperate(fileName=r'log.txt',fileType='a',readType='write')
                print('[{}] 写入失败，网络加载太慢'.format(nowTime()))

        elif publishType =='1':
            try:
                page.get('https://editor.mdnice.com/')
                login = page.ele('xpath:/html/body/div[2]/div/div[2]/div/div[2]/div')
                if login:
                    pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                    sys.exit()
                page.ele('xpath://*[@id="article-sidebar-container"]/div/div/div[2]/div/div/div/ul/li').click()
                page.wait(1)
                page.ele('xpath://*[@id="nice-md-editor"]/div/div[6]').click()
                page.wait(1)
                ac.type(Keys.CTRL_A)
                page.wait(1)
                ac.type(Keys.CTRL_V)
                page.wait(1)
                page.ele('xpath://*[@id="nice-sidebar-wechat"]').click()
                print('[{}] 公众号写入文章......'.format(nowTime()))
                page.get('https://mp.weixin.qq.com/')
                login = page.ele('xpath://*[@id="header"]/div[2]/div/div/div[2]/a')
                if login:
                    pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                    sys.exit()
                newCreation = page.ele('xpath://*[@id="app"]/div[2]/div[3]/div[2]/div')
                for i in newCreation.children():
                    if i.text == '图文消息':
                        i.click()
                        break
                    else:
                        print('meizhaodao')
                editPage = page.latest_tab
                editAc = Actions(editPage)
                editPage.wait(3)
                editPage.ele('@id=edui1_contentplaceholder').click()
                editAc.type(Keys.CTRL_V)
                editPage.wait(1)
                editPage.scroll.to_top()
                editPage.wait(1)
                editPage.ele('@id=title').input(title)
                editPage.wait(1)
                editPage.ele('xpath://*[@id="js_submit"]/button').click()

                print('[{}] 开始插入图片......'.format(nowTime()))
                imgNum = 3
                if len(imgList) > 0:
                    for img in imgList:
                        newpage = page.new_tab(img)
                        new_ac = Actions(newpage)
                        newpage.wait(1)
                        if newpage.url =='about:blank':
                            newpage.close()
                            continue
                        newpage.ele('tag:img').click()
                        newpage.wait(1)
                        new_ac.type(Keys.CTRL_C)
                        newpage.wait(1)
                        newpage.close()
                        newpage.wait(1)
                        lenProse = editPage.ele('tag:section')
                        if imgNum > len(lenProse.children()):
                            imgNum = len(lenProse.children())
                        editPage.wait(1)
                        lenProse.child(imgNum).click.at(0, 0)
                        editPage.wait(1)
                        editAc.key_down(Keys.HOME).key_up(Keys.HOME)
                        editPage.wait(1)
                        editAc.type(Keys.CTRL_V)
                        editPage.wait(1)
                        editAc.type(Keys.ENTER)
                        imgNum = imgNum + 2
                else:
                    pass
                editPage.ele('xpath://*[@id="js_submit"]/button').click()
                editPage.wait(3)
                editPage.close()
            except Exception:
                fileOperate(fileName=r'log.txt',fileType='a',readType='write')
                print('[{}] 写入失败，网络加载太慢'.format(nowTime()))

        elif publishType =='2':
            page.get('https://editor.mdnice.com/')
            login = page.ele('xpath:/html/body/div[2]/div/div[2]/div/div[2]/div')
            if login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                sys.exit()
            page.ele('xpath://*[@id="article-sidebar-container"]/div/div/div[2]/div/div/div/ul/li').click()
            page.wait(1)
            page.ele('xpath://*[@id="nice-md-editor"]/div/div[6]').click()
            page.wait(1)
            ac.type(Keys.CTRL_A)
            page.wait(1)
            ac.type(Keys.CTRL_V)
            page.wait(1)
            page.ele('xpath://*[@id="nice-sidebar-wechat"]').click()
            print('[{}] 百家号写入文章......'.format(nowTime()))
            page.get('https://baijiahao.baidu.com/')
            login = page.ele('xpath://*[@id="root"]/div/div/div[1]/div[2]/div[2]/div')
            if login:
                pyautogui.alert(text='请先登录，并且重新运行程序', title='警告', button='我知道了')
                sys.exit()
            page.ele('xpath://*[@id="layout-main-aside"]/div/aside/div/button').click()
            page.wait(1)
            nice = page.ele('@id=nice')
            if nice :
                nice.child(1).click()
            else:
                page.ele('xpath:/html/body/p').click()
            page.wait(1)
            ac.type(Keys.CTRL_A)
            page.wait(1)
            ac.type(Keys.CTRL_V)
            page.wait(1)
            page.ele('xpath://*[@id="newsTextArea"]/div/div/div/div/div/div/div[1]/div/div[1]/textarea').click()
            page.wait(1)
            ac.type(Keys.CTRL_A)
            page.wait(1)
            page.ele('xpath://*[@id="newsTextArea"]/div/div/div/div/div/div/div[1]/div/div[1]/textarea').input(title)
            page.wait(1)
            print('[{}] 开始插入图片......'.format(nowTime()))
            imgNum = 3
            if len(imgList) > 0:
                for img in imgList:
                    newpage = page.new_tab(img)
                    new_ac = Actions(newpage)
                    newpage.wait(1)
                    if newpage.url =='about:blank':
                        newpage.close()
                        continue
                    newpage.ele('tag:img').click()
                    newpage.wait(1)
                    new_ac.type(Keys.CTRL_C)
                    newpage.wait(1)
                    newpage.close()
                    newpage.wait(1)
                    lenProse = page.ele('@id=nice')
                    if imgNum > len(lenProse.children()):
                        imgNum = len(lenProse.children())
                    newpage.wait(1)
                    lenProse.child(imgNum).click.at(0, 0)
                    page.wait(1)
                    ac.key_down(Keys.HOME).key_up(Keys.HOME)
                    page.wait(1)
                    ac.type(Keys.CTRL_V)
                    imgNum = imgNum + 3
            page.wait(1)
            page.ele('xpath:/html/body/div[4]/div/div/div[2]/div/div/div[2]/span/div[4]/button').click()
            page.wait(3)
        if releaseType == '0':
            if publishType == '0':
                page.wait(1)
                page.ele('xpath://*[@id="root"]/div/div[1]/div/div[3]/div/button[3]/span').click()
                page.wait(2)
                page.ele('xpath://*[@id="root"]/div/div[1]/div/div[3]/div/button[2]/span').click()
                page.wait(3)

        page.wait(3)
        successNum += 1
        logStr = '[{}] 共成功 {} 条'.format(nowTime(), successNum)
        print(logStr)
        if articleType == '0':
            fileUrl = fileOperate(fileName=r'文章链接.txt', fileType='r', readType='read')
            delUrl = fileUrl.replace(url, '')
            fileOperate(fileName=r'文章链接.txt', fileType='w', readType='write', msg=delUrl)
pyautogui.alert(text='程序运行完毕，一共洗稿 {} 条'.format(successNum), title='警告', button='我知道了')