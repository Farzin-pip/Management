from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import (BuildingSerializer, BuildingMembershipSerializer, UnitSerializer,
                        OwnershipSerializer, TenancySerializer, FacilitiesSerializer, FacilityBookingsSerializer,
                        AnnouncementsSerializer, TicketsSerializer, TicketMessagesSerializer, FloorSerializer)
from .models import (Building, BuildingMembership, Unit, Ownership, Tenancy,  Facilities, FacilityBookings,
                     Announcements, Tickets, TicketMessages, Floors)


class BuildingView(APIView):
    def get(self, request):
        building = Building.objects.all()
        ser_data = BuildingSerializer(instance=building, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = BuildingSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        building = Building.objects.get(pk=pk)
        ser_data = BuildingSerializer(instance=building, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        building = Building.objects.get(pk=pk)
        building.delete()
        return Response({'message': 'Building Deleted!'}, status=status.HTTP_200_OK)


class BuildingMembershipView(APIView):
    def get(self, request):
        building_membership = BuildingMembership.objects.all()
        ser_data = BuildingMembershipSerializer(instance=building_membership, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = BuildingMembershipSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        building_membership = BuildingMembership.objects.get(pk=pk)
        ser_data = BuildingMembershipSerializer(instance=building_membership, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        building_membership = BuildingMembership.objects.get(pk=pk)
        building_membership.delete()
        return Response({'message': 'Building Membership Deleted!'}, status=status.HTTP_200_OK)


class UnitView(APIView):
    def get(self, request):
        unit = Unit.objects.all()
        ser_data = UnitSerializer(instance=unit, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = UnitSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        unit = Unit.objects.get(pk=pk)
        ser_data = UnitSerializer(instance=unit, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = Unit.objects.get(pk=pk)
        unit.delete()
        return Response({'message': 'Unit Deleted!'}, status=status.HTTP_200_OK)


class OwnershipView(APIView):
    def get(self, request):
        ownership = Ownership.objects.all()
        ser_data = OwnershipSerializer(instance=ownership, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = OwnershipSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ownership = Ownership.objects.get(pk=pk)
        ser_data = OwnershipSerializer(instance=ownership, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ownership = Ownership.objects.get(pk=pk)
        ownership.delete()
        return Response({'message': 'Ownership Deleted!'}, status=status.HTTP_200_OK)


class TenancyView(APIView):
    def get(self, request):
        tenancy = Tenancy.objects.all()
        ser_data = TenancySerializer(instance=tenancy, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TenancySerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_200_OK)

    def put(self, request, pk):
        tenancy = Tenancy.objects.get(pk=pk)
        ser_data = TenancySerializer(instance=tenancy ,data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tenancy = Tenancy.objects.get(pk=pk)
        tenancy.delete()
        return Response({'message': 'Tenancy Deleted!'}, status=status.HTTP_200_OK)


class FloorsView(APIView):
    def get(self, request):
        floors = Floors.objects.all()
        ser_data = FloorSerializer(instance=floors, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FloorSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        floor = Floors.objects.get(pk=pk)
        ser_data = FloorSerializer(instance=floor, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        floor = Floors.objects.get(pk=pk)
        floor.delete()
        return Response({'message': 'Floor Deleted!'}, status=status.HTTP_200_OK)


class FacilitiesView(APIView):
    def get(self, request):
        facilities = Facilities.objects.all()
        ser_data = FacilitiesSerializer(instance=facilities, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FacilitiesSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        facilities = Facilities.objects.get(pk=pk)
        ser_data = FacilitiesSerializer(instance=facilities, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facilities = Facilities.objects.get(pk=pk)
        facilities.delete()
        return Response({'message': 'Facilities Deleted!'}, status=status.HTTP_200_OK)


class FacilityBookingsView(APIView):
    def get(self, request):
        facility_bookings = FacilityBookings.objects.all()
        ser_data = FacilityBookingsSerializer(instance=facility_bookings, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FacilityBookingsSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        facility_booking = FacilityBookings.objects.get(pk=pk)
        ser_data = FacilityBookingsSerializer(instance=facility_booking, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facility_booking = FacilityBookings.objects.get(pk=pk)
        facility_booking.delete()
        return Response({'message': 'Facility Booking Deleted!'}, status=status.HTTP_200_OK)


class AnnouncementsView(APIView):
    def get(self, request):
        announcements = Announcements.objects.all()
        ser_data = AnnouncementsSerializer(instance=announcements, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = AnnouncementsSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        announcement = Announcements.objects.get(pk=pk)
        ser_data = AnnouncementsSerializer(instance=announcement, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        announcement = Announcements.objects.get(pk=pk)
        announcement.delete()
        return Response({'message': 'Announcement Deleted!'}, status=status.HTTP_200_OK)


class TicketsView(APIView):
    def get(self, request):
        tickets = Tickets.objects.all()
        ser_data = TicketsSerializer(instance=tickets, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TicketsSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ticket = Tickets.objects.get(pk=pk)
        ser_data = TicketsSerializer(instance=ticket, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = Tickets.objects.get(pk=pk)
        ticket.delete()
        return Response({'message': 'Ticket Deleted!'}, status=status.HTTP_200_OK)


class TicketMessagesView(APIView):
    def get(self, request):
        ticket_messages = TicketMessages.objects.all()
        ser_data = TicketMessagesSerializer(instance=ticket_messages, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TicketMessagesSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ticket_message = TicketMessages.objects.get(pk=pk)
        ser_data = TicketMessagesSerializer(instance=ticket_message, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket_message = TicketMessages.objects.get(pk=pk)
        ticket_message.delete()
        return Response({'message': 'Ticket Message Deleted!'}, status=status.HTTP_200_OK)