from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include

from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('todo',views.TodoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.login,name='login'),
    path('api/logout/', views.logout,name='logour'),
    path('api/register/', views.register,name='register'),
    path('api/todo/search/', views.search,name='search'),
    path('api/token/refresh',TokenRefreshView.as_view(),name = 'token refresh'),
    path('', include(router.urls)),
    
    # Password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
