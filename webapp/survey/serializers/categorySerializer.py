from rest_framework import serializers

from survey.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['type']

    def to_representation(self, instance):
        return instance.type
