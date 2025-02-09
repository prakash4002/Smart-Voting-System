from django.urls import path
from . import views
urlpatterns = [

    path('',views.admin_login,name='admin_login'),
    path('add_voter/',views.add_voter,name = 'add_voter'),
    path('home/',views.home,name = 'home'),
    path('add_candidate/',views.add_candidate,name = 'add_candidate'),
    path('view_candidate/',views.view_candidate,name = 'view_candidate'),
    path('view_voter/',views.view_voter,name = 'view_voter'),
    path('voter_login/',views.voter_login,name = 'voter_login'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.logout,name = 'logout'),
    path('candidate_list/',views.candidate_list,name = 'candidate_list'),
    path('greeting/<str:face_id>/',views.Greeting,name='greeting'),
    path('pool_vote/',views.pool_vote,name='pool_vote'),
    path('voted/',views.voted,name='voted'),
    path('my_vote/',views.my_vote,name='my_vote'),
    path('all_vote/',views.all_vote,name='all_vote'),
    path('result/',views.result,name='result'),
]