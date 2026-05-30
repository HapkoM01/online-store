from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import Custom404View, Custom500View

# Настройка обработчиков ошибок
handler404 = Custom404View.as_view()
handler500 = Custom500View.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blogs/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
