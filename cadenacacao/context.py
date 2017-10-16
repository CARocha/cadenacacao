from directorio.forms import *

def buscador(request):
	search = BuscadorForm()

	return {'search':search}