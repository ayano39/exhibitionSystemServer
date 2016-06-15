# -*- coding:utf-8 -*-
import copy
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'exhibitionSystemServer.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from exhibitionSystem.RouteInfo import *
from exhibitionSystem.models import *

'''
创建类routeInfo:
 *属性grade(int):路径评分，通过该路径上展台的主题评分和用户的兴趣评分以及迭代深度获得。
 *属性path[](dict):路径，通过键值对表示路径，其中key上一个展台，value为下一个展台。如（“1”：“2”，“2”:“3”）表示展台1→2→3
 在每次需找当前展台的相邻展台时，都根据新的路径实例化一个routeInfo的对象，其中grade是到从起点到该相邻展台的路径的评分，path[]中为路径。
'''

'''
方法make_route(uid, boothId):
 该方法在每次点击某个展台时调用
 集合interests[5]中保存当前用户的兴趣评分
 集合allRoute[]为全局变量，保存所有可能的路径，每个元素都是一个routeInfo对象
 集合conBooId[]中保存与boothId相邻的所有展台
 #变量level表示当前层数，初始化为0
 实例化一个routeInfo对象，其中grade = 0,path为空
 每次调用都通过request获得点击的展台的boothId和当前的userId
 使用interests[] = user_theme.objects.filter(uid = userId)从数据库中查询该用户的兴趣评分
 使用conBooId[] = booth_conn.objects.filter(B1 = boothId)从数据库中查询所有与当前展台相邻的展台,只选B1保证不会往回走
 调用三层以内不剪枝（boothId,interests,routeInfo,conBooId)
 三层以内不剪枝方法结束后，allRoute中应该有三层内的所有路径
 调用方法getMaxGrad(allRoute),选出其中grade最大的，继续递归遍历
 这时候的递归遍历就不用每个相邻展台都迭代遍历了，只需要选择grade最大的，直到出口即可
 调用三层外递归
'''
'''
方法三层以内不剪枝(boothId,interests[],routeInfo,conBooId[]):
 该方法在三层以内递归调用计算路径，三层内不同层有不同权重
 当前的层数通过routeInfo中键值对的数量获得
 level = 1：levelWeight = 1，level = 2：levelWeight = 0.5，level = 3：levelWeight = 0.1
 通过遍历conBooId[]中的展台，为每个展台实例化routeInfo对象，调用gradeCal3计算路径评分
 for(i = 0;i < conBooId[].size();i++){
   展台主题评分boothTheGra[] = getBoothGra(conBooId[i])
   新的展台信息对象routeInfoOb = routeInfo(新的路径分数gradeCal3(levelWeight,interests[],boothTheGra[]),routeInfo.path)
   routeInfoOb.path.add(boothId:conBooId[i])
   将新的展台信息对象加到集合中，用于后续比较allRoute.add(routeInfOb)
   使用newConBooId[] = booth_conn.objects.filter(B1 = conBooId[i])从数据库中查询新的所有与当前展台相邻的展台
   if(routeInfo.size < 4)//键值对小于4，三层以内递归
       调用三层以内不剪枝（conBooId[i],interests[],routeInfoOb,newConBooId)
   else
       return
 }
'''

'''
方法三层外递归(boothId,interests[],routeInfo,conBooId[]):
 该方法在三层外递归调用计算路径，此时不用计算权重，因为不用再保存所有的路径只要选最大的
 集合grades[]中保存了每个相邻展台的评分
 变量index为最后选中的评分最高的展台的下标
 for(i = 0;i < conBooId[].size();i++){
   展台主题评分boothTheGra[] = getBoothGra(conBooId[i])
   grades[i] = gradeCal(interests[],boothTheGra[])
 }
 找出grades[]中值最大的，下标为index，最后选中的下一个展台就是conBooId[index]
 routeInfo.path.add(boothId:conBooId[index])
 if(conBooId[index] > 0)//不是出口，继续递归{
     使用newConBooId[] = booth_conn.objects.filter(B1 = conBooId[index])从数据库中查询新的所有与下一展台展台相邻的展台
     递归调用三层外递归(conBooId[index],interests[],routeInfo,newBooId[])
 }
 else//已经到出口了
    return routeInfo
'''

'''
方法getBoothGra(boothId):
 该方法获得某个展台的主题评分
 集合boothInfo[]中为数据库查询返回的展台信息
 boothInfo[] = boothInfo.objects.filter(boothid = boothId)从数据库中查询展台的信息
 因为展台信息中除了主题评分还有其他信息，需要过滤掉
 boothGra[] = boothInfo[2][3][4][5][6]
 返回集合boothGra[]，为展台的主题评分
'''

'''
方法gradeCal3(levelWeight,interests[],boothTheGra[]):
 该方法在递归三层以内计算每条路径的当前评分
 因为三层以内每次有不同的权重，而三层以外可直接比较grade大小来选择
 参数中的levelWeight为当前的层数的权重，interests[]为用户兴趣评分，boothTheGra[]为该展台的主题评分
 新的grade = levelWeight * (interests * boothTheGra)

'''

