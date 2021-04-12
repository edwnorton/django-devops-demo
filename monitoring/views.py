# -*- coding: UTF-8 -*-
import json
import os
import logging
from django.http import HttpResponse, JsonResponse
import traceback
from datetime import datetime
import uuid
from .models import alerts as alerts_t
from . import yamldata
#from .tasks import callTask, callTasklfs
from .models import *
from rest_framework import viewsets, filters, generics
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

index_view = never_cache(TemplateView.as_view(template_name='index.html'))

# LOG模块相关
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'monitoring.log')
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
fmt = '%(asctime)s - %(levelname)s - %(lineno)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger(__name__)
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

# 获取告警信息
alerts_info = alertsinf.objects
alerts_req = alerts_t()


def webhook(request):
    alerts_list = []
    if request.method == 'POST':
        try:
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
            alerts = request_dict['alerts']
            alerts_name = alerts[0]['labels']['alertname']
            alerts_status = alerts[0]['status']
            alert_msg = alerts[0]['annotations']
            startsAt = alerts[0]['startsAt'][0:19]
            endsAt = alerts[0]['endsAt'][0:19]
            alert_level = alerts[0]['labels']['level']
            alert_instance = alerts[0]['labels']['instance']
            start_obj = datetime.strptime(startsAt, "%Y-%m-%dT%H:%M:%S")
            start_sec = start_obj.timestamp()
            uid_str = str(start_sec) + alerts_name + alert_instance
            p_id = uuid.uuid3(uuid.NAMESPACE_DNS, uid_str)
            alerts_list.append([p_id, alerts_name, alert_instance, startsAt, alerts_status, alert_level, alert_msg, endsAt])
            dt = datetime.now()
            silentstatus = if_silent(dt, alerts_name)
            alert_name_res = if_alert_exist(alerts_list[0][1])
            if alert_name_res == '1':
                # 告警不在alertinfo中，不写入数据库
                print('告警不在alertinfo中，不写入数据库:')
                pass
            else:
                if alerts_list[0][4] == 'firing':
                    # 根据alert发送的告警'alertname'在数据库中匹配查询
                    m = [i for i in alerts_t.objects.values().filter(id=p_id)]
                    if len(m) != 0:
                        ins = alerts_t.objects.values().get(id=p_id)
                        alert_task_id = ins['id']
                        # 判断是否为静默时间告警，不在静默时间则更新silentstatus为'0'
                        if ins['status'] == 'firing' and silentstatus == '1':
                            logger.info('alert_task_id is firing but silence now... waiting to call {0}'.format(alert_task_id))
                            print('alert_task_id is firing but silence now... waiting to call {0}'.format(alert_task_id))
                        elif ins['status'] == 'firing' and silentstatus == '0':
                            a_obj = alerts_t.objects.get(id=p_id)
                            if a_obj.silentstatus == '0':
                                pass
                            else:
                                a_obj.silentstatus = silentstatus
                                a_obj.save()
                            logger.info('alert_task_id is firing... ... waiting to call {0}'.format(alert_task_id))
                            print('alert_task_id is firing... ...  waiting to call {0}'.format(alert_task_id))
                        else:
                            pass
                    else:
                        # 写入数据库
                        write_alert_db(alerts_list, silentstatus)
                        #t = work_process(alerts_list[0][0], alerts_list[0][1], alerts_list[0][2], silentstatus)
                if alerts_list[0][4] == 'resolved':
                    # 查询告警在数据库中是否存在
                    m = [i for i in alerts_t.objects.values().filter(id=p_id)]
                    if len(m) != 0:
                        a_obj = alerts_t.objects.get(id=p_id)
                        a_obj.endsAt = alerts_list[0][7]
                        a_obj.status = alerts_list[0][4]
                        a_obj.save()
                        logger.info('alert upodate id status:{0}'.format(p_id))
                        print('alert upodate id status:{0}'.format(p_id))
                    else:
                        logger.info('告警在数据库中不存在')
                        print('告警在数据库中不存在')
                        pass
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
        finally:
            return HttpResponse(1)


