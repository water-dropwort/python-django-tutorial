from django.urls import path
from . import views, login_views

app_name = "testpolls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("login/", login_views.login_, name="login"),
    path("logout/", login_views.logout_, name="logout"),
]
