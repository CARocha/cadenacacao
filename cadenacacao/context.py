from directorio.forms import *

def buscador(request):
	search = BuscadorForm()
	asd = OrganizacionForm()

	return {'search':search, 'asd': asd}