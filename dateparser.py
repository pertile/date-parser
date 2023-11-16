'''
It should be a function that receives: weekday, day number, month, year, hour, minute, second
quarter, timezone, especial
all the other have None value as default

it manages deterministic dates. They could be relative days (i.e. in two months and 5 days),
absolute (i.e. January 2024, 2024-05-02 09:35 Central Time)
or especial (especial.LATER, especial.WEEKEND, especial.TONIGHT)


SUGGESTIONS
Another function tries to find alternatives for text input. It should manage languages.
Alternatives are deterministic for the previous function
If you write week it suggests "next week", "in two weeks" or "weekend"
If you write "tw" it suggests matches with "Two", "Twenty", "twentieth", "twelve" or "twelfth"
If you write "01-06" it suggests June 1st or January 6th depending on your language

MAKE LOT OF TESTS
'''
# TODO: replace 8 with constant
# TODO: replace 2nd element in glossary tuple with constants

import calendar
from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import locale as lc

import unicodedata
import sys

def normalize(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

class Especial(Enum):
    LATER = 'later'
    WEEKEND = 'weekend'
    TONIGHT = 'tonight'
    TOMORROW = 'tomorrow'
    NEXT_WEEK = 'next_week'
    NEXT_MONTH = 'next_month'
    NEXT_QUARTER = 'next_quarter'
    NEXT_YEAR = 'next_year'

GLOSSARY = {
    'en': [
        ('tomorrow', 'especial', Especial.TOMORROW),
        ('tmrw', 'especial', Especial.TOMORROW),
        ('tomorow', 'especial', Especial.TOMORROW),
        ('later', 'especial', Especial.LATER),
        ('few', 'especial', Especial.LATER),
        ('a few hours', 'especial', Especial.LATER),
        ('tonight', 'especial', Especial.TONIGHT),
        ('weekend', 'especial', Especial.WEEKEND),
        ('next week', 'especial', Especial.NEXT_WEEK),
        ('next month', 'especial', Especial.NEXT_MONTH),
        ('next quarter', 'especial', Especial.NEXT_QUARTER),
        ('next year', 'especial', Especial.NEXT_YEAR),
        ('morning', 'hour', 8),
        ('noon', 'hour', 12),
        ('afternoon', 'hour', 13),
        ('evening', 'hour', 20),
        ('night', 'hour', 20),
        ('midnight', 'hour', 0),
        ('monday', 'weekday', 0),
        ('tuesday', 'weekday', 1),
        ('wednesday', 'weekday', 2),
        ('thursday', 'weekday', 3),
        ('friday', 'weekday', 4),
        ('saturday', 'weekday', 5),
        ('sunday', 'weekday', 6),
        ('january', 'month', 1),
        ('february', 'month', 2),
        ('march', 'month', 3),
        ('april', 'month', 4),
        ('may', 'month', 5),
        ('june', 'month', 6),
        ('july', 'month', 7),
        ('august', 'month', 8),
        ('september', 'month', 9),
        ('october', 'month', 10),
        ('november', 'month', 11),
        ('december', 'month', 12),
        ('next month', 'months', 1),
        ('next year', 'years', 1),
        ('qone', 'quarter', 1),
        ('qtwo', 'quarter', 2),
        ('qthree', 'quarter', 3),
        ('qfour', 'quarter', 4),
        ('ct', 'timezone', 'America/Chicago'),
        ('cst', 'timezone', 'America/Chicago'),
        ('central', 'timezone', 'America/Chicago'),
        ('in', 'in', ''),
        ('days', 'relative', 'days'),
        ('weeks', 'relative', 'weeks'),
        ('months', 'relative', 'months'),
        ('years', 'relative', 'years'),
        ('hours', 'relative', 'hours'),
        ('hrs', 'relative', 'hours'),
        ('minutes', 'relative', 'minutes'),
        ('mins', 'relative', 'minutes'),
        ('fortnights', 'relative', 'fortnights'),
        ('quarters', 'relative', 'quarters'),
        ('a', 'value', '1'),
        ('an', 'value', '1'),
    ],
    'es': [
        ('manana', 'especial', Especial.TOMORROW),
        ('mnn', 'especial', Especial.TOMORROW),
        ('despues', 'especial', Especial.LATER),
        ('mas tarde', 'especial', Especial.LATER),
        ('esta noche', 'especial', Especial.TONIGHT),
        ('finde', 'especial', Especial.WEEKEND),
        ('fin de semana', 'especial', Especial.WEEKEND),
        ('siguiente semana', 'especial', Especial.NEXT_WEEK),
        ('proxima semana', 'especial', Especial.NEXT_WEEK),
        ('semana que viene', 'especial', Especial.NEXT_WEEK),
        ('siguiente mes', 'especial', Especial.NEXT_MONTH),
        ('proximo mes', 'especial', Especial.NEXT_MONTH),
        ('mes que viene', 'especial', Especial.NEXT_MONTH),
        ('siguiente cuatrimestre', 'especial', Especial.NEXT_QUARTER),
        ('proximo cuatrimestre', 'especial', Especial.NEXT_QUARTER),
        ('siguiente ano', 'especial', Especial.NEXT_YEAR),
        ('proximo ano', 'especial', Especial.NEXT_YEAR),
        ('ano que viene', 'especial', Especial.NEXT_YEAR),
        ('temprano', 'hour', 8),
        ('a la manana', 'hour', 8),
        ('por la manana', 'hour', 8),
        ('a la tarde', 'hour', 16),
        ('por la tarde', 'hour', 16),
        ('mediodia', 'hour', 12),
        ('noche', 'hour', 20),
        ('medianoche', 'hour', 0),
        ('siesta', 'hour', 13),
        ('lunes', 'weekday', 0),
        ('martes', 'weekday', 1),
        ('miercoles', 'weekday', 2),
        ('jueves', 'weekday', 3),
        ('viernes', 'weekday', 4),
        ('sabado', 'weekday', 5),
        ('domingo', 'weekday', 6),
        ('enero', 'month', 1),
        ('febrero', 'month', 2),
        ('marzo', 'month', 3),
        ('abril', 'month', 4),
        ('mayo', 'month', 5),
        ('junio', 'month', 6),
        ('julio', 'month', 7),
        ('agosto', 'month', 8),
        ('septiembre', 'month', 9),
        ('octubre', 'month', 10),
        ('noviembre', 'month', 11),
        ('diciembre', 'month', 12),
        ('siguiente mes', 'months', 1),
        ('siguiente año', 'years', 1),
        ('proximo mes', 'months', 1),
        ('proximo ano', 'years', 1),
        ('ct', 'timezone', 'America/Chicago'),
        ('cst', 'timezone', 'America/Chicago'),
        ('central', 'timezone', 'America/Chicago'),
        ('en', 'in', ''),
        ('dentro de', 'in', ''),
        ('dias', 'relative', 'days'),
        ('semanas', 'relative', 'weeks'),
        ('meses', 'relative', 'months'),
        ('anos', 'relative', 'years'),
        ('horas', 'relative', 'hours'),
        ('minutos', 'relative', 'minutes'),
        ('quincenas', 'relative', 'fortnights'),
        ('trimestres', 'relative', 'quarters'),
        ('un', 'value', '1'),
        ('una', 'value', '1'),
    ],
}

# TODO: only works with one word phrases (doesn'w find 'dentro de')
def find_pos_in_glossary(phrase, kind, language="en"):
    glossary = GLOSSARY[language]
    phrase = phrase.split(" ")
    kind_words = [word for word, kind_term, _ in glossary if kind == kind_term]
    for i, word in enumerate(phrase):
        if word in kind_words:
            return i
    return None

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

def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days=days_ahead)


