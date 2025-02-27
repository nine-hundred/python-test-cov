from django.urls import path

from .views import (
    DeleteAccountView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    UserView,
    NicknameAndProfileImageView,
)

# URL 패턴 정의
urlpatterns = [
    path("accounts/register", RegisterView.as_view(), name="register"),  # 사용자 등록
    path("accounts/login", LoginView.as_view(), name="login"),  # 로그인
    path(
        "accounts/user", UserView.as_view(), name="user"
    ),  # 사용자 정보 조회 (쿠키로 JWT 토큰 인증)
    path("accounts/logout", LogoutView.as_view(), name="logout"),  # 로그아웃
    path(
        "accounts/delete", DeleteAccountView.as_view(), name="delete-account"
    ),  # 계정 삭제 (회원 탈퇴)
    path(
        "accounts/password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),  # 비밀번호 재설정 요청
    path(
        "accounts/password-reset/confirm",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),  # 비밀번호 재설정 확인
    path(
        "accounts/edit",
        NicknameAndProfileImageView.as_view(),
        name="edit"
    ), #nickname and profile image change
]
