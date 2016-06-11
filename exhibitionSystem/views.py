from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from exhibitionSystem.models import *

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
    if(userid == None or boothid == None):
        return ""
    try:
        userBooth = user_booth.objects.get(uid = userid , booth = boothid);
    except Exception as ex:
        reached = 1
        userBooth = user_booth()
        userBooth.uid = userid
        userBooth.booth = boothid
        userBooth.reached = reached
        userBooth.save()
    else:
        userBooth.uid = userid
        userBooth.booth = boothid
        reached = userBooth.reached
        userBooth.reached = reached + 1
        userBooth.save()
    update_intvec(request)
    return

#该方法的触发时机：影响用户兴趣向量的行为发生时
#该方法的两种思路:
#   1.每次将最新的用户行为以参数形式传进来（例如传入user_booth表的一条记录），
#   用新的行为【更新】之前的评分（因此不用遍历以前所有的行为记录）（类似于网络里计算RTTs的模式）
#   2.每次方法被调用时，都在数据库里搜索出所有能影响兴趣评分的记录，
#   综合所有记录计算出兴趣向量
def update_intvec(request):
    pass

#该方法的触发时机：影响用户兴趣向量的行为发生时 or 定时被调用
#该方法实现的难题：
#   1.怎么表示展台与展台间相邻的关系？
#   2.展台的兴趣向量 以及 用户的兴趣向量， 两者之间怎么比对？怎么转换成加权值？
#   3.人群密度加到哪个表里？
def make_route():
    pass
