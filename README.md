
Proxy for Sqlmap by Spider
=======
Spider是用的ProxyPool这个项目
使用方式在这里：https://github.com/jhao104/proxy_pool

    ______                        ______             _
    | ___ \_                      | ___ \           | |
    | |_/ / \__ __   __  _ __   _ | |_/ /___   ___  | |
    |  __/|  _// _ \ \ \/ /| | | ||  __// _ \ / _ \ | |
    | |   | | | (_) | >  < \ |_| || |  | (_) | (_) || |___
    \_|   |_|  \___/ /_/\_\ \__  |\_|   \___/ \___/ \_____\
                           __ / /
                          /___ /


### 这里的代码就很简单了，使用上面的API随机获取代理，然后绑定到127.0.0.1:9998

* 首先下载源码

```shell
git clone git@github.com:SQQS123/proxy_for_sqlmap.git

```

* 安装依赖:

```shell
这个文件没几行，打开看着安装依赖就行，重点是那上面的爬虫运行起来，一切都好说了

```

* 启动:

```shell
python3 proxy_for_sqlmap.py

```

* sqlmap使用这个代理
```shell
Linux下有的可以直接用sqlmap，或者直接用sqlmap.py
sqlmap -u "url" --proxy=http://127.0.0.1:9998

Windows下可以
python sqlmap.py -u "url" --proxy=http://127.0.0.1:9998
```