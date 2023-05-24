from django.shortcuts import redirect
from rest_framework.views import APIView


class PaymentRedirectAPIView(APIView):
    def get(self, request):
        return redirect('http://localhost')
   