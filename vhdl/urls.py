from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('component/creation', views.component_creation, name='component_creation'),
    path('component/list', views.component_list, name='component_list'),
    path('structural/selection', views.structural_selection, name='structural_selection'),
    path('structural/mapping/<int:pk>', views.structural_mapping, name='structural_mapping'),
    path('structural/finalize/<int:pk>', views.structural_finalize, name='structural_finalize'),
    path('structural/detail_view/<int:pk>', views.structural_detail_view, name='structural_detail_view'),
]