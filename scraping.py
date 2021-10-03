import sys
import time
import re
import requests
import bs4

from bs4 import BeautifulSoup

class Syosetsu:
    def __init__(self, title, lines):
        self.title = title
        self.lines = lines

id = sys.argv[1]
# id = 'n1850ew'

try:
    page = 1
    while True:

        #1ページ分リクエスト
        load_url = f"https://ncode.syosetu.com/{id}/{page}/"
        print(load_url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        html = requests.get(load_url, headers=headers)

        if html.status_code != 200:
            break

        soup = BeautifulSoup(html.content, "html.parser")

        #話のタイトル抜き出し
        title = soup.find(class_="novel_subtitle")
        if title is None:
            continue
        
        #本文抜き出し
        honbun = soup.find(id="novel_honbun")
        if honbun is None:
            continue
        
        lines = []
        for line in honbun.find_all(id=re.compile("^L")):
            try:
                #１行分のテキスト
                linecontenttext = ''
                
                #行ごとにルビなどの要素が含まれるため、for分で回しながら１行分のテキストを作成
                for linecontent in line.contents:

                    #改行は無視
                    if linecontent.name == 'br':
                        continue

                    # ルビの部分は破棄, 内容のみ取得
                    if linecontent.name == 'ruby':
                        linecontenttext += linecontent.contents[0].contents[0]
                        continue

                    if type(linecontent) is not bs4.element.NavigableString:
                        continue

                    #通常行
                    linecontenttext += linecontent
            except:
                print('スキップ')
                pass
            
            #１行分として追加
            lines.append(linecontenttext)

        #１話分として追加
        with open(f'./{id}.txt', mode='a') as f:
            f.write(f'【{title.contents[0]}】')
            f.write('\r\n')
            for l in lines:
                try:
                    f.write(l)
                    f.write('\n')
                except:
                    pass
        page += 1

        #サーバ負荷対策
        time.sleep(0.5)

except Exception as e:
    print(e)