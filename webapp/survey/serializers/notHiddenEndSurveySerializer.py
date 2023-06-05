from rest_framework import serializers

from cart.models import Cart
from order.models import Order
from participant.models import Participant
from survey.models import Survey
from user.models import User
from user.serializers import ReceiverSerializer


class NotHiddenEndSurveySerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    winningPercentage = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'writer',
            'title',
            'thumbnail',
            'category',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'data',
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
            'category',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'data',
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
        return serializer.data
