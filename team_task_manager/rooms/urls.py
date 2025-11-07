from django.urls import path
from .views import RoomListCreateView, RoomDetailView, AddMemberView, RemoveMemberView

urlpatterns = [
    path('', RoomListCreateView.as_view(), name='room-list-create'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('<int:pk>/add-member/', AddMemberView.as_view(), name='add-member'),
    path('<int:pk>/remove-member/', RemoveMemberView.as_view(), name='remove-member'),
]
