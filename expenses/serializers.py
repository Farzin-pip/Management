# from time import timezone
from django.utils import timezone

from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from buildings.serializers import UnitSerializer
from .models import (ExpenseCategory, Expenses, ExpenseAllocations, Invoices, InvoiceItem, Payment)


class ExpenseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'


class ExpenseAllocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseAllocations
        fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoices
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class OverdueInvoicesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    unit_id = UnitSerializer(read_only=True)
    date = serializers.SerializerMethodField()


    class Meta:
        model = Invoices

        fields = [
            'id',
            'user',
            'unit_id',
            'period_start',
            'period_end',
            'due_date',
            'total_amount',
            'status',
            'date'
        ]

    def get_date(self, obj):
        return timezone.now()

class SendOverdueSMSSerializer(serializers.Serializer):

    invoice_id = serializers.IntegerField()

