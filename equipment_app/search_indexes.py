from haystack import indexes
from .models import EquipmentModel

class EquipmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    equipment_type = indexes.CharField(model_attr='Category')
    equipment_mdoel = indexes.CharField(model_attr='ModelNumber')
    
    
    def get_model(self):
        return EquipmentModel
    
    def index_queryset(self, using=None):
        return EquipmentModel.objects.all()