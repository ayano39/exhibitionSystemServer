import json

def get_map():
    group1_1 = [{"boothId": 44, "theme": 3, "cell": [1, 2]},
                {"boothId": 45, "theme": 1, "cell": [3, 4]}]
    group1_2 = [{"boothId": 43, "theme": 1, "cell": [1]},
                {"boothId": 42, "theme": 5, "cell": [2]},
                {"boothId": 41, "theme": 6, "cell": [3, 4]}]
    group1_3 = [{"boothId": 25, "theme": 2, "cell": [1]},
                {"boothId": 24, "theme": 4, "cell": [2]},
                {"boothId": 26, "theme": 2, "cell": [3]},
                {"boothId": 27, "theme": 1, "cell": [4]}]
    group1_4 = [{"boothId": 22, "theme": 1, "cell": [1]},
                {"boothId": 21, "theme": 2, "cell": [2]},
                {"boothId": 23, "theme": 3, "cell": [3]},
                {"boothId": 20, "theme": 5, "cell": [4]}]
    group1_5 = [{"boothId": 8, "theme": 1, "cell": [1]},
                {"boothId": 7, "theme": 3, "cell": [2]},
                {"boothId": 9, "theme": 5, "cell": [3, 4]}]
    group1_6 = [{"boothId": 6, "theme": 4, "cell": [1, 2]},
                {"boothId": 5, "theme": 1, "cell": [3, 4]}]

    g_row1 = [{"group": group1_1, "x_pad": 0, "y_pad": 1},
              {"group": group1_2, "x_pad": 0, "y_pad": 1},
              {"group": group1_3, "x_pad": 1, "y_pad": 1},
              {"group": group1_4, "x_pad": 1, "y_pad": 0},
              {"group": group1_5, "x_pad": 1, "y_pad": 1},
              {"group": group1_6, "x_pad": 0, "y_pad": 1}]

    group2_1 = [{"boothId": -1, "theme": 7, "cell": [1, 2, 3, 4]}]
    group2_2 = [{"boothId": 40, "theme": 1, "cell": [1, 3]},
                {"boothId": 39, "theme": 5, "cell": [2]},
                {"boothId": 38, "theme": 4, "cell": [4]}]
    group2_3 = [{"boothId": 28, "theme": 3, "cell": [1, 2]},
                {"boothId": 30, "theme": 6, "cell": [3]},
                {"boothId": 29, "theme": 1, "cell": [4]}]
    group2_4 = [{"boothId": 19, "theme": 2, "cell": [1]},
                {"boothId": 18, "theme": 3, "cell": [2]},
                {"boothId": 17, "theme": 4, "cell": [3, 4]}]
    group2_5 = [{"boothId": 11, "theme": 1, "cell": [1, 3]},
                {"boothId": 10, "theme": 2, "cell": [2, 4]}]
    group2_6 = [{"boothId": 4, "theme": 2, "cell": [1]},
                {"boothId": 3, "theme": 1, "cell": [2]},
                {"boothId": 2, "theme": 5, "cell": [3, 4]}]

    g_row2 = [{"group": group2_1, "x_pad": 0, "y_pad": 0},
              {"group": group2_2, "x_pad": 1, "y_pad": 0},
              {"group": group2_3, "x_pad": 1, "y_pad": 1},
              {"group": group2_4, "x_pad": 1, "y_pad": 1},
              {"group": group2_5, "x_pad": 0, "y_pad": 0},
              {"group": group2_6, "x_pad": 0, "y_pad": 1}]

    group3_1 = [{"boothId": 46, "theme": 5, "cell": [1, 2, 3, 4]}]
    group3_2 = [{"boothId": 37, "theme": 2, "cell": [1]},
                {"boothId": 36, "theme": 4, "cell": [2]},
                {"boothId": 35, "theme": 5, "cell": [3]},
                {"boothId": 34, "theme": 1, "cell": [4]}]
    group3_3 = [{"boothId": 31, "theme": 3, "cell": [1]},
                {"boothId": 32, "theme": 2, "cell": [2]},
                {"boothId": 33, "theme": 6, "cell": [3, 4]}]
    group3_4 = [{"boothId": 16, "theme": 1, "cell": [1, 3]},
                {"boothId": 15, "theme": 3, "cell": [2, 4]}]
    group3_5 = [{"boothId": 13, "theme": 1, "cell": [1]},
                {"boothId": 12, "theme": 2, "cell": [2]},
                {"boothId": 14, "theme": 6, "cell": [3, 4]}]
    group3_6 = [{"boothId": 1, "theme": 3, "cell": [1, 2, 3, 4]}]

    g_row3 = [{"group": group3_1, "x_pad": 0, "y_pad": 0},
              {"group": group3_2, "x_pad": 0, "y_pad": 0},
              {"group": group3_3, "x_pad": 1, "y_pad": 1},
              {"group": group3_4, "x_pad": 0, "y_pad": 1},
              {"group": group3_5, "x_pad": 1, "y_pad": 1},
              {"group": group3_6, "x_pad": 0, "y_pad": 0}]

    map_array = [g_row1, g_row2, g_row3]
    # with open("booth.json", "w") as fout:
    # fout.write(json.dumps(map_array))
    return json.dumps(map_array)
