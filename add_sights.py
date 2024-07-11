import json
import requests
from date_validator import rating_validator
import datetime
from sqlite_req import main

datatime = datetime.datetime.now()
date = datatime.now().strftime("%d.%m.%Y") 

#main("DELETE FROM Sights;")

"""
add museums
"""
# with open("E:\DataTurismBot\museum_2gis.json", 'r', encoding='utf8') as json_museum:
#     try:
#         museum = json.load(json_museum)
#     except Exception as e:
#         print(e)

# for ms in museum:
#     try: 
#         name = f'{ms["org"]["name"].split(",")[0]}'
#         adress = f'{ms["point"]["lon"]},{ms["point"]["lat"]}'
#         url = f'{ms["contact_groups"][0]["contacts"][2]["text"]}' 
#         main_photo = f'{ms["external_content"][0]["main_photo_url"]}' 
#         rating = f'{rating_validator(int(ms["reviews"]["org_rating"]))}'
#     except Exception as e:
#         # print(e)
#         continue
    
#     main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{adress}', '{None}', '{None}', '{None}', '{name}\n{url}', '{None}', '{rating}', 'музей', '{date}', '806902493', 'ul_mus_img\\{name}.jpg')")
#     print(f"\nИмя: {name}\nАдрес: {adress}\nРейтинг: {rating}\nСсылка: {url}\nФото: ul_mus_img\\{name}.jpg\n") 

    

"""
add cinemas
"""
# with open("E:\DataTurismBot\cinema_2gis.json", 'r', encoding='utf-8-sig') as json_cinema:
#     try:
#         cinema = json.load(json_cinema)
#     except Exception as e:
#         print(e)
# for cn in cinema:
#     try:
#         name = f'{cn["org"]["name"].split(",")[0]}'
#         adress = f'{cn["point"]["lon"]},{cn["point"]["lat"]}'
#         url = f'{cn["contact_groups"][0]["contacts"][2]["value"]}'
#         main_photo = f'{cn["external_content"][0]["main_photo_url"]}'
#         rating = f'{rating_validator(int(cn["reviews"]["general_rating"]))}'
#         area = f'{cn["adm_div"][4]["name"].split()[0]}'
#     except Exception:
#         continue

#     main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{adress}', '{None}', '{None}', '{None}', '{name}\n{url}', '{None}', '{rating}', 'кинотеатр', '{date}', '806902493', 'ul_cin_img\\{name}.jpg')")
#     print(f"\nИмя: {name}\nАдрес: {adress}\nРейтинг: {rating}\nСсылка: {url}\nФото: ul_mus_img\\{name}.jpg\n") 


"""
add cafe
"""
# with open("E:\DataTurismBot\cafe_2gis.json", 'r', encoding='utf-8-sig') as json_cafe:
#     try:
#         cafe = json.load(json_cafe)
#     except Exception as e:
#         print(e)

# for cf in cafe:
#     try: 
#         name = f'{cf["org"]["name"].split(",")[0]}'
#         adress = f'{cf["point"]["lon"]},{cf["point"]["lat"]}'
#         url = f'{cf["contact_groups"][0]["contacts"][2]["text"]}' 
#         main_photo = f'{cf["external_content"][0]["main_photo_url"]}' 
#         rating = f'{rating_validator(int(cf["reviews"]["org_rating"]))}'
#         area = f'{cf["adm_div"][4]["name"].split()[0]}'
#     except Exception as e:
#         continue

#     r = requests.get(main_photo) 
#     with open(f"ul_cafe_img\\{name}.jpg", 'wb') as fd: 
#         for photo in r.iter_content():
#             fd.write(photo)

#     main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{adress}', '{None}', '{None}', '{None}', '{name}\n{url}', '{None}', '{rating}', 'кафе', '{date}', '806902493', 'ul_cafe_img\\{name}.jpg')")
#     print(f"\nРайон: {area}\nИмя: {name}\nАдрес: {adress}\nРейтинг: {rating}\nСсылка: {url}\nФото: ul_cafe_img\\{name}.jpg\n") 