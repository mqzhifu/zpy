import random
import urllib.request

comm_ua_list = {
    "pc":[
        #火狐
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",

        #Opera
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",

        #Safari
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",

        #Chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",

        #360
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",

        #淘宝
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    ],
    "mobile":[
        #Safari
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    ]
    ,
}

def get_common_header():
    headers = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        # "referer": "https://hjd2048.com/2048/thread.php?fid-13-page-1.html",
        #           "accept-encoding": "gzip, deflate, br",
    # "accept-language": "zh-CN,zh;q=0.9",
    # "cache-control": "max-age=0",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": "macOS",
    #    "sec-fetch-dest": "document",
    #    "sec-fetch-mode": "navigate",
    #                                "sec-fetch-site": "none",
    #                                "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    #
    #     "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    #
    #     "cookie":"zh_choose=n; a22e7_threadlog=,4,13,; a22e7_lastpos=F13; a22e7_ol_offset=257147; a22e7_lastvisit=1024	1652070198	/2048/thread.php?fid-13-page-1.html",
        # "User-Agent":  get_rand_one_ua("pc"),
        #           "accept-encoding": "gzip, deflate, br",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "referer":"https://er23w1232.xyz/",
        # "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7",
    }
    return headers

def get_rand_one_ua (category):
    list = comm_ua_list[category]
    max = len(list)
    r = random.randint(0,max)

    return list[r]

def save_content_to_file(filePath,fileName,content):
    fullPath = filePath + fileName
    with open(fullPath,"w",encoding="utf-8")as fp:
        fp.write(content)

def get_proxe():
    ProxyList = {
        "socks5":"127.0.0.1:10010",
    }
    proxy_handler =  urllib.request.ProxyHandler(ProxyList)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    # opener.open(url)
