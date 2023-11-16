from rest_framework.serializers import ModelSerializer
from paramettre.models import Comsites

 

 
class ComsitesSerializer(ModelSerializer):
 
    class Meta:
        model = Comsites
        fields = '__all__'
        