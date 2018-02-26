# -*- coding: utf-8 -*-
#
# Copyright 2014 error.d@gmail.com
# by error.d@gmail.com
# 2014-11-19
#

import re
import logging
import time
import arrow
#import json

#
# weekday base on 0 (星期一)
#

def always(start_time, end_time):
    """is always
    start_day: YYYY-MM-DD or YYYY-MM-DD HH:mm:ss
    end_day: YYYY-MM-DD or YYYY-MM-DD HH:mm:ss
    """
    if (start_time == '0000-00-00' and end_time == '0000-00-00') or \
           (start_time == '0000-00-00 00:00:00' and \
            end_time == '0000-00-00 00:00:00'):
        return True
    else:
        return False

def one_year(start_day, end_day):
    """is one year
    start_day: YYYY-MM-DD
    end_day: YYYY-MM-DD
    """
    start = arrow.get(start_day)
    end = arrow.get(end_day)

    if (end - start).days == 364:
        return True
    return False

def zero_time(*args):
    """
    is zero time
    args is time dict or string list
    """
    for ztime in args:
        if isinstance(ztime, dict) and \
            (ztime['hour'] != '00' or ztime['minute'] != '00'):
            return False
    return True

def zero_date(*args):
    """
    is zero date
    """
    for ztime in args:
        if isinstance(ztime, str) and \
               (ztime == '0000-00-00' or ztime == '0000-00-00 00:00:00'):
            return True
    return False

def get_this_year():
    """
    this year
    """
    return time.localtime().tm_year

def get_current_time():
    """
    current time
    """
    return arrow.get().format('YYYY-MM-DD HH:mm:ss')

def day_add(day, num):
    """
    num: add +1, sub -1
    """
    return arrow.get(day).replace(days=num).format('YYYY-MM-DD')

def day_to_iso(day):
    """
    day to iso format
    """
    return '%(year)s-%(month)s-%(day)s' % day

def time_to_iso(time_struct):
    """
    time to iso format
    """
    #return '%(hour)s:%(minute)s' % time_struct
    hour = int(time_struct['hour'])
    if not hour:
        hour = '00'
    return '%s:%s' % (hour, time_struct['minute'])

def is_today(start_time, cur_time):
    """
    start_time is today
    """
    if arrow.get(start_time).date() == \
           arrow.get(cur_time).date():
        return True
    return False

def is_tomorrow(start_time, cur_time):
    """
    start_time is tomorrow
    """
    if arrow.get(start_time).date() == \
           arrow.get(cur_time).replace(days=1).date():
        return True
    return False

def is_tswk(start_time, cur_time):
    """
    start_time is this week
    """
    if zero_date(start_time, cur_time):
        return False
    if arrow.get(start_time).isocalendar()[0:2] == \
           arrow.get(cur_time).isocalendar()[0:2]:
        return True
    return False

def is_nextweek(start_time, cur_time):
    """
    start_time is next week
    BUG: cross year
    """
    if zero_date(start_time, cur_time):
        return False
    cw = arrow.get(cur_time).isocalendar()[0:2]
    sw = arrow.get(start_time).isocalendar()[0:2]
    cw = (cw[0], cw[1]+1)
    if cw == sw:
        return True
    return False

def is_tsmh(start_time, cur_time):
    """
    start_time is this month
    """
    if arrow.get(start_time).date().month == \
           arrow.get(cur_time).date().month:
        return True
    return False

def is_continuation_week(event_weekdays):
    """
    continuation week
    """
    weekday_len = len(event_weekdays)
    if weekday_len < 3:
        return False

    for idx, week in enumerate(event_weekdays):
        if idx + 1 < weekday_len:
            if week+1 != event_weekdays[idx+1]:
                return False
    return True

def convert_week_day(event_weekdays):
    """
    convert week day
    """
    all_set = set([0, 1, 2, 3, 4, 5, 6])
    return list(all_set - set(event_weekdays))


def week_number(day):
    """
    week number
    """
    arrow_t = arrow.get(day)
    return arrow_t.isocalendar()[1]

def weekday(day):
    """
    weekday
    """
    return arrow.get(day).weekday()

