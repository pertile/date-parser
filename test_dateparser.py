import unittest
from dateparser import parse
from datetime import datetime

import pytz

class TestDateParser(unittest.TestCase):

    def test_tomorrow(self):
        # test tomorrow
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 8, 0, 0, 0)
        self.assertEqual(parse('tomorrow', base_date=base_date), expected_date)

        # test tmrw
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 8, 0, 0, 0)
        self.assertEqual(parse('tmrw', base_date=base_date), expected_date)

        # test tomor
        base_date = datetime(2023, 11, 8, 7, 33, 0)
        expected_date = datetime(2023, 11, 9, 8, 0, 0, 0)
        self.assertEqual(parse('tomor', base_date=base_date), expected_date)

        # test mañana
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 8, 0, 0, 0)
        self.assertEqual(parse('mañana', base_date=base_date, language="es"), expected_date)


    def test_tomorrow_10am(self):
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 10, 0, 0)
        self.assertEqual(parse('tomorrow 10am', base_date=base_date), expected_date)

        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 10, 0, 0, 0)
        self.assertEqual(parse('tomorrow 10 am', base_date=base_date), expected_date)

        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 10, 0, 0, 0)
        self.assertEqual(parse('mñn 10a.m.', base_date=base_date, language="es"), expected_date)

    def test_today_11pm(self):
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 8, 23, 0, 0)
        self.assertEqual(parse('today 11pm', base_date=base_date), expected_date)

        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 8, 23, 0, 0, 0)
        self.assertEqual(parse('today 11 p.m.', base_date=base_date), expected_date)
        
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 8, 23, 0, 0, 0)
        self.assertEqual(parse('hoy 11p.m.', base_date=base_date, language="es"), expected_date)
    
    def test_later(self):
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 8, 16, 0, 0)
        self.assertEqual(parse('later', base_date=base_date), expected_date)

        # test a few hours
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 8, 16, 0, 0)
        self.assertEqual(parse('a few hours', base_date=base_date), expected_date)

        # test a few hours
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 8, 16, 0, 0)
        self.assertEqual(parse('más tarde', base_date=base_date, language="es"), expected_date)

    def test_tonight(self):
        # test tonight
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 8, 20, 0, 0)
        self.assertEqual(parse('tonight', base_date=base_date), expected_date)

        # test tonight and now is tonight
        base_date = datetime(2023, 11, 20, 20, 33, 0)
        expected_date = None
        self.assertEqual(parse('tonight', base_date=base_date), expected_date)

        # test esta noche
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 8, 20, 0, 0)
        self.assertEqual(parse('esta noche', base_date=base_date, language='es'), expected_date)

    def test_weekend(self):
        # test weekend
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 11, 8, 0, 0)
        self.assertEqual(parse('weekend', base_date=base_date), expected_date)

        # test next weekend  (it's Saturday)
        base_date = datetime(2023, 11, 11, 12, 33, 0)
        expected_date = datetime(2023, 11, 18, 8, 0, 0)
        self.assertEqual(parse('weeke', base_date=base_date), expected_date)

        # test next weekend  (it's Sunday)
        base_date = datetime(2023, 11, 12, 13, 33, 0)
        expected_date = datetime(2023, 11, 18, 8, 0, 0)
        self.assertEqual(parse('fin de sem', base_date=base_date, language="es"), expected_date)

        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 11, 15, 0, 0)
        self.assertEqual(parse('weekend 3pm', base_date=base_date), expected_date)


    def test_next_week(self):
        # test next week
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 13, 8, 0, 0)
        self.assertEqual(parse('next week', base_date=base_date), expected_date)

        # test next week
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 13, 8, 0, 0)
        self.assertEqual(parse('proxima semana', base_date=base_date, language="es"), expected_date)

    def test_next_month(self):
        # test next month
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 12, 1, 8, 0, 0)
        self.assertEqual(parse('next month', base_date=base_date), expected_date)

        # test next month - spanish
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 12, 1, 8, 0, 0)
        self.assertEqual(parse('siguiente mes', base_date=base_date, language="es"), expected_date)

    def test_tuesday(self):
        # just Tuesday
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 14, 8, 0, 0)
        self.assertEqual(parse('Tuesday', base_date=base_date), expected_date)

        # on Tuesday
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 14, 8, 0, 0)
        self.assertEqual(parse('on tuesday', base_date=base_date), expected_date)

        # next Tuesday - spanish
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2023, 11, 14, 8, 0, 0)
        self.assertEqual(parse('siguiente martes', base_date=base_date, language="es"), expected_date)


    def test_march(self):
        # just March
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2024, 3, 1, 8, 0, 0)
        self.assertEqual(parse('March', base_date=base_date), expected_date)

        # next March - spanish
        base_date = datetime(2023, 11, 8, 12, 33, 0)
        expected_date = datetime(2024, 3, 1, 8, 0, 0)
        self.assertEqual(parse('siguiente marzo', base_date=base_date, language="es"), expected_date)

    def test_next_month(self):
        base_date = datetime(2023,11,10,15,22)
        expected_date = datetime(2023,12,1,8,0)
        self.assertEqual(parse('next month', base_date=base_date), expected_date)

    def test_q2(self):
        # test q2
        base_date = datetime(2023, 9, 10, 15, 22)
        expected_date = datetime(2024, 4, 1, 8, 0)
        self.assertEqual(parse('q2', base_date=base_date), expected_date)

        # test qone
        base_date = datetime(2023, 9, 10, 15, 22)
        expected_date = datetime(2024, 4, 1, 8, 0)
        self.assertEqual(parse('qtwo', base_date=base_date), expected_date)


    def test_next_quarter(self):
        # next quarter
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2023, 10, 1, 8, 0)
        self.assertEqual(parse('next quarter', base_date=base_date), expected_date)

        # next quarter - spanish
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2023, 10, 1, 8, 0)
        self.assertEqual(parse('próximo cuatri', base_date=base_date, language="es"), expected_date)

    def test_2024(self):
        # just 2024
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2024, 1, 1, 8, 0)
        self.assertEqual(parse('2024', base_date=base_date), expected_date)

    def test_next_year(self):
        # next year
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2024, 1, 1, 8, 0)
        self.assertEqual(parse('next year', base_date=base_date), expected_date)

        # next year - spanish
        base_date = datetime(2023, 12, 10, 15, 22)
        expected_date = datetime(2024, 1, 1, 8, 0)
        self.assertEqual(parse('año que viene', base_date=base_date, language="es"), expected_date)

    def test_noon(self):
        # test just noon
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2023, 7, 11, 12, 0)
        self.assertEqual(parse('noon', base_date=base_date), expected_date)

        # test tomorrow noon
        base_date = datetime(2023, 7, 10, 8, 22)
        expected_date = datetime(2023, 7, 11, 12, 0)
        self.assertEqual(parse('tomorrow noon', base_date=base_date), expected_date)

        # test Monday noon
        base_date = datetime(2023, 11, 10, 8, 22)
        expected_date = datetime(2023, 11, 13, 12, 0)
        self.assertEqual(parse('Monday noon', base_date=base_date), expected_date)

    def test_midnight(self):
        # test just midnight
        base_date = datetime(2023, 7, 10, 15, 22)
        expected_date = datetime(2023, 7, 11, 0, 0)
        self.assertEqual(parse('midnight', base_date=base_date), expected_date)

        # test tomorrow midnight - spanish
        base_date = datetime(2023, 7, 10, 8, 22)
        expected_date = datetime(2023, 7, 11, 0, 0)
        self.assertEqual(parse('mañana a la medianoche', base_date=base_date, language="es"), expected_date)

        # test Friday midnight
        base_date = datetime(2023, 11, 8, 8, 22)
        expected_date = datetime(2023, 11, 10, 0, 0)
        self.assertEqual(parse('Friday midnight', base_date=base_date), expected_date)

    def test_morning(self):
        # test just morning
        base_date = datetime(2023, 7, 10, 4, 22)
        expected_date = datetime(2023, 7, 10, 8, 0)
        self.assertEqual(parse('morning', base_date=base_date), expected_date)

        # test tomorrow morning
        base_date = datetime(2023, 7, 10, 8, 22)
        expected_date = datetime(2023, 7, 11, 8, 0)
        self.assertEqual(parse('tomorrow morning', base_date=base_date), expected_date)

        # test Thursday morning
        base_date = datetime(2023, 11, 6, 8, 22)        
        expected_date = datetime(2023, 11, 9, 8, 0)
        self.assertEqual(parse('jueves por la mañana', base_date=base_date, language="es"), expected_date)

    def test_night(self):
        # test just night
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 10, 20, 0)
        self.assertEqual(parse('noche', base_date=base_date, language="es"), expected_date)

        # test tomorrow night
        base_date = datetime(2023, 7, 10, 20, 22)
        expected_date = datetime(2023, 7, 11, 20, 0)
        self.assertEqual(parse('tomorrow night', base_date=base_date), expected_date)

        # test Tuesday night
        base_date = datetime(2023, 11, 10, 20, 22)
        expected_date = datetime(2023, 11, 14, 20, 0)
        self.assertEqual(parse('Tuesday night', base_date=base_date), expected_date)

        # test just evening
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 10, 20, 0)
        self.assertEqual(parse('evening', base_date=base_date), expected_date)
        
        # test tomorrow evening
        base_date = datetime(2023, 7, 10, 20, 22)
        expected_date = datetime(2023, 7, 11, 20, 0)
        self.assertEqual(parse('tomorrow evening', base_date=base_date), expected_date)

        # test Wednesday evening
        base_date = datetime(2023, 11, 10, 20, 22)
        expected_date = datetime(2023, 11, 15, 20, 0)
        self.assertEqual(parse('Wednesday evening', base_date=base_date), expected_date)


    def test_just_hour(self):
        # test 5am
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 11, 5, 0)
        self.assertEqual(parse('5am', base_date=base_date), expected_date)

        # test 5pm
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 10, 17, 0)
        self.assertEqual(parse('5pm', base_date=base_date), expected_date)

        # test 06am
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 11, 6, 0)
        self.assertEqual(parse('06am', base_date=base_date), expected_date)
        
        # test 07pm
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 10, 19, 0)
        self.assertEqual(parse('07pm', base_date=base_date), expected_date)

        # test 8a.m.
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 11, 8, 0)
        self.assertEqual(parse('8a.m.', base_date=base_date), expected_date)

        # test 9 p.m.
        base_date = datetime(2023, 7, 10, 2, 22)
        expected_date = datetime(2023, 7, 10, 21, 0)
        self.assertEqual(parse('9 p.m.', base_date=base_date), expected_date)


    def test_hour_and_timezone(self):
        # test 5am CT
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_tz = pytz.timezone('US/Central')
        expected_date = datetime(2023, 7, 11, 5, 0, tzinfo=expected_tz)
        
        tz = pytz.timezone('US/Central')
        self.assertEqual(parse('5am CT', base_date=base_date, locale_timezone=tz), expected_date)

        # test 6pm Buenos Aires
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        expected_date = datetime(2023, 7, 11, 5, 0, tzinfo=expected_tz)
        tz = pytz.timezone('US/Central')
        self.assertEqual(parse('5am Buenos Aires', base_date=base_date, locale_timezone=tz), expected_date)
        

    def test_hour_minute(self):
        # test 5:30
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 11, 5, 30)
        self.assertEqual(parse('5:30', base_date=base_date), expected_date)

        # test 05:30
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 11, 5, 30)
        self.assertEqual(parse('05:30', base_date=base_date), expected_date)

        # test 5:30pm
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 7, 10, 17, 30)
        self.assertEqual(parse('05:30pm', base_date=base_date), expected_date)


    def test_just_day_ordinal(self):
        # test 1st
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 8, 1, 8, 0)
        self.assertEqual(parse('1st', base_date=base_date), expected_date)

        # test 02nd
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 8, 2, 8, 0)
        self.assertEqual(parse('02nd', base_date=base_date), expected_date)

        # test 3rd
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2023, 8, 3, 8, 0)
        self.assertEqual(parse('3rd', base_date=base_date), expected_date)

        # test 08th
        base_date = datetime(2023, 12, 10, 16, 22)
        expected_date = datetime(2024, 1, 8, 8, 0)
        self.assertEqual(parse('08th', base_date=base_date), expected_date)

        # test 31th in a month with 30 days
        base_date = datetime(2023, 6, 10, 16, 22)
        expected_date = datetime(2023, 7, 31, 8, 0)
        self.assertEqual(parse('31st', base_date=base_date), expected_date)

        # test 31st in a month with 31 days
        base_date = datetime(2023, 7, 15, 16, 22)
        expected_date = datetime(2023, 7, 31, 8, 0)
        self.assertEqual(parse('31st', base_date=base_date), expected_date)

        # test 31th in a month with 30 days last_day of month
        base_date = datetime(2023, 6, 30, 16, 22)
        expected_date = datetime(2023, 7, 31, 8, 0)
        self.assertEqual(parse('31st', base_date=base_date), expected_date)

        # test 31th in a month with 31 days last_day of month
        base_date = datetime(2023, 8, 31, 16, 22)
        expected_date = datetime(2023, 10, 31, 8, 0)
        self.assertEqual(parse('31st', base_date=base_date), expected_date)

        # test 32th
        base_date = datetime(2023, 7, 31, 16, 22)
        expected_date = None
        self.assertEqual(parse('32th', base_date=base_date), expected_date)


    def test_just_month(self):
        # test January
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2024,1,1,8)
        self.assertEqual(parse('January', base_date=base_date), expected_date)

        # test Feb
        base_date = datetime(2023, 1, 10, 16, 22)
        expected_date = datetime(2023,2,1,8)
        self.assertEqual(parse('February', base_date=base_date), expected_date)


        # test Marc
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2024,3,1,8)
        self.assertEqual(parse('Marc', base_date=base_date), expected_date)


    def test_just_year(self):
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2024,1,1,8)
        self.assertEqual(parse('2024', base_date=base_date), expected_date)
        
    def test_day_and_month(self):
        # test 1st April
        base_date = datetime(2023, 7, 10, 16, 22)
        expected_date = datetime(2024,4,1,8)
        self.assertEqual(parse('1st April', base_date=base_date), expected_date)

        # test 02 May
        base_date = datetime(2023, 2, 10, 16, 22)
        expected_date = datetime(2023,5,1,8)
        self.assertEqual(parse('02 May', base_date=base_date), expected_date)

        # test 03rd Jun
        base_date = datetime(2023, 6, 1, 16, 22)
        expected_date = datetime(2023,6,3,8)
        self.assertEqual(parse('03rd Jun', base_date=base_date), expected_date)

    def test_leap_day(self):
        # test 29th Feb in July 2024
        base_date = datetime(2024, 7, 1, 16, 22)
        expected_date = datetime(2028,2,29,8)
        self.assertEqual(parse('29th Feb', base_date=base_date), expected_date)
        

    def test_day_month_year(self):
        # test 4th July 2023
        base_date = datetime(2023, 6, 1, 16, 22)
        expected_date = datetime(2023,7,4,8)            
        self.assertEqual(parse('4th July 2023', base_date=base_date), expected_date)

        # test 05th Augu 2024
        base_date = datetime(2023, 6, 1, 16, 22)
        expected_date = datetime(2024,8,5,8)
        self.assertEqual(parse('05th Augu 2024', base_date=base_date), expected_date)        


    def test_day_and_month_separated_by_slash_dash_or_hyphen(self):
        # test 7-Oct
        # base_date = datetime(2023, 6, 1, 16, 22)
        # expected_date = datetime(2023,10,7,8)
        # self.assertEqual(parse('7-Oct', base_date=base_date), expected_date)

        # test 08/Nove

        # test 9-12 with locale set to US

        # test 9-12 with locale set to UK

        # test 10/01 with locale set to US

        # test 10/01 with locale set to UK

        # test 11\Febr

        # test 12–April (dash is not hyphen)
        pass

    def test_day_month_year_separated_by_slash_dash_or_hyphen(self):
    #     # test 13-May-2024

    #     # test 14/Jun/24

    #     # test 15\06\2032

    #     # test 16–7–2033 (dash is not hyphen)

        # test 2024-08-05
            base_date = datetime(2023, 6, 1, 16, 22)
            expected_date = datetime(2024,8,5,8)
            self.assertEqual(parse('2024-08-05', base_date=base_date), expected_date)

        # test 2023-9-6
            base_date = datetime(2023, 6, 1, 16, 22)
            expected_date = datetime(2023,9,6,8)
            self.assertEqual(parse('2023-9-6', base_date=base_date), expected_date)

    # def test_in_days(self):
    #     # test in 5 days

    #     # test in 5 days and 3 hours

    #     # test in 5 days 3 hours and 2 minutes

    #     # test in 5 days 3 hours 2 minutes and 1 second
    #     pass

    # def test_in_months(self):
    #     # test in 6 months

    #     # test in 6 months and 4 days

    #     # test in 6 months 4 days and 3 hours
    #     pass

    # def test_in_weeks(self):
    #     # test in 4 weeks

    #     # test in 4 weeks and 2 days

    #     # test in 4 weeks 2 days and 1 hour
    #     pass
    
    # def test_in_years(self):
    #     pass

    # def test_in_quarters(self):
    #     pass

    # def test_in_fortnights(self):
    #     pass

    # def test_in_hours(self):
    #     # test in 8 hours

    #     # test in 8 hours and 5 minutes

    #     # test in 10 hrs
    #     pass

    # def test_in_minutes(self):
    #     # test in 9 mins
    #     pass

    # def test_numbers
    
    # test 17 25
    # test 0800 (format like military time)
    # test 6 Septem 2031
    # test 05 06 2023 (US)
    # test 05 06 2023 (UK)
    # test 05 06 24 (UK)
    # test 05 06 24 (UK)
    # test 
    # test 19 02 2024 12:30
        


if __name__ == '__main__':
    unittest.main()
