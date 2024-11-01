from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('registration/',views.registration,name="registration"),
    path('login/',views.log_in,name="login"),
    path('logout/',views.log_out,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('event_list/',views.event_list,name="event_list"),
    path('event_create/',views.event_create,name="event_form"),
    path('event_update/<int:pk>/',views.event_edit,name="event_edit"),
    path('event_delete/<int:pk>/',views.event_delete,name="event_delete"),
    path('event_booking/<int:pk>/',views.event_book,name="event_book"),
    path('my_event_bookings/',views.my_bookings,name="my_bookings"),
]