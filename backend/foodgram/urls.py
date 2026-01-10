from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Foodgram - Administration'
admin.site.site_title = 'FG'
admin.site.index_title = 'Welcome, Admin!'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
