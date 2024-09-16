from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import Actions,Keys


golePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
co = ChromiumOptions().set_browser_path(golePath)
page = ChromiumPage(co)
ac = Actions(page)
page.set.window.max()

def getArticle(url):
    page.get(url)
    connect = page.ele('tag:article').text
    title = page.ele('@class=article-content').ele('tag:h1').text
    img = page.ele('tag:article').eles('tag:img')
    imgList = img.get.links()
    return connect,title,imgList

def aiRewrite(article):
    page.get('https://yiyan.baidu.com/')
    page.set.load_mode.normal()
    page.ele('.yc-editor-paragraph').input(article)
    ac.key_down(Keys.ENTER)  # 输入按键名称
    print('第一次等待显示重新生成')
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
    ac.key_down(Keys.ENTER)  # 输入按键名称
    print('等待复制显示')
    page.wait(5)
    page.wait.ele_hidden((page.ele('@id=sendBtn')).next(),timeout=1200)
    page.wait(5)
    page.ele('@id:chat-id-').eles('tag:span')[3].click()

url = 'https://www.toutiao.com/article/7414670664654717451/?log_from=3e4c730c1a9db_1726399786687'
article,title,imgList = getArticle(url)
print(title)
aiRewrite(article)
page.ele('@id:chat-id-').eles('tag:span')[3].click()

# article='''
# 文|朋朋说八卦编辑|朋朋说八卦动动手指，点个关注，好运财运接踵而来！点赞评论，财源广进！还记得几天前，那个在卫星云图上旋转着，像一颗不安分的蓝色纽扣一样的台风贝碧嘉吗？它一路走来，可谓是“命途多舛”，经历了生成、增强、“散架”、再到现在的“起死回生”，可谓是一波三折，牵动着无数人的心，而它最终的“落脚点”究竟在哪？又会带来怎样的风雨影响？今天，我们就来一起追踪贝碧嘉的最新动态图片来源于网络贝碧嘉，这个名字听起来温柔，却拥有着台风家族的强大基因，它在生成的最初几天，汲取着海洋的能量，迅速发展壮大，云系结构清晰，仿佛一位蓄势待发的舞者，在西太平洋上旋转起舞，就在大家以为它会一路向西，直奔我国东南沿海而来的时候，贝碧嘉却突然来了个“急刹车”，路径开始变得扑朔迷离起来原来，在贝碧嘉前进的道路上，出现了一股强大的干冷空气，就像一位武功高强的“拦路虎”，与贝碧嘉正面交锋，与此风切变也来“凑热闹”，对贝碧嘉进行“侧面攻击”，在这两种力量的夹击下，贝碧嘉的结构遭到破坏，强度迅速减弱，一度只剩下一个模糊的云团，仿佛失去了灵魂的舞者，在海上漫无目的地游荡图片来源于网络贝碧嘉的故事并没有就此结束，就在大家以为它会逐渐消散的时候，它却又一次展现出了惊人的“求生欲”，在有利的气象条件下，贝碧嘉抓住机会，重新整合能量，云系结构逐渐清晰，强度也开始缓慢回升，仿佛一位重拾信心的舞者，再次回到了舞台中央这一次，贝碧嘉的目标似乎更加明确，它一路向北，目标直指我国东南沿海，根据气象部门的最新预报，贝碧嘉将于9月15号前后在苏南到浙北一带登陆，这意味着，长三角地区将迎来一次明显的风雨考验图片来源于网络那么，贝碧嘉究竟会带来多大的风雨影响呢？根据气象部门的分析，贝碧嘉登陆时，强度可能达到台风或强台风级别，将给登陆地附近地区带来强风暴雨，届时，狂风怒吼，巨浪滔天，暴雨倾盆，仿佛一场大自然的“狂欢”对于长三角地区来说，这将是一场严峻的考验，城市内涝、山体滑坡、农作物受损等灾害都有可能发生，因此，相关部门和居民要提前做好防范措施，尽量减少损失图片来源于网络要密切关注气象部门发布的最新预警信息，及时了解台风的最新动态，做到心中有数，要做好防风加固工作，特别是住在低洼地带、危旧房屋的居民，要提前转移到安全地带，还要备好食物、水、手电筒等应急物资，以备不时之需我们也要保持冷静，不要过度恐慌，毕竟，台风也是自然现象的一种，我们无法阻止它的到来，但我们可以通过科学的防范措施，将损失降到最低图片来源于网络除了长三角地区，贝碧嘉还将给其他地区带来降雨影响，预计9月15号，内蒙古西南部、青海中东部、四川中部、浙江东南部、福建东部沿海、江西西部、广东中西部、广西东部和南部、台湾等地将出现中到大雨，其中浙江东南部、四川中部等地部分地区将出现暴雨9月15-16号，受台风影响，江浙沪地区降雨将增强，江苏南部、上海、浙江北部、安徽东南部将出现大到暴雨，长三角一带还可能出现大暴雨，并伴有8级以上大风，华南地区、云南、四川、甘肃中东部、宁夏、内蒙古中部也将出现中到大雨，四川中部、内蒙古部分地区可能出现暴雨图片来源于网络9月16号，河南、安徽、江苏中部等地雨势加大，普遍有中到大雨，安徽中南部、江苏西南部还有暴雨或大暴雨，另外，广西、云南、四川中南部、内蒙古中部一带也将出现中到大雨贝碧嘉的到来将给我国南方大部地区带来一次明显的降雨过程，部分地区雨势较大，需要警惕防范，而对于北方地区来说，虽然不会受到贝碧嘉的直接影响，但也要关注冷空气的活动，做好防寒保暖工作图片来源于网络天气变化无常，我们能做的就是及时关注气象信息，做好防范措施，保护好自己和家人的安全，也希望贝碧嘉能够“温柔”一些，将损失降到最低对于贝碧嘉的未来走向，你有什么看法？欢迎在评论区留言分享你的观点图片来源于网络本文传播正能量，无不良信息，如有侵权请联系删除。
# '''
page.get('http://www.wenpipi.com/sim')
page.ele('@id=content2').click()
ac.key_down(Keys.CTRL).type('v')
page.wait(2)
page.ele('@id=content1').input(article)
page.wait(2)
page.ele('@id=animation-container').click()
page.wait(2)