'''
方法gradeCal(interests[],boothTheGra[]):
 该方法在递归三层以外计算每条路径的当前评分
 参数中interests[]为用户兴趣评分，boothTheGra[]为该展台的主题评分
 新的grade = interests * boothTheGra

'''

'''
方法getMaxGra(allRoute):
 找到allRoute中grade最大的routeInfo返回
'''

#通过request获得当前userid和boothid
#通过userid获得兴趣向量，根据兴趣向量计算出每个主题所占的百分比，存入interests[5]
#通过boothid获取主题向量，theme[5]
#类routeinfo{int grade;dict path[]}用来存储分数和路径
#对当前所在节点 根据boothid在表booth_conn中找到其后继三层节点，计算到每个最末节点的路径获得的分数
#计算分数的方法是，sum 层数权重*interests[n]*theme[n]，层数权重可选1,0.5,0.25
#在三层查找完毕后选出目前最佳的路径，以末层节点为根继续计算三层，直至到达出口(不如递归，写循环不如递归)
#方法可以包括，从conn中获取后继fetchson()，计算三层的递归方法trilayer()，计算整个路径getpath(),计算兴趣向量百分比gettheme()，

all_3_route = []
levelWeight = {1:1, 2:0.5, 3:0.1}


def make_route(booth_id,interests):
    global all_3_route
    all_3_route = []
    path = []
    conboo = booth_conn.objects.filter(B1=booth_id)
    con_boo_id = get_conn_id(conboo)
    npath = copy.copy(path)
    npath.append(int(booth_id))
    route_first = RouteInfo(0, npath)
    iteration_3_layers(interests, route_first, con_boo_id)
    max_in_3_layer = get_max_gra()
    if max_in_3_layer.path[-1] == -1:
        return max_in_3_layer
    else:
        nconboo = booth_conn.objects.filter(B1=max_in_3_layer.path[-1])
        new_con_boo_id = get_conn_id(nconboo)
        #final_route = RouteInfo(0,[])
        #fr = iteration_all_layers(interests,  max_in_3_layer, new_con_boo_id)
        #final_route.grade = fr.grade
        #final_route.path = copy.copy(fr.path)
        final_route = iteration_all_layers(interests,  max_in_3_layer, new_con_boo_id)
        return final_route


def iteration_3_layers(interests,route_info,con_boo_id):
    for booth in list(con_boo_id):
        booth_theme_grade = get_booth_grades(booth)
        new_grade = grade_cal_3(route_info, interests,booth_theme_grade)
        new_path = copy.copy(route_info.path)
        new_route_info = RouteInfo(route_info.grade + new_grade, new_path)
        new_route_info.path.append(booth)
        conboo = booth_conn.objects.filter(B1=booth)
        new_con_boo_id = get_conn_id(conboo)
        if new_route_info.path[-1] == -1:
            global all_3_route
            all_3_route.append(new_route_info)
        elif len(new_route_info.path) < 4:
            iteration_3_layers(interests, new_route_info, new_con_boo_id)
        else:
            all_3_route.append(new_route_info)
    return


def iteration_all_layers(interests,route_info,con_boo_id):
    grades = []
    for booth in list(con_boo_id):
        booth_theme_grade = get_booth_grades(booth)
        grades.append(grade_cal(interests, booth_theme_grade))
    max_grade = max(grades)
    max_index = grades.index(max_grade)
    route_info.path.append(con_boo_id[max_index])
    if con_boo_id[max_index] > 0:
        conboo = booth_conn.objects.filter(B1=con_boo_id[max_index])
        new_con_boo_id = get_conn_id(conboo)
        return iteration_all_layers(interests, route_info, new_con_boo_id)
    else:
        return route_info


def grade_cal_3(route_info,interests,booth_grades):
    global levelWeight
    i = len(route_info.path)
    weight = levelWeight[i]
    grade = weight * grade_cal(interests,booth_grades)
    return grade


def get_booth_grades(booth_Id):
    if booth_Id == -1:
        return [0, 0, 0, 0, 0]
    else:
        booth_info = boothInfo.objects.get(booth_id=booth_Id)
        booth_grades = []
        i = 0
        booth_grades.append(booth_info.medical)
        booth_grades.append(booth_info.vehicle)
        booth_grades.append(booth_info.home)
        booth_grades.append(booth_info.industry)
        booth_grades.append(booth_info.wear)
        return booth_grades


def grade_cal(interests,booth_grades):
    i = 0
    grade = 0
    while i < 5:
        grade = grade + interests[i] * booth_grades[i]
        i = i + 1
    return grade


def get_max_gra():
    global all_3_route
    max = all_3_route[0]
    for r in all_3_route:
        if r.grade > max.grade:
            max = r
    return max


def get_conn_id(con_boo_id):
    connid = []
    for line in con_boo_id:
        connid.append(int(line.B2))
    return connid
