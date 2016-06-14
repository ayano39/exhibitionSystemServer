import json

def get_map():
    group1_1 = [{"boothId": 44, "cell": [1, 2]},
                {"boothId": 45, "cell": [3, 4]}]
    group1_2 = [{"boothId": 43, "cell": [1]},
                {"boothId": 42, "cell": [2]},
                {"boothId": 41, "cell": [3, 4]}]
    group1_3 = [{"boothId": 25, "cell": [1]},
                {"boothId": 24, "cell": [2]},
                {"boothId": 26, "cell": [3]},
                {"boothId": 27, "cell": [4]}]
    group1_4 = [{"boothId": 22, "cell": [1]},
                {"boothId": 21, "cell": [2]},
                {"boothId": 23, "cell": [3]},
                {"boothId": 20, "cell": [4]}]
    group1_5 = [{"boothId": 8, "cell": [1]},
                {"boothId": 7, "cell": [2]},
                {"boothId": 9, "cell": [3, 4]}]
    group1_6 = [{"boothId": 6, "cell": [1, 2]},
                {"boothId": 5, "cell": [3, 4]}]

    g_row1 = [{"group": group1_1, "x_pad": 0, "y_pad": 1},
              {"group": group1_2, "x_pad": 0, "y_pad": 1},
              {"group": group1_3, "x_pad": 1, "y_pad": 1},
              {"group": group1_4, "x_pad": 1, "y_pad": 0},
              {"group": group1_5, "x_pad": 1, "y_pad": 1},
              {"group": group1_6, "x_pad": 0, "y_pad": 1}]

    group2_1 = [{"boothId": -1, "cell": [1, 2, 3, 4]}]
    group2_2 = [{"boothId": 40, "cell": [1, 3]},
                {"boothId": 39, "cell": [2]},
                {"boothId": 38, "cell": [4]}]
    group2_3 = [{"boothId": 28, "cell": [1, 2]},
                {"boothId": 30, "cell": [3]},
                {"boothId": 29, "cell": [4]}]
    group2_4 = [{"boothId": 19, "cell": [1]},
                {"boothId": 18, "cell": [2]},
                {"boothId": 17, "cell": [3, 4]}]
    group2_5 = [{"boothId": 11, "cell": [1, 3]},
                {"boothId": 10, "cell": [2, 4]}]
    group2_6 = [{"boothId": 4, "cell": [1]},
                {"boothId": 3, "cell": [2]},
                {"boothId": 2, "cell": [3, 4]}]

    g_row2 = [{"group": group2_1, "x_pad": 0, "y_pad": 0},
              {"group": group2_2, "x_pad": 1, "y_pad": 0},
              {"group": group2_3, "x_pad": 1, "y_pad": 1},
              {"group": group2_4, "x_pad": 1, "y_pad": 1},
              {"group": group2_5, "x_pad": 0, "y_pad": 0},
              {"group": group2_6, "x_pad": 0, "y_pad": 1}]

    group3_1 = [{"boothId": 46, "cell": [1, 2, 3, 4]}]
    group3_2 = [{"boothId": 37, "cell": [1]},
                {"boothId": 36, "cell": [2]},
                {"boothId": 35, "cell": [3]},
                {"boothId": 34, "cell": [4]}]
    group3_3 = [{"boothId": 31, "cell": [1]},
                {"boothId": 32, "cell": [2]},
                {"boothId": 33, "cell": [3, 4]}]
    group3_4 = [{"boothId": 16, "cell": [1, 3]},
                {"boothId": 15, "cell": [2, 4]}]
    group3_5 = [{"boothId": 13, "cell": [1]},
                {"boothId": 12, "cell": [2]},
                {"boothId": 14, "cell": [3, 4]}]
    group3_6 = [{"boothId": 1, "cell": [1, 2, 3, 4]}]

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
