from django.urls import path
from .views import *

# allows to view all amenities, query amenities, create a new amenity
urlpatterns = [
    path('', PropertiesList.as_view(), name='properties-list'),
    path('mine/', PropertiesMine.as_view(), name='properties-mine'),
    path('mine/archived/', PropertiesArchived.as_view(), name='properties-archived'),
    path('user/<int:user_id>/', PropertiesUser.as_view(), name='properties-user'),
    path('<int:id>/', PropertiesOne.as_view(), name='properties-one'),
]