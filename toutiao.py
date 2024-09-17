from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import Actions,Keys

page = ChromiumPage()
ac = Actions(page)
page.set.window.max()


def getArticleUrl(navItem,scrollNum =1):
    page.get('https://www.toutiao.com/')
    page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul').ele('text:{}'.format(navItem)).click()
    # page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[9]/div[2]/ul').ele('text:{}'.format(navItem)).click()
    page.wait(3)
    for i in range(scrollNum):
        page.scroll.to_bottom()
        page.wait(3)
    page.wait(3)
    articleCard  = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]').children()
    articleUrlList = []
    for i in range(len(articleCard)):
        url = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div[{}]/div/div/a'.format(i+1)).link
        articleUrlList.append(url)
        page.wait(1)
    print('自动获取文章完毕')
    return articleUrlList


def getArticle(url):
    page.get(url)
    connect = page.ele('tag:article').text
    title = page.ele('@class=article-content').ele('tag:h1').text
    img = page.ele('tag:article').eles('tag:img')
    imgList = img.get.links()
    print('获取文章完毕')
    return connect,title,imgList

def aiRewrite(article):
    page.get('https://yiyan.baidu.com/')
    page.set.load_mode.normal()
    page.ele('.yc-editor-paragraph').input(article)
    ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
    page.wait(5)
    page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=1200)
    page.wait(3)
    aiPromat = '''
    背景：我需要根据上述文章进行仿写，目标是保持原文的意思不变，同时确保事件过程生动精彩，结果客观真实。该任务要求将文章重新编写成具有原创性的新闻报道，避免被识别为AI创作。
    角色：希望你扮演一位资深新闻编辑，擅长用专业的新闻语言重新表达信息，确保逻辑清晰，层层递进，同时保持文章的原始意思。
    任务：根据提供的文章信息，重新撰写一篇新闻报道，要求前言引人注目，正文条理清晰，结语引发读者互动。确保文章原创度高，避免与原文相似度过高。
    要求：
    1. 文章文字数量不少于1800字，包括前言、正文和结语。
    2. 前言要引人注目，能够吸引读者的兴趣。
    3. 正文部分需要详细、有理有据地展开，逻辑清晰，层层递进。
    4. 结语部分要与读者互动，引发思考或讨论。
    5. 文章需保持原创度高，与原文相似度低于30%，避免被识别为AI创作。
    6. 润色文章，删除关联词如“首先/其次/最后、因为/所以/但是、同时/此外、然而”，使文章更自然流畅。
    7. 确保文章情感丰富，避免枯燥无味。
    '''
    page.ele('.yc-editor-paragraph').input(aiPromat)
    page.wait(3)
    ac.key_down(Keys.ENTER).key_up(Keys.ENTER)
    page.wait(5)
    page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=1200)
    page.wait(5)
    page.ele('@id:chat-id-').eles('tag:span')[3].click()
    print('洗稿完成')

def articleContrast(originalText):
    page.get('http://www.wenpipi.com/sim')
    page.wait(2)
    page.ele('@id=content2').click()
    ac.type(Keys.CTRL_V)
    page.wait(2)
    page.ele('@id=content1').input(originalText)
    page.wait(2)
    page.ele('@id=animation-container').click()
    page.wait(2)
    result = page.ele('xpath://*[@id="judgeDivId"]/font[2]/strong').text
    return result

articleUrlList = getArticleUrl(navItem='体育',scrollNum=1)
# url = 'https://www.toutiao.com/article/7414787250170446375/?log_from=443710d388bfc_1726463928376'
for url in articleUrlList:
    article,title,imgList = getArticle(url)
    aiRewrite(article)
    # page.ele('@id:chat-id-').eles('tag:span')[3].click()
    articleContrast(article)

    page.get('https://mp.toutiao.com/profile_v4/index')
    page.wait(2)
    page.ele('@class=byte-menu-item').click()
    page.wait(2)
    page.ele('@class=ProseMirror').click()
    ac.type(Keys.CTRL_V)
    page.wait(2)
    page.ele('@class=feedback-wrapper feedback-questions').click()
    page.wait(2)
    # title = '炸裂！沈阳一女子挑衅骚扰民警，指着生殖器:你那个多长给我看看'
    page.ele('xpath://*[@id="root"]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div/div/div/textarea').input(title)
    # imgList = ['https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/b6dda7f3fe544f15887c51944cadc957~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=FAqPSY9dFObfwUKKt7qt%2FJLkhW8%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/08bcf3ba4bdd4adba9d9870dd66a733d~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=xr9aoRi0Cq37VO5PiB629n2rVtU%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/f3762cd2e664434aa8474b260fc913ac~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=8yuxaUoXLmBzN8LMqCL0icvL5lc%3D', 'https://p26-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/f3762cd2e664434aa8474b260fc913ac~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=6jfa172ChEqryJi1BtGmq3xDjkY%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/9613da2c690e47b2a3cb0d71f7be6a92~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=MloS4Z51yk5Zr1ZOVYyvgXFlkns%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/9c9c893310f047b5bfc5d35dbda77ceb~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=G%2F5Srg5ZHAchdGndThNaFIpRdog%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/fed33658cedc47f1bc9a64eb8e20bd38~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=ICUYy9cvhwzYPdl%2FEBIShsZ8gmI%3D']
    imgNum=4
    for img in imgList:
        newpage = page.new_tab(img)
        newpage.wait(2)
        newpage.ele('tag:img').click()
        new_ac = Actions(newpage)
        new_ac.type(Keys.CTRL_C)
        newpage.wait(2)
        newpage.close()
        newpage.wait(2)
        if imgNum > len(page.ele('@class:ProseMirror').children()):
            imgNum = len(page.ele('@class:ProseMirror').children())
        page.ele('@class:ProseMirror').child(imgNum).click.at(0,0)
        # print(page.ele('@class:ProseMirror').child(NUM))
        # page.wait(2)
        ac.key_down(Keys.HOME).key_up(Keys.HOME)
        page.wait(2)
        ac.type(Keys.CTRL_V)
        page.wait(2)
        # print(NUM)
        imgNum = imgNum + 3