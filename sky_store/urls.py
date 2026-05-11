from django.contrib import admin
from django.urls import path, include

handler404 = 'catalog.views.custom_404'
handler500 = 'catalog.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
]
