from django.utils import timezone
from rest_framework import serializers
from accounts.serializers import UserSerializer
from buildings.serializers import UnitSerializer
from .models import (ExpenseCategory, Expenses, ExpenseAllocations, Invoices, InvoiceItem, Payment, InvoicePenalty)


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


class DebtItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class DebtPaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    paid_at = serializers.DateTimeField(allow_null=True)
    reference_id = serializers.CharField(allow_null=True)


class UnitInvoiceDebtSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    status = serializers.CharField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    due_date = serializers.DateField(allow_null=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    penalty = serializers.DecimalField(max_digits=12, decimal_places=2)
    items = DebtItemSerializer(many=True)
    payments = DebtPaymentSerializer(many=True)


class UnitDebtDetailSerializer(serializers.Serializer):
    unit_id = serializers.IntegerField()
    unit_number = serializers.CharField()
    invoices = UnitInvoiceDebtSerializer(many=True)
    total_debt = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_penalty = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=14, decimal_places=2)

