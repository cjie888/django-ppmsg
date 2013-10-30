# -*- coding: UTF-8 -*-

from django.test import Client, TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse

from forms import RegisterForm, LoginForm, ChangePasswordForm, PrepareResetPasswordForm, ResetPasswordForm, ChangeUserIconForm
from config import EMAIL_SUFFIX


class ViewTestCases(TestCase):
    fixtures = ['account.json']


    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        self.client.logout()
        TestCase.tearDown(self)


    def test_register_get_method(self):
        """ want response_code == 200 and RegisterForm returned """
        register_url = "/auth/register/"
        response = self.client.get(register_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.context["form"], RegisterForm))

    def test_register_post_all_blank_params(self):
        """want return a RegisterForm with error msgs"""
        register_url = "/auth/register/"
        response = self.client.post(register_url, {})
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], RegisterForm)

    def test_register_post_only_one_blank_param(self):
        """want return a RegisterForm with error msgs"""
        register_url = "/auth/register/"
        post_data = {"username": "", "email": "test1@funshion.com",
                     "password1": "test1", "password2": "test1", }
        response = self.client.post(register_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], RegisterForm)

    def test_register_post_illegal_email(self):
        """want return a RegisterForm with error msgs"""
        register_url = "/auth/register/"
        post_data = {"username": "test1", "email": "test1",
                     "password1": "test1", "password2": "test1", }
        response = self.client.post(register_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], RegisterForm)

    def test_register_post_email_not_end_with_EMAIL_SUFFIX(self):
        """want return a RegisterForm with error msgs"""
        if EMAIL_SUFFIX:
            register_url = "/auth/register/"
            post_data = {"username": "test1", "email": "a@a.com",
                         "password1": "test1", "password2": "test1", }
            response = self.client.post(register_url, post_data)
            self.assertTrue(response.status_code == 200)
            self.check_form_type_and_errors(response.context["form"], RegisterForm)

    def test_register_post_password_too_short(self):
        """want return a RegisterForm with error msgs"""
        register_url = "/auth/register/"
        post_data = {"username": "test1", "email": "a@funshion.com",
                     "password1": "t", "password2": "t", }
        response = self.client.post(register_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], RegisterForm)

    def test_register_incorrect_verify_code(self):
        """want return a RegisterForm with error msgs"""
        register_url = "/auth/register/"
        post_data = {"username": "test1", "email": "test1@funshion.com",
                     "password1": "test11", "password2": "test11", "verificationcode": u"猜不出来"}
        response = self.client.post(register_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], RegisterForm)


    def test_login_get_method(self):
        """want response_code == 200 and a LoginForm returned"""
        login_url = reverse("account.views.login")
        response = self.client.get(login_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.context["form"], LoginForm))

    def test_login_post_blank_params(self):
        """want response_code == 200 and a LoginForm with errors returned"""
        login_url = reverse("account.views.login")
        response = self.client.post(login_url, {})
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], LoginForm)

    def test_login_post_user_not_exist(self):
        """want response_code == 200 and a LoginForm with errors returned"""
        login_url = reverse("account.views.login")
        post_data = {"username": "not_exist", "password": "not_exist"}
        response = self.client.post(login_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], LoginForm)

    def test_login_post_username_not_match_password(self):
        """want response_code == 200 and a LoginForm with errors returned"""
        login_url = reverse("account.views.login")
        post_data = {"username": "test", "password": "not_exist"}
        response = self.client.post(login_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], LoginForm)

    def test_login_ok(self):
        """want login ok, response_code == 302"""
        login_url = reverse("account.views.login")
        post_data = {"username": "test", "password": "test"}
        response = self.client.post(login_url, post_data)
        self.assertTrue(response.status_code == 302)


    def test_logout(self):
        """want response_code == 302"""
        logout_url = reverse("account.views.logout")
        response = self.client.get(logout_url)
        self.assertTrue(response.status_code == 302)


    def test_home_without_login(self):
        """want response_code == 302"""
        home_url = reverse("account.views.home")
        response = self.client.get(home_url)
        self.assertTrue(response.status_code == 302)

    def test_home_logined(self):
        """want response_code == 200"""
        home_url = reverse("account.views.home")
        self.client.login(username="test", password="test")
        response = self.client.get(home_url)
        self.assertTrue(response.status_code == 200)


    def test_change_password_logined_but_get_method(self):
        """want response_code == 200 and a ChangePasswordForm returned"""
        chnage_password_url = reverse("account.views.change_password")
        self.client.login(username="test", password="test")
        response = self.client.get(chnage_password_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.context["form"], ChangePasswordForm))

    def test_change_password_not_login(self):
        """want response_code == 302"""
        chnage_password_url = reverse("account.views.change_password")
        response = self.client.post(chnage_password_url)
        self.assertTrue(response.status_code == 302)

    def test_change_password_post_blank_params(self):
        """want response_code == 200 and a changepasswordform with errors"""
        chnage_password_url = reverse("account.views.change_password")
        post_data = {}
        self.client.login(username="test", password="test")
        response = self.client.post(chnage_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], ChangePasswordForm)

    def test_change_password_wrong_old_password(self):
        """want response_code == 200 and a changepasswordform with errors"""
        chnage_password_url = reverse("account.views.change_password")
        post_data = {"old_password": "123456", "new_password1": "change", "new_password2": "change"}
        self.client.login(username="test", password="test")
        response = self.client.post(chnage_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], ChangePasswordForm)

    def test_change_password_when_two_new_passwords_not_same(self):
        """want response_code == 200 and a changepasswordform with errors"""
        chnage_password_url = reverse("account.views.change_password")
        post_data = {"old_password": "test", "new_password1": "changed", "new_password2": "notchanged"}
        self.client.login(username="test", password="test")
        response = self.client.post(chnage_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], ChangePasswordForm)

    def test_change_password_when_new_password_too_short(self):
        """want response_code == 200 and a changepasswordform with errors"""
        chnage_password_url = reverse("account.views.change_password")
        post_data = {"old_password": "test", "new_password1": "a", "new_password2": "a"}
        self.client.login(username="test", password="test")
        response = self.client.post(chnage_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], ChangePasswordForm)

    def test_change_password_ok(self):
        """want response_code == 302 and login ok with new password"""
        chnage_password_url = reverse("account.views.change_password")
        post_data = {"old_password": "test", "new_password1": "testtest", "new_password2": "testtest"}
        self.client.login(username="test", password="test")
        response = self.client.post(chnage_password_url, post_data)
        self.assertTrue(response.status_code == 302)

        login_url = reverse("account.views.login")
        post_data = {"username": "test", "password": "testtest"}
        response = self.client.post(login_url, post_data)
        self.assertTrue(response.status_code == 302)


    def test_prepare_reset_password_get_method(self):
        """want response_code == 200 and a new blank form"""
        prepare_reset_password_url = reverse("account.views.prepare_reset_password")
        response = self.client.get(prepare_reset_password_url)
        self.assertTrue(response.status_code == 200)
        self.assertFalse(response.context["form"].errors)

    def test_prepare_reset_password_illegal_email(self):
        """want response_code == 200 and a form with errors"""
        prepare_reset_password_url = reverse("account.views.prepare_reset_password")
        post_data = {"email": "xxxxx"}
        response = self.client.post(prepare_reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], PrepareResetPasswordForm)

    def test_prepare_reset_password_email_not_exist(self):
        """want response_code == 200 and a form with errors"""
        prepare_reset_password_url = reverse("account.views.prepare_reset_password")
        post_data = {"email": "%s%s" % ("not_exists_sb", EMAIL_SUFFIX)}
        response = self.client.post(prepare_reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], PrepareResetPasswordForm)

    def test_prepare_reset_password_ok(self):
        """want response_code == 200 and status==ok"""
        django_user = DjangoUser.objects.create_user(username="django", password="password", email="xxx@funshion.com")
        prepare_reset_password_url = reverse("account.views.prepare_reset_password")
        post_data = {"email": django_user.email}
        response = self.client.post(prepare_reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["statu"] == "ok")
        django_user.delete()


    def test_reset_password_user_not_exist(self):
        """want return user not exist"""
        reset_password_url = reverse("account.views.reset_password", args=(0, 123456))
        response = self.client.get(reset_password_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == u"该用户不存在!")

    def test_reset_password_token_error(self):
        """want return token param error"""
        django_user = DjangoUser.objects.create_user(username="django", password="password")
        reset_password_url = reverse("account.views.reset_password", args=(django_user.id, 1))
        response = self.client.get(reset_password_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == u"参数错误!")
        django_user.delete()

    def test_reset_password_get_method(self):
        """want return a new blank ResetPasswordForm, no error msg"""
        user, token = self.create_user_and_make_token()
        reset_password_url = reverse("account.views.reset_password", args=(user.id, token))
        response = self.client.get(reset_password_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == "")
        self.assertFalse(response.context["form"].errors)
        user.delete()

    def test_reset_password_post_blank_params(self):
        """want return a ResetPasswordForm with error"""
        user, token = self.create_user_and_make_token()
        reset_password_url = reverse("account.views.reset_password", args=(user.id, token))
        post_data = {"new_password1": "", "new_password2": ""}

        response = self.client.post(reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == "")
        self.check_form_type_and_errors(response.context["form"], ResetPasswordForm)
        user.delete()

    def test_reset_password_post_two_password_not_same(self):
        """want return a ResetPasswordForm with error"""
        user, token = self.create_user_and_make_token()
        reset_password_url = reverse("account.views.reset_password", args=(user.id, token))
        post_data = {"new_password1": "1111111111", "new_password2": "2222222"}

        response = self.client.post(reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == "")
        self.check_form_type_and_errors(response.context["form"], ResetPasswordForm)
        user.delete()

    def test_reset_password_post_password_too_short(self):
        """want return a ResetPasswordForm with error"""
        user, token = self.create_user_and_make_token()
        reset_password_url = reverse("account.views.reset_password", args=(user.id, token))
        post_data = {"new_password1": "1", "new_password2": "1"}

        response = self.client.post(reset_password_url, post_data)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context["msg"] == "")
        self.check_form_type_and_errors(response.context["form"], ResetPasswordForm)
        user.delete()

    def test_reset_password_ok(self):
        """want reset password ok, and login ok with new password"""
        user, token = self.create_user_and_make_token()
        reset_password_url = reverse("account.views.reset_password", args=(user.id, token))
        post_data = {"new_password1": "11111111", "new_password2": "11111111"}

        response = self.client.post(reset_password_url, post_data)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(authenticate(username=user.username, password=post_data["new_password1"]))
        user.delete()


    def test_change_user_icon_not_login(self):
        """want response_code==302"""
        change_icon_url = reverse("account.views.change_user_icon")
        response = self.client.get(change_icon_url)
        self.assertTrue(response.status_code == 302)

    def test_change_user_icon_logined_post_blank_param(self):
        """want response_code==302 and a ChangeUserIconForm with errors"""
        change_icon_url = reverse("account.views.change_user_icon")
        self.client.login(username="test", password="test")
        response = self.client.post(change_icon_url)
        self.assertTrue(response.status_code == 200)
        self.check_form_type_and_errors(response.context["form"], ChangeUserIconForm)


    def test_user_cleaned(self):
        """want only one user that filled by fixture exists , no code create user"""
        user_count = DjangoUser.objects.all().count()
        self.assertTrue(user_count == 1)

    def check_form_type_and_errors(self, form, formclass):
        """assert form type and errors"""
        self.assertTrue(isinstance(form, formclass))
        self.assertTrue(form.errors)

    def create_user_and_make_token(self):
        django_user = DjangoUser.objects.create_user(username="django", password="password")
        token = default_token_generator.make_token(django_user)
        return (django_user, token)
