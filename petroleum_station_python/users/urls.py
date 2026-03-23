from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:pk>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/approve/accountant/', views.report_accountant_approve, name='report_accountant_approve'),
    path('reports/<int:pk>/approve/admin/', views.report_admin_approve, name='report_admin_approve'),
    path('reports/<int:pk>/reject/', views.report_reject, name='report_reject'),
    path('profile/', views.profile, name='profile'),
    path('messages/report-issue/<int:sale_id>/', views.report_issue, name='report_issue'),
    path('messages/inbox/', views.inbox, name='inbox'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('shares/transaction/', views.share_transaction, name='share_transaction'),
    path('shares/requests/', views.share_request_list, name='share_request_list'),
    path('shares/requests/<int:pk>/approve/accountant/', views.share_accountant_approve, name='share_accountant_approve'),
    path('shares/requests/<int:pk>/approve/admin/', views.share_admin_approve, name='share_admin_approve'),
    path('shares/requests/<int:pk>/reject/', views.share_reject, name='share_reject'),
    path('shares/config/', views.share_config_update, name='share_config_update'),
    path('shares/partners/', views.partner_share_list, name='partner_share_list'),
    path('shares/partners/<int:pk>/edit/', views.partner_share_edit, name='partner_share_edit'),
    path('shares/partners/<int:pk>/delete/', views.partner_share_delete, name='partner_share_delete'),
    path('messages/partner/', views.partner_message, name='partner_message'),
    path('', views.dashboard, name='home'),
]