def if_alert_exist(alertname):
    alert_name_res = [i for i in alerts_info.values().filter(alertname=alertname)]
    # 判断告警是否在alertinfo中
    if len(alert_name_res) == 0:
        # 无匹配结果返回1
        return '1'
    else:
        return '0'


def if_silent(time_now, alertname):
    g_res = [i for i in alerts_info.values().filter(alertname=alertname)]
    # yaml_data = yamldata.get_yaml_data(yaml_path)
    silence_data = SilenceInfo.objects.values()
    if len(g_res) != 0:
        alert_level = g_res[0]['severity']
        # res = yaml_data['silence'][alert_level]
        res_dict = list(silence_data.filter(alertlevel=alert_level))[0]
    else:
        # res = yaml_data['silence']['high']
        res_dict = list(silence_data.filter(alertlevel='high'))[0]
    dt_h = time_now.strftime('%H')
    res = res_dict['silencetime'].strip().split('-')
    print(res)
    # if int(dt_h) < res['before'] or int(dt_h) > res['after']:
    if int(dt_h) < int(res[0]) or int(dt_h) > int(res[1]):
        return '1'
    else:
        return '0'


#def work_process(taskid, alertname, alertins, silentstatus):
#    r = callTask.delay(taskid, silentstatus)
#    logger.info('task [{0},{1},{2}] is waiting to call ...'.format(alertname, alertins, taskid))
#    print('task [{0},{1},{2}] is waiting to call ...'.format(alertname, alertins, taskid))
#    return r


def write_alert_db(alerts_list, silent_status):
    alerts_req.id = alerts_list[0][0]
    alerts_req.alertname = alerts_list[0][1]
    alerts_req.instance = alerts_list[0][2]
    alerts_req.startsAt = alerts_list[0][3]
    alerts_req.status = alerts_list[0][4]
    alerts_req.severity = alerts_list[0][5]
    alerts_req.message = alerts_list[0][6]
    alerts_req.endsAt = alerts_list[0][7]
    alerts_req.silentstatus = silent_status
    if silent_status == '1':
        alerts_req.callstatus = 'waittocall'
    else:
        alerts_req.callstatus = 'calling'
    alerts_req.save()
    logger.info('new alert,write to db and waiting to call')
    print('new alert,write to db and waiting to call')
    return alerts_list[0][1]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = AlertGroup.objects.all()
    serializer_class = AlertGroupSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('group', 'number')


class UpdateGroup(generics.UpdateAPIView):
    queryset = AlertGroup.objects.all()
    serializer_class = AlertGroupSerializer
    lookup_field = 'pk'


class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = alerts_t.objects.all()
    serializer_class = AlertsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('alertname', 'instance', 'startsAt', 'status',
                  'severity', 'message', 'endsAt', 'callee', 'callstatus', 'silentstatus')


class SilenceInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = SilenceInfo.objects.all()
    serializer_class = SilenceInfoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('alertlevel', 'silencetime')


class SilenceInfoUpdate(generics.UpdateAPIView):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = SilenceInfo.objects.all()
    serializer_class = SilenceInfoSerializer
    lookup_field = 'pk'


class AlertInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = alertsinf.objects.all()
    serializer_class = AlertsinfSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('alertname', 'telgroup', 'severity')


class AlertInfoUpdate(generics.UpdateAPIView):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = alertsinf.objects.all()
    serializer_class = AlertsinfSerializer
    lookup_field = 'pk'


