from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cinemaa.urls')),
    path('', include('movie.urls')),
    path('', include(('booking.urls', 'booking'), namespace='booking')),
    path('', include(('account.urls','account'), namespace='account')),
    path('', include(('api.urls', 'account'), namespace='api')),
    path('profile/<int:id>', profile, name="profile"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
