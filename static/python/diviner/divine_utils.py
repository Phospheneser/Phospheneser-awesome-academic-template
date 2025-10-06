import time
import random
import json

import hashlib
import datetime
import random


def get_seed_from_query(query: str, granularity="day") -> int:
    now = datetime.datetime.now()
    if granularity == "day":
        time_key = now.strftime("%Y-%m-%d")
    elif granularity == "hour":
        time_key = now.strftime("%Y-%m-%d-%H")
    elif granularity == "minute":
        time_key = now.strftime("%Y-%m-%d-%H-%M")
    else:
        time_key = now.isoformat()
    seed_str = f"{query}-{time_key}"
    return int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)


def with_seed(func):
    def wrapper(query, *args, **kwargs):
        seed = get_seed_from_query(query)
        random.seed(seed)
        return func(query, *args, **kwargs)

    return wrapper


@with_seed
def JiuGongLiuRen(query, Divintype="time", need_return=False, need_print=True):
    month, day, hour = time.strftime("%m %d %H").split()
    if Divintype == "time":
        n1, n2, n3 = int(month), int(day), int(int(hour) / 2)
    elif Divintype == "random":
        n1 = random.randint(1, 12)
        n2 = random.randint(1, 31)
        n3 = random.randint(1, 12)
    else:
        raise NotImplementedError("type must be 'time' or 'random'")

    elements = [
        "大安（震）（木）：平安吉祥，诸事顺遂",
        "留连（坎）（水）：事情拖延，难以决断",
        "速喜（离）（火）：喜事临门，好消息快来",
        "赤口（兑）（金）：口舌是非，易生争执",
        "小吉（巽）（木）：小有收获，平稳略好",
        "空亡（震）（木）：虚无缥缈，难有结果",
        "病符（坤）（土）：不适不顺，多有不便",
        "桃花（艮）（土）：姻缘桃花，人际和谐",
        "天德（乾）（金）：吉祥如意，贵人相助",
    ]

    # 从"大安"开始，获取对应的元素
    first_index = (n1 - 1) % len(elements)
    second_index = (n1 + n2 - 2) % len(elements)
    third_index = (n1 + n2 + n3 - 3) % len(elements)
    if need_print:
        print("对于你的问题：【" + query + "】  得到的卦象是")
        print(
            "【"
            + elements[first_index]
            + "】->【"
            + elements[second_index]
            + "】->【"
            + elements[third_index]
            + "】"
        )

    if need_return:
        return elements[first_index], elements[second_index], elements[third_index]
    else:
        return


def random_get_liu_yao(Divintype="three_coin"):
    yaoNameList = ["老阴", "阳", "阴", "老阳"]
    if Divintype == "total_random":
        yaoListGot = []
        for i in range(6):
            yaoListGot.append(random.choice(yaoNameList))
        return yaoListGot
    elif Divintype == "three_coin":
        yaoListGot = []
        for i in range(6):
            coin1 = random.randint(0, 1)
            coin2 = random.randint(0, 1)
            coin3 = random.randint(0, 1)
            yaoListGot.append(yaoNameList[coin1 + coin2 + coin3])
        return yaoListGot
    else:
        raise NotImplementedError("type must be 'total_random' or 'three_coin'")


@with_seed
def getGuaYaoCiFromYaoListGot(yaoListGot):
    guaMapping = {
        "阳阳阳": "天",
        "阳阳阴": "泽",
        "阳阴阳": "火",
        "阴阳阳": "风",
        "阳阴阴": "雷",
        "阴阳阴": "水",
        "阴阴阳": "山",
        "阴阴阴": "地",
    }
    fanguaMapping = {
        "天": "地",
        "地": "天",
        "泽": "山",
        "山": "泽",
        "火": "水",
        "水": "火",
        "风": "雷",
        "雷": "风",
    }
    yaoPrefix = ["初", "二", "三", "四", "五", "上"]
    dongyaoIndexList = []
    jingyaoIndexList = []

    for index, yao in enumerate(yaoListGot):
        if yao[0] == "老":
            dongyaoIndexList.append(index)
        else:
            jingyaoIndexList.append(index)
    jiyaoCount = len(dongyaoIndexList)

    gua1 = yaoListGot[0][-1] + yaoListGot[1][-1] + yaoListGot[2][-1]
    gua2 = yaoListGot[3][-1] + yaoListGot[4][-1] + yaoListGot[5][-1]
    guaName = guaMapping[gua2] + guaMapping[gua1] + "卦"
    ciName = ""
    if jiyaoCount == 0:
        ciName = "卦辞"
    elif jiyaoCount == 1:
        ciName = yaoPrefix[dongyaoIndexList[0]] + "爻"
    elif jiyaoCount == 2:
        if yaoListGot[dongyaoIndexList[0]][1] == yaoListGot[dongyaoIndexList[1]][1]:
            ciName = yaoPrefix[dongyaoIndexList[1]] + "爻"
        else:
            ciName = (
                yaoPrefix[
                    (
                        dongyaoIndexList[0]
                        if yaoListGot[dongyaoIndexList[0]][1] == "阴"
                        else dongyaoIndexList[1]
                    )
                ]
                + "爻"
            )
    elif jiyaoCount == 3:
        ciName = yaoPrefix[dongyaoIndexList[1]] + "爻"
    elif jiyaoCount == 4:
        ciName = yaoPrefix[jingyaoIndexList[0]] + "爻"
    elif jiyaoCount == 5:
        ciName = yaoPrefix[jingyaoIndexList[0]] + "爻"
    elif jiyaoCount == 6:
        guaName = fanguaMapping[guaName[0]] + fanguaMapping[guaName[1]] + "卦"
        if guaName == "地地卦":
            ciName = "用六"
        if guaName == "天天卦":
            ciName = "用九"
        else:
            ciName = "卦辞"
    return guaName, ciName


