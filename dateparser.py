'''
It should be a function that receives: weekday, day number, month, year, hour, minute, second
quarter, timezone, special
all the other have None value as default

it manages deterministic dates. They could be relative days (i.e. in two months and 5 days),
absolute (i.e. January 2024, 2024-05-02 09:35 Central Time)
or special (Special.LATER, Special.WEEKEND, Special.TONIGHT)


SUGGESTIONS
Another function tries to find alternatives for text input. It should manage languages.
Alternatives are deterministic for the previous function
If you write week it suggests "next week", "in two weeks" or "weekend"
If you write "tw" it suggests matches with "Two", "Twenty", "twentieth", "twelve" or "twelfth"
If you write "01-06" it suggests June 1st or January 6th depending on your language

MAKE LOT OF TESTS
'''
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import locale as lc
import json

import unicodedata
import re


TODAY = 'TODAY'
WEEKEND = 'WEEKEND'
TONIGHT = 'TONIGHT'
TOMORROW = 'TOMORROW'
NEXT_WEEK = 'NEXT_WEEK'
NEXT_MONTH = 'NEXT_MONTH'
NEXT_QUARTER = 'NEXT_QUARTER'
NEXT_YEAR = 'NEXT_YEAR'
LATER_TONIGHT = 'LATER_TONIGHT'

DEFAULT_HOUR = 9
TONIGHT_TIME = 20
END_OF_DAY_TIME = 17

DAYS = 'days'
DAY = 'day'
WEEKDAY = 'weekday'
MONTH = 'month'
QUARTER = 'quarter'
WEEKS = 'weeks'
MONTHS = 'months'
YEARS =  'years'
HOUR = 'hour'
HOURS = 'hours'
# next X hours but minute = 0
HOURS_NO_MIN = 'hours-no-min'
TIMEZONE = 'timezone'
AM_PM = ['am', 'pm', 'a.m.', 'p.m.', 'a.m', 'p.m', 'am.', 'pm.', 'a', 'p']
ORDINALS = ['st', 'nd', 'rd', 'th']
SEPARATORS = ['/', '-', '\\', '–']

# TODO: 2 hours // 30 minutes (or mins)
# TODO: 2h // 30m 
# TODO: 1 wk or 1 week
# TODO: 2 mo

with open("glossary.json", "r") as read_file:
    GLOSSARY = json.load(open("glossary.json", "r"))


'''Return text without accents (á, ä, â, ñ, ç) and in lowercase.'''
def normalize(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()


def find_pos_in_glossary(phrase, kind, language="en"):
    glossary = GLOSSARY[language]
    phrase = phrase.split(" ")
    kind_words = [x['target'] for x in glossary if kind in [y['type'] for y in x['result']]]
    for size in range(3, 0, -1):
        formatted_phrase = []
        for i in range(len(phrase) - size + 1):
            formatted_phrase.append(' '.join(phrase[i:i+size]))
        # stop looking at len(words) - size, so if there are 10 words you can only look up to 8th word for a 3 words prhase
        for i, word in enumerate(formatted_phrase):
            if word in kind_words:
                return i
    return None

def find_exact_in_glossary(text, kind, language="en"):
    words = text.split(" ")
    glossary = GLOSSARY[language]
    kind_words = [x['target'] for x in glossary if kind in [y['type'] for y in x['result']]]
    for pos, word in enumerate(words):
        if word in kind_words:
            return pos
    
    return None

'''Return the position of month and year in locale.

This should be done with locale.nl_langinfo but isn't available on Windows.
Args:
    locale (string): locale
Returns:
    (int, int): position of month and year in locale
'''
def get_locale_monthdate(locale):
    lc.setlocale(lc.LC_ALL, locale)
    MONTH = 8
    DAY = 6
    test_date = datetime(2023,MONTH,DAY)
    test = test_date.strftime('%x')
    separator = [x for x in test if not x.isdigit()][0]
    date_array = test.split(separator)
    day = None
    month = None
    for i, val in enumerate(date_array):
        if int(val) == DAY:
            day = i
        elif int(val) == MONTH:
            month = i
    return (month, day)

def can_be_year(year, base_date):
    if isinstance(year, str):
        if year.isdigit():
            year = int(year)
        else:
            return None
    if year < 100:
        year = year + 2000
    return year >= base_date.year and year <= base_date.year + 10

def can_be_day(day):
    if isinstance(day, str):
        if day.isdigit():
            day = int(day)
        else:
            return None
    return day < 32


def can_be_month(month):
    if isinstance(month, str):
        if month.isdigit():
            month = int(month)
        else:
            return None
    return month < 13

def can_be_hour(hour):
    if isinstance(hour, str):
        if hour.isdigit():
            hour = int(hour)
        else:
            return None
    return hour < 24

def can_be_minute(minute):
    if isinstance(minute, str):
        if minute.isdigit():
            minute = int(minute)
        else:
            return None
    return minute < 60



''' Return the next weekday after the input date

Args:
    date (datetime): base date
    weekday (int): 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
Returns:
    datetime: next weekday after the input date
'''
def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days=days_ahead)

