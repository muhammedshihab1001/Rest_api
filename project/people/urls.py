from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'person',views.personviewsets,basename='person')
urlpatterns=router.urls

urlpatterns = [
    path('',views.index,name='index'),
    path('person/',views.person,name='person'),
    path('classperson/',views.classperson.as_view(),name='classperson'),
    path('personviews/',include(router.urls)),
    path('login/',views.loginapi.as_view(),name='login'),
    path('register/',views.registerapi.as_view(),name='register')
]