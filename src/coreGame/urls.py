from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('info/<int:name>/', include('info.urls')),
    path('admin/', admin.site.urls),
]
