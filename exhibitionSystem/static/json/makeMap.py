import json

group1_1 = [{"boothId": 44, "cell": [1, 2]},
            {"boothId": 45, "cell": [3, 4]}]
group1_2 = [{"boothId": 43, "cell": [1]},
            {"boothId": 42, "cell": [2]},
            {"boothId": 41, "cell": [3, 4]}]
group1_3 = [{"boothId": 25, "cell": [1]},
            {"boothId": 24, "cell": [2]},
            {"boothId": 26, "cell": [3]},
            {"boothId": 27, "cell": [3]}]
g_row1 = [group1_1, group1_2, group1_3]
map_array = [{"name": "g_row1", "row": g_row1 }]
with open("booth.json", "w") as fout:
    fout.write(json.dumps(map_array))
