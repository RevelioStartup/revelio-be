from rest_framework import serializers

from .models import Transaction
from package.serializers import PackageSerializer


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    package = PackageSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'