class Rule(object):
    """
    Time Rule
    """

    def __init__(self, name, rule, example, use_groupdict=False):
        """
        """
        self._name = name
        self._rule = rule
        self._example = example
        self._use_groupdict = use_groupdict
        self._rec = re.compile(rule)

    def _check_extract(self, data):
        """
        use rule check and extract on data
        """
        data = data.strip()
        res = self._rec.match(data)
        if not res:
            logging.error('check %s failed data:%s rule:%s example:%s',
                          self._name, data, self._rule, self._example)
            return None
        return res.groupdict() if self._use_groupdict else res.groups()

    def __call__(self, *args):
        """
        caller args is list, *xx
        pylint 'W:xx,xx: Used * or ** magic (star-args)'
        """
        if len(args) is 1 and type(args[0]) is list:
            args = args[0]
        res = [self._check_extract(data) for data in args]
        return res if len(res) > 1 else res[0]

    def rule(self):
        """
        return rule
        """
        return self._rule

    def example(self):
        """
        return example
        """
        return self._example

class LeoEventTime(object):
    """
    Leo Event Time
    """

    type_unknow = 0
    type_oneday = 1
    type_time_range = 2
    type_continue_day = 3
    type_week = 4
    type_intermittent = 5

    # default value
    besides_week = 5

    # rule
    day_rule = Rule(name='day rule',
                    rule=r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$',
                    example='2014-11-19', use_groupdict=True)

    time_rule = Rule(name='time rule',
                     rule=r'^(?P<hour>\d{2}):(?P<minute>\d{2}):\d{2}$',
                     example='09:32:00', use_groupdict=True)

    date_rule = Rule(name='date rule',
                     rule=r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) ' \
                     r'(?P<hour>\d{2}):(?P<minute>\d{2}):\d{2}$',
                     example='2014-11-19 17:59:05', use_groupdict=True)

    # data
    week_map = {
        0 : '一', 1 : '二', 2 : '三',
        3 : '四', 4 : '五', 5 : '六',
        6 : '日'
        }

    week_prefix = '周'

    day_list = [('year', '年'), ('month', '月'), ('day', '日')]

    time_list = [('hour', '点'), ('minute', '分')]

    def __init__(self, this_year=None, cur_time=None):
        """

        Arguments:
        - `this_year`: this year default None, use get_this_year
        - `cur_time`: this current time default None, use get_current_time
        """
        self._event_time_type = self.type_unknow
        self._letd = ''
        self._leotime_desc = ''
        self._event_start_time = ''
        self._event_end_time = ''
        self._event_time_option = None
        self._this_year = int(this_year) if this_year else get_this_year()
        self._cur_time = cur_time if cur_time else get_current_time()
        self._more_desc = ''

    def _load_letd(self):
        """
        load letd
        """
        letd = self._letd
        self._event_time_type = letd['type']
        self._leotime_desc = letd['desc']
        self._event_start_time = letd['event_start_time']
        self._event_end_time = letd['event_end_time']
        self._event_time_option = letd['option']
        self._more_desc = letd['more_desc']

    def _week_day(self, day, week_prefix=True):
        """
        week day
        """
        week_prefix = self.week_prefix if week_prefix else ''
        tstruct = time.localtime(
            time.mktime(time.strptime(day, "%Y-%m-%d")))
        return week_prefix + self.week_map[tstruct.tm_wday]

    def _wn_to_cn(self, num, week_prefix=True):
        """
        week day number to week day chinese
        """
        week_prefix = self.week_prefix if week_prefix else ''
        return week_prefix + self.week_map[int(num)]

    def _day_to_chinese(self, day, remove_this_year=True):
        """
        day to chinese fromat
        """
        day_list = self.day_list
        if remove_this_year and int(day['year']) == self._this_year:
            day_list = day_list[1:]
        return ''.join([str(int(day[item[0]])) + item[1] for item in day_list])

    def _time_to_chinese(self, time_struct):
        """
        time to chinese format
        """
        time_list = self.time_list
        return ''.join([time_struct[item[0]] + item[1] for item in time_list])

    def _mk_desc(self, desc):
        """
        make desc, attach more desc
        """
        return '%s%s' % (desc, " %s" % self._more_desc if \
                         self._more_desc else '')

    def _is_event_start(self):
        """
        True if event start other return False
        """
        start_time = arrow.get(self.get_event_start_time())
        end_time = arrow.get(self.get_event_end_time())
        cur_time = arrow.get(self.get_current_time())

        return cur_time >= start_time and cur_time < end_time

    def _is_event_no_start(self):
        """
        True if event no start other return False
        """
        start_time = arrow.get(self.get_event_start_time())
        cur_time = arrow.get(self.get_current_time())

        return cur_time < start_time

    def _is_event_close(self):
        """
        True if event close other return False
        """
        end_time = arrow.get(self.get_event_end_time())
        cur_time = arrow.get(self.get_current_time())

        return cur_time >= end_time

    def _week_day_cn(self, event_weekdays, multi_week,
                     cur_week=False, next_week=False):
        """
        event weekdays to cn
        """
        remove_tag = ''
        remove_append = ''
        week_tag = ''

        if next_week:
            week_tag = '下'
        elif multi_week:
            week_tag = '每'
        elif cur_week:
            week_tag = '本'

        if len(event_weekdays) == 1:
            week_day_cn = '%s%s' %  (week_tag,
                                     self._wn_to_cn(event_weekdays[0]))
        else:
            event_weekdays_len = len(event_weekdays)
            if is_continuation_week(event_weekdays):
                return '%s%s至%s' % (week_tag,
                                    self._wn_to_cn(event_weekdays[0]),
                                    self._wn_to_cn(event_weekdays[-1]))
            elif event_weekdays_len >= self.besides_week:
                event_weekdays = convert_week_day(event_weekdays)
                remove_tag = '除'
                remove_append = '外，其余每天'
            space_tag = '' if event_weekdays_len == 6 else '、'
            week_day_cn = '%s%s%s%s%s%s' % (
                remove_tag,
                week_tag,
                self._wn_to_cn(event_weekdays[0]),
                space_tag,
                '、'.join( \
                [self._wn_to_cn(item, week_prefix=False) for \
                 item in event_weekdays[1:]]),
                remove_append)
        return week_day_cn

    def _base_week_info(self, event_weekdays, days, times,
                        check_event_time_range=True,
                        cur_week=False, next_week=False):
        """
        get week base info
        """
        start_day_dict, end_day_dict = self.day_rule(days)
        start_time_dict, end_time_dict = self.time_rule(times)

        if None in (start_day_dict, end_day_dict,
                    start_time_dict, end_time_dict):
            return None

        event_weekdays.sort()
        event_start_time = '%s %s' % (days[0], times[0])
        event_end_time = '%s %s' % (days[1], times[1])

        is_always = always(day_to_iso(start_day_dict),
                           day_to_iso(end_day_dict))
        is_one_year = True if is_always else one_year(
            day_to_iso(start_day_dict),
            day_to_iso(end_day_dict))

        multi_week = False
        if check_event_time_range:
            multi_week = True if is_one_year else \
                         not is_tswk(event_start_time, event_end_time)
        elif cur_week is False:
            multi_week = True
        week_day_cn = self._week_day_cn(event_weekdays,
                                        multi_week, cur_week=cur_week,
                                        next_week=next_week)
        time_cn = '全天' if zero_time(start_time_dict, end_time_dict) else \
                  '%s-%s' % (time_to_iso(start_time_dict),
                             time_to_iso(end_time_dict))
        return dict(start_day_dict=start_day_dict,
                    end_day_dict=end_day_dict,
                    start_time_dict=start_time_dict,
                    end_time_dict=end_time_dict,
                    event_start_time=event_start_time,
                    event_end_time=event_end_time,
                    is_always=is_always,
                    is_one_year=is_one_year,
                    week_day_cn=week_day_cn,
                    time_cn=time_cn)

    def _intermittent_real_start_time(self):
        """
        get intermittent real start time
        """
        assert self.event_time_type() == self.type_intermittent, \
               'get_intermittent, event_time_type ' \
               'need type_intermittent, type:%s' % \
               self.event_time_type()

        time_list = self.get_event_time_option()['time_list']
        time_dict = []
        for tdict in time_list:
            start = '%(day)s %(start_time)s' % tdict
            arrow_s = arrow.get(start)
            time_dict.append((arrow_s, start))

        # sort time by start time
        time_dict.sort(key=lambda x: x[0])

        cur_time = arrow.get(self.get_current_time())
        for time_item in time_dict:
            if cur_time < time_item[0]:
                return time_item[1]
        return None

    def _realtime_desc_in_week(self, start_time, cur_time):
        """
        Ture if start_time and cur_time in on week
        """
        start_time_dict = self.date_rule(start_time)
        time_str = '全天' if zero_time(start_time_dict) else \
                   time_to_iso(start_time_dict)
        if is_today(start_time, cur_time):
            return "今天 %s" % time_str
        if is_tomorrow(start_time, cur_time):
            return "明天 %s" % time_str
        if is_tswk(start_time, cur_time):
            return "本周%s %s" % (
                self._week_day(day_to_iso(start_time_dict),
                               week_prefix=False), time_str)
        return None

    def _realtime_desc_onday(self, start_time):
        """
        1. 如果时间为今天，则显示为「今天 10:00」 或 「今天 全天」 下同
        2. 如果时间为明天，则显示为「明天 10:00」
        3. 如果时间为本周，则显示为「本周三 10:00」
        4. 如果时间非本周，则显示具体日期「4月30日 17:00」
        """
        start_time_dict = self.date_rule(start_time)
        cur_time = self.get_current_time()
        desc = self._realtime_desc_in_week(start_time, cur_time)
        if desc:
            return desc
        day_cn = self._day_to_chinese(start_time_dict)
        time_str = '全天' if zero_time(start_time_dict) else \
                   time_to_iso(start_time_dict)
        return "%s %s" % (day_cn, time_str)

    def _realtime_desc_by_timetype_1(self):
        """
        by type_oneday

        使用onday规则
        """
        start_time = self.get_event_start_time()
        return self._realtime_desc_onday(start_time)

    def _realtime_desc_by_timetype_2(self, time_range=True):
        """
        by type_time_range

        1. 如果已经开始，则显示为「截止至5月10日」
        2. 如果未开始，且为本周内：
                1. 如果时间为今天，则显示为「今天 10:00」
                2. 如果时间为明天，则显示为「明天 10:00」
                3. 如果时间为本周，则显示为「本周三 10:00」
        3. 如果未开始，且为本月，但不为本周开始，则显示为「本月10日~20日」，
           如果时间延续到次月，显示为「5月10日~6月20日」
        4. 如果为0000-00-00:
                1. time_range则显示「随时」
                2. continue_day则显示为「每天 16:32」
        """
        start_time = self.get_event_start_time()
        start_time_dict = self.date_rule(start_time)
        cur_time = self.get_current_time()
        end_time = self.get_event_end_time()
        end_time_dict = self.date_rule(self.get_event_end_time())
        if always(day_to_iso(start_time_dict), day_to_iso(end_time_dict)):
            if time_range:
                return "随时"
            else:
                time_option = self.get_event_time_option()
                start_time = time_option.get('start_time', '00:00:00')
                start_time_dict = self.time_rule(start_time)
                return "每天 %s" % time_to_iso(start_time_dict)
        if self._is_event_start():
            return "截止至%s" % self._day_to_chinese(end_time_dict)
        if self._is_event_no_start():
            if is_tswk(start_time, cur_time):
                desc = self._realtime_desc_in_week(start_time, cur_time)
                if desc:
                    return desc
            if is_tsmh(start_time, cur_time) and \
                   is_tsmh(end_time, cur_time):
                return "本月%s日~%s日" % (
                    int(start_time_dict['day']),
                    int(end_time_dict['day']))
            desc = "%s~%s" % (self._day_to_chinese(start_time_dict),
                              self._day_to_chinese(end_time_dict))
            return desc

        day_cn = self._day_to_chinese(start_time_dict)
        return "%s %s" % (day_cn, time_to_iso(start_time_dict))

    def _realtime_desc_by_timetype_3(self):
        """
        by type_continue_day

        rule like timetype_2(type_time_range)
        """
        return self._realtime_desc_by_timetype_2(time_range=False)

    def _realtime_desc_by_timetype_4(self):
        """
        by type_week

        本周显示为 「本周四 18:30」，其余显示为 「每周四 18:30」
        """

        option = self.get_event_time_option()
        event_weekdays = option['event_weekdays']
        days = option['days']
        times = option['times']
        start_time = self.get_event_start_time()
        end_time = self.get_event_end_time()
        cur_week = is_tswk(start_time, self.get_current_time())
        next_week = is_nextweek(start_time, self.get_current_time())
        base_week_info = self._base_week_info(
            event_weekdays,
            days, times, check_event_time_range=False,
            cur_week=cur_week, next_week=next_week)            
        time_str = '全天' if zero_time(
            base_week_info['start_time_dict']) else \
            time_to_iso(base_week_info['start_time_dict'])
        week_cn = base_week_info['week_day_cn']
        return "%s %s" % (week_cn, time_str)

    def _realtime_desc_by_timetype_5(self):
        """
        by type_intermittent

        则取距离当前时间最近的一个时间,使用onday规则
        """
        start_time = self._intermittent_real_start_time()
        if not start_time:
            start_time = self.get_event_start_time()
        return self._realtime_desc_onday(start_time)

    #
    # Public Method
    #

    def dumps(self):
        """
        dump letd
        letd -- Leo Event Time Data
        return letd
        """
        # python 2.7 not auto process str and unicode, so use eval and str
        #return json.dumps(self._letd)
        return str(self._letd)

    def loads(self, letd):
        """

        Arguments:
        - `letd`: Leo Event Time Data
        """

        # python 2.7 not auto process str and unicode, so use eval and str
        #self._letd = json.loads(letd)
        self._letd = eval(letd)
        self._load_letd()

    def event_time_type(self):
        """
        return: event time type
        """
        return self._event_time_type

    def get_current_time(self):
        """
        get current time
        """
        return self._cur_time


    def get_event_start_time(self):
        """
        return: event start time
        """
        return self._event_start_time

    def get_event_end_time(self):
        """
        return: event end time
        """
        return self._event_end_time

    def get_event_time_desc(self):
        """
        return human-readable event time description
        """
        return self._leotime_desc

    def get_realtime_desc(self):
        """
        return human-readable realtime(current time) time description
        """
        time_type = self.event_time_type()
        func = '_realtime_desc_by_timetype_%s' % time_type
        if not hasattr(self, func):
            return ''
        return getattr(self, func)()

    def get_more_desc(self):
        """get more desc"""
        return self._more_desc

    def get_event_time_option(self):
        """
        return event time option

        oneday format:
        {
        'day': day,
        'start_time': start_time_option,
        'end_time': end_time_option
        }

        time_range format:
        {
        'start_time': start_time,
        'end_time': end_time
        }

        continue_day format:
        {
        'start_day': start_day,
        'end_day': end_day,
        'start_time': start_time,
        'end_time': end_time
        }

        week format:
        {
        'event_weekdays': event_weekdays,
        'days': days,
        'times': times
        }

        intermittent format:
        {'time_list': time_list}

        """
        return self._event_time_option

    def attach_more_desc(self, desc):
        """attach more desc"""

        self._more_desc = desc

    def make_oneday(self, day, start_time, end_time):
        """

        Arguments:
        - `day`: event day '2014-11-19'
        - `start_time`: begin time '09:30:00'
        - `end_time`: end time '22:30:32'

        desc: 11月19日 周三 09:30-22:30
              11月19日 周三 全天
        """

        day_dict = self.day_rule(day)
        start_time_dict, end_time_dict = self.time_rule(start_time, end_time)

        if None in (day_dict, start_time_dict, end_time_dict):
            return False

        option = {
            'day': day,
            'start_time': start_time,
            'end_time': end_time
            }

        day_cn = self._day_to_chinese(day_dict)
        week_day_cn = self._week_day(day)

        if zero_time(start_time_dict, end_time_dict):
            desc = '%s %s 全天' % (day_cn, week_day_cn)
            event_end_time = "%s %s" % (day_add(day, 1), end_time)
        else:
            desc = '%s %s %s-%s' % (day_cn,
                                    week_day_cn,
                                    time_to_iso(start_time_dict),
                                    time_to_iso(end_time_dict))
            event_end_time = "%s %s" % (day, end_time)

        event_start_time = "%s %s" % (day, start_time)

        self._letd = {
            'type' : self.type_oneday,
            'event_start_time' : event_start_time,
            'event_end_time' : event_end_time,
            'desc' : self._mk_desc(desc),
            'more_desc': self._more_desc,
            'option': option
            }
        self._load_letd()
        return True

    def make_time_range(self, start_time, end_time):
        """

        Arguments:
        - `start_time`: event start time '2014-11-19 09:30:32'
        - `end_time`: event end time '2014-11-30 22:30:00'

        desc: 11月19日 09:30 ~ 11月30日 22:30
              12月05日 ~ 2015年03月24日
              12月05日 16:00 ~ 2015年02月28日
              12月05日 ~ 2015年03月25日 08:21
              无时间限制
        """

        start_time_dict, end_time_dict = self.date_rule(start_time, end_time)

        if None in (start_time_dict, end_time_dict):
            return False

        option = {
            'start_time': start_time,
            'end_time': end_time
            }

        event_start_time = start_time
        event_end_time = end_time

        start_day = day_to_iso(start_time_dict)
        end_day = day_to_iso(end_time_dict)

        if always(start_day, end_day):
            desc = "无时间限制"
        else:
            if zero_time(start_time_dict):
                start_time_desc = ''
            else:
                start_time_desc = ' %s' % time_to_iso(start_time_dict)

            if zero_time(end_time_dict):
                end_time_desc = ''
                end_day_iso = day_to_iso(end_time_dict)
                end_day_cn = self._day_to_chinese(
                    self.day_rule(day_add(end_day_iso, -1)))
            else:
                end_time_desc = ' %s' % time_to_iso(end_time_dict)
                end_day_cn = self._day_to_chinese(end_time_dict)

            desc = '%s%s ~ %s%s' % (self._day_to_chinese(start_time_dict),
                                    start_time_desc,
                                    end_day_cn,
                                    end_time_desc)

        self._letd = {
            'type' : self.type_time_range,
            'event_start_time' : event_start_time,
            'event_end_time' : event_end_time,
            'desc' : self._mk_desc(desc),
            'more_desc': self._more_desc,
            'option': option
            }
        self._load_letd()
        return True

    def make_continue_day(self, start_day, end_day, start_time, end_time):
        """

        Arguments:
        - `start_day`: start day '2014-11-19'
        - `end_day`: end day '2015-3-30'
        - `start_time`: everyday start time '09:30:00'
        - `end_time`: everyday end time '22:30:32', not is '00:00:xx'

        desc: 11月19日 ~ 2015年3月30日 每天 09:30-22:30
              全年 每天 09:30-22:30
              每天 09:30-22:30
        """

        start_day_dict, end_day_dict = self.day_rule(start_day, end_day)
        start_time_dict, end_time_dict = self.time_rule(start_time, end_time)

        assert not zero_time(end_time_dict), \
               'continue day not end time is zero %s' % end_time

        if None in (start_day_dict, end_day_dict,
                    start_time_dict, end_time_dict):
            return False

        option = {
            'start_day': start_day,
            'end_day': end_day,
            'start_time': start_time,
            'end_time': end_time
            }

        event_start_time = '%s %s' % (start_day, start_time)
        event_end_time = '%s %s' % (end_day, end_time)

        if always(start_day, end_day):
            desc = "每天 %s-%s" % (time_to_iso(start_time_dict), \
                                   time_to_iso(end_time_dict))
            event_start_time = '0000-00-00 00:00:00'
            event_end_time = '0000-00-00 00:00:00'
        elif one_year(start_day, end_day):
            desc = "全年 每天 %s-%s" % (time_to_iso(start_time_dict), \
                                        time_to_iso(end_time_dict))
        else:
            desc = '%s ~ %s 每天 %s-%s' % (
                self._day_to_chinese(start_day_dict),
                self._day_to_chinese(end_day_dict),
                time_to_iso(start_time_dict),
                time_to_iso(end_time_dict))

        self._letd = {
            'type' : self.type_continue_day,
            'event_start_time' : event_start_time,
            'event_end_time' : event_end_time,
            'desc' : self._mk_desc(desc),
            'more_desc': self._more_desc,
            'option': option
            }
        self._load_letd()
        return True

    def make_week(self, event_weekdays, days, times):
        """

        Arguments:
        - `event_weekdays`: 0-6, event day on week,
                            week_wed week_sun event is [0, 3, 6]
        - `days`: event range start and end day ['2014-11-19', '2015-1-30']
        - `times`: everyday start and end time ['09:30', '22:30']

        desc: 11月19日 ~ 2015年1月30日 每周三，日 09:30-22:30
              11月19日 ~ 2015年1月30日 每周三，日 全天
              全年 每周四 10:30-21:00
              每周四 10:30-21:00
        """

        base_week_info = self._base_week_info(event_weekdays, days, times)
        if base_week_info is None:
            return False

        if base_week_info['is_always']:
            desc = "%s %s" % (base_week_info['week_day_cn'],
                              base_week_info['time_cn'])
            base_week_info['event_start_time'] = '0000-00-00 00:00:00'
            base_week_info['event_end_time'] = '0000-00-00 00:00:00'
        elif base_week_info['is_one_year']:
            desc = "全年 %s %s" % (
                base_week_info['week_day_cn'],
                base_week_info['time_cn'])
            if zero_time(base_week_info['end_time_dict']):
                base_week_info['event_end_time'] = '%s 00:00:00' % day_add( \
                    day_to_iso(base_week_info['end_day_dict']), 1)
        else:
            if zero_time(base_week_info['end_time_dict']):
                end_day_iso = day_to_iso(base_week_info['end_day_dict'])
                base_week_info['end_day_cn'] = self._day_to_chinese(
                    self.day_rule(day_add(end_day_iso, -1)))
            else:
                base_week_info['end_day_cn'] = self._day_to_chinese(
                    base_week_info['end_day_dict'])

            desc = '%s ~ %s %s %s' % (
                self._day_to_chinese(base_week_info['start_day_dict']),
                base_week_info['end_day_cn'],
                base_week_info['week_day_cn'], base_week_info['time_cn'])
        self._letd = {
            'type': self.type_week,
            'event_start_time': base_week_info['event_start_time'],
            'event_end_time': base_week_info['event_end_time'],
            'desc' : self._mk_desc(desc),
            'more_desc': self._more_desc,
            'option': {'event_weekdays': event_weekdays,
                       'days': days,
                       'times': times}
            }
        self._load_letd()
        return True

    def make_intermittent(self, time_list):
        """

        Arguments:
        - `time_list`: event time list,
            [
            {'day': '2013-03-20', 'start_time': '12:32:36',
            'end_time': '22:30:30'},

            {'day': '2014-05-28', 'start_time': '00:00:00',
            'end_time': '00:00:00'},

            {'day': '2014-08-29', 'start_time': '02:32:36',
            'end_time': '12:30:30'},
            ]

        desc: 2013年03月20日 12:32-22:30、08月29日 02:32-12:30、05月28日
              11月19日、11月30日、2015年12月05日
        """
        time_dict = []
        for tdict in time_list:
            start = '%(day)s %(start_time)s' % tdict
            end = '%(day)s %(end_time)s' % tdict
            tdict = self.date_rule(start, end)
            if None in tdict:
                return False
            arrow_s = arrow.get(start)
            arrow_e = arrow.get(end)
            time_dict.append(((arrow_s, tdict[0], start),
                              (arrow_e, tdict[1], end)))

        # sort time by start time
        time_dict.sort(key=lambda x: x[0][0])
        event_start_time = time_dict[0][0][2]
        if zero_time(time_dict[-1][1][1]):
            event_end_time = '%s 00:00:00' % day_add(time_dict[-1][1][2], 1)
        else:
            event_end_time = time_dict[-1][1][2]

        desc_list = []
        for time_d in time_dict:
            day_cn = self._day_to_chinese(time_d[0][1])
            sdict = time_d[0][1]
            edict = time_d[1][1]
            if zero_time(sdict, edict):
                desc_list.append(day_cn)
            else:
                desc_list.append('%s %s-%s' % (day_cn,
                                               time_to_iso(sdict),
                                               time_to_iso(edict)))
        self._letd = {
            'type' : self.type_intermittent,
            'event_start_time' : event_start_time,
            'event_end_time' : event_end_time,
            'desc' : self._mk_desc('、'.join(desc_list)),
            'more_desc': self._more_desc,
            'option': {'time_list': time_list}
            }
        self._load_letd()
        return True
