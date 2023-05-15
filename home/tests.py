from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from home.models import Hotel, HotelBooking
from home.views import check_booking


class TestCheckBooking(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.hotel = Hotel.objects.create(hotel_name='Test Hotel', room_count=5, hotel_price=100)
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.next_week = self.today + timedelta(days=7)

    def test_check_booking(self):
        # Test when no bookings exist
        result = check_booking(self.tomorrow, self.next_week, self.hotel.uid, self.hotel.room_count)
        assert result == True

        # Create a booking for the hotel
        booking = HotelBooking.objects.create(hotel=self.hotel, user=self.user, start_date=self.tomorrow, end_date=self.next_week, booking_type='Pre Paid')

        # Test when the hotel is fully booked
        result = check_booking(self.tomorrow, self.next_week, self.hotel.uid, self.hotel.room_count)
        assert result == False
