
from .models import userData
from rest_framework import serializers

class userDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = userData
        excluse = ['password']
        
        fields = '__all__'