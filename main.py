import threading
import requests
import re
import os

path = 'image'
if not os.path.isdir(path):
    os.mkdir(path)

cookies = '***COOKIES***' #TODO:在這裡填入cookies
cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")} 

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71"
headers = {'user-agent': user_agent}

class toolbox:
    def download_image(url,file_path):
        print(f"download start : {file_path}")
        with open(file_path,'wb') as f:
            response = requests.get(url)
            f.write(response.content)
            print("download finish : "+file_path)
    
    def saved_file_name(file_name):
        return re.sub(r'[/\\:*?"<>|]*', '', file_name)

threads = []

def geturl(userid,start):

    global threads

    root = requests.get("https://www.pixiv.net/ajax/user/"+str(userid)+"/illusts/bookmarks?tag=&offset="+str(start)+"&limit=48&rest=show&lang=zh_tw",cookies=cookie,headers=headers)

    works = root.json()["body"]["works"]

    if not(works):
        return True

    for work in works:
        ImageName = toolbox.saved_file_name(work["title"])
        if work["pageCount"] > 1:
            for i in range(work["pageCount"]):
                threads.append(threading.Thread(target=toolbox.download_image, args=(
                    f'https://pixiv.cat/{str(work["id"])}-{str(i+1)}.jpg',
                    f"image/{ImageName}-{str(i)}.jpg"
                )))
        else:
            threads.append(threading.Thread(target=toolbox.download_image, args=(
                f'https://pixiv.cat/{str(work["id"])}.jpg',
                f"image/{ImageName}.jpg"
            )))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    threads = []

    return False

set = 0
while True:
    if geturl(67290483,set):
        break
    set+=48

print("下載完畢")