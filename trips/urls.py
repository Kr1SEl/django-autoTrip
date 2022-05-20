from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.active_trips, name='list-trips'),
    path('add_trip/', views.add_trip, name='add-trip'),
    path('my_trips/', views.my_trips, name='my-trips'),
    path('trip/<trip_id>', views.trip_details, name='trip-details'),
    path('free_place/<trip_id>', views.trip_free_place, name='free-place'),
    path('delete_trip/<trip_id>', views.delete_trip, name='delete-trip'),
    path('update_trip/<trip_id>', views.update_trip, name='update-trip'),
    path('ddl/load-cities/', views.load_cities,
         name='load-ddl-cities'),
]
