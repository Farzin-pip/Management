from django.urls import path
from . import views

app_name = 'expenses'
urlpatterns = [
    path('expense_category/', views.ExpenseCategoryView.as_view()),
    path('expense_category/<int:pk>/', views.ExpenseCategoryView.as_view()),
    path('expense/', views.ExpensesView.as_view()),
    path('expense/<int:pk>/', views.ExpensesView.as_view()),
    path('expense_allocations/', views.ExpenseAllocationsView.as_view()),
    path('expense_allocations/<int:pk>/', views.ExpenseAllocationsView.as_view()),
    path('invoice/', views.InvoicesView.as_view()),
    path('invoice/<int:pk>/', views.InvoicesView.as_view()),
    path('invoice_items/', views.InvoiceItemView.as_view()),
    path('invoice_items/<int:pk>/', views.InvoiceItemView.as_view()),
    path('payments/', views.PaymentView.as_view()),
    path('payments/<int:pk>/', views.PaymentView.as_view()),
    path('overdue_invoices/', views.OverdueInvoicesView.as_view()),
    path('send_overdue_sms/', views.SendOverdueInvoiceSMSView.as_view()),
]