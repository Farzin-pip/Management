from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from kavenegar import HTTPException, APIException, KavenegarAPI
from django.conf import settings
from .models import ExpenseCategory, Expenses, ExpenseAllocations, Invoices, InvoiceItem, Payment
from .serializers import (ExpenseCategorySerializer, ExpensesSerializer, ExpenseAllocationsSerializer,
                          InvoicesSerializer, InvoiceItemSerializer, PaymentSerializer, OverdueInvoicesSerializer,
                          SendOverdueSMSSerializer)
from .selectors import (expense_category_list, expenses_list, expense_allocations_list, invoices_list,
                        invoice_items_list, payments_list, overdue_invoices_list, overdue_invoice_by_id)
from .services import (create_expense_category, update_expense_category, delete_expense_category,
                       create_expenses, update_expenses, delete_expenses,
                       create_expense_allocations, update_expense_allocations, delete_expense_allocations,
                       create_invoice, update_invoice, delete_invoice,
                       create_invoice_item, update_invoice_item, delete_invoice_item,
                       create_payment, update_payment, delete_payment)


class ExpenseCategoryView(APIView):
    def get(self, request):
        expense_category = expense_category_list()
        ser_data = ExpenseCategorySerializer(instance=expense_category, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpenseCategorySerializer(data=request.data)
        if ser_data.is_valid():
            expense_category = create_expense_category(ser_data.validated_data)
            return Response(ExpenseCategorySerializer(expense_category).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, pk=pk)
        ser_data = ExpenseCategorySerializer(instance=expense_category, data=request.data, partial=True)
        if ser_data.is_valid():
            expense_category = update_expense_category(expense_category, ser_data.validated_data)
            return Response(ExpenseCategorySerializer(expense_category).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_category = get_object_or_404(ExpenseCategory, pk=pk)
        delete_expense_category(expense_category)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpensesView(APIView):
    def get(self, request):
        expenses = expenses_list()
        ser_data = ExpensesSerializer(instance=expenses, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpensesSerializer(data=request.data)
        if ser_data.is_valid():
            expenses = create_expenses(ser_data.validated_data)
            return Response(ExpensesSerializer(expenses).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expenses = get_object_or_404(Expenses, pk=pk)
        ser_data = ExpensesSerializer(instance=expenses, data=request.data, partial=True)
        if ser_data.is_valid():
            expenses = update_expenses(expenses, ser_data.validated_data)
            return Response(ExpensesSerializer(expenses).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expenses = get_object_or_404(Expenses, pk=pk)
        delete_expenses(expenses)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseAllocationsView(APIView):
    def get(self, request):
        expense_allocations = expense_allocations_list()
        ser_data = ExpenseAllocationsSerializer(instance=expense_allocations, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = ExpenseAllocationsSerializer(data=request.data)
        if ser_data.is_valid():
            expense_allocations = create_expense_allocations(ser_data.validated_data)
            return Response(ExpenseAllocationsSerializer(expense_allocations).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense_allocations = get_object_or_404(ExpenseAllocations, pk=pk)
        ser_data = ExpenseAllocationsSerializer(instance=expense_allocations, data=request.data, partial=True)
        if ser_data.is_valid():
            expense_allocations = update_expense_allocations(expense_allocations, ser_data.validated_data)
            return Response(ExpenseAllocationsSerializer(expense_allocations).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense_allocations = get_object_or_404(ExpenseAllocations, pk=pk)
        delete_expense_allocations(expense_allocations)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvoicesView(APIView):
    def get(self, request):
        invoices = invoices_list()
        ser_data = InvoicesSerializer(instance=invoices, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = InvoicesSerializer(data=request.data)
        if ser_data.is_valid():
            invoice = create_invoice(ser_data.validated_data)
            return Response(InvoicesSerializer(invoice).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        invoice = get_object_or_404(Invoices, pk=pk)
        ser_data = InvoicesSerializer(instance=invoice, data=request.data, partial=True)
        if ser_data.is_valid():
            invoice = update_invoice(invoice, ser_data.validated_data)
            return Response(InvoicesSerializer(invoice).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        invoice = get_object_or_404(Invoices, pk=pk)
        delete_invoice(invoice)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvoiceItemView(APIView):
    def get(self, request):
        invoice_items = invoice_items_list()
        ser_data = InvoiceItemSerializer(instance=invoice_items, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = InvoiceItemSerializer(data=request.data)
        if ser_data.is_valid():
            invoice_item = create_invoice_item(ser_data.validated_data)
            return Response(InvoiceItemSerializer(invoice_item).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        invoice_item = get_object_or_404(InvoiceItem, pk=pk)
        ser_data = InvoiceItemSerializer(instance=invoice_item, data=request.data, partial=True)
        if ser_data.is_valid():
            invoice_item = update_invoice_item(invoice_item, ser_data.validated_data)
            return Response(InvoiceItemSerializer(invoice_item).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        invoice_item = get_object_or_404(InvoiceItem, pk=pk)
        delete_invoice_item(invoice_item)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentView(APIView):
    def get(self, request):
        payments = payments_list()
        ser_data = PaymentSerializer(instance=payments, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = PaymentSerializer(data=request.data)
        if ser_data.is_valid():
            payment = create_payment(ser_data.validated_data)
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        ser_data = PaymentSerializer(instance=payment, data=request.data, partial=True)
        if ser_data.is_valid():
            payment = update_payment(payment, ser_data.validated_data)
            return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        delete_payment(payment)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OverdueInvoicesView(APIView):
    def get(self, request):
        invoices = overdue_invoices_list()
        ser_data = OverdueInvoicesSerializer(instance=invoices, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class SendOverdueInvoiceSMSView(APIView):
    def post(self, request):
        ser_data = SendOverdueSMSSerializer(data=request.data)
        if ser_data.is_valid():
            invoice_id = ser_data.validated_data['invoice_id']
            try:
                invoice = overdue_invoice_by_id(invoice_id)
            except Invoices.DoesNotExist:
                return Response(
                    {'error': 'قبض معوقه‌ای با این شناسه پیدا نشد.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            user = invoice.user
            unit = invoice.unit_id
            message = (
                f'{user.first_name} {user.last_name} عزیز، '
                f'قبض واحد {unit.number} به مبلغ {invoice.total_amount} '
                f'پرداخت نشده است. لطفاً در اسرع وقت پرداخت کنید.'
            )

            try:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
                params = {
                    'sender': settings.KAVENEGAR_SENDER,
                    'receptor': user.phone_number,
                    'message': message
                }
                api.sms_send(params)
            except APIException:
                return Response(
                    {'error': 'خطا در ارتباط با سامانه پیامکی.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except HTTPException:
                return Response(
                    {'error': 'خطای HTTP هنگام ارسال پیامک.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response({
                'message': 'پیامک با موفقیت ارسال شد.',
                'invoice_id': invoice.id,
                'user_id': user.id,
                'phone_number': user.phone_number,
                'unit_number': unit.number,
                'amount': invoice.total_amount
            }, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

