from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="DRF Authentication API",
      default_version='v1',
      description="api description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="phonglex@gmail.com"),
      license=openapi.License(name="Phone License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('books/', include('book.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)