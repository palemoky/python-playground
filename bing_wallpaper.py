"""
[Python 中 Requests 模块的异常值处理](https://blog.csdn.net/Urbanears/article/details/79288972)
[pyexiv2 修改图片 exvif](https://blog.csdn.net/mihu_tutu/article/details/103238526)
"""

import requests
from urllib import parse

def req(url):
    r = requests.get(url)
    if 200 != r.status_code:
        raise requests.exceptions.HTTPError('Request failed, http code: ' + r.status_code)
    return r


def main():
    try:
        homepage = 'https://cn.bing.com'

        response = req(homepage + '/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1572500909531&pid=hp&FORM=BEHPTB&video=1').json()

        img_url = homepage + response['images'][0]['url']

        # 获取参数部分
        q = parse.urlsplit(response['images'][0]['url']).query

        # 解析参数，并将 list 转为 dict
        filename = dict(parse.parse_qsl(q))['id']

        # 将获取的图片保存
        with open(filename, 'wb') as file:
            file.write(req(img_url).content)
    except requests.exceptions.HTTPError as e:
        return e


if __name__ == '__main__':
    main()
