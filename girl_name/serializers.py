from rest_framework import serializers
from girl_name.models import Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['name', 'user', 'choice']

