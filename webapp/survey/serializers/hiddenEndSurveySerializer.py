from rest_framework import serializers

from cart.models import Cart
from order.models import Order
from participant.models import Participant
from survey.models import Survey, Category
from user.models import User
from user.serializers import ReceiverSerializer


class HiddenEndSurveySerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    winningPercentage = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'writer',
            'title',
            'outline',
            'thumbnail',
            'basic_thumbnail',
            'category',
            'category_name',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'is_survey_hidden',
            'participants',
            'created_at',
            'winningPercentage',
            'receiver',
        ]
        read_only_fields = [
            'id',
            'writer',
            'title',
            'thumbnail',
            'basic_thumbnail',
            'category',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'category_name',
            'is_survey_hidden',
            'participants',
            'created_at',
            'winningPercentage',
            'receiver',
        ]

    def get_participants(self, obj):
        try:
            return obj.participant_set.count()
        except AttributeError:
            return 0

    def get_winningPercentage(self, obj):
        return obj.winningPercentage

    def get_receiver(self, obj):
        carts = Cart.objects.filter(survey=obj)
        receivers = []
        for cart in carts:
            orders = Order.objects.filter(cart=cart, receiver__isnull=False)
            receivers.extend(orders.values_list('receiver', flat=True).distinct())
        winnerParticipant = Participant.objects.filter(id__in=receivers)
        winnerUsers = User.objects.filter(participant__in=winnerParticipant)

        serializer = ReceiverSerializer(winnerUsers, many=True)
        serializer_data = serializer.data

        for data in serializer_data:
            order = Order.objects.filter(cart__survey=obj, receiver__user__id=data['id']).first()
            data['brand_name'] = order.cart.template.brand_name
            data['brand_image'] = order.cart.template.brand_image_url
            data['product_name'] = order.cart.template.product_name
            data['product_image'] = order.cart.template.product_thumb_image_url

        return serializer.data

    def get_category_name(self, obj):
        return obj.category.type
