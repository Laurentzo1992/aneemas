from rest_framework.serializers import ModelSerializer
from paramettre.models import Comsites, Typesites, Statutsites


 
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
        
        