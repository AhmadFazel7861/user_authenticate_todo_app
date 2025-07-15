from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.todo_list, name='todo'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    # Update and delete-task URLs
    path('delete-task/<str:name>/', views.delete_task, name='delete'),
    path('update-task/<str:name>/', views.update_task, name='update'),
]
