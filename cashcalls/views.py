from cashcalls.models.bill.models import Bill
from rest_framework import viewsets
from cashcalls.serializers import BillSerializer
from django_filters.rest_framework import DjangoFilterBackend


class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bills to be viewed or edited.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['investor']
    def get_queryset(self):
        """
        Optionally restricts the returned bills to a given investor,
        by filtering against a `investor` query parameter in the URL.
        """
        queryset = Bill.objects.all()
        investor = self.request.query_params.get('investor')
        if investor is not None:
            queryset = queryset.filter(investor=investor)
        return queryset