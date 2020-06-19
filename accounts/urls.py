from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', views.profileview, name='profile'),
    path('friendrequest/<int:id>', views.friend_request, name='friendrequest'),
    path('friendapprove/<int:id>', views.friend_approve, name='friendapprove'),
    path('friendreject/<int:id>', views.friend_reject, name='friendreject'),

    path('requestslist/', views.requestlist, name='requestslist'),
    path('myfriends/', views.myfriends, name='myfriends'),
    path('find/', views.find_friends, name='home'),
]
