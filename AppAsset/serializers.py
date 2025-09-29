from rest_framework import serializers
from AppAsset.models import ContainerData


class ContainerSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=100)
    # storyline = serializers.CharField(max_length=100)
    # active = serializers.BooleanField(default=True)


    class Meta:
        model = ContainerData
        fields = ('id', 'system_code', 'container_code', 'container_name')
        # fields = '__all__'
