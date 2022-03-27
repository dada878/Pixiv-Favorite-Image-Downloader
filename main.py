import requests
import re

#cookie處理
cookies = 'first_visit_datetime_pc=2022-03-26+12%3A34%3A21; p_ab_id=5; p_ab_id_2=3; p_ab_d_id=280327097; yuid_b=UQmVIoA; _gcl_au=1.1.1402934168.1648265663; PHPSESSID=67290483_1DBMKol0PDlXK53ZsqLFDH3J3ZoXDcym; device_token=02b6ea47e54f14a89bf0eaff95a63199; c_type=99; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; __cf_bm=buW7hu72cF0EdDIu5BgEkUW361Hd6DMP.uTFGZkTlV4-1648382204-0-AZFy3CL4NNfi/v3CUYQy/tHmIDaSZbnfTwdkVOQFawPJV+Jd5dE/Er6g6wXZhg/VMtdqQiQ+U2SSEtt32IjRwHJrmDOziiYkn9ZApz5VlvqSbG8CTc6KuLh96oRJ2ryyQlwdUDuhLg0toVF2lZ4w3INbhNrNI6NsCG169M8pRphADQpwO1YXqjvI6XG5JUkKzQ==; tag_view_ranking=0xsDLqCEW6~_EOd7bsGyl~r01unnQL0a~11kS06gAX8~yHh3msZCuv~Ie2c51_4Sp~fb6PpXmETl~q7MQz1NdYA~Lt-oEicbBr~5oPIfUbtd6~DADQycFGB0~Bd2L9ZBE8q~_hSAdpN9rx~u8McsBs7WV~jk9IzfjZ6n~Bcdk6oWmUE~engSCj5XFq~_3oeEue7S7~NzsShxkKo0~T0MnZNtAk3~srKLKqXYuP~40FmdeOiB3~XlINpTQfL-~CbhyJ8r4Mo~emBeiFN8Zl~txZ9z5ByU7~CrFcrMFJzz~0Sds1vVNKR~MnGbHeuS94~jk05zxCumb~RTJMXD26Ak~dps-4XMi57~q303ip6Ui5~UnI8eZzpBM~KrMg4c4zFf~HY55MqmzzQ~B_OtVkMSZT~C1gSQiPu1R~kovglUgBN2~4h0o0dAXfL~ETjPkL0e6r~HBlflqJjBZ~-B0wgi3Odg~lRxin4V3-v~Txs9grkeRc~cNur-S0G6f~bVIRv95aZ5~28gdfFXlY7~aKhT3n4RHZ~v5g4rgVYZq~m2vWDkcGhb~ox9m8zoGwy~0JqkVYdbcR~JgRWi06-Dy~H8PnvH8xAE~nTvmI69Dgp~0GU4k-mic3~jEoxuA2PIS~27XlejXJsP~l5WYRzHH5-~8JMhJ971hb~AI_aJCDFn0~GNcgbuT3T-~3gc3uGrU1V~5EOES-gQLS~AntZi-aWy_~51-IKFATYd~_vCZ2RLsY2~iVTmZJMGJj~zyKU3Q5L4C~ftZLeIHm13~I-ST5EF_lI~wOoq4sXjoA~Hvc3ekMyyh~_bee-JX46i~aLBjcKpvWL~SESsD0AjlF~-o--a5rIBR~9HraoGBekC~C51QU99RgX~EGnDNbuIp8~8p7FrLtVHU~aMSPvw-ONW~ssIwL3o3l4~9o8i_bXtl_~_gHluYoV0r~SxmI-ep6z3~AQizdn3Zp7~c15D8Cg2xk~th6yticcgo~oWPAcFYBPl~D7T5DZdXh1~VzfKuwHIlz~koy1qR49Et~6sKo849Id3~nVdh5tLRD4~S-UxNeWJhs~ITVapWvXyh~EttOqqgGxI~W4_X_Af3yY; QSI_S_ZN_5hF4My7Ad6VNNAi=r:10:16'
cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")} 

#header處理
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71"
headers = {'user-agent': user_agent}

class toolbox:
    def download_image(url,file_path):
        with open(file_path,'wb') as f:
            response = requests.get(url)
            f.write(response.content)
            print("download finish : "+file_path)
    
    def saved_file_name(file_name):
        return re.sub(r'[/\\:*?"<>|]*', '', file_name)

#連結網頁
def geturl(userid,start):
    root = requests.get("https://www.pixiv.net/ajax/user/"+str(userid)+"/illusts/bookmarks?tag=&offset="+str(start)+"&limit=48&rest=show&lang=zh_tw",cookies=cookie,headers=headers)

    works = root.json()["body"]["works"]

    if not(works):
        return True

    for work in works:
        ImageName = toolbox.saved_file_name(work["title"])
        if work["pageCount"] > 1:
            for i in range(work["pageCount"]):
                toolbox.download_image(
                    f'https://pixiv.cat/{str(work["id"])}-{str(i+1)}.jpg',
                    f"image/{ImageName}.png"
                )
        else:
            toolbox.download_image(
                f'https://pixiv.cat/{str(work["id"])}.jpg',
                f"image/{ImageName}.png"
            )

    return False

set = 0
while True:
    if geturl(67290483,set):
        break
    set+=48

print("下載完畢")