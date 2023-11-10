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

from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

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
        # ('CT', 'timezone', 'America/Chicago'),
        # ('CST', 'timezone', 'America/Chicago'),
        # ('Central', 'timezone', 'America/Chicago'),
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
        # ('CT', 'timezone', 'America/Chicago'),
        # ('CST', 'timezone', 'America/Chicago'),
        # ('Central', 'timezone', 'America/Chicago'),

    ],
}
def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days=days_ahead)


def future_datetime(weekday=None, weeks=0, day_number=None, days=0, month=None, months=0, 
    year=None, years=0, hour=None, hours=0, minute=None, minutes=0, second=None, seconds=0, 
    quarter=None, timezone=None, especial=None, base_date=None):

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
        base_date = datetime.now()
    base_weekday = base_date.weekday()
    base_month = base_date.month
    base_year = base_date.year

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


    if years == 0 and months == 0 and days == 0 and hours == 0 and minutes == 0 and seconds == 0 and weeks == 0:
        hour_was_none = hour is None


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
        if year is None:
            year = base_year
            if month < base_month or (month == base_month and day_number < base_date.day):
                plus_year = 1
        
        temp_date = datetime(year, month, day_number) + relativedelta(days=plus_day, months=plus_month, years=plus_year)
        day_number = temp_date.day
        month = temp_date.month
        year = temp_date.year


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

    # if year is None:
    #     year = base_year
    # if month is None:
    #     month = base_month
    # if day_number is None:
    #     day_number = base_date.day
    if hour is None:
        hour = base_date.hour
    if minute is None:
        minute = base_date.minute
    if second is None:
        second = base_date.second

    # print(year, month, day_number, hour, minute, second, years, months, days, weeks, hours, minutes, seconds)
    result = datetime(year, month, day_number, hour, minute, second, microsecond=0) + relativedelta(years=years, 
        months=months, days=days, weeks=weeks, hours=hours, minutes=minutes, seconds=seconds)

    if  result > base_date:
        return result
    else:
        return None
    

def parse(text, language='en', base_date=None):
    if base_date is None:
        base_date = datetime.now()

    text = normalize(text)
    words = text.split(" ")
    results = []
    
    #### FIND WORDS ######
    # start looking for 3 words phrases, then 2 words phrases and finally 1 word
    for size in range(3, 0, -1):
        # stop looking at len(words) - size, so if there are 10 words you can only look up to 8th word for a 3 words prhase
        for i in range(len(words) - size + 1):
            # print(f"Position {i} of {len(words)-size}. Word:")
            
            # conditional to avoid looking for erased words
            if words[i] is not None:
                # print(words[i:i+size])
                result = words_to_datepart(' '.join(words[i:i+size]), language)
                if result is not None:
                    results.append(result)
                    # set words to None so they aren't considered again
                    words[i:i+size] = [None] * size
        # remove empty words (erased words because they are part of a phrase)
        words[:] =  (value for value in words if value != None)
    
    especial = None
    year = None
    years = 0
    month = None
    months = 0
    day_number = None
    days = 0
    weeks = 0
    weekday = None
    hour = None
    minute = None
    second = None
    quarter = None
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
        elif r[1] = 'timezone':
            timezone = r[2]

    
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
        
        if separator is not None:
            date_array = word.split(separator)
            # year is at the beginning, is yyyy-mm or yyyy-mm-dd
            if len(date_array[0]) == 4:
                year = int(date_array[0])
                month = int(date_array[1])
                if len(date_array) == 3:
                    day_number = int(date_array[2])
                else:
                    day_number = 1
            
        #### FIND TIMEZONE ###
        # if word in pytz.common_timezones:
        #     timezone = word

    # print("calling future", year, month, day_number, days, weekday, hour, minute, second, especial, weeks, years, months, quarter)
    return future_datetime(base_date=base_date, especial=especial, days=days, weekday=weekday, 
        day_number=day_number, month=month, year=year, hour=hour, minute=minute, second=second,
        weeks=weeks, years=years, months=months, quarter=quarter, timezone=timezone)
    

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
    
    
    
# if __name__ == '__main__': 
    
#     language = 'en'

#     print(parse(sys.argv[1]))
