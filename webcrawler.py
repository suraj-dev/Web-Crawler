import socket
import sys
import re
import sys

sys.setrecursionlimit(10000)

crawledLinks = []
linksCrawledCount = 0

def getRequestConstructor(address, csrfToken, serverSessionId):
    return '''GET ''' + address + ''' HTTP/1.1
Host: cs5700f16.ccs.neu.edu
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: WebCrawler/1.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://cs5700f16.ccs.neu.edu/accounts/login/?next=/fakebook/
Cookie: csrftoken=''' + csrfToken + '''; sessionid=''' + serverSessionId + '''

'''

def urlCollector(page, csrfToken, serverSessionId):
    htmlPage = str(page)
    statusCode = re.search('HTTP/1.1 (.+?) ', htmlPage).group(1)
    #print(statusCode)
    #print(htmlPage)
    secretFlag = re.search(r"<h2 class=\\'secret_flag\\' style=\"color:red\">FLAG: (.){64}</h2>", htmlPage)
    if secretFlag:
        print(secretFlag.group(0))

    if statusCode == '200':
        linkPattern = re.compile(r'[/]fakebook[/][0-9]+[/](friends)?[/]?[0-9]?[/]?')

        for link in linkPattern.finditer(htmlPage):
            if link.group(0) not in crawledLinks:
                crawledLinks.append(link.group(0))
                global linksCrawledCount
                linksCrawledCount = linksCrawledCount + 1
                #print(link.group(0))
                pageRequest = getRequestConstructor(link.group(0), csrfToken, serverSessionId)
                serverResponse = httpRequestHandler(bytes(pageRequest,'utf8'))
                #print(serverResponse)
                urlCollector(serverResponse, csrfToken, serverSessionId)


def httpRequestHandler(request):
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print('Failed to create socket.Error message : ' + msg[1])
        sys.exit()
    sc.connect(("cs5700f16.ccs.neu.edu", 80))
    sc.send(request)
    response = sc.recv(5000)
    sc.close()
    return response

def main():
    username = "001684864"
    password = "C2XW7QQ1"
    httpPostLogin = '''POST /accounts/login/ HTTP/1.1
Host: cs5700f16.ccs.neu.edu
Connection: keep-alive
Content-Length: 109
Cache-Control: max-age=0
Origin: http://cs5700f16.ccs.neu.edu
Upgrade-Insecure-Requests: 1
User-Agent: WebCrawler/1.0
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://cs5700f16.ccs.neu.edu/accounts/login/?next=/fakebook/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8
Cookie: _ga=GA1.2.1244877655.1453326659; csrftoken=8ac9d5bd2d6557822ca291719c91a82f; sessionid=3ee5e97d782123dc761053dd838910fd

username=001684864&password=C2XW7QQ1&csrfmiddlewaretoken=8ac9d5bd2d6557822ca291719c91a82f&next=%2Ffakebook%2F'''
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print('Failed to create socket.Error message : ' + msg[1])
        sys.exit()

    sc.connect(("cs5700f16.ccs.neu.edu", 80))
    sc.send(b'''GET /accounts/login/ HTTP/1.1
Host: cs5700f16.ccs.neu.edu
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8

''')
    serverResponse = sc.recv(5000)
    #print(serverResponse)
    text = str(serverResponse)
    csrftoken = re.search('csrftoken=(.+?);', text).group(1)
    clientSessionId = re.search('sessionid=(.+?);', text).group(1)
    #print(csrftoken)
    #print(clientSessionId)
    loginRequest = bytes('''POST /accounts/login/ HTTP/1.1
Host: cs5700f16.ccs.neu.edu
Connection: keep-alive
Content-Length: 109
Cache-Control: max-age=0
Origin: http://cs5700f16.ccs.neu.edu
Upgrade-Insecure-Requests: 1
User-Agent: WebCrawler/1.0
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://cs5700f16.ccs.neu.edu/accounts/login/?next=/fakebook/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8
Cookie: csrftoken=''' + csrftoken + '''; sessionid=''' + clientSessionId + '''

username=001684864&password=C2XW7QQ1&csrfmiddlewaretoken=''' + csrftoken + '''&next=%2Ffakebook%2F''', 'utf8')
    loginResponse = httpRequestHandler(loginRequest)
    #print(loginResponse)
    serverSessionId = re.search('sessionid=(.+?);', str(loginResponse)).group(1)
    #print(serverSessionId)
    homePageRequest = bytes('''GET /fakebook/ HTTP/1.1
Host: cs5700f16.ccs.neu.edu
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: WebCrawler/1.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://cs5700f16.ccs.neu.edu/accounts/login/?next=/fakebook/
Cookie: csrftoken=''' + csrftoken + '''; sessionid=''' + serverSessionId + '''

''', 'utf8')
    homePageResponse = httpRequestHandler(homePageRequest)
    #print(homePageResponse)
    crawledLinks.append('/fakebook/')
    urlCollector(homePageResponse, csrftoken, serverSessionId)
    print(linksCrawledCount)
main()

