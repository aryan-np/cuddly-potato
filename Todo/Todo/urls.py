
from django.contrib import admin
from django.urls import path,include

from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('todo',views.TodoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('api/token/refresh',TokenRefreshView.as_view(),name = 'token refresh'),
    path('', include(router.urls))
]
