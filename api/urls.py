from . import views
from django.urls import path

urlpatterns = [
    # path("test", views.test, name='test'),  
    path('users/<str:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('organisations', views.OrganisationView.as_view(), name='Organisation-create'),
    path('organisations/<uuid:org_id>/', views.OrganisationView.as_view(), name='Organisation-detail'),
    path('organisations/<uuid:org_id>/users/', views.OrganisationView.as_view(), name='Organisation-add-user'),
] 