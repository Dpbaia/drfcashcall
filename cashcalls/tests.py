from django.test import TestCase
from django import utils
from cashcalls.models.bill.models import Bill
from datetime import date, timedelta

class BillTestCase(TestCase):
    def test_upfront_fees_are_calculated_correctly(self):
        """Upfront fees are correctly calculated"""
        upfront_bill = Bill.objects.create(type_of_fee = "up", amount_invested= 100, fee_percentage= 0.5, date= "2016-02-01", cash_call_status= "vl")
        self.assertEqual(upfront_bill.final_fee, 250)

    def test_older_yearly_fees_are_calculated_correctly(self):
        """Older yearly fees are correctly calculated"""
        first_year_yearly_fee = Bill.objects.create(type_of_fee = "yr", amount_invested= 100, fee_percentage= 0.5, date= "2019-02-01", cash_call_status= "vl")
        other_years_yearly_fee = Bill.objects.create(type_of_fee = "yr", amount_invested= 100, fee_percentage= 0.5, date= "2016-02-01", cash_call_status= "vl")
        self.assertEqual(round(first_year_yearly_fee.final_fee, 2), 4.38)
        self.assertEqual(other_years_yearly_fee.final_fee, 50)

    def test_recent_yearly_fees_are_calculated_correctly(self):
        """Recent yearly fees are correctly calculated"""
        current_date = utils.timezone.now().date()
        first_year_yearly_fee = Bill.objects.create(type_of_fee = "yr", amount_invested= 100, fee_percentage= 0.5, date= current_date - timedelta(1), cash_call_status= "vl")
        second_year_yearly_fee = Bill.objects.create(type_of_fee = "yr", amount_invested= 100, fee_percentage= 0.5, date= current_date.replace(year=current_date.year - 1) - timedelta(1), cash_call_status= "vl")
        third_year_yearly_fee = Bill.objects.create(type_of_fee = "yr", amount_invested= 100, fee_percentage= 0.5, date= current_date.replace(year=current_date.year - 2) - timedelta(1), cash_call_status= "vl")
        self.assertEqual(first_year_yearly_fee.final_fee, first_year_yearly_fee.date.timetuple().tm_yday/365 * 0.5 * 100)
        self.assertEqual(second_year_yearly_fee.final_fee, 50)
        self.assertEqual(third_year_yearly_fee.final_fee, 30)
