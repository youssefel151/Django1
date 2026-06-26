from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('afkir/', include('afkir.urls')),
    path('grades/', include('grades.urls')),
    path('scolarite/', include('gestion_ensg.urls')),
    path('subjects/', include('subjects.urls')),
    path('', include('siteweb.urls')),
]
