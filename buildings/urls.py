from django.urls import path
from . import views


app_name = 'buildings'
urlpatterns = [
    path('building/', views.BuildingView.as_view()),
    path('building/<int:pk>/', views.BuildingView.as_view()),
    path('membership/', views.BuildingMembershipView.as_view()),
    path('membership/<int:pk>/', views.BuildingMembershipView.as_view()),
    path('floor/', views.FloorsView.as_view()),
    path('floor/<int:pk>/', views.FloorsView.as_view()),
    path('unit/', views.UnitView.as_view()),
    path('unit/<int:pk>/', views.UnitView.as_view()),
    path('ownership/', views.OwnershipView.as_view()),
    path('ownership/<int:pk>/', views.OwnershipView.as_view()),
    path('tenancy/', views.TenancyView.as_view()),
    path('tenancy/<int:pk>/', views.TenancyView.as_view()),
    path('facilities/', views.FacilitiesView.as_view()),
    path('facilities/<int:pk>/', views.FacilitiesView.as_view()),
    path('facility_bookings/', views.FacilityBookingsView.as_view()),
    path('facility_bookings/<int:pk>/', views.FacilityBookingsView.as_view()),
    path('announcements/', views.AnnouncementsView.as_view()),
    path('announcements/<int:pk>/', views.AnnouncementsView.as_view()),
    path('tickets/', views.TicketsView.as_view()),
    path('tickets/<int:pk>/', views.TicketsView.as_view()),
    path('ticket_messages/', views.TicketMessagesView.as_view()),
    path('ticket_messages/<int:pk>/', views.TicketMessagesView.as_view()),
]