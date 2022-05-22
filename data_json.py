import json


def Json_data_create(data_list):
    with open("data.json", "w") as file:
        json.dump(data_list, file, indent=1, ensure_ascii=False)