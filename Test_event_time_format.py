#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# by error.d@gmail.com
# 2014-11-21
#

import sys
sys.path.insert(0, '../')

from event_time_format import (LeoEventTime,
                                    is_today,
                                    is_tomorrow,
                                    is_tswk,
                                    is_tsmh,
                                    week_number,
                                    weekday)

this_year = 2014
cur_time = '2015-01-28 17:25:37'

def setUp():
    pass

def tearDown():
    pass

def failed_msg(fn, msg, value, real_value, case):
    return "%s %s '%s' != '%s' detail look example %s" % (
        fn, msg, value, real_value, case)

def TestBaseFunction():

    # is today
    # 1
    today = is_today('2015-01-25 23:40:32', '2015-01-25 10:00:00')
    assert today == True, failed_msg('is_today1', 'failed', today, True,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # 2
    today = is_today('2015-01-25 00:00:00', '2015-01-24 23:59:59')
    assert today == False, failed_msg('is_today2', 'failed', today, False,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # 3
    today = is_today('2015-01-25 23:40:32', '2015-01-26 00:00:00')
    assert today == False, failed_msg('is_today3', 'failed', today, False,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # is tomorrow
    # 1
    tomorrow = is_tomorrow('2015-01-25 23:40:32', '2015-01-24 00:00:00')
    assert tomorrow == True, failed_msg('is_tomorrow1', 'failed', tomorrow, True,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # 2
    tomorrow = is_tomorrow('2015-01-25 23:40:32', '2015-01-23 23:59:59')
    assert tomorrow == False, failed_msg('is_tomorrow2', 'failed', tomorrow, False,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # 3
    tomorrow = is_tomorrow('2015-01-25 23:40:32', '2015-01-26 00:00:00')
    assert tomorrow == False, failed_msg('is_tomorrow3', 'failed', tomorrow, False,
                                    '2015-01-25 23:40:32 == 2015-01-25 00:00:00')

    # is this week
    # 1
    tswk = is_tswk('2015-01-25 23:40:32', '2015-01-19 00:00:00')
    assert tswk == True, failed_msg('is_tswk1', 'failed', tswk, True,
                                    '2015-01-25 23:40:32 == 2015-01-19 00:00:00')

    # 2
    tswk = is_tswk('2015-01-25 23:40:32', '2015-01-18 00:00:00')
    assert tswk == False, failed_msg('is_tswk2', 'failed', tswk, False,
                                    '2015-01-25 23:40:32 == 2015-01-19 00:00:00')

    # 3
    tswk = is_tswk('2015-01-25 23:40:32', '2015-01-26 00:00:00')
    assert tswk == False, failed_msg('is_tswk3', 'failed', tswk, False,
                                    '2015-01-25 23:40:32 == 2015-01-19 00:00:00')

    # is this month
    # 1
    tsmh = is_tsmh('2015-01-01 00:00:00', '2015-01-30 23:59:59')
    assert tsmh == True, failed_msg('is_tsmh1', 'failed', tsmh, True,
                                    '2015-01-01 00:00:00 == 2015-01-30 23:59:59')

    # 2
    tsmh = is_tsmh('2015-01-01 00:00:00', '2015-02-01 00:00:00')
    assert tsmh == False, failed_msg('is_tsmh2', 'failed', tsmh, False,
                                    '2015-01-01 00:00:00 == 2015-01-30 23:59:59')

    # 3
    tsmh = is_tsmh('2015-01-01 00:00:00', '2014-12-31 23:59:59')
    assert tsmh == False, failed_msg('is_tsmh3', 'failed', tsmh, False,
                                    '2015-01-01 00:00:00 == 2015-01-30 23:59:59')


    # week number
    wn = week_number('2015-01-02 00:00:00')
    assert wn == 1, failed_msg('week_number', 'failed', wn, 1,
                               '2015-01-02 00:00:00 == 1')
    wn = week_number('2015-01-28')
    assert wn == 5, failed_msg('week_number', 'failed', wn, 5, '2015-01-28 == 5')

    # weekday
    day = weekday('2015-01-28')
    assert day == 2, failed_msg('weekday', 'failed', day, 2, '2015-01-28 == 2')
    day = weekday('2015-01-28 00:00:00')
    assert day == 2, failed_msg('weekday', 'failed', day, 2,
                                '2015-01-28 00:00:00== 2')


def _base_case_test(case_args):
    case = case_args['case']
    fn = case_args['fn']
    if 'this_year' in case_args:
        real_this_year = case_args['this_year']
    else:
        real_this_year = this_year
    if 'cur_time' in case_args:
        real_cur_time = case_args['cur_time']
    else:
        real_cur_time = cur_time
    let = LeoEventTime(this_year=real_this_year, cur_time=real_cur_time)
    func = getattr(let, fn)
    func_args = case_args['func_args']
    attach_more_desc = case_args.get('attach_more_desc', None)

    if attach_more_desc:
        let.attach_more_desc(attach_more_desc)

    assert func(*func_args), '%s return failed' % fn

    desc = case_args.get('desc', None)
    if desc:
        real_desc = let.get_event_time_desc()
        assert real_desc == desc, \
               failed_msg(fn, 'desc failed', desc, real_desc, case)

    real_desc = case_args.get('real_desc', None)
    if real_desc:
        real_desc2 = let.get_realtime_desc()
        assert real_desc2 == real_desc, \
               failed_msg(fn, 'real desc failed', real_desc, real_desc2, case)

    option = case_args.get('option', None)
    if option:
        real_option = let.get_event_time_option()
        assert real_option == option, \
               failed_msg(fn, 'option failed', option, real_option, case)

    start_time = case_args.get('start_time', None)
    if start_time:
        real_start_time = let.get_event_start_time()
        assert real_start_time == start_time, \
               failed_msg(fn, 'start_time failed',
                      start_time, real_start_time, case)
    
    end_time = case_args.get('end_time', None)
    if end_time:
        real_end_time = let.get_event_end_time()
        assert real_end_time == end_time, \
               failed_msg(fn, 'end_time failed',
                          end_time, real_end_time, case)

    if attach_more_desc:
        more_desc = let.get_more_desc()
        assert attach_more_desc == more_desc, \
               failed_msg(fn, 'more desc failed',
                          more_desc, attach_more_desc, case)
        
    return let

def TestOneday_Case1():
    case_args = {
        'case': 'case1',
        'fn': 'make_oneday',
        'func_args': ['2014-02-05', '08:32:00', '22:20:00'],
        'desc': '2月5日 周三 8:32-22:20',
        'option': {'start_time': '08:32:00', 'day': '2014-02-05',
                   'end_time': '22:20:00'},
        'start_time': '2014-02-05 08:32:00',
        'end_time': '2014-02-05 22:20:00'
        }
    _base_case_test(case_args)

    
def TestOneday_Case2():
    case_args = {
        'case': 'case2',
        'fn': 'make_oneday',
        'func_args': ['2016-12-15', '00:00:00', '00:00:00'],
        'desc': '2016年12月15日 周四 全天',
        'option': {'start_time': '00:00:00', 'day': '2016-12-15',
                   'end_time': '00:00:00'},
        'start_time': '2016-12-15 00:00:00',
        'end_time': '2016-12-16 00:00:00'
        }
    _base_case_test(case_args)
        
def TestTimerange_Case3():
    case_args = {
        'case': 'case3',
        'fn': 'make_time_range',
        'func_args': ['2014-12-05 16:32:00', '2015-03-25 12:00:20'],
        'desc': '12月5日 16:32 ~ 2015年3月25日 12:00',
        'option': {'start_time': '2014-12-05 16:32:00',
                   'end_time': '2015-03-25 12:00:20'},
        'start_time': '2014-12-05 16:32:00',
        'end_time': '2015-03-25 12:00:20'
        }
    _base_case_test(case_args)

def TestTimerange_Case4():
    case_args = {
        'case': 'case4',
        'fn': 'make_time_range',
        'func_args': ['2014-12-05 00:00:00', '2015-03-25 00:00:00'],
        'desc': '12月5日 ~ 2015年3月24日',
        'option': {'start_time': '2014-12-05 00:00:00',
                   'end_time': '2015-03-25 00:00:00'},
        'start_time': '2014-12-05 00:00:00',
        'end_time': '2015-03-25 00:00:00'
        }
    _base_case_test(case_args)

def TestTimerange_Case5():
    case_args = {
        'case': 'case5',
        'fn': 'make_time_range',
        'attach_more_desc': '(周六，周日除外)',
        'func_args': ['2014-12-05 16:00:00', '2015-03-01 00:00:00'],
        'desc': '12月5日 16:00 ~ 2015年2月28日 (周六，周日除外)',
        'option': {'start_time': '2014-12-05 16:00:00',
                   'end_time': '2015-03-01 00:00:00'},
        'start_time': '2014-12-05 16:00:00',
        'end_time': '2015-03-01 00:00:00'
        }
    _base_case_test(case_args)

def TestTimerange_Case6():
    case_args = {
        'case': 'case6',
        'fn': 'make_time_range',
        'func_args': ['2014-12-05 00:00:00', '2015-03-25 08:21:00'],
        'desc': '12月5日 ~ 2015年3月25日 8:21',
        'option': {'start_time': '2014-12-05 00:00:00',
                   'end_time': '2015-03-25 08:21:00'},
        'start_time': '2014-12-05 00:00:00',
        'end_time': '2015-03-25 08:21:00'
        }
    _base_case_test(case_args)

def TestContinueday_Case7():
    case_args = {
        'case': 'case7',
        'fn': 'make_continue_day',
        'func_args': ['2014-12-05', '2016-03-25',
                      '16:32:00', '12:00:20'], 
        'desc': '12月5日 ~ 2016年3月25日 每天 16:32-12:00',
        'option': {'start_day': '2014-12-05', 'end_day': '2016-03-25',
                   'start_time': '16:32:00', 'end_time': '12:00:20'},
        'start_time': '2014-12-05 16:32:00',
        'end_time': '2016-03-25 12:00:20'
        }
    _base_case_test(case_args)

def TestContinueday_Case8():
    try:
        let = LeoEventTime(2014)
        let.make_continue_day('2014-12-05', '2016-03-25',
                              '16:32:00', '00:00:20'), \
                              let.get_event_time_desc()
    except AssertionError as real_msg:
        msg = 'continue day not end time is zero 00:00:20'
        assert msg == str(real_msg), \
               '\'%s\' != \'%s\' detail look case8' % (msg, real_msg)

def TestWeek_Case9():
    case_args = {
        'case': 'case9',
        'fn': 'make_week',
        'func_args': [[0, 3, 6],
                      ['2014-12-05', '2016-03-25'],
                      ['16:32:00', '22:00:20']],
        'desc': '12月5日 ~ 2016年3月25日 每周一、四、日 16:32-22:00',
        'option': {'event_weekdays': [0, 3, 6],
                   'days': ['2014-12-05', '2016-03-25'],
                   'times': ['16:32:00', '22:00:20']},
        'start_time': '2014-12-05 16:32:00',
        'end_time': '2016-03-25 22:00:20'
        }
    _base_case_test(case_args)

def TestWeek_Case10():
    case_args = {
        'case': 'case10',
        'fn': 'make_week',
        'func_args': [[0, 3, 6],
                      ['2015-12-05', '2016-03-25'],
                      ['00:00:00', '00:00:00']],
        'desc': '2015年12月5日 ~ 2016年3月24日 每周一、四、日 全天',
        'option': {'event_weekdays': [0, 3, 6],
                   'days': ['2015-12-05', '2016-03-25'],
                   'times': ['00:00:00', '00:00:00']},
        'start_time': '2015-12-05 00:00:00',
        'end_time': '2016-03-25 00:00:00'
        }
    _base_case_test(case_args)

def TestWeek_Case11():
    case_args = {
        'case': 'case11',
        'fn': 'make_week',
        'func_args': [[6],
                      ['2014-12-05', '2014-12-06'],
                      ['00:00:00', '13:00:00']],
        'desc': '12月5日 ~ 12月6日 周日 00:00-13:00',
        'option': {'event_weekdays': [6],
                   'days': ['2014-12-05', '2014-12-06'],
                   'times': ['00:00:00', '13:00:00']},
        'start_time': '2014-12-05 00:00:00',
        'end_time': '2014-12-06 13:00:00'
        }
    _base_case_test(case_args)

def TestIntermittent_Case12():
    case_args = {
        'case': 'case12',
        'fn': 'make_intermittent',
        'func_args': [[{'day': '2014-08-29', 'start_time': '02:32:36',
                        'end_time': '12:30:30'},
                       {'day': '2014-05-28', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2013-03-20', 'start_time': '12:32:36',
                        'end_time': '22:30:30'},
                       ]],
        'desc': '2013年3月20日 12:32-22:30、5月28日、8月29日 2:32-12:30',
        'option': {'time_list': [{'start_time': '02:32:36',
                                  'day': '2014-08-29',
                                  'end_time': '12:30:30'},
                                 {'start_time': '00:00:00',
                                  'day': '2014-05-28', 'end_time': '00:00:00'},
                                 {'start_time': '12:32:36',
                                  'day': '2013-03-20', 'end_time': '22:30:30'}]},
        'start_time': '2013-03-20 12:32:36',
        'end_time': '2014-08-29 12:30:30'
        }
    _base_case_test(case_args)

def TestIntermittent_Case13():
    case_args = {
        'case': 'case13',
        'fn': 'make_intermittent',
        'func_args': [[{'day': '2014-09-29', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2015-05-28', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2015-03-20', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2014-11-20', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       ]],
        'desc': '9月29日、11月20日、2015年3月20日、2015年5月28日',
        'option': {'time_list': [{'start_time': '00:00:00',
                                  'day': '2014-09-29', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2015-05-28', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2015-03-20', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2014-11-20', 'end_time': '00:00:00'}]},
        'start_time': '2014-09-29 00:00:00',
        'end_time': '2015-05-29 00:00:00'
        }
    _base_case_test(case_args)

LETD = None
def TestDumps_Case14():
    case_args = {
        'case': 'case14',
        'fn': 'make_intermittent',
        'func_args': [[{'day': '2014-09-29', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2015-05-28', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2015-03-20', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2014-11-20', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       ]],
        'desc': '9月29日、11月20日、2015年3月20日、2015年5月28日',
        'option': {'time_list': [{'start_time': '00:00:00',
                                  'day': '2014-09-29', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2015-05-28', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2015-03-20', 'end_time': '00:00:00'},
                                 {'start_time': '00:00:00',
                                  'day': '2014-11-20', 'end_time': '00:00:00'}]},
        'start_time': '2014-09-29 00:00:00',
        'end_time': '2015-05-29 00:00:00'
        }
    let = _base_case_test(case_args)

    dstr = str(eval("{'option': {'time_list': [{'start_time': '00:00:00', 'day': '2014-09-29', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2015-05-28', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2015-03-20', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2014-11-20', 'end_time': '00:00:00'}]}, 'more_desc': '', 'event_start_time': '2014-09-29 00:00:00', 'event_end_time': '2015-05-29 00:00:00', 'type': 5, 'desc': '9月29日、11月20日、2015年3月20日、2015年5月28日'}"))

    global LETD
    LETD = let.dumps()
    assert LETD == dstr, failed_msg('dumps', 'dumps failed',
                                           LETD, dstr, case_args['case'])

def TestLoads_Case15():
    case = 'case15'
    fn = 'loads'
    load_faield = 'loads failed'
    let = LeoEventTime()

    option = let.get_event_time_option()
    assert option == None, failed_msg(fn, load_faield,
                                      option, None, case)
    desc = let.get_event_time_desc()
    assert desc == '', failed_msg(fn, load_faield, desc, None, case)

    let.loads(LETD)

    option = let.get_event_time_option()
    real_option = "{'time_list': [{'start_time': '00:00:00', 'day': '2014-09-29', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2015-05-28', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2015-03-20', 'end_time': '00:00:00'}, {'start_time': '00:00:00', 'day': '2014-11-20', 'end_time': '00:00:00'}]}"

    assert real_option == str(option), failed_msg(fn, load_faield,
                                                  option, real_option, case)    

    desc = let.get_event_time_desc()
    real_desc = '9月29日、11月20日、2015年3月20日、2015年5月28日'
    assert real_desc == str(desc), failed_msg(fn, load_faield,
                                              desc, real_desc, case)    
def TestTimerange_Case16():
    case_args = {
        'case': 'case16',
        'fn': 'make_time_range',
        'func_args': ['0000-00-00 00:00:00', '0000-00-00 00:00:00'],
        'desc': '无时间限制',
        'option': {'start_time': '0000-00-00 00:00:00',
                   'end_time': '0000-00-00 00:00:00'},
        'start_time': '0000-00-00 00:00:00',
        'end_time': '0000-00-00 00:00:00'
        }
    _base_case_test(case_args)

def TestContinueday_Case17():
    case_args = {
        'case': 'case17',
        'fn': 'make_continue_day',
        'func_args': ['2014-01-01', '2014-12-31',
                      '16:32:00', '12:00:20'], 
        'desc': '全年 每天 16:32-12:00',
        'option': {'start_day': '2014-01-01', 'end_day': '2014-12-31',
                   'start_time': '16:32:00', 'end_time': '12:00:20'},
        'start_time': '2014-01-01 16:32:00',
        'end_time': '2014-12-31 12:00:20'
        }
    _base_case_test(case_args)

def TestContinueday_Case18():
    case_args = {
        'case': 'case18',
        'fn': 'make_continue_day',
        'func_args': ['0000-00-00', '0000-00-00',
                      '16:32:00', '12:00:20'], 
        'desc': '每天 16:32-12:00',
        'option': {'start_day': '0000-00-00', 'end_day': '0000-00-00',
                   'start_time': '16:32:00', 'end_time': '12:00:20'},
        'start_time': '0000-00-00 00:00:00',
        'end_time': '0000-00-00 00:00:00'
        }
    _base_case_test(case_args)

def TestWeek_Case19():
    case_args = {
        'case': 'case19',
        'fn': 'make_week',
        'func_args': [[0, 2, 3, 6],
                      ['2014-01-01', '2014-12-31'],
                      ['16:32:00', '22:00:20']],
        'desc': '全年 每周一、三、四、日 16:32-22:00',
        'option': {'event_weekdays': [0, 2, 3, 6],
                   'days': ['2014-01-01', '2014-12-31'],
                   'times': ['16:32:00', '22:00:20']},
        'start_time': '2014-01-01 16:32:00',
        'end_time': '2014-12-31 22:00:20'
        }
    _base_case_test(case_args)

def TestWeek_Case20():
    case_args = {
        'case': 'case20',
        'fn': 'make_week',
        'func_args': [[0, 1, 2, 3],
                      ['0000-00-00', '0000-00-00'],
                      ['16:32:00', '22:00:20']],
        'desc': '每周一至周四 16:32-22:00',
        'option': {'event_weekdays': [0, 1, 2, 3],
                   'days': ['0000-00-00', '0000-00-00'],
                   'times': ['16:32:00', '22:00:20']},
        'start_time': '0000-00-00 00:00:00',
        'end_time': '0000-00-00 00:00:00'
        }
    _base_case_test(case_args)

def TestWeek_Case21():
    case_args = {
        'case': 'case21',
        'fn': 'make_week',
        'func_args': [[0, 1, 2, 3, 6],
                      ['0000-00-00', '0000-00-00'],
                      ['00:00:00', '00:00:00']],
        'desc': '除每周五、六外，其余每天 全天',
        'option': {'event_weekdays': [0, 1, 2, 3, 6],
                   'days': ['0000-00-00', '0000-00-00'],
                   'times': ['00:00:00', '00:00:00']},
        'start_time': '0000-00-00 00:00:00',
        'end_time': '0000-00-00 00:00:00'
        }
    _base_case_test(case_args)

def TestWeek_Case22():
    case_args = {
        'case': 'case22',
        'fn': 'make_week',
        'func_args': [[3],
                      ['2014-01-01', '2014-12-31'],
                      ['00:00:00', '00:00:00']],
        'desc': '全年 每周四 全天',
        'option': {'event_weekdays': [3],
                   'days': ['2014-01-01', '2014-12-31'],
                   'times': ['00:00:00', '00:00:00']},
        'start_time': '2014-01-01 00:00:00',
        'end_time': '2015-01-01 00:00:00'
        }
    _base_case_test(case_args)


#
# get realtime description
#

def TestRealtime_Oneday_Case23():
    case_args = {
        'case': 'case23',
        'fn': 'make_oneday',
        'func_args': ['2015-01-28', '08:32:00', '22:20:00'],
        'real_desc': '今天 8:32',
        }
    _base_case_test(case_args)


def TestRealtime_Oneday_Case24():
    case_args = {
        'case': 'case24',
        'fn': 'make_oneday',
        'cur_time' : '2015-01-27 17:25:37',
        'func_args': ['2015-01-28', '08:32:00', '22:20:00'],
        'real_desc': '明天 8:32',
        }
    _base_case_test(case_args)


def TestRealtime_Oneday_Case25():
    case_args = {
        'case': 'case25',
        'fn': 'make_oneday',
        'cur_time' : '2015-01-26 17:25:37',
        'func_args': ['2015-01-29', '08:32:00', '22:20:00'],
        'real_desc': '本周四 8:32',
        }
    _base_case_test(case_args)


def TestRealtime_Oneday_Case26():
    case_args = {
        'case': 'case26',
        'fn': 'make_oneday',
        'cur_time' : '2015-01-10 17:25:37',
        'this_year' : 2015,
        'func_args': ['2015-01-16', '18:32:00', '22:20:00'],
        'real_desc': '1月16日 18:32',
        }
    _base_case_test(case_args)


def TestRealtime_Oneday_Case27():
    case_args = {
        'case': 'case27',
        'fn': 'make_oneday',
        'cur_time' : '2015-01-10 17:25:37',
        'this_year' : 2014,
        'func_args': ['2015-01-16', '00:32:00', '22:20:00'],
        'real_desc': '2015年1月16日 00:32',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case28():
    case_args = {
        'case': 'case28',
        'fn': 'make_time_range',
        'cur_time' : '2015-01-10 17:25:37',
        'this_year' : 2015,
        'func_args': ['2014-12-05 16:32:00', '2015-03-25 12:00:20'],
        'real_desc': '截止至3月25日',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case29():
    case_args = {
        'case': 'case29',
        'fn': 'make_time_range',
        'cur_time' : '2014-12-04 17:25:37',
        'this_year' : 2015,
        'func_args': ['2014-12-05 16:32:00', '2015-03-25 12:00:20'],
        'real_desc': '明天 16:32',
        }
    _base_case_test(case_args)

def TestRealtime_TimeRange_Case30():
    case_args = {
        'case': 'case30',
        'fn': 'make_time_range',
        'cur_time' : '2014-12-03 17:25:37',
        'this_year' : 2015,
        'func_args': ['2014-12-05 16:32:00', '2015-03-25 12:00:20'],
        'real_desc': '本周五 16:32',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case31():
    case_args = {
        'case': 'case31',
        'fn': 'make_time_range',
        'cur_time' : '2015-12-03 17:25:37',
        'this_year' : 2015,
        'func_args': ['2014-12-05 16:32:00', '2015-03-25 12:00:20'],
        'real_desc': '2014年12月5日 16:32',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case32():
    case_args = {
        'case': 'case32',
        'fn': 'make_time_range',
        'cur_time' : '2014-12-02 17:25:37',
        'this_year' : 2015,
        'func_args': ['2014-12-09 16:32:00', '2014-12-25 12:00:20'],
        'real_desc': '本月9日~25日',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case33():
    case_args = {
        'case': 'case33',
        'fn': 'make_time_range',
        'cur_time' : '2014-11-03 17:25:37',
        'this_year' : 2014,
        'func_args': ['2014-12-05 16:32:00', '2014-12-30 12:00:20'],
        'real_desc': '12月5日~12月30日',
        }
    _base_case_test(case_args)


def TestRealtime_TimeRange_Case34():
    case_args = {
        'case': 'case34',
        'fn': 'make_time_range',
        'cur_time' : '2014-11-03 17:25:37',
        'this_year' : 2014,
        'func_args': ['2014-12-05 16:32:00', '2015-01-30 12:00:20'],
        'real_desc': '12月5日~2015年1月30日'
        }
    _base_case_test(case_args)


def TestRealtime_Continue_Case35():
    case_args = {
        'case': 'case35',
        'fn': 'make_continue_day',
        'cur_time' : '2014-11-05 13:25:37',
        'this_year' : 2014,
        'func_args': ['2014-11-05', '2015-03-25',
                      '16:32:00', '12:00:20'],
        'real_desc': '今天 16:32'
        }
    _base_case_test(case_args)

def TestRealtime_Continue_Case36():
    case_args = {
        'case': 'case36',
        'fn': 'make_continue_day',
        'cur_time' : '2014-11-03 17:25:37',
        'this_year' : 2014,
        'func_args': ['2014-12-05', '2016-03-25',
                      '16:32:00', '12:00:20'],
        'real_desc': '12月5日~2016年3月25日'
        }
    _base_case_test(case_args)


def TestRealtime_Intermittent_Case37():
    case_args = {
        'case': 'case37',
        'fn': 'make_intermittent',
        'cur_time' : '2014-05-26 17:25:37',
        'this_year' : 2014,
        'func_args': [[{'day': '2014-08-29', 'start_time': '02:32:36',
                        'end_time': '12:30:30'},
                       {'day': '2014-05-28', 'start_time': '00:00:00',
                        'end_time': '00:00:00'},
                       {'day': '2013-03-20', 'start_time': '12:32:36',
                        'end_time': '22:30:30'},
                       {'day': '2015-11-20', 'start_time': '12:32:36',
                        'end_time': '22:30:30'},
                       ]],
        'real_desc': '本周三 全天'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case38():
    case_args = {
        'case': 'case38',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[0, 3, 6],
                      ['2015-01-26', '2015-01-31'],
                      ['16:32:00', '22:00:20']],
        'real_desc': '本周一、四、日 16:32'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case39():
    case_args = {
        'case': 'case39',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[0, 3, 4, 5, 6],
                      ['2015-01-26', '2015-01-31'],
                      ['00:00:00', '00:00:00']],
        'real_desc': '除本周二、三外，其余每天 全天'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case40():
    case_args = {
        'case': 'case40',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[2, 3, 4, 5],
                      ['2015-01-26', '2015-01-31'],
                      ['10:00:00', '00:00:00']],
        'real_desc': '本周三至周六 10:00'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case41():
    case_args = {
        'case': 'case41',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[3, 4, 5, 6],
                      ['2015-01-26', '2015-01-31'],
                      ['00:00:00', '00:00:00']],
        'real_desc': '本周四至周日 全天'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case42():
    case_args = {
        'case': 'case42',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[3, 4, 5, 6],
                      ['2015-02-21', '2015-02-28'],
                      ['00:00:00', '00:00:00']],
        'real_desc': '每周四至周日 全天'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case43():
    case_args = {
        'case': 'case43',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[3, 4, 5, 6],
                      ['2015-02-21', '2015-02-28'],
                      ['08:25:00', '23:30:00']],
        'real_desc': '每周四至周日 8:25'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case44():
    case_args = {
        'case': 'case44',
        'fn': 'make_week',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[3, 2, 5, 6],
                      ['2015-02-21', '2015-02-28'],
                      ['08:25:00', '23:30:00']],
        'real_desc': '每周三、四、六、日 8:25'
        }
    _base_case_test(case_args)


def TestRealtime_Week_Case45():
    case_args = {
        'case': 'case45',
        'fn': 'make_week',
        'attach_more_desc': '周六，日 8:00-23:00',
        'cur_time' : '2015-01-30 17:25:37',
        'this_year' : 2015,
        'func_args': [[3, 2, 6],
                      ['2015-02-21', '2015-02-28'],
                      ['08:25:00', '23:30:00']],
        'real_desc': '每周三、四、日 8:25',
        }
    _base_case_test(case_args)

def TestRealtime_Desc_Loads_Case46():
    case = 'case46'
    fn = 'load and dumps'
    load_faield = 'loads and dumps failed'

    let = LeoEventTime(this_year=2015, cur_time='2015-01-30 17:25:37')
    let.make_week([3, 2, 5, 6],
                  ['2015-02-21', '2015-02-28'],
                  ['08:25:00', '23:30:00'])
    letd = let.dumps()

    let = LeoEventTime()
    let.loads(letd)

    realtime = let.get_realtime_desc()
    desc = "每周三、四、六、日 8:25"
    assert realtime == str(desc), failed_msg(fn, load_faield,
                                             realtime, desc, case)    

def TestRealtime_TimeRange_Case47():
    case_args = {
        'case': 'case47',
        'fn': 'make_time_range',
        'cur_time' : '2015-01-10 17:25:37',
        'this_year' : 2015,
        'func_args': ['0000-00-00 16:32:00', '0000-00-00 12:00:20'],
        'real_desc': '随时',
        }
    _base_case_test(case_args)


def TestRealtime_Continue_Case48():
    case_args = {
        'case': 'case48',
        'fn': 'make_continue_day',
        'cur_time' : '2014-11-05 13:25:37',
        'this_year' : 2014,
        'func_args': ['0000-00-00', '0000-00-00',
                      '16:32:00', '12:00:20'],
        'real_desc': '每天 16:32'
        }
    _base_case_test(case_args)

def TestRealtime_Week_Case49():
    case_args = {
        'case': 'case49',
        'fn': 'make_week',
        'cur_time' : '2015-03-28 17:25:37',
        'this_year' : 2015,
        'func_args': [[0, 2, 4, 5, 6],
                      ['0000-00-00', '0000-00-00'],
                      ['08:25:00', '23:30:00']],
        'real_desc': '除每周二、四外，其余每天 8:25'
        }
    _base_case_test(case_args)

def TestRealtime_Week_Case50():
    case_args = {
        'case': 'case50',
        'fn': 'make_week',
        'cur_time' : '2015-03-28 17:25:37',
        'this_year' : 2015,
        'func_args': [[0, 2, 5, 6],
                      ['0000-00-00', '0000-00-00'],
                      ['17:30:00', '21:35:00']],
        'real_desc': '每周一、三、六、日 17:30'
        }
    _base_case_test(case_args)

def TestRealtime_Week_Case51():
    case_args = {
        'case': 'case51',
        'fn': 'make_week',
        'cur_time' : '2015-03-28 17:25:37',
        'this_year' : 2015,
        'func_args': [[0, 1, 2, 4, 5, 6],
                      ['0000-00-00', '0000-00-00'],
                      ['08:25:00', '23:30:00']],
        'real_desc': '除每周四外，其余每天 8:25'
        }
    _base_case_test(case_args)

def TestRealtime_Week_Case52():
    case_args = {
        'case': 'case52',
        'fn': 'make_week',
        'cur_time' : '2015-07-29 14:25:37',
        'this_year' : 2015,
        'func_args': [[0, 2, 3, 4, 5, 6],
                      ['2015-08-03', '2015-08-09'],
                      ['16:00:00', '20:00:00']],
        'real_desc': '除下周二外，其余每天 16:00'
        }
    _base_case_test(case_args)
