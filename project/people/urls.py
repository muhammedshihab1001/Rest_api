
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, RegisterAPI, LoginAPI, ClassPerson, index, person
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'persons', PersonViewSet, basename='person')

urlpatterns = [
    path('', index, name='index'),
    path('classperson/', ClassPerson.as_view(), name='classperson'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('person/', person, name='person'),
    path('person/<int:id>/', person, name='person-detail'),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]