@with_seed
def LiuYaoQiGua(query, Divintype="three_coin", need_return=False, need_print=True):
    yaoListGot = []
    attriGuanemMapping = {
        "天": "乾",
        "地": "坤",
        "泽": "兑",
        "山": "艮",
        "火": "离",
        "水": "坎",
        "风": "巽",
        "雷": "震",
    }
    with open("./info/64卦.json", "r") as f:
        guaciInfo = json.load(f)
    # print(guaciInfo.keys())
    yaoListGot = random_get_liu_yao(Divintype)
    guaName, ciName = getGuaYaoCiFromYaoListGot(yaoListGot)
    guakey = (
        attriGuanemMapping[guaName[0]] + "上" + attriGuanemMapping[guaName[1]] + "下"
    )
    if need_print:
        print("对于你的问题：【" + query + "】")
        print("卜卦结果如下")
        reversedyaoList = yaoListGot[::-1]
        for yao in reversedyaoList:
            if yao == "老阳":
                print("---------- o")
            if yao == "老阴":
                print("----  ---- x")
            if yao == "阳":
                print("----------")
            if yao == "阴":
                print("----  ----")
        print(
            "得到的是【"
            + guaciInfo[guakey]["卦名"].split("(")[0]
            + "("
            + guaciInfo[guakey]["卦名直解"]
            + ")】"
        )
        if ciName != "卦辞":
            print(
                ciName
                + "爻变，爻辞为：【"
                + guaciInfo[guakey][ciName]["原文"][0]
                + guaciInfo[guakey][ciName]["原文"][1]
                + "】\n解释为：【"
                + guaciInfo[guakey][ciName]["解释"][0]
                + guaciInfo[guakey][ciName]["解释"][1]
                + "】"
            )
            print("吉凶：【" + guaciInfo[guakey][ciName]["吉凶/性质"] + "】")
        else:
            print(
                "卦辞为：【"
                + guaciInfo[guakey]["卦辞"]["原文"][0]
                + guaciInfo[guakey]["卦辞"]["原文"][1]
                + "】\n解释为："
                + guaciInfo[guakey]["卦辞"]["解释"][0]
                + guaciInfo[guakey]["卦辞"]["解释"][1]
                + "】"
            )
            print("性质是：【" + guaciInfo[guakey]["卦辞"]["吉凶/性质"] + "】")
    if need_return:
        return guaName, ciName, guakey, guaciInfo[guakey], yaoListGot
    else:
        return


@with_seed
def Tarot(
    query, Divintype="three_card", need_return=False, need_print=True, useRNR=False
):
    with open("./info/MergedTarot.json", "r") as f:
        tarotInfo = json.load(f)
    card_mean = []
    if Divintype == "three_card":
        card_num = 3
        card_mean = ["卡1", "卡2", "卡3"]
    elif Divintype == "four_card":
        card_num = 4
        card_mean = ["卡1", "卡2", "卡3", "卡4"]
    elif Divintype == "five_card":
        card_num = 5
        card_mean = ["卡1", "卡2", "卡3", "卡4", "卡5"]
    elif Divintype == "three_card_time_line":
        card_num = 3
        card_mean = ["过去", "现在", "未来"]
    else:
        raise NotImplementedError("unknown divination type")

    selected_cards = random.sample(list(tarotInfo.keys()), card_num)
    RNRList = []
    for i in range(card_num):
        if useRNR:
            RNRList.append(random.randint(0, 1))
        else:
            RNRList.append(1)

    if need_print:
        print("对于你的问题：【" + query + "】")
        print("抽到的卡牌如下")
        for idx, card_name in enumerate(selected_cards):
            if RNRList[idx] == 1:
                print(
                    card_mean[idx],
                    ":【正位",
                    card_name,
                    ":",
                    tarotInfo[card_name]["正位关键词"],
                    "】",
                )
                # for text in tarotInfo[card_name]["正位"]:
                #     print(text)
            else:
                # print( card_mean[idx], ":【逆位", card_name, ":", tarotInfo[card_name]["逆位关键词"], "】")
                # 修改成格式化的输出
                print(
                    "{0} : 【逆位 {1} : {2}】".format(
                        card_mean[idx], card_name, tarotInfo[card_name]["逆位关键词"]
                    )
                )

                # for text in tarotInfo[card_name]["逆位"]:
                #     print(text)

    selected_cards_info = []
    for card_name in selected_cards:
        card_dict = {}
        card_dict[card_name] = tarotInfo[card_name]
        selected_cards_info.append(card_dict)
    if need_return:
        return selected_cards, selected_cards_info, card_name, RNRList
    else:
        return
