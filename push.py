import requests
import crawler

# { 
# "categoryid": 1,
# "brandid": 1,
# "name": "test",
# "perweight": 60,
# "carbohydrate": 33,
# "protein": 22,
# "transfat": 11,
# "calorie": 33
# }

# 네네치킨
# 교촌치킨
# 굽네치킨
# 멕시카나
# 페리카나
# 비비큐
# 호식이두마리치킨
# BHC

# sample
data = {'name': '치킨', 'info': '1 중간크기 조각당 - 칼로리: 249kcal | 지방: 14.85g | 탄수화물: 8.58g | 단백질: 19.19g'}

refine = {'categoryid': 3, "brandid": 0}

# not exists fat field
seq = ['name', 'perweight', 'calorie', 'fat', 'carbohydrate', 'protein']
result = [] # 

result.append(data['name'])
result.append(data['info'].split(' - ')[0])
for detail in data['info'].split(' - ')[1].split(' | '):
    result.append(detail.split(': ')[1])

# print(result)
# Need to RemoveSuffix (g, kcal) & Set unit

if len(seq) == len(result):
    for index in range(len(result)):
        refine[seq[index]] = result[index]

else:
    print(result)

print("done")
print(refine)