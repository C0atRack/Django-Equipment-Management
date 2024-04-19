from haystack import indexes
from .models import EquipmentModel, User

class EquipmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    equipment_type = indexes.CharField(model_attr='Category')
    equipment_model = indexes.CharField(model_attr='ModelNumber')
    
    def get_model(self):
        return EquipmentModel
    
    def index_queryset(self, using=None):
        return EquipmentModel.objects.all()
    

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    email = indexes.EdgeNgramField(model_attr="email")
    first_name = indexes.EdgeNgramField(model_attr="first_name")
    last_name = indexes.EdgeNgramField(model_attr="last_name")

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return User.objects.all()