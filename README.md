# Back End for Homi

Deployed [database on Heroku.](https://homi-456b248c7f0d.herokuapp.com/)

## urls.py

### Users
#### `path('', include('users.urls'))`

* `users/register/` CreateUserView.as_view()
* `users/login/` LoginView.as_view()
* `users/token/refresh/` VerifyUserView.as_view()
* `users/profile/` UserProfileView.as_view()

### Amenities
#### `path('amenities/', include('amenities.urls'))`

* ` `  AmenitiesList.as_view()

### Properties
#### `path('properties/', include('properties.urls'))`


* ` ` PropertiesList.as_view() 
* `mine/` PropertiesMine.as_view() 
* `mine/archived/` PropertiesArchived.as_view()
* `user/<int:user_id>/` PropertiesUser.as_view()
* `<int:id>/` PropertiesOne.as_view()


### Bookings
#### `path('bookings/', include('bookings.urls'))`


* ` ` BookingsList.as_view()
* `upcoming/` UpcomingBookings.as_view() 
* `new/<int:prop_id>/` BookingsNew.as_view()
* `<int:id>/` BookingsOne.as_view()
* `host/` BookingsHost.as_view()
* `prop/<int:prop_id>/` BookingsProperty.as_view()


### Admin
#### `path('admin/', admin.site.urls)`