# from django.conf.urls import url
from django.urls import path
from basicapp import views

#tempelate tagging
app_name="basicapp"

urlpatterns=[
    path("relative/",views.relative,name="relative"),
    path("other/",views.other,name="other"),
    # path("register/", views.register_request, name="register"),
    # path("login/", views.login_request, name="login"),
    # path('create/author/', views.create_author, name='create_author'),
    # path('blog_home/', views.blog_home, name='blog_home'),
    path('client_details/', views.add_client, name='client_page'),
    # path('calculate/', views.calculate_sum_view, name='calculate_sum'),
    # path('get_result/<str:task_id>/', views.get_result_view, name='get_result'),
    path('coderun_scalping/', views.run_bot, name='run_bot'),
    path('coderun_straddle/', views.straddle_bot, name='straddle_bot'),

]
