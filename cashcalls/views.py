from django.shortcuts import render
from django.contrib.auth.models import User, Group
from cashcalls.models.bill.models import Bill
from rest_framework import viewsets
from rest_framework import permissions
from cashcalls.serializers import UserSerializer, GroupSerializer, BillSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bills to be viewed or edited.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    # Maybe find way of blocking out fields when they not needed?
