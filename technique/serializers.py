from rest_framework.serializers import ModelSerializer
from paramettre.models import *

class RegionsSerializer(ModelSerializer):
 
    class Meta:
        model = Regions
        fields = '__all__'
 
class ComsitesSerializer(ModelSerializer):
 
    class Meta:
        model = Comsites
        fields = '__all__'
        
        
        
class TypesitesSerializer(ModelSerializer):
 
    class Meta:
        model = Typesites
        fields = '__all__'
        
        
class StatutsitesSerializer(ModelSerializer):
 
    class Meta:
        model = Statutsites
        fields = '__all__'
        
        