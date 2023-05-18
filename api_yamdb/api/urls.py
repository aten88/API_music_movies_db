from django.urls import include, path

from api.views import send_confirmation_code, get_jwt_token

v1_auth_patterns = [
    path('signup/', send_confirmation_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
]
