from haystack import indexes
from directorio.models import Organizacion


class OrganizacionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr='nombre')
    objetivo = indexes.CharField(model_attr='objetivo')
    contacto_1 = indexes.CharField(model_attr='contacto_1',null=True)
    contacto_2 = indexes.CharField(model_attr='contacto_2',null=True)
    pais_sede = indexes.CharField(model_attr='pais_sede__nombre')
    paises_labora = indexes.CharField(model_attr='paises_labora__nombre')

    def get_model(self):
        return Organizacion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all().order_by('-ratings__average','nombre')