result = page.ele('xpath://*[@id="judgeDivId"]/font[2]/strong').text
print(result)
if result =='原创':
    print(result)
else:
    pass
page.get('https://mp.toutiao.com/profile_v4/manage/content/all?is_new_connect=0&is_new_user=0')
page.wait(2)
page.ele('@class=byte-menu-item').click()
page.wait(2)
page.ele('@class=ProseMirror').click()
ac.key_down(Keys.CTRL).type('v')
page.wait(2)
page.ele('@class=feedback-wrapper feedback-questions').click()
page.wait(2)
# title = '炸裂！沈阳一女子挑衅骚扰民警，指着生殖器:你那个多长给我看看'
page.ele('xpath://*[@id="root"]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div/div/div/textarea').input(title)

# imgList = ['https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/b6dda7f3fe544f15887c51944cadc957~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=FAqPSY9dFObfwUKKt7qt%2FJLkhW8%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/08bcf3ba4bdd4adba9d9870dd66a733d~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=xr9aoRi0Cq37VO5PiB629n2rVtU%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/f3762cd2e664434aa8474b260fc913ac~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=8yuxaUoXLmBzN8LMqCL0icvL5lc%3D', 'https://p26-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/f3762cd2e664434aa8474b260fc913ac~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=6jfa172ChEqryJi1BtGmq3xDjkY%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/9613da2c690e47b2a3cb0d71f7be6a92~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=MloS4Z51yk5Zr1ZOVYyvgXFlkns%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/9c9c893310f047b5bfc5d35dbda77ceb~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=G%2F5Srg5ZHAchdGndThNaFIpRdog%3D', 'https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/fed33658cedc47f1bc9a64eb8e20bd38~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1727009033&x-signature=ICUYy9cvhwzYPdl%2FEBIShsZ8gmI%3D']
NUM=3

for img in imgList:
    newpage = page.new_tab(img)
    newpage.wait(2)
    newpage.ele('tag:img').click()
    new_ac = Actions(newpage)
    new_ac.key_down(Keys.CTRL).type('c')
    newpage.wait(2)
    newpage.close()
    newpage.wait(2)
    page.ele('@class:ProseMirror').child(NUM).click.at(0,0)
    print(page.ele('@class:ProseMirror').child(NUM))
    ac.key_down(Keys.HOME)
    page.wait(2)
    ac.key_down(Keys.CTRL).type('v')
    newpage.wait(2)
    print(NUM)
    NUM = NUM + 3