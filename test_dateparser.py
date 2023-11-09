import unittest
from dateparser import parse
from datetime import datetime

class TestDateParser(unittest.TestCase):

    def test_tomorrow(self):
        # test tomorrow
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 11, 33, 0, 0)
        self.assertEqual(parse('tomorrow', base_date=base_date), expected_date)

        # test tmrw
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 11, 33, 0, 0)
        self.assertEqual(parse('tmrw', base_date=base_date), expected_date)

        # test tomor
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 11, 33, 0, 0)
        self.assertEqual(parse('tomor', base_date=base_date), expected_date)

        # test mañana
        base_date = datetime(2023, 11, 8, 11, 33, 0)
        expected_date = datetime(2023, 11, 9, 11, 33, 0, 0)
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

        # on Tuesday

        # next Tuesday
        pass

    # def test_march(self):
    #     # just March

    #     # next March
    #     pass

    # def test_next_month(self):
    #     pass

    # def test_q1(self):
    #     # test q1

    #     # test qone
    #     pass

    # def test_next_quarter(self):
    #     pass

    # def test_2024(self):
    #     pass

    # def test_next_year(self):
    #     pass

    # def test_noon(self):
    #     # test just noon

    #     # test tomorrow noon

    #     # test Monday noon
    #     pass

    # def test_midnight(self):
    #     # test just midnight

    #     # test tomorrow midnight

    #     # test Friday midnight
    #     pass

    # def test_morning(self):
    #     # test just morning

    #     # test tomorrow morning

    #     # test Thursday morning
    #     pass

    # def test_night(self):
    #     # test just night

    #     # test tomorrow night

    #     # test Tuesday night

    #     # test just evening

    #     # test tomorrow evening

    #     # test Wednesday evening
    #     pass

    # def test_q2(self):
    #     # test q2

    #     # test qtwo
    #     pass

    # def test_just_hour(self):
    #     # test 5am

    #     # test 5pm

    #     # test 06am
        
    #     # test 07pm
    #     pass

    # def test_hour_and_timezone(self):
    #     # test 5am CT

    #     # test 6pm Buenos Aires
    #     pass

    # def test_hour_minute(self):
    #     # test 5:30

    #     # test 05:30

    #     # test 17 25

    #     # test 5:30pm

    #     pass

    # def test_just_day_ordinal(self):
    #     # test 1st

    #     # test 02nd

    #     # test 3rd

    #     # test 08th

    #     # test 31th

    #     # test 32th
    #     pass

    # def test_just_month(self):
    #     # test January

    #     # test Feb

    #     # test Marc
    #     pass

    # def test_just_year(self):
    #     # test 2024
    #     pass
        
    # def test_day_and_month(self):
    #     # test 1st April

    #     # test 02 May

    #     # test 03rd Jun

    #     pass

    # def test_day_month_year(self):
    #     # test 4th July 2023

    #     # test 05th Augu 24

    #     # test 6 Septem 2031
    #     pass

    # def test_day_and_month_separated_by_slash_dash_or_hyphen(self):
    #     # test 7-Oct

    #     # test 08/Nove

    #     # test 9-12 with locale set to US

    #     # test 9-12 with locale set to UK

    #     # test 10/01 with locale set to US

    #     # test 10/01 with locale set to UK

    #     # test 11\Febr

    #     # test 12–April (dash is not hyphen)
    #     pass

    # def test_day_month_year_separated_by_slash_dash_or_hyphen(self):
    #     # test 13-May-2024

    #     # test 14/Jun/24

    #     # test 15\06\2032

    #     # test 16–7–2033 (dash is not hyphen)

    #     # test 2024-08-05

    #     # test 2023-9-6
    #     pass

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

    
if __name__ == '__main__':
    unittest.main()
