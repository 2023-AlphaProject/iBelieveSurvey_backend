from django.urls import path

from .views.participantListAPIView import ParticipantListAPIView
from .views.participantDetailAPIView import ParticipantDetailAPIView

app_name = 'participant'

urlpatterns = [
    path('', ParticipantListAPIView.as_view()),
    path('<int:pk>/', ParticipantDetailAPIView.as_view()),
]
