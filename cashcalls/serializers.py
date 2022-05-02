from cashcalls.models.bill.models import Bill
from rest_framework import serializers


class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ['url', 'type_of_fee', 'amount_invested', 'fee_percentage',
                  'date', 'cash_call_status', 'investor', 'final_fee']
