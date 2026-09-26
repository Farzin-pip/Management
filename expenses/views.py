from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import ExpenseCategory, Expenses, ExpenseAllocations, Invoices, InvoiceItem, Payment
from .serializers import (ExpenseCategorySerializer, ExpensesSerializer, ExpenseAllocationsSerializer,
                          InvoicesSerializer, InvoiceItemSerializer, PaymentSerializer)



class ExpenseCategoryView(APIView):
    def get(self, request):
        expense_category = ExpenseCategory.objects.all()
        ser_data = ExpenseCategorySerializer(instance=expense_category, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpenseCategorySerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense_category = ExpenseCategory.objects.get(pk=pk)
        ser_data = ExpenseCategorySerializer(instance=expense_category, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_category = ExpenseCategory.objects.get(pk=pk)
        expense_category.delete()
        return Response({'message': 'Expense Category Deleted!'}, status=status.HTTP_200_OK)


class ExpensesView(APIView):
    def get(self, request):
        expenses = Expenses.objects.all()
        ser_data = ExpensesSerializer(instance=expenses, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpensesSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expenses = Expenses.objects.get(pk=pk)
        ser_data = ExpensesSerializer(instance=expenses, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expenses = Expenses.objects.get(pk=pk)
        expenses.delete()
        return Response({'message': 'Expenses Deleted!'}, status=status.HTTP_200_OK)

class ExpenseAllocationsView(APIView):
    def get(self, request):
        expense_allocations = ExpenseAllocations.objects.all()
        ser_data = ExpenseAllocationsSerializer(instance=expense_allocations, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpenseCategorySerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense_allocations = ExpenseAllocations.objects.get(pk=pk)
        ser_data = ExpenseAllocationsSerializer(instance=expense_allocations, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_allocations = ExpenseAllocations.objects.get(pk=pk)
        expense_allocations.delete()
        return Response({'message': 'Expense Allocation Deleted!'}, status=status.HTTP_200_OK)


class InvoicesView(APIView):
    def get(self, request):
        invoices = Invoices.objects.all()
        ser_data =InvoicesSerializer(instance=invoices, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = InvoicesSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        invoices = Invoices.objects.get(pk=pk)
        ser_data = InvoicesSerializer(instance=invoices, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        invoices = Invoices.objects.get(pk=pk)
        invoices.delete()
        return Response({'message': 'Invoices Deleted!'}, status=status.HTTP_200_OK)


class InvoiceItemView(APIView):
    def get(self, request):
        invoice_items = InvoiceItem.objects.all()
        ser_data = InvoiceItemSerializer(instance=invoice_items, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = InvoiceItemSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        invoice_item = InvoiceItem.objects.get(pk=pk)
        ser_data = InvoiceItemSerializer(instance=invoice_item, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        invoice_item = InvoiceItem.objects.get(pk=pk)
        invoice_item.delete()
        return Response({'message': 'Invoice Item Deleted!'}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        ser_data = PaymentSerializer(instance=payments, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = PaymentSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        ser_data = PaymentSerializer(instance=payment, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        payment.delete()
        return Response({'message': 'Payment Deleted!'}, status=status.HTTP_200_OK)

