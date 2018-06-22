# -*- coding: utf-8 -*-

from rest_framework.response import Response
from django.http import HttpResponseRedirect
import json


def NewRespRedirect(path):
    if path is None or path == '':
        return MSG_OK

    return HttpResponseRedirect(path)


MSG_CODE_PARAMETER_ERR = 1001
MSG_CODE_FILE_ERROR = 3001
MSG_CODE_NO_PERMISSION = 3002
MSG_CODE_PROTECT_ERROR = 3003
MSG_CODE_NO_CHANGE = 3004

MSG_OK = {'code': 0, 'message': u'OK'}

MSG_PARAMETER_ERR = {'code': MSG_CODE_PARAMETER_ERR, 'message': u'参数错误'}
MSG_RECURSIVE_ERR = {'code': 1002, 'message': u'超过最大迭代次数'}
MSG_AUTH_FAIL = {'code': 2001, 'message': u'用户名或密码错误'}
MSG_AUTH_PWD_FAIL = {'code': 2002, 'message': u'密码验证失败'}


def RespErr(msg, status=400):
    return Response(msg, status)


def NewRespErr(code, msg, status=400):
    return RespErr({'code': code, 'message': msg}, status=status)


def NewRespErrWithExistCode(msg, msg_str):
    msg['message'] = msg_str
    return RespErr(msg)


def NewOtherMsg(msg):
    return {'code': 400, 'message': msg}


RESP_OK = Response(MSG_OK, status=200)
RESP_DELETED = Response(None, status=204)
RESP_CREATED = Response(None, status=201)