def web_alert(request):
    alerts_list = []
    if request.method == 'POST':
        try:
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
            alerts = request_dict
            alerts_name = alerts['name']
            alerts_status = alerts['status']
            alert_msg = alerts['alertsmessage']
            startsAt = alerts['time']
            alert_instance = alerts['alertssystem']
            alert_level = 'high'
            endsAt = alerts['time']
            start_obj = datetime.strptime(startsAt, "%Y-%m-%d %H:%M:%S")
            start_sec = start_obj.timestamp()
            uid_str = str(start_sec) + alerts_name + alert_instance
            p_id = uuid.uuid3(uuid.NAMESPACE_DNS, uid_str)
            alerts_list.append([p_id, alerts_name, alert_instance, startsAt, alerts_status, alert_level, alert_msg, endsAt])
            dt = datetime.now()
            silentstatus = if_silent(dt, alerts_name)
            alert_name_res = if_alert_exist(alerts_list[0][1])
            if alert_name_res == '1':
                # 告警不在alertinfo中，不写入数据库
                logger.info('{0} 告警不在alertinfo中，不写入数据库:'.format(alerts_name))
                print('{0} 告警不在alertinfo中，不写入数据库:'.format(alerts_name))
                pass
            else:
                if alerts_list[0][4] == 'firing' and alerts_list[0][6]["success"] == 0:
                    # 根据alert发送的告警'alertname'在数据库中匹配查询
                    m = [i for i in alerts_t.objects.values().filter(id=p_id)]
                    if len(m) != 0:
                        ins = alerts_t.objects.values().get(id=p_id)
                        alert_task_id = ins['id']
                        # 判断是否为静默时间告警，不在静默时间则更新silentstatus为'0'
                        if ins['status'] == 'firing' and silentstatus == '1':
                            logger.info('alert_task_id is firing but silence now... waiting to call {0}'.format(alert_task_id))
                            print('alert_task_id is firing but silence now... waiting to call {0}'.format(alert_task_id))
                        elif ins['status'] == 'firing' and silentstatus == '0':
                            a_obj = alerts_t.objects.get(id=p_id)
                            if a_obj.silentstatus == '0':
                                pass
                            else:
                                a_obj.silentstatus = silentstatus
                                a_obj.save()
                            logger.info('alert_task_id is firing... ... waiting to call {0}'.format(alert_task_id))
                            print('alert_task_id is firing... ...  waiting to call {0}'.format(alert_task_id))
                        else:
                            pass
                    else:
                        # 写入数据库
                        write_alert_db(alerts_list, silentstatus)
                        #t = work_process(alerts_list[0][0], alerts_list[0][1], alerts_list[0][2], silentstatus)
                if alerts_list[0][4] == 'resolved':
                    # 查询告警在数据库中是否存在
                    m = [i for i in alerts_t.objects.values().filter(id=p_id)]
                    if len(m) != 0:
                        a_obj = alerts_t.objects.get(id=p_id)
                        a_obj.endsAt = alerts_list[0][7]
                        a_obj.status = alerts_list[0][4]
                        a_obj.save()
                        logger.info('alert upodate id status:{0}'.format(p_id))
                        print('alert upodate id status:{0}'.format(p_id))
                    else:
                        logger.info('告警在数据库中不存在')
                        print('告警在数据库中不存在')
                        pass
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
        finally:
            return HttpResponse(1)


# 容灾告警任务
#def work_process_lfs(req, obj_id):
#    r = callTasklfs.delay(obj_id, req)
#    logger.info('laifushi task [{0}] is waiting to call ...'.format(req))
#    print('laifushi task [{0}] is waiting to call ...'.format(req))
#    return r


# 容灾告警接口
def alarm_out(request):
    if request.method == 'POST':
        try:
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
            obj_id = request_dict["alert_id"]
            t = work_process_lfs(request_dict, obj_id)
            return JsonResponse(request_dict)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()


# 查询告警状态
def get_alert_status(request):
    if request.method == 'GET':
        try:
            req_id = request.GET.get('id')
            m = list(alerts_t.objects.values().filter(id=req_id))
            alert_status = m[0]["status"]
            if len(m) != 0 and alert_status == "resolved":
                data = {"alertstatus": alert_status}
            elif len(m) != 0 and alert_status == "firing":
                data = {"alertstatus": alert_status}
            else:
                data = {"alertstatus": "unknow"}
            return JsonResponse(data)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()


# 更新告警呼叫状态
def post_alert_status(request):
    if request.method == 'POST':
        try:
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
            obj_id = request_dict["id"]
            m = list(alerts_t.objects.values().filter(id=obj_id))
            callstatus = request_dict["callstatus"]
            callee = request_dict["callee"]
            if len(m) != 0:
                a_obj = alerts_t.objects.get(id=obj_id)
                a_obj.callstatus = callstatus
                a_obj.callee = callee
                a_obj.save()
            else:
                pass
            return JsonResponse({"data": "0"})
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
