

from django.urls import path
from . import views

urlpatterns = [
    
    path('transactions/', views.TransactionViews.as_view(), name='transactions'),
    path('transactions/<uuid:id>/', views.TransactionDeleteUpdateViews.as_view(), name='transaction-detail'),
    
    # Members
    path('members/', views.MemberListCreateView.as_view(), name='members'),
    path('members/<uuid:id>/', views.MemberDetailView.as_view(), name='member-detail'),
    
    # Cotisations
    path('cotisations/', views.CotisationListCreateView.as_view(), name='cotisations'),
    path('cotisations/<uuid:id>/', views.CotisationDetailView.as_view(), name='cotisation-detail'),
    
    # Depenses
    path('depenses/', views.DepenseListCreateView.as_view(), name='depenses'),
    path('depenses/<uuid:id>/', views.DepenseDetailView.as_view(), name='depense-detail'),
    

    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    
    
    path("users/", views.UserListCreateView.as_view(), name="user"),
    path("users/<uuid:id>/", views.UserDetailView.as_view(), name="user-detail"),
    
    path("auth/login",  views.LoginView.as_view(), name='auth'),
    path("auth/login/<uuid:id>", views.UserDetailView.as_view(), name="auth-detail"),
    
    
    path("auth/register", views.RegisterView.as_view(), name='register'),
    path("auth/me", views.MeView.as_view(), name="me"),
    
    
    path('admin/stats', views.AdminStatsView.as_view(), name='admin-stats'),
    path('admin/export', views.ExportDataView.as_view(), name='admin-export'),
    
]