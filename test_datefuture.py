import unittest
from dateparser import future_datetime as future, Especial
from datetime import datetime

class TestFutureDate(unittest.TestCase):

    def test_especial_later(self):
        base_date = datetime(2023,10,27,11,30,0)
        self.assertEqual(future(especial=Especial.LATER, base_date=base_date), datetime(2023,10,27,15,0,0),
            "It should be 4 hours later without minutes and seconds")

    def test_especial_weekend(self):
        # laborable day
        base_date = datetime(2023,10,25,11,30,0) # Wednesday
        self.assertEqual(future(base_date=base_date, especial=Especial.WEEKEND), datetime(2023,10,28,8,0), "Should be next Saturday")
        
        # Saturday
        base_date = datetime(2023,10,28,11,30,0) # Saturday
        self.assertEqual(future(base_date=base_date, especial=Especial.WEEKEND), datetime(2023,11,4,8,0), "Should be Saturday next week")
    
    def test_tonight(self):
        # morning
        base_date = datetime(2023,10,25,11,30,0) # morning
        self.assertEqual(future(base_date=base_date, especial=Especial.TONIGHT), datetime(2023,10,25,20,0), "Should be today at 20:00")

        # night
        base_date = datetime(2023,10,25,20,30,0) # night
        self.assertEqual(future(base_date=base_date, especial=Especial.TONIGHT), None, "Should be None because it is already tonight")

    def test_just_wednesday(self):
        WEDNESDAY = 2
        # it's Wednesday, so returns 7 days ahead
        base_date = datetime(2023,10,25)
        self.assertEqual(future(base_date=base_date, weekday=WEDNESDAY), datetime(2023,11,1,8,0), "Should be next Wednesday")

        # it's Friday, so returns 5 days ahead
        base_date = datetime(2023,11,3)
        self.assertEqual(future(base_date=base_date, weekday=WEDNESDAY), datetime(2023,11,8,8,0), "Should be next Wednesday")

        # it's Monday, so returns 2 days ahead
        base_date = datetime(2023,11,13)
        self.assertEqual(future(base_date=base_date, weekday=WEDNESDAY), datetime(2023,11,15,8,0), "Should be next Wednesday")

    def test_just_18th(self):
        # it's 18th, so returns 18th next month
        base_date = datetime(2023,10,18,9)
        self.assertEqual(future(base_date=base_date, day_number=18), datetime(2023,11,18,8,0), "Should be 18th next month")

        # it's 19th, so returns 18th next month
        base_date = datetime(2023,10,19)
        self.assertEqual(future(base_date=base_date, day_number=18), datetime(2023,11,18,8,0), "Should be 18th next month")

        # it's 17th, so returns 17th same month
        base_date = datetime(2023,10,17)
        self.assertEqual(future(base_date=base_date, day_number=18), datetime(2023,10,18,8,0), "Should be 18th same month")

    def test_edge_cases(self):
        # test 31st in June 5th, should return 31st July
        base_date = datetime(2023,6,5)
        self.assertEqual(future(base_date=base_date, day_number=31), datetime(2023,7,31,8,0), "Should be 31st July")

        # test 8am in January 31st 9 am, should return 8am on February 1st
        base_date = datetime(2023,1,31,9)
        self.assertEqual(future(base_date=base_date, hour=8), datetime(2023,2,1,8,0), "Should be 8am in February 1st")

        # test 8am in Dicember 31st 9 am, should return 8am on January 1st
        base_date = datetime(2023,12,31,9)
        self.assertEqual(future(base_date=base_date, hour=8), datetime(2024,1,1,8,0), "Should be 8am in January 1st")

        # test February 29th in April 2023, should return February 29th in 2024
        base_date = datetime(2023,4,1,9)
        self.assertEqual(future(base_date=base_date, month=2, day_number=29), datetime(2024,2,29,8,0), "Should be February 29th 2024")

        # test February 29th in April 2022, should return February 29th in 2023
        base_date = datetime(2022,4,1,9)
        self.assertEqual(future(base_date=base_date, month=2, day_number=29), datetime(2023,3,1,8,0), "Should be March 1st 2023")

    def test_just_april(self):
        APRIL = 4
        # it's June, so returns April next year (2024-04-01 08:00)
        base_date = datetime(2023,6,5)
        self.assertEqual(future(base_date=base_date, month=APRIL), datetime(2024,4,1,8,0), "Should be April next year")


        # it's April, so returns April next year
        base_date = datetime(2023,4,10)
        self.assertEqual(future(base_date=base_date, month=APRIL), datetime(2024,4,1,8), "Should be April next year")

        # it's February, so returns April this year (2023-04-01 08:00)
        base_date = datetime(2023,2,15)
        self.assertEqual(future(base_date=base_date, month=APRIL), datetime(2023,4,1,8,0), "Should be April same year")        

    def test_just_2023(self):
        # it's 2023, so returns None
        base_date = datetime(2023,5,1)
        self.assertEqual(future(base_date=base_date, year=2023), None, "Should be None (same year)")
        
        # it's 2022, so returns 2023-01-01 08:00
        base_date = datetime(2022,6,5)
        self.assertEqual(future(base_date=base_date, year=2023), datetime(2023,1,1,8,0), "Should be first day of 2023")

        # it's 2024, so returns None
        base_date = datetime(2024,6,5)
        self.assertEqual(future(base_date=base_date, year=2023), None, "Should be None (previous year)")

    def test_2nd_may(self):
        # it's 2nd May 2023, so returns 2024-05-02 08:00
        base_date = datetime(2023,5,2,9)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5), datetime(2024,5,2,8,0), "Should be 2nd May 2024")

        # it's 1st May 2023, so returns 2023-05-02 08:00
        base_date = datetime(2023,5,1)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5), datetime(2023,5,2,8,0), "Should be 2nd May 2023")
        
        # it's 3rd May 2023, so returns 2024-05-02 08:00
        base_date = datetime(2023,5,3)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5), datetime(2024,5,2,8,0), "Should be 2nd May 2024")

        # it's 15th April 2023, so returns 2023-05-02 08:00
        base_date = datetime(2023,4,15)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5), datetime(2023,5,2,8,0), "Should be 2nd May 2023")

        # it's 10th June 2023, so returns 2024-05-02 08:00
        base_date = datetime(2023,6,10)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5), datetime(2024,5,2,8,0), "Should be 2nd May 2024")

        # try with hour
        base_date = datetime(2023,6,10,8)
        self.assertEqual(future(base_date=base_date, day_number=2, month=5, hour=10, minute=30), datetime(2024,5,2,10,30), "Should be 2nd May 2024 10:30")

    def test_april_2023(self):
        # # it's February 2023, so returns 2023-04-01 08:00
        base_date = datetime(2023,2,1)
        self.assertEqual(future(base_date=base_date, month=4, year=2023), datetime(2023,4,1,8,0), "Should be April 2023")

        # # it's April 2023, so returns None
        base_date = datetime(2023,4,1,8)
        self.assertEqual(future(base_date=base_date, month=4, year=2023), None, "Should be None (same month)")

        # # it's June 2023, so returns None
        base_date = datetime(2023,6,1)
        self.assertEqual(future(base_date=base_date, month=4, year=2023), None, "Should be None (previous month)")

        # try with hour 11:15
        base_date = datetime(2023,2,1,8,0)
        self.assertEqual(future(base_date=base_date, month=4, year=2023, hour=11, minute=15), datetime(2023,4,1,11,15), "Should be April 1st 2023 11:15")

    def test_16th_2024(self):
        # it's 16th Jan 2024, so returns next month
        base_date = datetime(2024,1,16, 9)
        self.assertEqual(future(base_date=base_date, day_number=16, year=2024), datetime(2024,2,16,8,0), "Should be next month")

        # it's 18th Jan 2024, so returns 16th Feb 2024
        base_date = datetime(2024,1,18)
        self.assertEqual(future(base_date=base_date, day_number=16, year=2024), datetime(2024,2,16,8,0), "Should be 16th next month")

        # it's 1st January 2023 so returns 2024-01-16 08:00
        base_date = datetime(2023,1,1)
        self.assertEqual(future(base_date=base_date, day_number=16, year=2024), datetime(2024,1,16,8,0), "Should be 16th January 2024")

        # try 4 pm
        base_date = datetime(2023,1,1,8)
        self.assertEqual(future(base_date=base_date, day_number=16, year=2024, hour=16), datetime(2024,1,16,16,0), "Should be 16th January 2024 16:00")

    def test_april_15th_2023(self):
        # it's April 1st 2023 so returns 2023-04-15 08:00
        # print("First case")
        base_date = datetime(2023,1,4)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023), datetime(2023,4,15,8,0), "Should be April 15th 2023")

        # print("Second case")
        # it's April 15th 2023 so returns None
        base_date = datetime(2023,4,15,9)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023), None, "Should be None (same day)")

        # print("Third case")
        # it's April 30th 2023 so returns None
        base_date = datetime(2023,4,30)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023), None, "Should be None (previous day)")


    def test_april_15th_2023_9am(self):
        # it's April 15th 2023 8am so returns 2023-04-15 09:00
        base_date = datetime(2023,4,15,8)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023, hour=9), datetime(2023,4,15,9,0), "Should be April 15th 2023 9am")

        # it's April 15th 2023 9am so returns None
        base_date = datetime(2023,4,15,9)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023, hour=9), None, "Should be None (same date and time)")

        # it's April 15th 2023 10am so returns None
        base_date = datetime(2023,4,15,10)
        self.assertEqual(future(base_date=base_date, day_number=15, month=4, year=2023, hour=10), None, "Should be None (previous time)")


    def test_just_9am(self):
        # it's 8am so returns today 9am
        base_date = datetime(2023,4,15,8)
        self.assertEqual(future(base_date=base_date, hour=9), datetime(2023,4,15,9,0), "Should be today 9am")

        # it's 9am so returns tomorrow 9am
        base_date = datetime(2023,4,15,9)
        self.assertEqual(future(base_date=base_date, hour=9), datetime(2023,4,16,9,0), "Should be tomorrow 9am")

        # it's 10am so returns tomorrow 9am
        base_date = datetime(2023,4,15,10)
        self.assertEqual(future(base_date=base_date, hour=9), datetime(2023,4,16,9,0), "Should be tomorrow 9am")


    def test_tuesday_april(self):
        # last Tuesday in April 2023 is April 25th
        # it's Wednesday after last Tuesday in April, so returns first Tuesday in April next year
        base_date = datetime(2023,4,26,8)
        self.assertEqual(future(base_date=base_date, weekday=1, month=4), datetime(2024,4,2,8,0), "Should be first Tuesday in April next year")

        # it's March same year, so returns first Tuesday in April this year
        base_date = datetime(2023,1,15)
        self.assertEqual(future(base_date=base_date, weekday=1, month=4), datetime(2023,4,4,8,0), "Should be first Tuesday in April this year")

        # it's May same year, so returns first Tuesday in April next year
        base_date = datetime(2023,5,26)
        self.assertEqual(future(base_date=base_date, weekday=1, month=4), datetime(2024,4,2,8,0), "Should be first Tuesday in April next year")

    def test_monday_month_starts_on_monday(self):
        base_date = datetime(2023,11,6,8)
        self.assertEqual(future(base_date=base_date, weekday=0, month=1), datetime(2024,1,1,8,0,0), "Should be first Monday in January 2024, which is 1st")

    def test_thursday_2024(self):
        # it's Friday after last Thursday in 2024, so returns None
        base_date = datetime(2024,12,27)
        self.assertEqual(future(base_date=base_date, weekday=3, year=2024), None, "Should be None")

        # it's Thursday same year, so returns next Thursday 08:00
        base_date = datetime(2024,12,12,11)
        self.assertEqual(future(base_date=base_date, weekday=3, year=2024, hour=8), datetime(2024,12,19,11), "Should be next Thursday")

        # it's Friday same year, so returns next Thursday 08:00
        base_date = datetime(2024,12,13)
        self.assertEqual(future(base_date=base_date, weekday=3, year=2024), datetime(2024,12,19), "Should be next Thursday")
    
    def test_wednesday_2nd(self):
        # it's April 2nd 2023, first 2nd Wedneesday is in August
        base_date = datetime(2023,4,2,9)
        self.assertEqual(future(base_date=base_date, day_number=2, weekday=2), datetime(2023,8,2,8,0), "Should be first 2nd that is Wednesday since next month")

        # it's Tuesday 1st, so returns tomorrow
        base_date = datetime(2022,11,1,9)
        self.assertEqual(future(base_date=base_date, day_number=2, weekday=2), datetime(2022,11,2,8,0), "Should be next day")

        # it's 3rd, so returns first 2nd that is Wednesnday since next month
        base_date = datetime(2023,9,3,9)
        self.assertEqual(future(base_date=base_date, day_number=2, weekday=2), datetime(2024,10,2,8,0), "Should be first 2nd that is Wednesday since next month")
    
    def test_thursday_3rd_january(self):
        # it's 3rd January 2023, first 3rd Thursday is in February
        base_date = datetime(2023,1,3,9)
        self.assertEqual(future(base_date=base_date, day_number=3, month=1, weekday=3), datetime(2030,1,3,8,0), "Should be first 3rd that is Thursday since next year")

        # it's 1st January 2019, so returns 3rd January 209
        base_date = datetime(2019,1,1,9)
        self.assertEqual(future(base_date=base_date, day_number=3, month=1, weekday=3), datetime(2019,1,3,8,0), "Should be 3rd January 2019")

        # it's 4th January 2030, so returns first 3rd that is Thursday since next month
        base_date = datetime(2030,1,4,9)
        self.assertEqual(future(base_date=base_date, day_number=3, month=1, weekday=3), datetime(2036,1,3,8,0), "Should be first 3rd that is Thursday since next month")

    def test_friday_4th_2024(self):
        # it's 4th January 2024, first 4th Friday is in October
        base_date = datetime(2024,1,4,9)
        self.assertEqual(future(base_date=base_date, day_number=4, year=2024, weekday=4), datetime(2024,10,4,8,0), "Should be first 4th that is Friday since next month")

        # it's 3rd October 2024, so returns 4th October 2024
        base_date = datetime(2024,10,3,9)
        self.assertEqual(future(base_date=base_date, day_number=4, year=2024, weekday=4), datetime(2024,10,4,8,0), "Should be 4th October 2024")

        # it's 5th October 2024, so returns None
        base_date = datetime(2024,10,5,9)
        self.assertEqual(future(base_date=base_date, day_number=4, year=2024, weekday=4), None, "There is no 4th Friday in 2024 after October")
    
    def test_saturday_march_2024(self):
        # it's 5th January 2024, first Saturday March is March 2nd
        base_date = datetime(2024,1,5,9)
        self.assertEqual(future(base_date=base_date, month=3, year=2024, weekday=5), datetime(2024,3,2,8,0), "Should be first Saturday in March 2024")

        # it's 4th March 2024, so returns 9th March 2024
        base_date = datetime(2024,3,4,9)
        self.assertEqual(future(base_date=base_date, month=3, year=2024, weekday=5), datetime(2024,3,9,9,0), "Should be second Saturday in March 2024")

    def test_friday_march_2024(self):
        # it's Saturday 30th March 2024, so returns None
        base_date = datetime(2024,3,30,9)
        self.assertEqual(future(base_date=base_date, month=3, year=2024, weekday=4), None, "There is no Saturday in March after March 30th 2024")
        
    def test_just_q2(self):
        # it's q1_2023, so returns 2023-04-01
        base_date = datetime(2023,1,1,9)
        self.assertEqual(future(base_date=base_date, quarter=2), datetime(2023,4,1,8), "Should be April 1st 2023")

        # it's q2_2023, so returns 2024-04-01 08:00
        base_date = datetime(2023,4,5,9)
        self.assertEqual(future(base_date=base_date, quarter=2), datetime(2024,4,1,8), "Should be April 1st 2024")

        # it's q4_2023, so returns 2024-04-01 08:00
        base_date = datetime(2023,12,5,9)
        self.assertEqual(future(base_date=base_date, quarter=2), datetime(2024,4,1,8), "Should be April 1st 2024")
        

    def test_q1_2023(self):
        # it's q1_2023, so returns None
        base_date = datetime(2023,1,1,9)
        self.assertEqual(future(base_date=base_date, quarter=1, year=2023), None, "Should be None")

        # it's q3_2022, so returns 2023-01-01 08:00
        base_date = datetime(2022,12,1,9)
        self.assertEqual(future(base_date=base_date, quarter=1, year=2023), datetime(2023,1,1,8), "Should be January 1st 2023")

        # it's q4_2023, so returns None
        base_date = datetime(2023,10,1,9)
        self.assertEqual(future(base_date=base_date, quarter=1, year=2023), None, "Should be None")
        

    def test_q2_9am(self):
        # it's q1_2023, so returns 2023-04-01
        base_date = datetime(2023,1,1,9)
        self.assertEqual(future(base_date=base_date, quarter=2, hour=9), datetime(2023,4,1,9), "Should be April 1st 2023 09am")

        # it's q2_2023, so returns 2024-04-01 09:00
        base_date = datetime(2023,4,5,9)
        self.assertEqual(future(base_date=base_date, quarter=2, hour=9), datetime(2024,4,1,9), "Should be April 1st 2024 09am")

        # it's q4_2023, so returns 2024-04-01 09:00
        base_date = datetime(2023,12,5,9)
        self.assertEqual(future(base_date=base_date, quarter=2, hour=9), datetime(2024,4,1,9), "Should be April 1st 2024")

    def test_inconsistent_weekday(self):
        # ask for Friday, October 26th 2023, 26th is Thursday so returns Thursday, October 26th 2023
        base_date = datetime(2023,2,26,7)
        self.assertEqual(future(base_date=base_date, month=10, day_number=26, year=2023, weekday=4), None, "Should be None because 2023-26-10 is Thursday not Friday")

        base_date = datetime(2023,1,26,7)
        self.assertEqual(future(base_date=base_date, month=10, day_number=26, year=2023, weekday=3), datetime(2023,10,26,8), "Should be 2023-26-10 because it is Thursday")


    def test_in_200_seconds(self):
        base_date = datetime(2023,4,1,8,15)
        self.assertEqual(future(base_date=base_date, second=200, relative=True), datetime(2023,4,1,8,18,20), "Should be 200 seconds later")

    def test_in_90_minutes(self):
        base_date = datetime(2023,4,1,8,15)
        self.assertEqual(future(base_date=base_date, minute=90, relative=True), datetime(2023,4,1,9,45,0), "Should be 90 minutes later")

    def test_in_3_hours(self):
        base_date = datetime(2023,4,1,8,15)
        self.assertEqual(future(base_date=base_date, hour=3, relative=True), datetime(2023,4,1,11,15,0), "Should be 3 hours later")


    def test_in_4_days(self):
        base_date = datetime(2023,4,1,16,25)
        self.assertEqual(future(base_date=base_date, days=4, relative=True), datetime(2023,4,5,16,25,0), "Should be 3 hours later")


    def test_in_5_weeks(self):
        base_date = datetime(2023,4,1,17,0)
        self.assertEqual(future(base_date=base_date, weeks=5, relative=True), datetime(2023,5,6,17,0,0), "Should be 5 weeks  later")


    def test_in_6_months(self):
        base_date = datetime(2023,7,2,18,10)
        self.assertEqual(future(base_date=base_date, month=6, relative=True), datetime(2024,1,2,18,10,0), "Should be 6 months later")
        

    def test_in_1_year(self):
        base_date = datetime(2023,8,3,19,5)
        self.assertEqual(future(base_date=base_date, year=1, relative=True), datetime(2024,8,3,19,5,0), "Should be 1 year later")


    def test_in_1_month_and_3_days(self):
        base_date = datetime(2023,8,3,19,5)
        self.assertEqual(future(base_date=base_date, month=1, days=3, relative=True), datetime(2023,9,6,19,5,0), "Should be 1 month and 3 days later")


    def test_in_3_weeks_and_2_days(self):
        base_date = datetime(2023,8,3,19,5)
        self.assertEqual(future(base_date=base_date, weeks=3, days=2, relative=True), datetime(2023,8,26,19,5,0), "Should be 23 days later")


    def test_in_5_hours_and_40_minutes(self):
        base_date = datetime(2023,8,3,19,5)
        self.assertEqual(future(base_date=base_date, hour=5, minute=40, relative=True), datetime(2023,8,4,0,45,0), "Should be 5 hours and 40 minutes later")


    def test_in_2_years_and_5_months(self):
        base_date = datetime(2023,8,3,19,5)
        self.assertEqual(future(base_date=base_date, year=2, month=5, relative=True), datetime(2026,1,3,19,5,0), "Should be 28 months later")
        
 

    

if __name__ == '__main__':
    unittest.main()
