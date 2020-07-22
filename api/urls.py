from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.schemas import get_schema_view

# drf_yasg code starts here
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views

schema_view = get_schema_view(
    openapi.Info(
        title="Product API",
        default_version='v1',
        description="Product API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # <-- Here
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('category/', views.CategoryAPI.as_view()),
    path('category/<int:category_id>/product/', views.GetPrductsByCategoryAPI.as_view()),
    path('product/', views.ProductAPI.as_view()),
    path('product/<int:product_id>/category/', views.GetCategoryByProductAPI.as_view()),
    path('product/<int:id>/', views.UpdateProductAPI.as_view()),
    # path('docs/', get_schema_view(
    #     title="Product Service",
    #     description="Product Service"
    # ), name='openapi-schema'),
    # path('swagger/', TemplateView.as_view(
    #     template_name='documentation.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
]
