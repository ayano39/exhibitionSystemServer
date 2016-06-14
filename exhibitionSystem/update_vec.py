# -*- coding:utf-8 -*-
from exhibitionSystem.make_route import *

#该方法的触发时机：影响用户兴趣向量的行为发生时
#该方法的两种思路:
#   1.每次将最新的用户行为以参数形式传进来（例如传入user_booth表的一条记录），
#   用新的行为【更新】之前的评分（因此不用遍历以前所有的行为记录）（类似于网络里计算RTTs的模式）
#   2.每次方法被调用时，都在数据库里搜索出所有能影响兴趣评分的记录，
#   综合所有记录计算出兴趣向量
'''
1.从request中使用POST.get方法得到uid和boothid，当前时间nowdate
2.在user列表中，查询到uid对应的表项，取出frontdate和frontboothid，判断frontdate的值
    如果是0，转3
    如果不是0，说明不是第一次点击
        停留时间date = nowdate - frontdate，将data存在user_booth中
        转4
3.说明是第一次点击，将五个变量均置为1，将新的兴趣向量更新到user_theme里面；系数 = (本次展台属性向量值/10)*100%+1），转7；
4.利用get方法根据uid从user_theme里面检索，得到对象的medical，vehicle，home，industry，wear的值，取出来保存到5个变量中；
5.计算 新的兴趣向量 = 旧的兴趣向量 + 旧的展台向量权重 * 停留时间，将新的兴趣向量更新到user_theme里面；
6.判断点击的站台的属性向量，公式暂时为（如果前一次站台的的属性向量值不为0且本次不为0，那么
    系数 = (（前一次本次展台向量值+本次展台属性向量值）/10)*100%+1
否则 系数 = (本次展台属性向量值/10)*100%+1）
7.将user表里面的frontdate和frontboothid，用nowdate和boothid更新，
8.将系数和取出的变量相乘，得到当前的数据，将他们化成百分比，然后传送给那个组；
'''
def update_intvec(userid , boothid , nowtime):
    coell = []
    per = []
    user_attr = []
    try:
        user_item = user.objects.get(uid=userid)
    except Exception as ex:  #no this user
        return ""
    else:
        frontdate = user_item.frontdate
        frontboothid = user_item.frontboothid
        print(frontboothid)
        if (frontboothid == 0): # the first click
            for i in range(5):
                user_attr.append(1)
            try:
                user_theme_item = user_theme.objects.get(uid=userid);
            except: # no this user
                return
            else: #find the user_them
                user_theme_item.medical = 1
                user_theme_item.vehicle = 1
                user_theme_item.home = 1
                user_theme_item.industry = 1
                user_theme_item.wear = 1
                user_theme_item.save()
                coell = cal_coell(boothid, frontboothid)
        else: #not the first click
            #print("not the first click")
            try:
                user_theme_item2 = user_theme.objects.get(uid = userid);
            except:  # no this user
                return
            else:
                #old single insterst
                user_attr.append(user_theme_item2.medical)
                user_attr.append(user_theme_item2.vehicle)
                user_attr.append(user_theme_item2.home)
                user_attr.append(user_theme_item2.industry)
                user_attr.append(user_theme_item2.wear)

                #stay time
                stay_time  = (nowtime - frontdate).seconds
                #old boooth insterst
                booth_front_theme = boothInfo.objects.get(booth_id=frontboothid)
                front_attr = []
                front_attr.append(booth_front_theme.medical)
                front_attr.append(booth_front_theme.vehicle)
                front_attr.append(booth_front_theme.home)
                front_attr.append(booth_front_theme.industry)
                front_attr.append(booth_front_theme.wear)
                #update
                new_user_attr = []
                for i in range(5):
                    new_user_attr.append(user_attr[i] + stay_time*front_attr[i])
                #save
                user_theme_item2.medical = new_user_attr[0]
                user_theme_item2.vehicle = new_user_attr[1]
                user_theme_item2.home = new_user_attr[2]
                user_theme_item2.industry = new_user_attr[3]
                user_theme_item2.wear = new_user_attr[4]
                user_theme_item2.save()
                coell = cal_coell(boothid,frontboothid)
    user_item.frontboothid = boothid
    user_item.frontdate = nowtime
    user_item.save()
    per = cal_per(coell, new_user_attr)
    return make_route(boothid, per)


        #计算系数
def cal_coell(boothid,frontboothid):
    coell = []
    try:
        booth_theme = boothInfo.objects.get(booth_id = boothid)
    except:
        return
    else:
        attr = []
        attr.append(booth_theme.medical)
        attr.append(booth_theme.vehicle)
        attr.append(booth_theme.home)
        attr.append(booth_theme.industry)
        attr.append(booth_theme.wear)
        if(frontboothid == 0):#first click
            for i in range(5):
                coell.append(attr[i] / 10 + 1)
        else:
            booth_front_theme = boothInfo.objects.get(booth_id = frontboothid)
            front_attr = []
            front_attr.append(booth_front_theme.medical)
            front_attr.append(booth_front_theme.vehicle)
            front_attr.append(booth_front_theme.home)
            front_attr.append(booth_front_theme.industry)
            front_attr.append(booth_front_theme.wear)
            for i in range(5):
                if(front_attr[i]!=0 and attr[i]!=0):
                    coell.append((front_attr[i]+attr[i]) / 10 + 1)
                else:
                    coell.append(attr[i] / 10 + 1)
        #print("coell")
        #for i in range(5):
         #   print (coell[i])
        return coell


    # 计算比例
def cal_per(coell , attr):
    per = []
    sum = 0
    for i in range(5):
        sum += coell[i] * attr[i]
    for i in range(5):
        per.append(coell[i] * attr [i] /sum)
    #print("per")
    #for i in range(5):
     #   print(per[i])
    return per
