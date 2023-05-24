from django.urls import path, include

from survey.views import SurveyAPIView, SurveyRetrieveUpdateDestoryAPIView

app_name = 'survey'

urlpatterns = [
    path('', SurveyAPIView.as_view()),
    path('<int:survey_id>/', SurveyRetrieveUpdateDestoryAPIView.as_view()),
    path('<int:survey_id>/carts/', include('cart.urls')),
]
