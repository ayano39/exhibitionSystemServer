# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from exhibitionSystem.update_vec import *
from exhibitionSystem.make_map import *
from django.utils import timezone
import json


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
    now_datetime = timezone.now()
    if (userid == None or boothid == None):
        return ""
    if boothid == -1:
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
    route = update_intvec(userid, boothid, now_datetime)
    return HttpResponse(json.dumps(route.toJson()), content_type="application/json")


def home_page(request):
    return render_to_response("boothMap.html")


def make_map(request):
    return HttpResponse(get_map(), content_type="application/json")

@csrf_exempt
def init(request):
    user_id = int(request.POST.get("uid"))

    user_item = user.objects.get(uid = user_id)
    user_item.frontboothid = 0
    user_item.save()

    visit_record = user_booth.objects.filter(uid = user_id)
    visit_record.delete()

    return HttpResponse(status=200)
