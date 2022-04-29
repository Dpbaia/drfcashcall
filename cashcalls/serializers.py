from django.contrib.auth.models import User, Group
from cashcalls.models.bill.models import Bill
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ['url', 'type_of_fee', 'amount_invested', 'fee_percentage', 'date', 'cash_call_status', 'investor', 'final_fee']

