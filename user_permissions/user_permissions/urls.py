from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
