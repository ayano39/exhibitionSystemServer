from django.shortcuts import render
import copy
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'exhibitionSystemServer.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from exhibitionSystem.models import *
from exhibitionSystem.RouteInfo import *
from django.views.decorators.csrf import csrf_exempt
from exhibitionSystem.models import *
import datetime
from django.utils import timezone

# Create your views here.

# 该方法被触发的时机：
#   在前端界面点击了某个展台的图标（用于模拟“用户已到达某展台”的事件）
# 该方法的实现流程:
#   1.获取当前用户编号uid以及新到达的展台编号boothId
#   2.在user_booth表中查找：是否有用户编号为uid且展台编号为boothId的记录
#       若有 → 转3
#       否则 → 转4
#   3.reached（到达某展台的次数）字段 + 1， update这条记录
#   4.将reached字段设为1， save这条记录
#   5.stayTime字段的更新将在下一轮迭代中完成~
#   6.调用update_intvec方法

@csrf_exempt
def update_trace(request):
    userid = request.POST.get("uid")
    boothid = request.POST.get("boothId")
    #now_datetime = request.POST.get("nowtime")
    #now_datetime = datetime.datetime.now()
    now_datetime = timezone.now()
    if (userid == None or boothid == None):
    #if(userid == None or boothid == None or now_datetime == None):
        return ""
    try:
        userBooth = user_booth.objects.get(uid = userid , booth_id = boothid);
    except Exception as ex:
        reached = 1
        userBooth = user_booth()
        userBooth.uid = userid
        userBooth.booth_id = boothid
        userBooth.reached = reached
        userBooth.save()
    else:
        userBooth.uid = userid
        userBooth.booth_id = boothid
        reached = userBooth.reached
        userBooth.reached = reached + 1
        userBooth.save()
    update_intvec(userid , boothid , now_datetime)
    return ""

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
    per = cal_per(coell,new_user_attr)
    make_route(boothid, per)


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


#该方法的触发时机：影响用户兴趣向量的行为发生时 or 定时被调用
#该方法实现的难题：
#   1.怎么表示展台与展台间相邻的关系？
#   2.展台的兴趣向量 以及 用户的兴趣向量， 两者之间怎么比对？怎么转换成加权值？
#   3.人群密度加到哪个表里？
def make_route(uid , boothid , interst):
    pass

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
    path = [booth_id]
    conboo = booth_conn.objects.filter(B1=booth_id)
    con_boo_id = get_conn_id(conboo)
    npath = copy.copy(path)
    route_first = RouteInfo(0, npath)
    iteration_3_layers(interests, route_first, con_boo_id)
    max_in_3_layer = get_max_gra()
    if max_in_3_layer.path[-1] == -1:
        return max_in_3_layer
    else:
        nconboo = booth_conn.objects.filter(B1=max_in_3_layer.path[-1])
        new_con_boo_id = get_conn_id(nconboo)
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