from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from exhibitionSystem.models import *
import datetime

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
    nowtime = request.POST.get("nowtime")
    if(userid == None or boothid == None or nowtime == None):
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
    update_intvec(userid , boothid , nowtime)
    return

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
def update_intvec(uid , boothid , nowtime):
    pass

#该方法的触发时机：影响用户兴趣向量的行为发生时 or 定时被调用
#该方法实现的难题：
#   1.怎么表示展台与展台间相邻的关系？
#   2.展台的兴趣向量 以及 用户的兴趣向量， 两者之间怎么比对？怎么转换成加权值？
#   3.人群密度加到哪个表里？
def make_route():
    pass
