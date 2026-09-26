from rest_framework import serializers
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