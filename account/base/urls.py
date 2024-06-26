from django.urls import path
from .views import FacebookLoginView, GoogleLoginView, CheckEmailView, \
    RegistrationView, VerifyAccountView, ResendVerificationCodeView, \
    PasswordResetView, SendPasswordResetView, ProfileView, BlockView, \
    ReportView, LoginView, LogoutView, AddressView, GetAllAddressesView, \
    FacebookLinkingView, GoogleLinkingView, GetSocialAccountListView, \
    EncloseAccountView, ChangeEmailHasPasswordAccountView, ChangeEmailNotHasPasswordAccountView, \
    DeleteAccountView, CheckAccountView, ChangePasswordView, DashboardView, \
    GetProfileView, SetFacebookEmailAccountView, CreatePasswordAccountView
from dj_rest_auth.registration.views import SocialAccountDisconnectView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view

app_name = 'account'

urlpatterns = [
    # POST : Get facebook token
    path('facebook/', FacebookLoginView.as_view()),
    # POST : Get google token
    path('google/', GoogleLoginView.as_view()),
    # POST : Check if email already exists
    path('check_email/', CheckEmailView.as_view()),
    # POST : Login with raw email/password
    path('login/', LoginView.as_view()),
    # GET : linked accounts list
    path('socials/', GetSocialAccountListView.as_view()),
    # POST : link facebook social account
    path('link_facebook/', FacebookLinkingView.as_view()),
    # POST : link google social account
    path('link_google/', GoogleLinkingView.as_view()),
    # POST : unlink social account
    # <int:pk> from socials api list
    path('unlink_social/<int:pk>/', SocialAccountDisconnectView.as_view()),
    # POST : Logout
    path('logout/', LogoutView.as_view()),
    # POST : Create account - verification code sent
    path('register/', RegistrationView.as_view()),
    # POST : Verify account
    path('verify_account/', VerifyAccountView.as_view()),
    # POST : Resend verification code
    path('resend_verification/', ResendVerificationCodeView.as_view()),
    # POST : Change password (from dj-rest-auth)
    # path('password_change/', PasswordChangeView.as_view()),
    path('password_change/', ChangePasswordView.as_view()),
    # POST : Password reset
    path('send_password_reset/', SendPasswordResetView.as_view()),
    # GET: check if email & code are valid
    # PUT: reset with new password
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset/<str:email>/<int:code>/', PasswordResetView.as_view()),
    # POST : Tokens, Verify if token valid, Refresh access token
    path('token_verify/', TokenVerifyView.as_view()),
    path('token_refresh/', get_refresh_view().as_view()),
    # PATCH : Edit profil
    # GET : Get profil data include avatar
    path('profil/', ProfileView.as_view()),
    path('get_profil/<int:user_pk>/', GetProfileView.as_view()),
    # Blocked Users
    # GET : Get blocked users list
    # POST : Block a user
    # DELETE : Unblock a user
    path('block/', BlockView.as_view()),
    path('block/<int:user_pk>/', BlockView.as_view()),
    # Repport
    # POST : Report a user
    path('report/', ReportView.as_view()),
    # Address
    # POST : Create new address
    # PATCH : Edit an address
    # GET : Get one address
    # DELETE : Delete an address
    path('address/', AddressView.as_view()),
    path('address/<int:address_pk>/', AddressView.as_view()),
    # GET : Get All user addresses
    path('addresses/', GetAllAddressesView.as_view()),
    # POST : Cloturer mon compte
    path('enclose/', EncloseAccountView.as_view()),
    # PUT : Change email
    # path('email/', ChangeEmailAccountView.as_view()),
    path('change_email_has_password/', ChangeEmailHasPasswordAccountView.as_view()),
    path('change_email_not_has_password/', ChangeEmailNotHasPasswordAccountView.as_view()),
    path('create_password/', CreatePasswordAccountView.as_view()),
    path('set_fb_email/', SetFacebookEmailAccountView.as_view()),
    # GET : check account
    path('check_account/', CheckAccountView.as_view()),
    # DELETE : Delete Account
    path('delete_account/', DeleteAccountView.as_view()),
    # GET : get sellers dashboard data
    path('dashboard/', DashboardView.as_view()),
    # GET : get buyer dashboard data
    # path('dashboard_buyer/', DashboardBuyerView.as_view()),
]
