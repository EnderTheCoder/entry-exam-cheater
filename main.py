import requests
from bs4 import BeautifulSoup  # 这里需要导入BeautifulSoup

cookie = {
    ".ASPXAUTH": "xxx",
    "CentersoftSSO": "xxx",
    "ASP.NET_SessionId": "xxx",
    "CenterSoft": "xxx"
}

with open("data.txt", 'a+') as f:
    for eid in range(90003, 90100):
        content = requests.get("https://xgxt.xjau.edu.cn/Sys/SystemForm/TestManage/LookTest.aspx?Eid=" + str(eid),
                               cookies=cookie).content
        bs = BeautifulSoup(content)
        count = 0
        j = 0
        k = 0
        choices = []
        for td in bs.find_all("td", {"bgcolor": "#FFFBEC"}, recursive=True):
            j += 1
            if j % 2 == 0:
                choices.append("")
                last_checked_flag = False
                for input_tag in td.children:
                    if last_checked_flag:
                        choices[int(j / 2 - 1)] += str(input_tag)
                        last_checked_flag = False
                    if input_tag.name is not None:
                        if str(input_tag).find("checked") != -1:
                            k += 1
                            last_checked_flag = True

        print(j)
        print(k)
        i = 0
        for tr in bs.find_all("td", {"style": "line-height:22px;letter-spacing: 1px;color:#444444;font-size:12px;"}):
            node_text = str(tr.text)

            json = {"question": "", "answer": ""}

            if node_text.find("【正确】") != -1:
                for header in tr:
                    header_str = str(header)
                    print(header_str[0:len(header_str) - 2])
                    json['question'] = header_str[0:len(header_str) - 2]
                    break
                f.write("\n")
                print(choices[i])
                json['answer'] = choices[i]
                f.write(str(json) + "\n")
                count += 1
            i += 1
        print(count)
