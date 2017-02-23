import urllib.request
import urllib.parse
import os
from bs4 import BeautifulSoup
import pdb


def parser_html(html):
    soup = BeautifulSoup(html, 'html5lib')
    links = soup.find_all('link', attrs={'rel': 'stylesheet'})
    fileSet = set()
    for link in links:
        try:
            href = link['href']
            full_href = urllib.parse.urljoin(url, href)
            fileSet.add(full_href)
        except:
            pass

    jsFiles = soup.find_all('script')
    for jsFile in jsFiles:
        try:
            src = jsFile['src']
            full_src = urllib.parse.urljoin(url, src)
            fileSet.add(full_src)
        except:
            pass

    return fileSet


def craw_files(url):
    con = urllib.request.urlopen(url)
    if con.getcode() != 200:
        print('code', con.getcode())
        return None

    return con.read()


# 下载文件 先建文件夹 再 存文件
def create_dir(pathArr, file):
    # 过略掉不能下载的资源
    arr = file.split(url)
    if len(arr) < 2:
        print('skip file...',file)
        return None

    path_length = len(pathArr)
    dir = ROOT_DIR+"/"
    for i in range(path_length - 1):
        dir += pathArr[i]
        try:
            os.mkdir(dir)
        except:
            pass

        dir += '/'
    filename = dir + pathArr[path_length - 1]
    print('dowloding...', file, filename)
    urllib.request.urlretrieve(file, filename)

def download_file(fileSet):
    for file in fileSet:
        relative_path = file.replace(url, '')
        pathArr = relative_path.split('/')
        create_dir(pathArr, file)

if __name__ == '__main__':
    # download url
    url = "http://www.jq22.com/code/20170223152855.html"
    ROOT_DIR = urllib.parse.urlparse(url).netloc
    try:
        os.mkdir(ROOT_DIR)
    except:
        pass
    html = craw_files(url)
    fileSet = parser_html(html)
    download_file(fileSet)
    print('generating... index.html')
    urllib.request.urlretrieve(url, ROOT_DIR+'/index.html')
