# safety_study

电子科技大学实验室安全与环保知识网络教育及考试无人值守脚本（2022修改）

## 考试网址：
http://222.197.182.137/redir.php?catalog_id=131&object_id=55714

## 功能说明：
这个考试需要在线学习满两个小时，系统的判定方法是前端每分钟发送一次POST给后端，内容为"cmd=xuexi_online"，后端返回当前在线时间，内容为"{"status":1,"shichang":"2小时38分1秒"}"（中文使用utf-8编码）。

前端也有检测机制，每5分钟弹出一个alert窗口确认用户是否还在，如果不点击确认则暂停发送POST，但该逻辑并不影响脚本POST。

修改版脚本的工作原理：使用cookies跳过模拟登录，每分钟向后端发送一次POST请求，给学习时间+1分钟（大概是因为+1s 太暴力了）。因为学习时间由后端累计，所以**本脚本需连续运行至少两个小时**。

目前尚未发现后端有什么反作弊的措施。本人亦使用该脚本将自己的学习时长刷到了3小时以上。

## 开发环境：
1. 系统版本：Windows10 64-bit
2. Python版本：3.6.5 64-bit
3. requests库版本：2.19.1

## 使用方法：
```bash
$ python safety_study.py 
```
本脚本需要安装requests库和json库，使用pip命令安装：
```
# pip install requests 
# pip install json
```
