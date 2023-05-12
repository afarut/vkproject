from django.urls import path
from core import views


app_name = "core"

urlpatterns = [
    path("", views.UserApiView.as_view()),
    path("createuser/", views.UserCreateAPIView.as_view()),
    path("friends/", views.UserFriendListAPIView.as_view()),
    path("subscribers/", views.UserSubscriberListAPIView.as_view()),
    path("requests/", views.RequestListAPIView.as_view()),
    path("user/<int:pk>/", views.UserLinkInfoAPIView.as_view()),
    path("user/delete/<int:pk>/", views.UserDeleteFriendAPIView.as_view()),
    path("user/gofriend/<int:pk>/", views.UserGoFriendAPIView.as_view()),
    path("user/reject/<int:pk>/", views.UserRejectFriendAPIView.as_view()),
]
