'''
It should be a function that receives: weekday, day number, month, year, hour, minute, second
quarter, timezone, especial
relative_date=False, relative_time=False
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


from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

import unicodedata

def normalize(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

class Especial(Enum):
    LATER = 'later'
    WEEKEND = 'weekend'
    TONIGHT = 'tonight'

KEYWORDS = {
    'en': [
        ('tomorrow', 'relative-days', 1),
        ('tmrw', 'relative-days', 1),
        ('tomorow', 'relative-days', 1),
        ('later', 'especial', Especial.LATER),
        ('few', 'especial', Especial.LATER),
        ('a few hours', 'especial', Especial.LATER),
        ('tonight', 'especial', Especial.TONIGHT),
        ('weekend', 'especial', Especial.WEEKEND),
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
    ],
    'es': [
        ('mañana', 'relative-days', 1),
        ('mñn', 'relative-days', 1),
        ('manana', 'relative-days', 1),
        ('despues', 'especial', Especial.LATER),
        ('mas tarde', 'especial', Especial.LATER),
        ('esta noche', 'especial', Especial.TONIGHT),
        ('finde', 'especial', Especial.WEEKEND),
        ('fin de semana', 'especial', Especial.WEEKEND),
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
    ],
}
def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days=days_ahead)

def future_datetime(weekday=None, weeks=None, day_number=None, days=None, month=None, year=None, hour=None, minute=None, 
    fortnights=None, second=None, quarter=None, timezone=None, especial=None, relative=False, base_date=None):


    HOURS_LATER = 4
    if base_date is None:
        base_date = datetime.now()
    base_weekday = base_date.weekday()
    base_month = base_date.month
    base_year = base_date.year

    if relative:
        if days is None:
            days = 0
        if weeks is None:
            weeks = 0
        months = month
        if months is None:
            months = 0
        years = year
        if years is None:
            years = 0
        hours = hour
        if hours is None:
            hours = 0
        minutes = minute
        if minutes is None:
            minutes = 0
        seconds = second
        if seconds is None:
            seconds = 0
        return base_date + relativedelta(days=days, weeks=weeks, months=months, years=years, hours=hours, minutes=minutes, seconds=seconds)



    if especial is not None:
        if especial == Especial.LATER:
            return (base_date + timedelta(hours=HOURS_LATER)).replace(minute=0, second=0, microsecond=0)
        elif especial == Especial.WEEKEND:
            days = 5 - base_weekday if base_weekday < 5 else 7
            return (base_date + timedelta(days=days)).replace(hour=8, minute=0, second=0, microsecond=0)
        elif especial == Especial.TONIGHT:
            if base_date.hour < 20:
                return base_date.replace(hour=20, minute=0, second=0, microsecond=0)
            else:
                return None

    hour_was_none = hour is None
    if hour is None:
        hour = 8
    if minute is None:
        minute = 0
    if second is None:
        second = 0

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


    day_was_none = day_number is None
    if day_number is None:
        if hour_was_none or quarter is not None:
            day_number = 1
        else:
            day_number = base_date.day
            if hour <= base_date.hour and month is None and year is None and quarter is None:
                day_number = day_number + 1
    
    month_was_none = month is None
    if month is None:
        if quarter is None:
            if day_was_none and hour_was_none:
                month = 1
            else:
                month = base_month
                if day_number < base_date.day or (day_number==base_date.day and hour <= base_date.hour):
                    month = month + 1
        else:
            month = (quarter - 1) * 3 + 1
        

    if year is None:
        year = base_year
        if month < base_month or (month == base_month and day_number < base_date.day) or (month == base_month and day_number == base_date.day and hour <= base_date.hour):
            year = year + 1

    if day_number == 29 and month == 2 and not calendar.isleap(year):
        day_number = 1
        month = 3

    # print(year, month, day_number)
    last_month_day = calendar.monthrange(year, month)[1]
    # this could be because you asked for 31st on a 30 days month (only day_number is present)
    # or if only hour is present but not day_number because you are in an hour after your base_hour so it adds a day
    # to the last day of a month (31, 30, 29 or 28, it depends on the month and the year)
    # solution is always getting the next month because there aren't two consecutives months with less than 31 days

    if day_number > last_month_day:
        month = month % 12 + 1
        # if day was present, you have to keep that day_number (and so you add a month)
        # if day was empty, your day_number move to the first day in next month
        if month == 1:
            year = year + 1
        if day_was_none:
            day_number = 1


    result = datetime(year, month, day_number, hour, minute, second, microsecond=0)
    # print(result, "result")
    # print(base_date, "base_date")
    if  result > base_date:
        return result
    else:
        return None
    

def parse(text, language='en'):
    text = normalize(text)
    words = text.split(" ")
    results = []
    
    #### FIND WORDS ######
    # start looking for 3 words phrases, then 2 words phrases and finally 1 word
    for size in range(3, 0, -1):
        # stop looking at len(words) - size, so if there are 10 words you can only look up to 8th word for a 3 word prhase
        for i in range(len(words) - size + 1):
            # print(f"Position {i} of {len(words)-size}. Palabra:")
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
    relative = False
    day_number = None
    days = None
    weekday = None
    month = None

    for r in results:
        if r[1] == 'especial':
            if especial is None:
                especial = r[2]
            else:
                return None
        elif r[1] == 'relative-days':
            relative = True
            if days is None:
                days = r[2]
            else:
                return None
        elif r[1] == 'weekday':
            weekday = r[2]
        elif r[1] == 'month':
            month = r[2]
    
    
    for word in words:
        
        #### FIND DAY WITH ORDINALS ######    
        if word[0].isdigit() and word[-2:] in ['st', 'nd', 'rd', 'th']:
            number = word[:-2]
            try:
                day_number = int(number)
            except ValueError:
                return None
    
        #### FIND YEAR ######
        if len(word) == 4 and word.startswith("20") and word.isdigit() and word[-2] >= datetime.now().year and word[-2] <= datetime.now().year + 10:
            year = int(word)
            if year > 2030 or year < 2020:
                return None

    print(future_datetime(especial=especial, relative=relative, days=days, weekday=weekday, day_number=day_number, month=month))

def words_to_datepart(text, language='en'):
    words = [x[0] for x in KEYWORDS[language]]
    if text in words:
        return KEYWORDS[language][words.index(text)]
    elif len([x for x in words if x.startswith(text)]) == 1:
        item = [x for x in words if x.startswith(text)][0]
        return KEYWORDS[language][words.index(item)]
    
    