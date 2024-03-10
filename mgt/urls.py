from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('delete_account/', delete_account, name='delete_account'),
    path('task/delete/<int:task_id>/',delete_task, name='delete_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('task/<int:task_id>/', task_details, name='task_details'),
    path('task/create/', create_or_edit_task, name='create_task'),
    path('task/<int:task_id>/edit/', create_or_edit_task, name='edit_task'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]
