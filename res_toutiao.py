import requests
import datetime
import time
import pandas as pd
import tkinter as tk

root = tk.Tk()
root.title('采集数据')
root.geometry('500x500+300+300')

radio_data = [
    ('推荐',1),
    ('体育',2),
    ('军事',3),
    ('历史',4),
    ('国际',5),
    ('娱乐',6),
    ('热点',7),
    ('科技',8),
    ('财经',9),
]


def get_radio_value():
    selected  = radio_data[int(v.get())-1][0]
    return selected


v = tk.StringVar()
v.set('1')
for girl, num in radio_data:
    b = tk.Radiobutton(root, text=girl, variable=v, value=num,command=get_radio_value)
    b.pack(anchor="w",side='left')


def toutiao(lable_value):
    lable = {
    '推荐':'https://www.toutiao.com/api/pc/list/feed?channel_id=0&min_behot_time=1723987285&offset=0&refresh_count=2&category=pc_profile_recommend&aid=24&app_name=toutiao_web&msToken=-jjglZrtC_AEHQdcskJlOcw80RMxtvbTd35El_rFfLYymRqKYg1XEkttPgyU6aWZMxX3Ptd-XZjZQqPXp9DV_NEtVCKwKUbZuTTiXMEAYLFaz1ZKvFpSrQ%3D%3D&a_bogus=DymqQRzXdDIk6D6p5A2LfY3qVf13Y8NX0t9bMDhqLx3vLg39HMT%2F9exESF7vI8SjN4%2FkIejjy4hbYpOgrQCnMZwf7Wsx%2F2CZs600t-P2sogS53iJeyUgrUwi-hsASeFQsv1IEQfkqwArFuRmWoFe-wc6PLZCcHhMHjDISpcG2Hj%3D',
    '体育':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398957&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=EX8MMQ0fDkfP6DW35A2LfY3qVWP3Y8E30t9bMDhqjn3v8639HMO-9exESNzvCvYjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLgloNe-wHvPjojx2f39gaH',
    '军事':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398960&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=m6RwBDLkdDgThVWp5A2LfY3qVlB3Y8E30t9bMDhqyd3vLy39HMYr9exESNzvIa8jN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLkl9Pe-wHvPjojx2f39gaU',
    '历史':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398965&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=Q6WZ%2F5hDDiDNhDWV5A2LfY3qV5B3Y8E30t9bMDhqwx3vD639HMT69exESNzvnUgjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLhlIPe-wHvPjojx2f39ga%2F',
    '国际':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398968&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=DX80MR0hdkdkgDy15A2LfY3qV113Y8E30t9bMDhqox3v-g39HMP09exESNzvTgEjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLgAore-wHvPjojx2f39gbX',
    '娱乐':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398972&max_behot_time=1723980179&offset=0&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=OwgYDaTVANL8bWfXjMJSWRM7w-2qdaexKTQYPuDI_dWRbpXeDjqyxhOoA1VRhmJh2MTybBCmQYG-rNLWN02ccXMOX11BSkrckgiqiuWiIUWetzqNKoB3KHWlAYnMbk8%3D&a_bogus=mvmMMRh6DiIpfD6V5A2LfY3qVI33YhLr0t9bMDhqCnfFRL39HMTI9exYSizvOzDjN4%2FkIe8jy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q528S53iJeyWmE0hO-ib3SFaM5XNAxc40y75azYT0W9xjmhO-PDIja3Lk96EtrNqL2o8j',
    '热点':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398996&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=dvW0%2FQ0kdidkfd625A2LfY3qVXe3Y8E30t9bMDhqDd3vH639HMYI9exESNzvh4WjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLZA9ae-wHvPjojx2f39gci',
    '科技':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398999&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=QymZB5zkdEITXfS15A2LfY3qVfe3Y8Eu0t9bMDhqzd3vUy39HMOu9exESEvvFnYjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLZlIPe-wHvPjojx2f39gGd',
    '财经':'https://www.toutiao.com/api/pc/list/feed?channel_id=3189399007&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22%3A%22filter%22%7D&aid=24&app_name=toutiao_web&msToken=uJ3NVpbHbZ9k9jOVNodUe7zPOKHrXy_GJ1itjwQckChkGAV0SNodVnMfp-4V4pXJWCV29x2Guz7CaLkp9JY8VZm9On2c-4RAaFuLowCn_Wxl-aFlvrhgPVaF1n-cmqk%3D&a_bogus=Q7RMQdufdifpvf6Z5A2LfY3qV4r3Y8Eu0t9bMDhq8x3vZg39HMOl9exESEvv7kbjN4%2FkIeLjy4hJT3PMx5VGA3vRHuDKUIcdmDSkKl5Q5xSSs1Xce6UgrUko-hsACFrQsv1lxOfkw7VbSYLgAore-wHvPjojx2f39gGf',
    }

    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'accept':'application/json, text/plain, */*',
    }

    article_list = {
                '标题':[],
                '链接':[],
                '作者':[],
                '发布时间':[],
                '阅读数':[],
                '评论数':[],
                '转发数':[],
            }
    for i in range(2):
        list = requests.get(url=lable[lable_value],headers=header)
        json_data =  list.json()
        data_list = json_data['data']
        for data in data_list:
            c_time = datetime.datetime.fromtimestamp(data['publish_time'])
            article_list['标题'].append(data['title'])
            article_list['链接'].append(data['url'])
            article_list['作者'].append(data['media_name'])
            article_list['发布时间'].append(c_time)
            article_list['阅读数'].append(data['read_count'])
            article_list['评论数'].append(data['comment_count'])
            article_list['转发数'].append(data['repin_count'])
        time.sleep(5)

    article_df =  pd.DataFrame.from_dict(article_list)
    article_df = article_df.drop_duplicates()
    article_df.to_excel(r'E:\虚拟机共享\文章采集\{}文章.xlsx'.format(lable_value))

button = tk.Button(root,text='采集',command=lambda :toutiao(get_radio_value()))
button.pack()

root.mainloop()