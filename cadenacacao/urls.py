"""cadenacacao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from directorio.views import *
from context import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^actores/busqueda/', include('haystack.urls')),
    #url(r'^correo/permiso-org/', enviar_correo_pedir_permiso, name="permiso-admin"),
    url(r'^correo/admin/', enviar_correo_administradores, name="soporte-admin"),
    # url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),

    # url(r'^accounts/logout/$', auth_views.logout,{'next_page': '/'}),
    url(r'^accounts/profile/$',user_profile,name='profile'),
    url(r'^accounts/profile/crear/$',crear_org,name='crear-org'),
    url(r'^accounts/profile/editar/(?P<slug>[\w-]+)/$',editar_org,name='editar-org'),
    url(r'^accounts/profile/user/editar/$',editar_user,name='editar-user'),
    url(r'^permisos/editar/(?P<user_id>[0-9]+)/(?P<org_id>[0-9]+)/$',permisos_organizacion,name='editar-permisos-user'),

    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


    #url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^buscador/$', buscador, name='search'),
    url(r'^actores/$', consulta, name='consulta'),
    url(r'^actores/perfil/(?P<slug>[\w-]+)/$', detail_org, name='detail-org'),
    url(r'^mapa/$', obtener_lista, name='obtener-lista'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^politica-condiciones/$', TemplateView.as_view(template_name="policy-service.html")),
    url(r'^servicios/$', Servicios.as_view()),

    #template correo
    url(r'^correo/$', TemplateView.as_view(template_name="correo.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
