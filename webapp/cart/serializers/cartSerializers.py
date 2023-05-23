from rest_framework import serializers

from cart.models import Cart
from survey.serializers import SurveyRetrieveSerializer
from template.serializers import TemplateSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "survey", "template", "quantity"]
        depth = 1

