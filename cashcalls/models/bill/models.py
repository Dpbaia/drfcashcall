from django.db import models
from django.core.exceptions import ValidationError
from fastapi import UploadFile
from datetime import date, timedelta
from django import utils
from calendar import isleap


# Create your models here.

# Link all of this to the serializers
# Then create a new view
# Then finally send it to routes so we can see it on the API
# TODO write tests
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
        choices = TYPE_OF_FEE_CHOICES,
        default = 'Upfront',
        max_length = 10,
    )
    amount_invested = models.FloatField(null = True, blank = True)
    fee_percentage = models.FloatField(null = True, blank = True)
    date = models.DateField(blank = False)
    cash_call_status = models.CharField(
        choices = CASH_CALL_STATUS_CHOICES,
        max_length = 10,
    )
    final_fee = models.FloatField(default = 0, editable = False)
    investor = models.CharField(max_length = 80, default="Investor 1")

    def clean(self):
        super().clean()
        type_of_fee = self.type_of_fee
        fee_percentage = self.fee_percentage
        if type_of_fee == 'up' or type_of_fee == 'yr':
            if not (fee_percentage and self.amount_invested):
                raise ValidationError(
                    "Must enter amount invested and fee percentage for this type of fee"
                ) # Transform this into a status code for the restAPI.
                
    def save(self, *args, **kwargs):
        self.full_clean()
        self.calculate_bill()
        super(Bill, self).save(*args, **kwargs)

    def calculate_bill(self):
        if self.type_of_fee == 'up':
            self.final_fee = self.fee_percentage * self.amount_invested * 5
        elif self.type_of_fee == 'yr':
            if self.date < date(2019,4,30) and ((date(2019,4,30) - self.date).days/365 <= 1) :
                self.final_fee = self.date.timetuple().tm_yday/365 * self.fee_percentage * self.amount_invested
            elif self.date < date(2019,4,30):
                self.final_fee = self.fee_percentage * self.amount_invested
            else:
                years_since_investment = (utils.timezone.now().date() - self.date).days/365
                if years_since_investment <= 1:
                    days_of_year = 366 if isleap(self.date.year) else 365
                    self.final_fee = (self.date.timetuple().tm_yday / days_of_year) * self.fee_percentage * self.amount_invested
                elif years_since_investment <= 2:
                    self.final_fee = self.fee_percentage * self.amount_invested
                elif years_since_investment <= 3:
                    self.final_fee = (self.fee_percentage - 0.20) * self.amount_invested
                elif years_since_investment <= 4:
                    self.final_fee = (self.fee_percentage - 0.5) * self.amount_invested
                else:
                    self.final_fee = (self.fee_percentage - 1) * self.amount_invested
        else:
            self.final_fee = 42 #TODO code the membership price, 3000 euro per year if investments that year are lower than 50000 euros
    # Kind of bill:
		# !Upfront fees: fee % x amount * 5 years
		# !Yearly
			#if before 04/2019 && if how_many_years <= 1
				# date / 365 * fee * amount
			# elsif before 04/2019 
				# amount * fee
			# else
				# case how_many_years 
					# 1
						#Date / amount of days in that year ( ano bissexto vai tomar no cu como caracas eu vou checar se é bissexto fdp) * fee * amount
                    # 2
                        #Fee * amount
                    # Third year:
                        #(fee percentage - 0.20 %) x amount invested
                    # Fourth year:
                        #(fee percentage - 0.50 %) x amount invested
                    # Following years:
                        #(fee percentage - 1 %) x amount invested
        # Create a way of calculating !membership
            # If all amount invested > 50000, final fee = 0 
            # Else, final fee = 3000


    
# Bill.objects.create(type_of_fee = "yr", amount_invested= 2.0, fee_percentage= 2.0, date= "2016-02-01", cash_call_status= "vl", investor= "aaaaa")