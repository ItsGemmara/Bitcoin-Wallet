from rest_framework import serializers


class BTCWalletSerializer(serializers.Serializer):
    key = serializers.CharField()
    address = serializers.CharField()

