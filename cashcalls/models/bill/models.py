from datetime import date
from calendar import isleap
from django import utils
from django.db import models
from cashcalls.custom_handlers import CustomBadRequest


class Bill(models.Model):
    UPFRONT = 'up'
    YEARLY = 'yr'
    MEMBERSHIP = 'mb'
    TYPE_OF_FEE_CHOICES = [
        (UPFRONT, 'Upfront'),
        (YEARLY, 'Yearly'),
        (MEMBERSHIP, 'Membership')
    ]
    VALIDATED = 'vl'
    SENT = 'sn'
    PAID = 'pd'
    OVERDUE = 'od'
    CASH_CALL_STATUS_CHOICES = [
        (VALIDATED, 'Validated'),
        (SENT, 'Sent'),
        (PAID, 'Paid'),
        (OVERDUE, 'Overdue')
    ]

    type_of_fee = models.CharField(
        choices=TYPE_OF_FEE_CHOICES,
        default='Upfront',
        max_length=10,
    )
    amount_invested = models.FloatField(null=True, blank=True)
    fee_percentage = models.FloatField(null=True, blank=True)
    date = models.DateField(blank=False)
    cash_call_status = models.CharField(
        choices=CASH_CALL_STATUS_CHOICES,
        max_length=10,
    )
    final_fee = models.FloatField(default=0, editable=False)
    investor = models.CharField(max_length=80, default="Investor 1")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.calculate_bill()
        self.final_fee = round(self.final_fee, 2)
        super(Bill, self).save(*args, **kwargs)

    def calculate_bill(self):
        if self.type_of_fee == 'up':
            self.final_fee = self.fee_percentage * self.amount_invested * 5
        elif self.type_of_fee == 'yr':
            if self.date < date(2019, 4, 30) and ((date(2019, 4, 30) - self.date).days/365 <= 1):
                self.final_fee = self.date.timetuple().tm_yday/365 * self.fee_percentage * \
                    self.amount_invested
            elif self.date < date(2019, 4, 30):
                self.final_fee = self.fee_percentage * self.amount_invested
            else:
                self.__calculate_based_on_years_since_investment()
        else:
            all_bills_by_current_investor = Bill.objects.filter(
                investor=self.investor)
            amount_invested = 0
            for bill in all_bills_by_current_investor:
                amount_invested += bill.amount_invested
            self.final_fee = 0 if (amount_invested >= 50000) else 3000

    def clean(self):
        super().clean()
        type_of_fee = self.type_of_fee
        fee_percentage = self.fee_percentage
        if type_of_fee == 'up' or type_of_fee == 'yr':
            if not (fee_percentage and self.amount_invested):
                raise CustomBadRequest(
                    detail="This type of fee requires fee percentage and amount invested.")

    def __calculate_based_on_years_since_investment(self):
        years_since_investment = (
            utils.timezone.now().date() - self.date).days/365
        if years_since_investment <= 1:
            days_of_year = 366 if isleap(self.date.year) else 365
            self.final_fee = (self.date.timetuple(
            ).tm_yday / days_of_year) * self.fee_percentage * self.amount_invested
        elif years_since_investment <= 2:
            self.final_fee = self.fee_percentage * self.amount_invested
        elif years_since_investment <= 3:
            self.final_fee = (self.fee_percentage - 0.20) * \
                self.amount_invested
        elif years_since_investment <= 4:
            self.final_fee = (self.fee_percentage - 0.5) * self.amount_invested
        else:
            self.final_fee = (self.fee_percentage - 1) * self.amount_invested
