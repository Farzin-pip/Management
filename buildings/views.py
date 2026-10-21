from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.permissions import IsAdmin, IsAdminOrAccountant, IsAdminOrResident
from .selectors import (building_list, building_by_id, facility_booking_by_id, resident_units, building_membership_list,
    building_membership_by_id, unit_list, unit_by_id, ownership_list, ownership_by_id, tenancy_by_id, tenancy_list,
    ticket_message_by_id, floor_list, floor_by_id, facilities_list, facilities_by_id, announcement_list,
    announcement_by_id, ticket_list, ticket_by_id, ticket_message_list, facility_bookings_list)
from .serializers import (BuildingSerializer, BuildingMembershipSerializer, UnitSerializer,
                        OwnershipSerializer, TenancySerializer, FacilitiesSerializer, FacilityBookingsSerializer,
                        AnnouncementsSerializer, TicketsSerializer, TicketMessagesSerializer, FloorSerializer,
                        VacantFloorReportSerializer, VacantUnitReportSerializer)
from .services import (create_building, update_building, delete_building, create_facility_booking,
                       update_facility_booking, create_building_membership, update_building_membership,
                       delete_building_membership, create_unit, update_unit, delete_unit, create_ownership,
                       update_ownership, delete_ownership, create_tenancy, update_tenancy, delete_tenancy,
                       create_floor, update_floor, delete_floor, create_facilities, update_facilities,
                       delete_facilities, create_announcement, update_announcement, delete_announcement,
                       create_ticket, update_ticket, delete_ticket, create_ticket_message, update_ticket_message,
                       delete_ticket_message, delete_facility_booking, vacant_units_overdue_report)


