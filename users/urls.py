from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserView.as_view(), name='sign_up_view'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
    path('profile/<int:user_id>/following/',
         views.FollowingView.as_view(), name='following_view'),
]
