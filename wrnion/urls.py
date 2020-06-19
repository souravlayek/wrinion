from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User


from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', "accounts"))),
    path('messages/', include('chat.urls', "messages")),
    path('', views.landing, name="landing"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Customizing admin texts
admin.site.site_header = 'Wrinion'
admin.site.index_title = 'Welcome to project'
admin.site.site_title = 'Control Panel'
