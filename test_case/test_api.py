# -*- coding: utf-8 -*-
# @Author  :  'zyx'
# @Email   : 458757014@qq.com
# @File    : test_api.py
# @Software: PyCharm Community Edition

import unittest
from ddt import ddt,data
from common.my_logger import logger
from common.filepath import *
from common.read_config import ReadConfig
from common.operate_excel import OperateExcel
from common.http_request import HttpRequests

excel_obj=OperateExcel(data_path+r'\test_datas.xlsx','test_data')
test_datas=excel_obj.read_data()
uri = ReadConfig(config_path+r'\config.ini').read_config('URI','uri')

#声明全局变量
COOKIES={}
INVEST_MEMBER_ID=''   #存储投资用户的用户ID


@ddt
class TestApi(unittest.TestCase):
    @data(*test_datas)
    def test_api(self,args):
        global COOKIES
        logger.info('正在执行第{0}条用例'.format(args['case_id']))
        logger.info('测试参数：{0}'.format(args))
        url = uri+args['apiName']
        #最终发送的参数
        logger.info('发送的请求参数为：{0}'.format(args['param']))
        logger.info('参数类型为：{0}'.format(type(args['param'])))
        #发起HTTP请求
        res = HttpRequests().http_request(url,args['method'],eval(args['param']),cookies=COOKIES)     #args['param']返回值为string，需转换为dict
        logger.info('返回结果：{0}'.format(res.json()))

        #获取投资用户的用户ID

        #获取返回结果中的cookie，若cookies不为空，则替换
        if res.cookies != {}:
            COOKIES=res.cookies

        #断言，比对结果
        try:
            logger.info('返回的code类型为{0}，期望code类型为{1}'.format(type(res.json()['code']),type(args['expected'])))
            logger.info('返回的code为{0}，期望code为{1}'.format(res.json()['code'],args['expected']))
            self.assertEqual(eval(res.json()['code']),args['expected'])
            logger.info('实际结果和期望结果匹配，测试通过')
            test_result='pass'
        except Exception as e:
            logger.exception('断言出错啦，期望结果为：{0}，实际结果为：{1}'.format(args['expected'],res.json()['code']))
            test_result='fail'
            raise e
        finally:
            excel_obj.write_back(args['case_id']+1,8,res.text)
            excel_obj.write_back(args['case_id']+1,9,test_result)
