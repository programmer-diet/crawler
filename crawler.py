from bs4 import BeautifulSoup
import requests

def getSoup(url):
    html = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return html, soup

def crawler(keyword):
    foodInfos = []
    pageNum = 0
    done = False

    while (not done):
        url = 'https://mobile.fatsecret.kr/칼로리-영양소/search?q=' + keyword + '&pg=' + str(pageNum)
        _, soup = getSoup(url)
        food_list = soup.select('div.next-link')

        if (not food_list):
            done = True
            break
        
        for food in food_list:
            foodInfos.append({
                'name': food.a.text,
                'info': (' ').join(food.div.text.split())
            })

        pageNum += 1

    return foodInfos
    
# for test
datas = crawler('치킨')

with open('test.txt', 'w') as f:
    f.write(str(datas))
    f.write(str(len(datas)))

print('done')