def future_datetime(weekday=None, weeks=0, day_number=None, days=0, month=None, months=0, 
    year=None, years=0, hour=None, hours=0, minute=None, minutes=0, second=None, seconds=0, 
    quarter=None, timezone=None, especial=None, base_date=None, locale_timezone=None,
    quarters=0):

    # if it is an especial day it doesn't consider any other information about date
    
    # if it has relative days, it doesn't consider any other information about date

    # if it is not especial nor relative, calculation will be different depending on
    # whether there is a weekday or not.
    # The logic for the absent date parts depends on whether there is a greater date part
    # if there is a greater date part it is the first value
    # i.e. you have year but not day_number nor month, day_number and month are 1st of January
    # i.e. you have month but not day_number, day_number is 1st of that month
    # if there is not a greater date part is current value (base_date value)
    # or the next one if current value of the lesser date parts is before
    # i.e. if it is 10th of January and you ask for 15th (without month or year), it is 15th of January
    # but if it is 20th of January and you ask for 15th it is 15th of February
    # idem for months and years, if it is July and you ask for October without year will be same year
    # but if you as for March will be March next year

    HOURS_LATER = 4
    if base_date is None:
        base_date = datetime.now(locale_timezone)
    base_weekday = base_date.weekday()
    base_month = base_date.month
    base_year = base_date.year
    
    hour_was_none = hour is None
    if hour is None:
        hour = 8
    if minute is None:
        minute = 0
    if second is None:
        second = 0

    if especial is not None:
        if especial == Especial.LATER:
            return (base_date + timedelta(hours=HOURS_LATER)).replace(minute=0, second=0, microsecond=0)
        elif especial == Especial.WEEKEND:
            # if it is weekend (Saturday or Sunday), add two days to current day so it is on a laborable day
            if base_date.day >= 5:
                base_date = base_date + relativedelta(days=2)
            # calculate next Saturday
            result = next_weekday(base_date, 5)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif especial == Especial.TONIGHT:
            if base_date.hour < 20:
                return base_date.replace(hour=20, minute=0, second=0, microsecond=0)
            else:
                return None
        elif especial == Especial.TOMORROW:
            return (base_date + timedelta(days=1)).replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif especial == Especial.NEXT_WEEK:
            # next Monday, if today is Monday next week Monday (today + 7 days)
            result = next_weekday(base_date, 0) if base_weekday > 0 else base_date + relativedelta(days=7)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif especial == Especial.NEXT_MONTH:
            # this quarter start date + 3 months
            result = base_date.replace(day=1) + relativedelta(months=1)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif especial == Especial.NEXT_QUARTER:
            # this quarter start date + 3 months
            result = base_date.replace(month=base_month // 3 * 3  + 1, day=1) + relativedelta(months=3)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)
        elif especial == Especial.NEXT_YEAR:
            result = base_date.replace(month=1, day=1) + relativedelta(years=1)
            return result.replace(hour=hour, minute=minute, second=second, microsecond=0)

    if quarters > 0:
        months = quarters * 3 - (base_month - 1) % 3
        day_number = 1

    if years == 0 and months == 0 and days == 0 and hours == 0 and minutes == 0 and seconds == 0 and weeks == 0 and quarters == 0:
        
        if weekday is not None:
        # only weekday, just look for next weekday
            if day_number is None and month is None and year is None:
                return next_weekday(base_date + relativedelta(days=1), weekday).replace(hour=hour, minute=minute, second=second, microsecond=0)
            
            # day number, month and year. Check if it is the same weekday and if it is in the future
            elif day_number is not None and month is not None and year is not None:
                result = datetime(year, month, day_number, hour, minute, second, microsecond=0)
                if result.weekday() == weekday and result > base_date:
                    return result
                else:
                    return None
                
            # day number
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

                # if the date is before the base date, it has to be the next month
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

        # if I don't have a day_number and I have a greater unit (month, year, quarter) I have to start on 1st day of that unit
        # if I don't have a greater unit, I have to start on current day, or may be tomorrow if hour is before base_hour
        
        plus_day = 0
        plus_month = 0
        plus_year = 0
        day_was_none = day_number is None
        if day_number is None:
            if month is not None or quarter is not None or year is not None:
                day_number = 1
            else:
                day_number = base_date.day
                # if I add 1 day to day_number, it could be after last_day of month
                # as last_day of month depends on the year (because of leap years)
                # I make that check after setting month and year
                if hour is not None and hour <= base_date.hour:
                    plus_day = 1
        
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
        
        # all of the next could be in a function that receives day, month and year and tries to 
        # make them consistent (29th Feb no year in July 2024 -> 2028-02-29)
        
        # as month is 1-based instead of 0-based I have to convert it to 0-based (substract 1) and then back to 1-based (add 1)
        # so I can use the modulo properly
        new_month = (month - 1 + plus_month) % 12 + 1
        # as month is 1-based instead of 0-based I have to convert it to 0-based (substract 1) to use // 12 properly to get years to add
        new_year = year + plus_year + (month - 1 + plus_month) // 12

        first_day_temp = datetime(new_year, new_month, 1)

        # if my new date is 29, 30 or 31 in a month that doesn't have that day, or it is the last day of the month and hour is before base_hour 
        # I have to add: a month if month was none, or a day if month was present. I have to do it up to date is consistent
        # This could be the case when you ask for a 29 Feb in Jun 2024, it will add a year until it gets year 2028
        # or if you are on 31st August 7 pm and you ask for 31st 5 pm, it will add a month and will get September 31
        # so it has to add another month in order to get October 31

        max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
            
        if max_day < day_number or (max_day == day_number and datetime(year, month, day_number, hour, minute, second) <= base_date):
            while True:
                # if day, nor month nor year are present then you add a day
                # I think this case is never used
                # Example: 6 pm and now is 8 pm, you have to add a day
                if day_was_none and month_was_none and year_was_none:
                    plus_day = plus_day + 1
                    first_day_temp = first_day_temp + relativedelta(days=1)    
                    max_day = calendar.monthrange(first_day_temp.year, first_day_temp.month)[1]
                # if month is not present you can add a month
                # Example: 30th of June and you ask for 31st, you have to add a month to get August
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


    #     # print(year, month, day_number)
    #     last_month_day = calendar.monthrange(year, month)[1]
    #     # this could be because you asked for 31st on a 30 days month (only day_number is present)
    #     # or if only hour is present but not day_number because you are in an hour after your base_hour so it adds a day
    #     # to the last day of a month (31, 30, 29 or 28, it depends on the month and the year)
    #     # solution is always getting the next month because there aren't two consecutives months with less than 31 days

    #     if day_number > last_month_day:
    #         month = month % 12 + 1
    #         # if day was present, you have to keep that day_number (and so you add a month)
    #         # if day was empty, your day_number move to the first day in next month
    #         if month == 1:
    #             year = year + 1
    #         if day_was_none:
    #             day_number = 1

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
    

def parse(text, language='en', base_date=None, locale_timezone=None, locale="en_US"):
    if base_date is None:
        base_date = datetime.now()

    if base_date.tzinfo is None and locale_timezone is not None:
        base_date = base_date.replace(tzinfo=locale_timezone)

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

    especial = None
    year = None
    month = None
    day_number = None
    weekday = None
    hour = None
    minute = None
    second = None
    quarter = None
    relative = False

    ### FIND RELATIVE ###
    start = find_pos_in_glossary(text, 'in', language)
    # I found an "in" word

    glossary = GLOSSARY[language]
    indefinite_articles = [(word, result) for word, kind_term, result in glossary if 'value' == kind_term]


    # replace "a" and "an" with 1
    for i, word in enumerate(words):
        for lookedupword, result in indefinite_articles:
            if lookedupword == word:
                words[i] = result

    if start is not None:
    
        #in_phrase is the maximum length for an in phrase (i.e. "in 2 days and an hour", 6 words)
        in_phrase = words[start: start+6]
        print("in phrase", in_phrase)
        relative_words = [(word, result) for word, kind_term, result in glossary if 'relative' == kind_term]
        print("relative_words", relative_words)
        relatives = {}
        for i, word in enumerate(in_phrase):
            for lookedupword, result in relative_words:
                if lookedupword.startswith(word):
                    relatives[result] = in_phrase[i-1]
                    break
        print("relatives", relatives)
        hours = int(relatives['hours']) if 'hours' in relatives else 0

        minutes = int(relatives['minutes']) if 'minutes' in relatives else 0
        years = int(relatives['years']) if 'years' in relatives else 0
        months = int(relatives['months']) if 'months' in relatives else 0
        days = int(relatives['days']) if 'days' in relatives else 0
        weeks = int(relatives['weeks']) if 'weeks' in relatives else 0
        quarters = int(relatives['quarters']) if 'quarters' in relatives else 0
        weeks = int(relatives['fortnights']) * 2 if 'fortnights' in relatives else weeks

        if hours == 0 and minutes == 0:
            hour = 8
        else:
            hour = base_date.hour
            if minutes > 0:
                minute = base_date.minute
    
    else:


        #### FIND WORDS ######
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
                        results.append(result)
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
        
        # print(results)
        for r in results:
            if r[1] == 'especial':
                if especial is None:
                    especial = r[2]
                else:
                    return None
            elif r[1] == 'days':
                if days == 0:
                    days = r[2]
                else:
                    return None
            elif r[1] == 'weekday':
                weekday = r[2]
            elif r[1] == 'month':
                month = r[2]
            elif r[1] == 'quarter':
                quarter = r[2]
            elif r[1] == 'weeks':
                weeks = r[2]
                weekday = 0
                hour = 8
                minute = 0
                second = 0
            elif r[1] == 'months':
                months = r[2]
                day_number = 1
                hour = 8
                minute = 0
                second = 0
            elif r[1] == 'years':
                years = r[2]
                month = 1
                day_number = 1
                hour = 8
                minute = 0
                second = 0
            elif r[1] == 'hour':
                hour = r[2]
            elif r[1] == 'timezone':
                timezone = pytz.timezone(r[2])
            elif r[1] == 'in':
                relative = True

        if relative:
            items = [GLOSSARY[language][words.index(x)] for x in words if x.startswith(text)]
        # check if am or pm is separated from the time. If it is, join them
        for i in range(1, len(words)):
            if words[i] in ['am', 'pm', 'a.m.', 'p.m.']:
                words[i-1] = words[i-1] + words[i]
                words[i] = None
            
        # remove empty words (erased am/pm)
        words[:] =  (value for value in words if value != None)
        # print(words)
        for word in words:
            
            #### FIND DAY WITH ORDINALS ######    
            if word[0].isdigit() and word[-2:] in ['st', 'nd', 'rd', 'th']:
                number = word[:-2]
                try:
                    day_number = int(number)
                except ValueError:
                    return None
            
            #### FIND HOUR ######
            if ':' in word and word[-1] not in['.', 'm']:
                word = word + 'am'

            if word[-2:] in ['am', 'pm'] or word[-4:] in ['a.m.', 'p.m.']:
                pm = False
                if 'p' in word:
                    pm = True
                word = word[:-2]
                if word[-1] == '.':
                    word = word[:-2]
                
                time = word.split(":")
                hour = int(time[0])
                
                hour = hour + 12 if pm and hour < 12 else hour
                minute = 0
                second = 0
                if len(time) > 1:
                    minute = int(time[1])
                if len(time) > 2:
                    second = int(time[2])
            
            #### FIND YEAR ######
            if len(word) == 4 and word.startswith("20") and word.isdigit() and int(word) >= datetime.now().year and int(word) <= datetime.now().year + 10:
                year = int(word)
                if year > 2030 or year < 2020:
                    return None
            
            #### FIND QUARTER ######
            if word[0] == 'q' and word[1:].isdigit():
                quarter = int(word[1:])
                if quarter > 4 or quarter < 1:
                    return None
                
            #### FIND DATE SEPARATED BY DASH OR SLASH ######
            separator = None
            if '-' in word:
                separator = '-'
            elif '/' in word:
                separator = '/'
            elif '\\' in word:
                separator = '\\'
            elif '–' in word:
                separator = '–'
            
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
                        # returns a tuple where first element is month position and second is day position, i.e. in US is (0,1) in UK is (1,0)
                        month_pos, day_pos = get_locale_monthdate(locale)

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
                        month = words_to_datepart(month, language=language)[2]
                
                day_number = int(date_array[day_is_in]) if day_is_in is not None else None

            
    print("calling future", year, month, day_number, days, weekday, hour, minute, second, especial, weeks, years, months, quarter, hours, minutes, timezone, locale_timezone)
    return future_datetime(base_date=base_date, especial=especial, days=days, weekday=weekday, 
        day_number=day_number, month=month, year=year, hour=hour, minute=minute, second=second,
        weeks=weeks, years=years, months=months, quarter=quarter, timezone=timezone, 
        hours=hours, minutes=minutes, quarters=quarters, locale_timezone=locale_timezone)
    

def words_to_datepart(text, language='en'):
    words = [x[0] for x in GLOSSARY[language]]
    items = [GLOSSARY[language][words.index(x)] for x in words if x.startswith(text)]

    # first ask if input text is exactly like one of the words in the glossary (word is first element of tuple of glossaries)
    if text in words:
        return GLOSSARY[language][words.index(text)]
    # then ask if there is at least one word that starts with input text
    elif len([x for x in words if x.startswith(text)]) >= 1:
        # get all of the words that start with input text
        items = [GLOSSARY[language][words.index(x)] for x in words if x.startswith(text)]

        # slice items to remove the word and make a set of it, so if there are two or more words that start with input text
        # and the result of those words is the same (i.e. they mean the same concept), it returns the first one
        # EXAMPLE: tomor for tomorrow and tomorow
        if len(set([x[1:] for x in items])) == 1:
            return items[0]

def get_timezone(text):
    #at least 3 characterse, if not returns 2
    if text is not None and len(text) >= 3:
        text = text.replace(' ', '_')
        timezones = [pytz.timezone(tz) for tz in pytz.all_timezones if text.lower() in tz.lower()]

        # if all timezones have the same offset, return the first timezone
        if len(set([x.utcoffset(datetime.now()) for x in timezones])) == 1:
            return timezones[0]
        
    return None



# if __name__ == '__main__': 
    
#     language = 'en'

#     print(parse(sys.argv[1]))

# a function that receives a text as a parameter, it replaces spaces with underscores and get possible timezones for that word