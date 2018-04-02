from django.conf.urls import url
from booking.views import Home, RoomBook, CheckAvailability, MyBookings

urlpatterns = [
    url(r'home/', Home.as_view()),
    url(r'room_book/', RoomBook.as_view()),
    url(r'check_availability/', CheckAvailability.as_view()),
    url(r'my_bookings', MyBookings.as_view())

]
