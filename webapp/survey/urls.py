from django.urls import path

from survey.views import SurveyAPIView, SurveyRetrieveDestoryAPIView

urlpatterns = [
    path('', SurveyAPIView.as_view()),
    path('<int:pk>/', SurveyRetrieveDestoryAPIView.as_view()),
]
