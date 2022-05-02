import requests
import json
import sqlite3
url = "https://www.breakingbadapi.com/api/characters"
res = requests.get(url)
# #დავალება N1
print(res)
print(res.headers['Content-Type'])
print(res.encoding)
print(res.headers)
print(res.text)
# #დავალება N2
json_data = res.json()
with open('bb_data.json', 'w') as file:
    json.dump(json_data, file, indent=4)
    file.close()
# დავალება N3-4
# ჩაშენებული ციკლით ვწვდებით სერიალის თითოეული პერსონაჟის
# მონაცემს-key_ს და value_ს(k, v) და ვარჩევთ იმ value_ს, რომელეთა key არის
# name ან  occupation ან status ან nickname.
# str_value გამოვიყენე, რათა მეორე მონაცემი (occupation) არის list და
# რადგან list_ს ბაზის ერთ სტრიქონში ვერ ჩავსვამთ,  string_ად გადავაკეთე
# და ბოლოს ეს მონაცემები ცარიელ ლისტში(data) ემატება.
data = []
str_value = None
for each in json_data:
    for k, v in each.items():
        if k == "name" or k == "occupation" or k == "status" or k == "nickname":
            str_value = str(v)
            data.append(str_value)
# data ლისტში არის string მონაცემები და ქვემოთ მოცემულ 2 ხაზში
# თითო პერსონაჟის მონაცემებს(4 მონაცემს) tuple_ებად ვყოფ და ლისტში ასე ვსვამ,
# რათა ბაზაში ერთიანად შევიტანო ყველა პერსონაჟის მონაცემი.
iterate = [iter(data)] * 4
list_of_tuples = list(zip(*iterate))


conn = sqlite3.connect("breaking_bad.sqlite")
cursor = conn.cursor()
cursor.execute(''' create table if not exists breaking_bad
            (full_name varchar(50),
            occupation varchar(150),
            status varchar(20),
            nickname varchar(20));''')
cursor.executemany("insert into breaking_bad(full_name, occupation, status,nickname) values (?,?,?,?)",
                   list_of_tuples)
conn.commit()
conn.close()
