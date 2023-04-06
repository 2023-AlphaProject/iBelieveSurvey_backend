from django.urls import path

from survey.views import SurveyAPIView, SurveyRetrieveUpdateDestoryAPIView

urlpatterns = [
    path('', SurveyAPIView.as_view()),
    path('<int:pk>/', SurveyRetrieveUpdateDestoryAPIView.as_view()),
]
