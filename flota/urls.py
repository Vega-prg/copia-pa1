from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler403
from .views import error_403

handler403 = error_403

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/registrar/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/<int:pk>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculos/<int:pk>/editar/', views.editar_vehiculo, name='editar_vehiculo'),

     # Mantenimientos Preventivos
    path('mantenimientos/preventivos/', views.lista_mantenimientos_preventivos, name='lista_mantenimientos_preventivos'),
    path('mantenimientos/preventivos/nuevo/', views.registrar_mantenimiento_preventivo, name='registrar_mantenimiento_preventivo'),
    path('mantenimientos/preventivos/<int:pk>/', views.detalle_mantenimiento_preventivo, name='detalle_mantenimiento_preventivo'),
    path('mantenimientos/preventivos/<int:pk>/editar/', views.editar_mantenimiento_preventivo, name='editar_mantenimiento_preventivo'),
    # Mantenimientos Correctivos
    path('mantenimientos/correctivos/', views.lista_mantenimientos_correctivos, name='lista_mantenimientos_correctivos'),
    path('mantenimientos/correctivos/nuevo/', views.registrar_mantenimiento_correctivo, name='registrar_mantenimiento_correctivo'),
    path('mantenimientos/correctivos/<int:pk>/', views.detalle_mantenimiento_correctivo, name='detalle_mantenimiento_correctivo'),
    path('mantenimientos/correctivos/<int:pk>/editar/', views.editar_mantenimiento_correctivo, name='editar_mantenimiento_correctivo'),
    path('calendario/', views.calendario, name='calendario'),
    path('alertas/', views.alertas, name='alertas'),
    # URLs de autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

]