class BuildingView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        building = building_list()
        ser_data = BuildingSerializer(instance=building, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = BuildingSerializer(data=request.data)
        if ser_data.is_valid():
            building = create_building(ser_data.validated_data)
            return Response(BuildingSerializer(instance=building).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        building = building_by_id(pk)
        ser_data = BuildingSerializer(instance=building, data=request.data, partial=True)
        if ser_data.is_valid():
            building = update_building(building, ser_data.validated_data)
            return Response(BuildingSerializer(instance=building).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        building = building_by_id(pk)
        delete_building(building)
        return Response({'message': 'Building Deleted!'}, status=status.HTTP_200_OK)


class BuildingMembershipView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        building_membership = building_membership_list()
        ser_data = BuildingMembershipSerializer(instance=building_membership, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = BuildingMembershipSerializer(data=request.data)
        if ser_data.is_valid():
            building_membership = create_building_membership(ser_data.validated_data)
            return Response(BuildingMembershipSerializer(instance=building_membership).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        building_membership = building_membership_by_id(pk)
        ser_data = BuildingMembershipSerializer(instance=building_membership, data=request.data, partial=True)
        if ser_data.is_valid():
            building_membership = update_building_membership(building_membership, ser_data.validated_data)
            return Response(BuildingMembershipSerializer(instance=building_membership).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        building_membership = building_membership_by_id(pk)
        delete_building_membership(building_membership)
        return Response({'message': 'Building Membership Deleted!'}, status=status.HTTP_200_OK)


class UnitView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        units = unit_list()
        ser_data = UnitSerializer(instance=units, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = UnitSerializer(data=request.data)
        if ser_data.is_valid():
            unit = create_unit(ser_data.validated_data)
            return Response(UnitSerializer(instance=unit).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        unit = unit_by_id(pk)
        ser_data = UnitSerializer(instance=unit, data=request.data, partial=True)
        if ser_data.is_valid():
            unit = update_unit(unit, ser_data.validated_data)
            return Response(UnitSerializer(instance=unit).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = unit_by_id(pk)
        delete_unit(unit)
        return Response({'message': 'Unit Deleted!'}, status=status.HTTP_200_OK)


class OwnershipView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        ownership = ownership_list()
        ser_data = OwnershipSerializer(instance=ownership, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = OwnershipSerializer(data=request.data)
        if ser_data.is_valid():
            ownership = create_ownership(ser_data.validated_data)
            return Response(OwnershipSerializer(instance=ownership).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ownership = ownership_by_id(pk)
        ser_data = OwnershipSerializer(instance=ownership, data=request.data, partial=True)
        if ser_data.is_valid():
            ownership = update_ownership(ownership, ser_data.validated_data)
            return Response(OwnershipSerializer(instance=ownership).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ownership = ownership_by_id(pk)
        delete_ownership(ownership)
        return Response({'message': 'Ownership Deleted!'}, status=status.HTTP_200_OK)


class TenancyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        tenancy = tenancy_list()
        ser_data = TenancySerializer(instance=tenancy, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TenancySerializer(data=request.data)
        if ser_data.is_valid():
            tenancy = create_tenancy(ser_data.validated_data)
            return Response(TenancySerializer(instance=tenancy).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tenancy = tenancy_by_id(pk)
        ser_data = TenancySerializer(instance=tenancy, data=request.data, partial=True)
        if ser_data.is_valid():
            tenancy = update_tenancy(tenancy, ser_data.validated_data)
            return Response(TenancySerializer(instance=tenancy).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tenancy = tenancy_by_id(pk)
        delete_tenancy(tenancy)
        return Response({'message': 'Tenancy Deleted!'}, status=status.HTTP_200_OK)


class FloorsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        floors = floor_list()
        ser_data = FloorSerializer(instance=floors, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FloorSerializer(data=request.data)
        if ser_data.is_valid():
            floor = create_floor(ser_data.validated_data)
            return Response(FloorSerializer(instance=floor).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        floor = floor_by_id(pk)
        ser_data = FloorSerializer(instance=floor, data=request.data, partial=True)
        if ser_data.is_valid():
            floor = update_floor(floor, ser_data.validated_data)
            return Response(FloorSerializer(instance=floor).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        floor = floor_by_id(pk)
        delete_floor(floor)
        return Response({'message': 'Floor Deleted!'}, status=status.HTTP_200_OK)


class FacilitiesView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        facilities = facilities_list()
        ser_data = FacilitiesSerializer(instance=facilities, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FacilitiesSerializer(data=request.data)
        if ser_data.is_valid():
            facilities = create_facilities(ser_data.validated_data)
            return Response(FacilitiesSerializer(instance=facilities).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        facilities = facilities_by_id(pk)
        ser_data = FacilitiesSerializer(instance=facilities, data=request.data, partial=True)
        if ser_data.is_valid():
            facilities = update_facilities(facilities, ser_data.validated_data)
            return Response(FacilitiesSerializer(instance=facilities).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facilities = facilities_by_id(pk)
        delete_facilities(facilities)
        return Response({'message': 'Facilities Deleted!'}, status=status.HTTP_200_OK)


class FacilityBookingsView(APIView):
    permission_classes = [IsAdminOrResident]

    def get(self, request):
        facility_bookings = facility_bookings_list()
        ser_data = FacilityBookingsSerializer(instance=facility_bookings, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = FacilityBookingsSerializer(data=request.data)
        if ser_data.is_valid():
            try:
                facility_booking = create_facility_booking(ser_data.validated_data)
                return Response(FacilityBookingsSerializer(facility_booking).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        facility_booking = facility_booking_by_id(pk)
        ser_data = FacilityBookingsSerializer(instance=facility_booking, data=request.data, partial=True)
        if ser_data.is_valid():
            try:
                facility_booking = update_facility_booking(facility_booking, ser_data.validated_data)
                return Response(FacilityBookingsSerializer(facility_booking).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facility_booking = facility_booking_by_id(pk)
        delete_facility_booking(facility_booking)
        return Response({'message': 'Facility Booking Deleted!'}, status=status.HTTP_200_OK)


class AnnouncementsView(APIView):
    permission_classes = [IsAdminOrResident]

    def get(self, request):
        announcements = announcement_list()
        ser_data = AnnouncementsSerializer(instance=announcements, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        ser_data = AnnouncementsSerializer(data=request.data)
        if ser_data.is_valid():
            announcement = create_announcement(ser_data.validated_data)
            return Response(AnnouncementsSerializer(instance=announcement).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if request.user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        announcement = announcement_by_id(pk)
        ser_data = AnnouncementsSerializer(instance=announcement, data=request.data, partial=True)
        if ser_data.is_valid():
            announcement = update_announcement(announcement, ser_data.validated_data)
            return Response(AnnouncementsSerializer(instance=announcement).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        announcement = announcement_by_id(pk)
        delete_announcement(announcement)
        return Response({'message': 'Announcement Deleted!'}, status=status.HTTP_200_OK)


class TicketsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        tickets = ticket_list()
        ser_data = TicketsSerializer(instance=tickets, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TicketsSerializer(data=request.data)
        if ser_data.is_valid():
            ticket = create_ticket(ser_data.validated_data)
            return Response(TicketsSerializer(instance=ticket).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ticket = ticket_by_id(pk)
        ser_data = TicketsSerializer(instance=ticket, data=request.data, partial=True)
        if ser_data.is_valid():
            ticket = update_ticket(ticket, ser_data.validated_data)
            return Response(TicketsSerializer(instance=ticket).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = ticket_by_id(pk)
        delete_ticket(ticket)
        return Response({'message': 'Ticket Deleted!'}, status=status.HTTP_200_OK)


class TicketMessagesView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        ticket_messages = ticket_message_list()
        ser_data = TicketMessagesSerializer(instance=ticket_messages, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = TicketMessagesSerializer(data=request.data)
        if ser_data.is_valid():
            ticket_message = create_ticket_message(ser_data.validated_data)
            return Response(TicketMessagesSerializer(instance=ticket_message).data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ticket_message = ticket_message_by_id(pk)
        ser_data = TicketMessagesSerializer(instance=ticket_message, data=request.data, partial=True)
        if ser_data.is_valid():
            ticket_message = update_ticket_message(ticket_message, ser_data.validated_data)
            return Response(TicketMessagesSerializer(instance=ticket_message).data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket_message = ticket_message_by_id(pk)
        delete_ticket_message(ticket_message)
        return Response({'message': 'Ticket Message Deleted!'}, status=status.HTTP_200_OK)


class VacantUnitsOverdueReportView(APIView):
    permission_classes = [IsAdminOrAccountant]

    def get(self, request):
        data = vacant_units_overdue_report()
        ser_data = VacantUnitReportSerializer(data, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
