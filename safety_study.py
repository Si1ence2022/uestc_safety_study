# -*- coding: UTF-8 -*-
import time
import json
import requests

'''
名称：安全教育学习无人值守脚本（2022.12.1之前仍能正常使用）

作者：bufbrane && Silence

开发环境：
    系统版本：Windows10 64-bit
    Python版本：3.9.1 64-bit
    requests库版本：2.28.1


注意事项：

1. 在电子科技大学2015级本科生前辈的脚本（https://github.com/bufbrane/safety_study.git）基础上修改，由于之前模拟登录函数（ExamLogin）除了只能通过账号信息获取cookie，现在实验室安全教育考试系统
添加了验证码验证，较难实现模拟登录，故直接使用cookie的方式发送post请求
2. 本脚本需要安装requests库和json库，使用pip命令安装：
# pip install requests 
# pip install json

3. 此学习网站需要客户端每分钟发送一次学习数据，因此本脚本必须保持运行直至时间刷满2小时。
PS.必须保证运行满2个小时，尚无改进方法（毕竟前端调用无力改变后端的脑残设定）

'''

# hostIP为 https://labsafetest.uestc.edu.cn/ 的ip地址
hostIP = "http://222.197.182.137"
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
accept = "*/*"


# 定时发送POST签到（60秒一次）
# ！！！注意： headers 在未来可能需要调整
class TimingPost(object):
    def __init__(self, cookies={}, uestc_id=""):
        self.uestc_id = uestc_id
        self.cookies = cookies
        self.endpoint = r"/exam_xuexi_online.php"
        self.url = "".join([hostIP, self.endpoint])
        self.headers = \
            {
                "Accept": accept,
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Length": "16",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "DNT": "1",
                "Host": "222.197.182.137",
                "Origin": hostIP,
                "Referer": hostIP + "/redir.php?catalog_id=121&object_id=2737",
                "sec-ch-ua": "Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": UserAgent,
                "X-Requested-With": "XMLHttpRequest"
            }
        self.data = "cmd=xuexi_online"

    def get_page(self):
        # print(self.url)
        # print(self.headers)
        # print(self.cookies)
        # print(self.data)
        r = requests.post(url=self.url, headers=self.headers, cookies=self.cookies, data=self.data)
        print("status_code: "+str(r.status_code))
        # print(r.raise_for_status())
        # print("None表示没异常")
        r.raise_for_status()
        jtext = json.loads(r.text)
        print("学号：", self.uestc_id, "学习时间：", jtext['shichang'])


def main():
    # 注意修改 cookie 内容！！！
    # 其实 uestc_id 可以不用填，post 请求时没用到，写上是因为后续循环打印时能知道是哪个账号罢了
    # 获取登录后的cookies
    cookies = {}
    cookies['iPlanetDirectoryPro'] = "xxxxxxxxxxxxxx"
    cookies['wsess'] = "XX-1111111-xxxxxxxxxxxxxxxx-xxxx-xxx"
    # print(type(cookies))
    uestc_id = input("请输入学号: ")
    # 提示信息
    print("本脚本每分钟会向系统注册一次，请务必保持本脚本一直运行！")

    # 每分钟POST一次学习动态（稳妥起见至少运行125分钟）
    for i in range(120):
        print("第 " + str(i+1) + " 轮")
        TimingPost(cookies, str(uestc_id)).get_page()
        time.sleep(60)  # 这里是阻塞调用。愚以为没有必要在此使用非阻塞，毕竟后端计时不是并发的，有些事急不得
    print("恭喜！俩小时结束了")


if __name__ == '__main__':
    main()