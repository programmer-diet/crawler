import requests, json
import crawler

DEBUG_MOD = True

URL = 'http://'
POST_CATEGORY = '/api/categories'
POST_BRAND = '/api/brands'
POST_FOOD = '/api/foods'
CATEGORY_BRANDS_LIST_FILE = './list.txt'

# raw_obj -> {'name': '치킨', 'info': '1 중간크기 조각당 - 칼로리: 249kcal | 지방: 14.85g | 탄수화물: 8.58g | 단백질: 19.19g'}
# Refine raw_obj to enum (name, details)
def food_refine(raw_obj):
    name = raw_obj['name']
    details = []    # [perweight, kcal, fat, carbohydrate, protein]
    details.append(raw_obj['info'].split(' - ')[0])
    for detail in raw_obj['info'].split(' - ')[1].split(' | '):
        details.append(detail.split(': ')[1].replace('kcal','').replace('g',''))

    return name, details

def remove_weight(perweight):
    weight = perweight
    if weight.find('(') > -1:
        weight = weight[weight.find('(')+1:weight.rfind(')')]
        weight = weight.replace('g','').replace('ml','')
        return float(weight)
    else: return -1

def get_unit(perweight):
    if perweight.find('g') > -1: return 1   # g
    elif perweight.find('ml') > -1: return 2   # ml
    else: return -1 # default

def get_category_id (category_name):

    # if not exists category
    url = URL + POST_CATEGORY
    data = { 'name': category_name }
    res = requests.post(url, json=data)

    # else
    # to be update

    if DEBUG_MOD:
        print('Post category \'' + category_name + '\'')

    return json.loads(res.text)['Id']

def get_brand_id (brand_name, category_id):

    # if not exists brand
    url = URL + POST_BRAND
    data = { 'name': brand_name, 'categoryid': category_id }
    res = requests.post(url, json=data)

    # else
    # to be update

    if DEBUG_MOD:
        print('Post brand \'' + brand_name + '\'')

    return json.loads(res.text)['Id']

def post_food (food_name, food_info, category_id, brand_id):
    url = URL + POST_FOOD

    # food_info -> ['perweight', 'calorie', 'fat', 'carbohydrate', 'protein']
    food_json = { 
        'categoryid': category_id,
        'brandid': brand_id,
        'name': food_name,
        'perweight': remove_weight(food_info[0]),
        'calorie': int(food_info[1]),
        'transfat': float(food_info[2]),       # Temporary fat -> transfat
        'carbohydrate': float(food_info[3]),
        'protein': float(food_info[4]),
        'unit': get_unit(food_info[0])
    }

    res = requests.post(url, json=food_json)

    if DEBUG_MOD:
        print('Post food ' + json.dumps(food_json))
    # return { 'result': 'fail', 'description': ''}

if __name__ == '__main__':
    with open(CATEGORY_BRANDS_LIST_FILE, 'r', encoding='utf8') as f:
        done = False
        while not done:
            data = f.readline().split()
            if data == []:
                done = True
                break

            category, brands = data[0], data[1:]

            category_id = get_category_id(category)
            for brand in brands:
                brand_id = get_brand_id(brand, category_id)
                brand_foods = crawler.crawler(brand)

                for food in brand_foods:
                    food_name, details = food_refine(food)
                    post_food(food_name, details, category_id, brand_id)
                    # To be update post_food fail exception -> logging