''' Return a datetime in the future based on the input params.

It's a mix between datetime() and relative delta that allows some flexibility, you can leave blank 
parameters and there are some specials as quarters

Args:
    weekday (int): 0 for Monday, 1 for Tuesday, ..., 6 for Sunday

    hour (int): hour of the day (0-23)
    year (int): year
    month (int): month of the year (1-12)
    quarter (int): 1 for first quarter, 2 for second quarter, 3 for third quarter, 4 for fourth quarter
    
    years (int): number of years in the future
    quarters (int): number of quarters in the future
    months (int): number of months in the future
    weeks (int): number of weeks in the future
    days (int): number of days in the future
    hours (int): number of hours in the future
    minutes (int): number of minutes in the future
    seconds (int): number of seconds in the future

    special (special): Special.LATER, Special.WEEKEND, Special.TONIGHT, Special.TOMORROW,
        Special.NEXT_WEEK, Special.NEXT_MONTH, Special.NEXT_QUARTER, Special.NEXT_YEAR
    base_date (datetime): base date to calculate the future date. It should be always blank so it
        takes current datetime, but it is useful for testing
    
    locale_timezone (timezone): timezone of the base_date
    timezone (timezone): timezone of the result
Returns:
    datetime: future datetime
'''
def future_datetime(weekday=None, weeks=0, day_number=None, days=0, month=None, months=0, 
    year=None, years=0, hour=None, hours=0, minute=None, minutes=0, second=None, seconds=0, 
    quarter=None, timezone=None, special=None, base_date=None, locale_timezone=None,
    quarters=0):

    # if it is a special day it doesn't consider any other information about date
    
    # if it has relative days, it doesn't consider any other information about date

    # if it is not special nor relative, calculation will be different depending on
    # whether there is a weekday or not.
    
    # WEEKDAY: If there is only a weekday it looks for the next weekday, but if you have another date unit
    # (day, month, year), you have to check the period when all conditions get satisfied
    # i.e. if you ask for Monday 3rd January 2024, it returns 3rd January 2024 if it is Monday

    # NO WEEKDAY: If there is no weekday, it looks for the first date that satisfies the conditions
    # The logic for the absent date parts depends on whether there is a greater date part
    # if there is a greater date part it is the first value
    # i.e. you have year but not day_number nor month, day_number and month are 1st of January
    # i.e. you have month but not day_number, day_number is 1st of that month
    # if there is not a greater date part is current value (base_date value)
    # or the next one if current value of the lesser date parts is before base_date
    # i.e. if it is 10th of January and you ask for 15th (without month or year), it is 15th of January
    # but if it is 20th of January and you ask for 15th it is 15th of February
    # idem for months and years, if it is July and you ask for October without year will be same year
    # but if you as for March will be March next year

    # check if there is nothing to calculate, it returns None
    if (weekday is None and weeks == 0 and day_number is None and days == 0 and month is None and months == 0
            and year is None and years == 0 and hour is None and hours == 0 and minute is None and minutes == 0
            and second is None and seconds == 0 and quarter is None and quarters == 0 and special is None):
        
        return None 

    HOURS_LATER = 4
    if base_date is None:
        base_date = datetime.now(locale_timezone)
    
    if timezone is None:
        timezone = locale_timezone

    base_weekday = base_date.weekday()
    base_month = base_date.month
    base_year = base_date.year
    
    # if hour is not set in params it is 9 am (DEFAULT_HOUR)
    hour_was_none = hour is None
    if hour is None:
        hour = DEFAULT_HOUR
    if minute is None:
        minute = 0
    if second is None:
        second = 0
    
    # if I have a special value I don't have to calculate anything else
    if special is not None:
        
        if special == TODAY:
            minute = 0
            second = 0
            if hour_was_none:
                if base_date.hour < 12:
                    hour = 12
                elif base_date.hour < 17:
                    hour = 17
                elif base_date.hour < 21:
                    hour = 21
                else:
                    hour = 23
                    minute = 59
            return (base_date.replace(minute=0, second=0, microsecond=0)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif special == WEEKEND:
            # if it is weekend (Saturday or Sunday), add two days to current day so it is on a laborable day
            if base_date.day >= 5:
                base_date = base_date + relativedelta(days=2)
            # calculate next Saturday
            result = next_weekday(base_date, 5)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif special == TONIGHT:
            if base_date.hour < 20:
                return base_date.replace(hour=TONIGHT_TIME, minute=0, second=0, microsecond=0)
            else:
                return None
        elif special == LATER_TONIGHT:

            if base_date.hour < TONIGHT_TIME - HOURS_LATER:
                return base_date.replace(hour=TONIGHT_TIME, minute=0, second=0, microsecond=0)
            else:
                return (base_date + relativedelta(hours=HOURS_LATER)).replace(minute=0, second=0)
        elif special == TOMORROW:
            return (base_date + timedelta(days=1)).replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif special == NEXT_WEEK:
            # next Monday, if today is Monday next week Monday (today + 7 days)
            result = next_weekday(base_date, 0) if base_weekday > 0 else base_date + relativedelta(days=7)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif special == NEXT_MONTH:
            result = base_date.replace(day=1) + relativedelta(months=1)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif special == NEXT_QUARTER:
            # this quarter start date + 3 months
            result = base_date.replace(month=base_month // 3 * 3  + 1, day=1) + relativedelta(months=3)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif special == NEXT_YEAR:
            result = base_date.replace(month=1, day=1) + relativedelta(years=1)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)

    # if I have relative quarters I translate it to relative months (get start of this quarter and
    # add quarters * 3)
    if quarters > 0:
        months = quarters * 3 - (base_month - 1) % 3
        day_number = 1

    # calculate if there isn't any relative date part
    if years == 0 and months == 0 and days == 0 and hours == 0 and minutes == 0 and seconds == 0 and weeks == 0 and quarters == 0:
        
        if weekday is not None:
        # only weekday, just look for next weekday
            if day_number is None and month is None and year is None:
                return next_weekday(base_date + relativedelta(days=1), weekday).replace(hour=hour, minute=minute, second=second, microsecond=0)
            
            # if day number, month and year are present have to check if that date has the same weekday and if it is in the future
            # i.e. 15th January 2024 is Monday, so if you ask for Monday 2024-01-15 it returns that day, but if you as for 
            # Tuesday 2024-01-15 it returns None
            elif day_number is not None and month is not None and year is not None:
                result = datetime(year, month, day_number, hour, minute, second, microsecond=0)
                if result.weekday() == weekday and result > base_date:
                    return result
                else:
                    return None
                
            # you have day number may be year, may be month, may be neither, but not both year and month
            # i.e. Monday 3rd (get next 3rd that is on Monday)
            # i.e. Monday 3rd January (get next 3rd January that is on Monday, for example 2022 or 2028)
            # i.e. Monday 3rd 2024 (get next day 3rd in 2024 that is on Monday, first Monday 3rd in the year is June)

            # you have to try advancing month by month or year by year until to you find a coincidence
            elif day_number is not None:
                # initial month is base month or the month you input
                start_month = base_month
                if month is not None:
                    start_month = month
                # initial year is base year or the year you input
                start_year = base_year
                if year is not None:
                    start_year = year
                try_date = datetime(start_year, start_month, day_number, hour=hour, minute=minute, second=second)

                # if the date is before the base date, it has to be the next month (or next year if month is not blank)
                if try_date < base_date:
                    if month is None:
                        try_date = try_date + relativedelta(months=1)
                    else:
                        try_date = try_date + relativedelta(years=1)
                
                stop_year = 99999
                if year is not None:
                    stop_year = year
                plus_months = 0
                plus_years = 0

                # if month is empty try month by month
                if month is None:
                    plus_months = 1
                else:
                    # if month is not empty try year by year
                    plus_years = 1

                # try advancing month or year until you find the weekday or year is ahead of input year            
                while try_date.weekday() != weekday and stop_year >= try_date.year:
                    try_date = try_date + relativedelta(months=plus_months, years=plus_years)
                
                if try_date.weekday() == weekday:
                    return try_date
                else:
                    return None
            
            # month but not day_number (and may be year)
            elif month is not None:

                start_date = base_date
                # if year is empty, could be this year or next year
                if year is  None:
                    # if month is not current month, it starts on 1st day of that month
                    if month != base_month:
                        start_date = datetime(base_year, month, 1, hour, minute, second)
                        # if year is empty and month is before current month, it has to be same month next year
                        if start_date < base_date:
                            start_date = start_date + relativedelta(years=1)
                else:
                    # if year is present, it starts on 1st day of that month-year
                    start_date = datetime(year, month, 1, hour, minute, second)
                    
                    # if it is current month-year it starts on current day
                    if start_date.year == base_date.year:
                        if start_date.month == base_date.month:
                            start_date = base_date
                    # if it is previous year returns None
                    elif start_date.year < base_date.year:
                        return None
                    
                result = next_weekday(start_date, weekday)

                if result.month == month:
                    return result
                else:
                    # it is a weekday after the last weekday in that month, so it looks for the first weekday same month next year
                    if year is None:
                        return next_weekday(start_date.replace(day=1) + relativedelta(years=1), weekday)
                    # if it is a weekday after the last weekday in that month, and year is present, it returns None
                    else:
                        return None

            # only year
            elif year is not None:
                start_date = base_date
                if year > base_year:
                    start_date = datetime(year, 1, 1, hour, minute, second)
                elif year < base_year:
                    return None
                elif weekday == start_date.weekday() and hour < start_date.hour:
                    start_date = start_date + relativedelta(days=1)
                
                result = next_weekday(start_date, weekday)
                if result.year == year:
                    return result
                else:
                    # it is a weekday after last weekday on the year
                    return None
        ### Here finished weekday is Not None ###

        # ********* weekday is blank *************

        plus_day = 0
        plus_month = 0
        plus_year = 0
        day_was_none = day_number is None

        # First I set day, which is in the params, or is base_date day or 1st day of month
        # if I don't have a day_number and I have a greater unit (month, year, quarter) I have to start on 1st day of that unit
        # if I don't have a greater unit, I have to start on current day, or may be tomorrow if hour is before base_hour
        if day_number is None:
            if month is not None or quarter is not None or year is not None:
                day_number = 1
            else:
                day_number = base_date.day
                # if I add 1 day to day_number, it could be after last_day of month
                # As last_day of month depends on the year (because of leap years)
                # I check that after setting month and year
                if hour is not None and hour <= base_date.hour:
                    plus_day = 1
        
        # then I set month, which is in the params, or is base_date month or is 1st month of year or quarter
        # if I don't have a month and I have a year I have to start on first month of that year
        # if I don't have a month and I have a quarter, I have to calculate which is the first month of that quarter
        # if I don't have a month nor any greater unit it should be current month, except day_number
        # is before base_day_number, in which case it should be next month
        month_was_none = month is None
        if month is None:
            if quarter is not None:
                month = (quarter - 1) * 3 + 1
            elif year is not None:
                month = 1
            else:
                month = base_month
                if day_number < base_date.day:
                    plus_month = 1
            
        # if I don't have a year it should be current year, EXCEPT:
        # if month is before base_month or month equals base_month and day_number is before base_day_number
        # in that case it should be next year
        year_was_none = year is None
        if year is None:
            year = base_year
            if (not month_was_none or quarter is not None) and (month < base_month or (month == base_month and day_number < base_date.day)):
                plus_year = 1

        if day_number > 31:
            return None

        if month > 12:
            return None
        
        # *** FIX MONTH ****
        # if after adding a month new month is 13 or more, I have to calculate modulo between new month and 12
        # and add years as the integer part between new month divided by 12
        # i.e. month = 11 + plus_month=4, new_month = (11 + 4) % 12 = 3, plus_year = 1

        # as month is 1-based instead of 0-based I have to convert it to 0-based (substract 1) and then back to 1-based (add 1)
        # so I can use the modulo properly
        new_month = (month - 1 + plus_month) % 12 + 1
        # as month is 1-based instead of 0-based I have to convert it to 0-based (substract 1) to use // 12 properly to get years to add
        new_year = year + plus_year + (month - 1 + plus_month) // 12

        
        # *** FIX DAY ***

        # if my new date is 29, 30 or 31 in a month that doesn't have that day, or it is the last day of the month and hour is before base_hour 
        # I have to add: a month if month was none, or a day if month was present, or a year if month and day are present.
        # I have to do it up to date is consistent
        # This could be the case when you ask for a 29 Feb in Jun 2024, it will add a year until it gets year 2028
        # or if you are on 31st August 7 pm and you ask for 31st 5 pm, it will add a month and will get September 31st
        # so it has to add another month in order to get October 31st
        
        first_day_temp = datetime(new_year, new_month, 1)
        max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
            
        if max_day < day_number or (max_day == day_number and datetime(year, month, day_number, hour, minute, second) <= base_date):
            while True:
                # if day, nor month nor year are present then you add a day
                # (I think this case is never used)
                # Example: 6 pm and now is 8 pm, you have to add a day
                if day_was_none and month_was_none and year_was_none:
                    plus_day = plus_day + 1
                    first_day_temp = first_day_temp + relativedelta(days=1)    
                    max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
                # if month is not present you can add a month
                # Example: 30th of June and you ask for 31st, you have to add a month to get July
                # Example: 31st August 8 pm and you ask for 31st 10 am, you have to add a monther to see if next month has 31
                # Example: 31st December 8 pm and you ask for 31st 10 am, you have to add a month to see if next month (January next year) has 31
                elif month_was_none:
                    plus_month = plus_month + 1
                    first_day_temp = first_day_temp + relativedelta(months=1)    
                    max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
                # if year is not present you can add a year
                # Example: 15th March 2024 and you ask for 29th of February, you have to add year so you test if next year is leap
                elif year_was_none:
                    plus_year = plus_year + 1
                    first_day_temp = first_day_temp + relativedelta(years=1)
                    max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
                
                if max_day >= day_number:
                    break
        
        day_number = day_number + plus_day
        year = year + plus_year + (month - 1 + plus_month) // 12
        month = (month - 1 + plus_month) % 12 + 1

    # print("hours", hours, "hour", hour, "minutes", minutes, "minute", minute, "seconds", seconds, "second", second)
    if year is None:
        year = base_year
    if month is None:
        month = base_month
    if day_number is None:
        day_number = base_date.day
    if hour is None:
        hour = base_date.hour
    if minute is None:
        minute = base_date.minute
    if second is None:
        second = base_date.second
    
    # print(year, month, day_number, hour, minute, second, years, months, days, weeks, hours, minutes, seconds)
    result = datetime(year, month, day_number, hour, minute, second, microsecond=0, tzinfo=timezone) + relativedelta(years=years, 
        months=months, days=days, weeks=weeks, hours=hours, minutes=minutes, seconds=seconds)
    if  result > base_date:
        return result
    else:
        return None
    
''' Try to convert a natural language text into a datetime.

Args:
    text: text to parse
    language: language of the text
    base_date: base date to calculate the future date. It should be always blank so it takes current datetime, but it is useful for testing
    locale_timezone: timezone of the base_date
    locale: locale of the base_date
Returns:
    datetime: future datetime or None if it can't parse
'''
def parse(text, language='en', base_date=None, locale_timezone=None, locale="en_US"):
    if base_date is None:
        base_date = datetime.now()

    if base_date.tzinfo is None and locale_timezone is not None:
        base_date = base_date.replace(tzinfo=locale_timezone)

    month_pos, day_pos = get_locale_monthdate(locale)

    text = normalize(text)
    words = text.split(" ")
    results = []
    
    timezone = None
    years = 0
    months = 0
    days = 0
    hours = 0
    minutes = 0
    weeks = 0
    quarters = 0

    special = None
    year = None
    month = None
    day_number = None
    weekday = None
    hour = None
    minute = None
    second = None
    quarter = None

    #### FIND NUMBERS AND LETTERS (1w, 2mo, 3d, 4h, 5m, 6mins) ######
    # replace with number and word for easier parsing
    for i, word in enumerate(words):
        if word[0].isdigit() and word[-1].isalpha() and not word.endswith(tuple(AM_PM)):
            last_digit = 0
            for i in reversed(range(len(word))):
                if word[i].isdigit():
                    last_digit = i
                    break
            
            number = int(word[:last_digit+1])
            letters = word[last_digit+1:]
            
            relative_word = words_to_datepart(letters, language, filter=["relative"])
            
            if relative_word is not None:
                new_word = str(number) + ' ' + relative_word['result'][0]['value']
                text = re.sub(r'\b' + word + r'\b', new_word, text)
                words = text.split(" ")

    
    ### FIND RELATIVE ###
    # first occurrence of "in" word
    start = find_pos_in_glossary(text, 'in', language)
    
    # first occurence of relative word
    if start is None:
        first_relative = find_exact_in_glossary(text, 'relative', language)
        
        # first relative minus one because number is before the first relative word
        if first_relative is not None:
            first_relative = first_relative - 1
            first_word = words[first_relative]
            if words_to_datepart(first_word, language, filter=["number"]) is not None or first_word.isdigit():
                start = first_relative
    
    # if there is an "in" phrase or a relative word, it has to be a relative date, it only looks for possible relative phrase
    # with two periods max (i.e. "in 2 days and 3 hours" but not "in a month, 2 days and 3 hours")
    if start is not None:
        #in_phrase is the maximum length for an in phrase (i.e. "in 2 days and an hour", 6 words)
        
        in_phrase = words[start: start+6]
        
        # replace "a" and "an" with 1
        # replace "one" with 1, "two" with 2 ... "fifteen" with 15
        for i, word in enumerate(in_phrase):
            result = words_to_datepart(word, language, filter=["number"])
            if result is not None:
                in_phrase[i] = str(result['result'][0]['value'])

        
        relatives = {}
        
        # tries to find relative period words and assign previous word as value
        # i.e. "in 2 days and 3 hours" -> {'days': 2, 'hours': 3}
        for i, word in enumerate(in_phrase):
            result = words_to_datepart(word, language, filter=["relative"])
            if result is not None:
                relatives[result['result'][0]['value']] = in_phrase[i-1]
        
        # after getting relative values it assigns them to the corresponding variable
        hours = int(relatives['hours']) if 'hours' in relatives else 0
        minutes = int(relatives['minutes']) if 'minutes' in relatives else 0
        years = int(relatives['years']) if 'years' in relatives else 0
        months = int(relatives['months']) if 'months' in relatives else 0
        days = int(relatives['days']) if 'days' in relatives else 0
        weeks = int(relatives['weeks']) if 'weeks' in relatives else 0
        quarters = int(relatives['quarters']) if 'quarters' in relatives else 0
        weeks = int(relatives['fortnights']) * 2 if 'fortnights' in relatives else weeks

        if hours == 0 and minutes == 0:
            hour = DEFAULT_HOUR
        else:
            hour = base_date.hour
            # if minutes > 0:
            minute = base_date.minute
    
    else:


        #### FIND WORDS ######
        # find words that are in the glossary and assign them to the corresponding variable
        # i.e. january -> month = 1, afternoon -> hour = 15

        # start looking for 3 words phrases, then 2 words phrases and finally 1 word
        for size in range(3, 0, -1):
            # stop looking at len(words) - size, so if there are 10 words you can only look up to 8th word for a 3 words prhase
            for i in range(len(words) - size + 1):
                # print(f"Position {i} of {len(words)-size}. Word:")
                word = ' '.join(words[i:i+size])
                # conditional to avoid looking for erased words
                if words[i] is not None:
                    # print(words[i:i+size])
                    result = words_to_datepart(word, language)
                    
                    if result is not None:
                        for x in result['result']:
                            results.append(x)
                        # set words to None so they aren't considered again
                        words[i:i+size] = [None] * size
                    else:
                        #### FIND TIMEZONE ONLY AT THE END ###
                        if i == len(words) - size:
                            if tz := get_timezone(word): 
                                timezone = tz
                                
                                words[i:i+size] = [None] * size

            
            # remove empty words (erased words because they are part of a phrase)
            words[:] =  (value for value in words if value != None)
        
        for r in results:
            if r['type'] == 'special':
                if special is None:
                    special = r['value']
                else:
                    return None
            elif r['type'] == DAYS:
                if days == 0:
                    days = r['value']
                else:
                    return None
            elif r['type'] == WEEKDAY:
                weekday = r['value']
            elif r['type'] == DAY:
                day_number = r['value']
            elif r['type'] == MONTH:
                month = r['value']
            elif r['type'] == QUARTER:
                quarter = r['value']
            elif r['type'] == WEEKS:
                weeks = r['value']
                weekday = 0
                hour = DEFAULT_HOUR
                minute = 0
                second = 0
            elif r['type'] == MONTHS:
                months = r['value']
                day_number = 1
                hour = DEFAULT_HOUR
                minute = 0
                second = 0
            elif r['type'] == YEARS:
                years = r['value']
                month = 1
                day_number = 1
                hour = DEFAULT_HOUR
                minute = 0
                second = 0
            elif r['type'] == HOUR:
                hour = r['value']            
            elif r['type'] == HOURS:
                hours = r['value']
                hour = base_date.hour
                minute = base_date.minute
                second = base_date.second
            elif r['type'] == HOURS_NO_MIN:
                hours = r['value']
                hour = base_date.hour
                minute = 0
                second = 0
            elif r['type'] == TIMEZONE:
                timezone = pytz.timezone(r['value'])

        # check if am or pm is separated from the time. If it is, join them
        for i in range(1, len(words)):
            if words[i] in AM_PM:
                words[i-1] = words[i-1] + words[i]
                words[i] = None
            
        # remove empty words (erased am/pm)
        words[:] =  (value for value in words if value != None)

        ##### FIND DATE PARTS THAT HAVE NUMBER IN THEM #####
        # i.e. 1st, 3rd, 5th for day, time separated by colon, dates separated by slashes or dashes
        # time in military format or quarter like q1, q2, q3, q4
        for pos, word in enumerate(words):

            #### FIND DAY WITH ORDINALS ######    
            # 1st = day 1, 5th = day 5, 31st = day 31
            if word[0].isdigit() and word[-2:] in ORDINALS:
                number = word[:-2]
                try:
                    day_number = int(number)
                    continue
                except ValueError:
                    return None
            
            #### FIND HOUR with semicolon, am or pm ######
            # 1:00 = 1 am, 1:14pm = 13:15, 1:00a.m. = 1 am, 1:00p.m. = 1 pm

            # if we don't have am or pm, we guess it is am
            new_hour, new_minute, new_second = get_time(word)

            if new_hour is not None:
                hour = new_hour
            if new_minute is not None:
                minute = new_minute
            if new_second is not None:
                second = new_second
            
            #### FIND YEAR ######
            # uses can_be_year function (if word is 4 digits and is between this year and this year + 10)
            # 2024 = year 2024
            if len(word) == 4 and word.isdigit():
                maybe_year = int(word)
                if can_be_year(maybe_year, base_date):
                    year = int(word)
                    continue

            #### FIND HOUR MILITARY FORMAT #####
            # 0830 = 08:30, 1600 = 16:00
            if len(word) == 4 and word.isdigit():
                hour = int(word[:2])
                minute = int(word[2:])
                if not can_be_hour(hour) or not can_be_minute(minute):
                    return None
                continue

            # #### FIND TIME BEFORE 12 WITHOUT AM/PM #####
            # if word.isdigit() and int(word) < 13:
            #     hour = int(word)
            #     continue

            #### FIND QUARTER ######
            # if starts with "q" and then a number between 1 and 4
            if word[0] == 'q' and word[1:].isdigit():
                quarter = int(word[1:])
                if quarter > 4 or quarter < 1:
                    return None
                continue
        

            #### FIND DATE SEPARATED BY DASH OR SLASH ######
            separator = None
            for char in word:
                if char in SEPARATORS:
                    separator = char
                    break
            
            # print(separator)
            if separator is not None:
                date_array = word.split(separator)
                year_is_in = None
                month_is_in = None
                day_is_in = None
                
                # year is at the beginning and it has 4 digits
                if len(date_array[0]) == 4 and date_array[0].isdigit():
                    year_is_in = 0
                    if len(date_array) == 3:
                        month_is_in = 1
                        day_is_in = 2
                # year is at the end (it could be a two part or three part date) and it has 4 digits
                elif len(date_array[-1]) == 4 and date_array[-1].isdigit():
                    year_is_in = len(date_array) - 1
                

                # GET MONTH IF IT IS NOT DIGIT
                for i, part in enumerate(date_array):
                    if not part.isdigit():
                        month_is_in = i
                        break
                
                # GET THE MONTH IF IS A TWO-PART ARRAY AND ALREADY HAVE YEAR
                if month_is_in is None and year_is_in is not None and len(date_array) == 2:
                    month_is_in = list({0,1} - {year_is_in})[0]

                # GET DAY IF IT IS A 3-PART DATE AND ALREADY HAVE YEAR AND MONTH
                if month_is_in is not None and year_is_in is not None and len(date_array) == 3:
                    day_is_in = list({0,1,2} - {year_is_in, month_is_in})[0]

                # Until here I get these options in a complete form:
                # two parts date: yyyy-mm or mm-yyyy
                # three parts date: yyyy and month in a string format, day by discarding

                # print("year is in, month is in, day is in", year_is_in, month_is_in, day_is_in)

                # if I still miss a param it could be that I got only the year or only the month
                if (year_is_in is not None) + (month_is_in is not None) + (day_is_in is not None) < len(date_array):

                    # If I know the month could be Nov-24 (month and day or month and year) or 05-Nov-24 (or any other combination of 3 parts)
                    if month_is_in is not None:
                        
                        # if it is a two-parts date the other part is the day if it is less than 32
                        # this could be an ambiguity: Nov-24 could be 24th of November or 2024-11-01, I assume it is 24th of November
                        # but Nov-33 it is 2033-11-01
                        if len(date_array) == 2:
                            # get the other value that is not month
                            value = date_array[not month_is_in]
                            if value.isdigit():
                                value = int(value)
                                if value < 32:
                                    day_is_in = not month_is_in
                                else:
                                    value = value + 2000
                                    if value >= base_date.year and value <= base_date.year + 10:
                                        year_is_in = i
                        else:
                            # if it is a three-parts date, I have to see which of the others could be a year. If it is not a year the other could be the day
                            for i, part in enumerate(date_array):
                                if i != month_is_in and part.isdigit():
                                    part = int(part)
                                    if year_is_in is None and can_be_year(part, base_date):
                                        year_is_in = i
                                    else:
                                        if can_be_day(part):
                                            day_is_in = i
                            
                    # if month is not on a string format it is more difficult, we can have next options:
                    
                    # 1. Two-parts date:
                    # 1.a year and month
                    # 1.b month and day (preferred value, if you have 24-11 it is 24th of November and not 2024-11-01)
                    # 1.c year and day is not an option (24-31 could be 2031-01-24 or 2024-01-31 but it is not natural)
                    
                    # 2. Three-parts date: in that case I have to check locale format
                    
                    else:
                        
                        if len(date_array) == 2:
                            can_have_month = date_array[0].isdigit() and (can_be_month(date_array[0]) or can_be_month(date_array[1]))
                            
                            if can_have_month:
                                # if the two can be months, the two can be days so I use locale
                                if can_be_month(date_array[0]) and can_be_month(date_array[1]):
                                    if month_pos == 0:
                                        month_is_in = 0
                                        day_is_in = 1
                                    else:
                                        month_is_in = 1
                                        day_is_in = 0
                                # first is month, second is day or year
                                elif can_be_month(date_array[0]):
                                    month_is_in = 0
                                    if can_be_day(date_array[1]):
                                        day_is_in = 1
                                    elif can_be_year(date_array[1]):
                                        year_is_in = 1
                                # second is month, first is day or year
                                else:
                                    month_is_in = 1
                                    if can_be_day(date_array[0]):
                                        day_is_in = 0
                                    elif can_be_year(date_array[0]):
                                        year_is_in = 0
                        # if I have 3 parts I just check positions according to locale
                        elif len(date_array) == 3:
                            if can_be_month(date_array[month_pos]) and can_be_day(date_array[day_pos]):
                                month_is_in = month_pos
                                day_is_in = day_pos
                                year_is_in = list({0,1,2} - {month_pos, day_pos})[0]

                year = int(date_array[year_is_in]) if year_is_in is not None else None
                year = year + 2000 if year is not None and year < 2000 else year

                month = date_array[month_is_in] if month_is_in is not None else None
                if month is not None:
                    if month.isdigit():
                        month = int(month)
                    else:
                        month = words_to_datepart(month, language=language, filter=["month"])['result'][0]['value']
                
                day_number = int(date_array[day_is_in]) if day_is_in is not None else None
                continue

            ###### FIND JUST NUMBERS THAT COULD BE DAY, MONTH, YEAR, HOUR OR MINUTE ######
            if word.isdigit():
                number = int(word)
                
                if  pos < len(words) - 1 and words[pos+1].isdigit():
                    if month_pos == 0:
                        if month is None and can_be_month(number):
                            month = number
                            continue
                    elif day_number is None and can_be_day(number):
                            day_number = number
                            continue
                
                if words[pos-1].isdigit():
                    if month_pos == 1:
                        if month is None and can_be_month(number):
                            month = number
                            continue
                    elif day_number is None and can_be_day(number):
                            day_number = number
                            continue
                
                # year as 4 digits was already treated, so 2 digits is only possibility
                # 2 digit year only makes sense if you have month and month is before year, 
                #   i.e "06 24" (June 2024) but not "24 06" nor "35 06" (24 and 35 can't represent year)
                # day_number + year is nos natural i.e. "15 24"
                # 32 to represent "year 2032" doesn't make sense neither
                if year is None and can_be_year(number, base_date) and month is not None:
                    year = number + 2000
                    continue
                if hour is None and can_be_hour(number):
                    if number < 12:
                        if base_date.hour < number:
                            hour = number
                        else:
                            hour = number + 12
                    continue
                if minute is None and can_be_minute(number):
                    # if hour is nothing but previous is day_number, previous represents hour not day_number
                    # i.e. "17 40", 17 could be day (first option), but 40 can only be minute, so 17 is hour
                    # "17 24" also means hour and minute because day_number and year without month doesn't make sense
                    # in "25 26" 25 only could be day (not hour) so 26 can't be minute
                    if hour is None and day_number is not None and words[i-1].isdigit() and int(words[i-1]) == day_number and can_be_hour(day_number):
                        hour = day_number
                        day_number = None
                    
                    if hour is not None:
                        minute = number
                    
                    continue


    # print(f"calling future: base_date {str(base_date)} special {special}\n year {year} quarter {quarter} month {month} day_number {day_number} hour {hour} minute {minute} \ntimezone {timezone} locale_timezone {locale_timezone} \nyears {years} quarters {quarters} months {months} weeks {weeks} days {days} hours {hours} minutes {minutes}")
    return future_datetime(base_date=base_date, special=special, days=days, weekday=weekday, 
        day_number=day_number, month=month, year=year, hour=hour, minute=minute, second=second,
        weeks=weeks, years=years, months=months, quarter=quarter, timezone=timezone, 
        hours=hours, minutes=minutes, quarters=quarters, locale_timezone=locale_timezone)
    
'''It looks for a phrase or word into the glossary and returns the correspoding tuple (word, type, value)

TODO: it has to return an object instead of a dict
Args:
    text (string): text to search into glossary
    language (string): language of the text
    filter (list): list of types to filter the search
Returns:
    (word, type, value): tuple with the word, type and value of the word
'''
def words_to_datepart(text, language='en', filter=None):
    glossary = GLOSSARY[language]
    if filter is not None:
        # kind_words = [x['target'] for x in glossary if kind in [y['type'] for y in x['result']]]
        glossary = [x for x in glossary if any(r['type'] in filter for r in x['result'])]
    words = [x['target'] for x in glossary]
    items = [glossary[words.index(x)] for x in words if x.startswith(text)]
    # first ask if input text is exactly like one of the words in the glossary (word is first element of tuple of glossaries)
    
    if text in words:
        return glossary[words.index(text)]
    
    # then ask if there is at least one word that starts with input text (if text is at least 3 characters long)
    elif len([x for x in words if x.startswith(text) and len(text) >= 3]) >= 1:
        # get all of the words that start with input text
        items = [glossary[words.index(x)] for x in words if x.startswith(text)]

        # slice items to remove the word and make a set of it, so if there are two or more words that start with input text
        # and the result of those words is the same (i.e. they mean the same concept), it returns the first one
        # EXAMPLE: tomor for tomorrow and tomorow
        for x in range(1, len(items)):
            if items[x]['result'] != items[x-1]['result']:
                return None
        return items[0]

'''It looks for a word or phrase into the list of timezones and returns the correspoding timezone

Args:
    text (string): text to search into the list of timezones in pytz library
Returns:
    timezone: timezone object
'''
def get_timezone(text):
    #at least 3 characterse, if not returns 2
    if text is not None and len(text) >= 3:
        text = text.replace(' ', '_')
        timezones = [pytz.timezone(tz) for tz in pytz.all_timezones if text.lower() in tz.lower()]

        # if all timezones have the same offset, return the first timezone
        if len(set([x.utcoffset(datetime.now()) for x in timezones])) == 1:
            return timezones[0]
        
    return None

def get_time(word):
    hour = None
    minute = None
    second = None

    # find colon or am/pm in the word
    if ':' in word or any(word.endswith(x) for x in AM_PM):
        time = word.split(":")
        am_pm = None
        for i, char in enumerate(word):
            if char.isalpha():
                time = [x for x in word[:i].split(":")]
                am_pm = word[i:]
                break
        
        time = [int(x) for x in time if x.isdigit()]
        # if we have pm, we add 12 to the hour
        pm = False
        if am_pm is not None and 'p' in am_pm:
            pm = True
        
        if len(time) == 1:
            hour = time[0]
        elif len(time) == 2:
            hour, minute = time
        elif len(time) == 3:
            hour, minute, second = time
        
        hour = hour + 12 if pm and hour < 12 else hour
    return hour, minute, second


def suggest(text, language='en', base_date=None, locale_timezone=None, locale="en_US", max_suggestions=4):
    if base_date is None:
        base_date = datetime.now()
    if locale_timezone is not None:
        base_date.replace(tzinfo=locale_timezone)
    text = normalize(text)
    
    first_result = parse(text, language=language, base_date=base_date, locale_timezone=locale_timezone, locale=locale)
    if first_result is not None:
        # print("a match ", first_result)
        return first_result
    
    glossary = GLOSSARY[language]
    suggestions = []
    for word, type, val in glossary:
        if word.startswith(text):
            if (type, val) not in [(s[1], s[2]) for s in suggestions]:
                if type == "timezone":
                    word = "10:00a.m. " + word
                suggestions.append((word, type, val))
        
        if len(suggestions) >= max_suggestions:
            break
    if len(suggestions) < max_suggestions:
        for word, type, val in glossary:
            if text in word:
                if (type, val) not in [(s[1], s[2]) for s in suggestions]:
                    if type == "timezone":
                        word = "10:00a.m. " + word
                    suggestions.append((word, type, val))
            
            if len(suggestions) >= max_suggestions:
                break
    
    if len(text.split()) == 1 and text.isdigit():
        results.append(("in " + text + " days", None, None))
        month = (base_date + relativedelta(months=1)).strftime("%B")
        if can_be_day(text):
            results.append((text + "-" + month, None, None))
        if can_be_year(text):
            results.append((text + "-" + month, None, None))
        if can_be_hour(text):
            results.append((text + ":00", None, None))

    results = [(x, parse(x, language=language, base_date=base_date, locale_timezone=locale_timezone, locale=locale)) for x, _, _ in suggestions]
    print("POSSIBLE DATES:")
    for x in results:
        print(x[0], x[1].strftime("%Y-%m-%d %H:%M:%S %Z%z"))
    

# suggest("33", locale_timezone=pytz.timezone('America/Buenos_Aires'))