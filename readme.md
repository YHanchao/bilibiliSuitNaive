# BiliBili 装扮素材说明文档

## 实现方式

模拟Bilibili浏览装扮页面，根据网页响应JSON保存相应媒体资源。

使用API：

> https://api.bilibili.co/x/garb/internal/mall/suit/all

请求方式：GET

返回格式：JSON

> https://api.bilibili.com/x/garb/mall/item/suit/v2

请求方式：GET

请求头：

- "part": suit
- "item_id"

返回格式：JSON

---

## 运行方式

1. 使用Python脚本运行：请确保 Python 环境已安装`requests`及`Flask`，确保安装之后运行`main.py`即可
2. 使用二进制文件直接运行：双击`main.exe`运行即可。由于缺少编译环境故只编译了Windows版本，其他版本建议使用Python源文件直接运行

打开过后会自动打开一个浏览器页面。打不开也没关系，手动在浏览器地址栏输入

```http
http://localhost:1418/
```

也可使用。

## 使用说明

1. 程序支持简单的装扮资源搜索与获取，装扮资源主要保留了emoji、粉丝IP主页装扮、装扮其他素材三类。
2. 点击“获取”之后相应装扮素材保存在目录`src`中，其他缓存文件可以通过点击页面最下方的`清空缓存`以清理。
3. 页面上方的`刷新`将会重新获取当前所有装扮列表，初次运行时已经默认加载，相应文件保存在`suit_list.json`中
4. 程序运行中产生的意外问题记录保存在`error_log`文件中

## 已知问题

1. 使用代理进行访问时可能会出现无响应的情况

2. 部分素材由于包含非法字符无法以原名称保存

---

## 注意事项

1. 程序仅供学习参考，请在下载后 24 小时内删除
2. 请不要短时间内进行大量操作，否则可能有 IP 封禁等风险
3. 请不要将脚本及脚本产生内容用作商业用途
4. 程序未经标准测试，可能在运行中产生 bug，请不要使用奇怪的姿势试探 bug

## 致谢

程序编写时参考的项目列表

- [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

虽然该 API 集合中未找到程序所依赖的 API，但这一项目提供了本程序的最初构想。本程序所依赖的 API 通过 js 分析法得到。
