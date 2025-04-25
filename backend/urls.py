from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse,HttpResponseServerError
from django.conf import settings
from django.conf.urls.static import static

from revproxy.views import ProxyView

class CustomProxyView(ProxyView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print("\n=================================================================\n")
            print('Có lỗi xảy ra.')
            print('Route: ' + request.build_absolute_uri())
            print('Nodejs server không hoạt động.')
            return HttpResponseServerError("Nodejs server is offline.")

def hello_world(request):
    return HttpResponse("hello world")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world),
    path('', include('base.urls')),
    path('', include('message.urls')),
    path('', include('notification.urls')),
    path('', include('service.urls')),
    path('', include('user.urls')),
    path('', include('user_profile.urls')),
    path('', include('workout.urls')),
    re_path(r'^nodejs/(?P<path>.*)', CustomProxyView.as_view(upstream=settings.NODEJS_HOST + '/nodejs/')),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
