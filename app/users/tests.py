from datetime import datetime

from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy

from ..users.models import User


class SetUpTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Obiwan',
            last_name='Kenobi',
            username='jedi',
        )
        self.user.set_password('qwerty777')
        self.user.save()

        self.client.login(
            username='jedi', password='qwerty777',
        )


class UserCreateTestCase(SetUpTestCase):
    def test_user_creation(self):
        user = self.user

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.first_name, 'Obiwan')
        self.assertEqual(str(user), 'Obiwan Kenobi')

        user_created_at = user.created_at.strftime('%Y-%m-%d')
        curr_time = datetime.now().strftime('%Y-%m-%d')
        self.assertEqual(user_created_at, curr_time)

    def test_user_registration_success(self):
        response = self.client.post(
            reverse_lazy('users_create'),
            {'first_name': 'Anakin',
             'last_name': 'Skywalker',
             'username': 'redsaber',
             'password1': '456123987qwerty',
             'password2': '456123987qwerty'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'User is successfully registered',
            'Пользователь успешно зарегистрирован',
        ])

    def test_user_registration_fail_username_already_exist(self):
        response = self.client.post(
            reverse_lazy('users_create'),
            {'first_name': 'Obiwan',
             'last_name': 'Kenobi',
             'username': 'jedi',
             'password1': 'qwerty777',
             'password2': 'qwerty777'}
        )
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

    def test_user_registration_fail_passwords_not_match(self):
        response = self.client.post(
            reverse_lazy('users_create'),
            {'first_name': 'Anakin',
             'last_name': 'Skywalker',
             'username': 'red_saber_is_good',
             'password1': 'q1w2e3r4t5',
             'password2': 'Q1w2e3r4T5'}
        )
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

        curr_language = response.context['LANGUAGE_CODE']
        if curr_language == 'en-us':
            self.assertIn(
                'The two password fields didn’t match.',
                str(response.context['form'])
            )
        elif curr_language == 'ru-ru':
            self.assertIn(
                'Введенные пароли не совпадают.',
                str(response.context['form'])
            )


class UserUpdateTestCase(SetUpTestCase):
    def test_user_update_view(self):
        response = self.client.get(reverse_lazy('users_update',
                                                kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/update.html')

    def test_user_update_success(self):
        response = self.client.post(
            reverse_lazy('users_update', kwargs={'pk': 1}),
            {'first_name': 'Obiwan',
             'last_name': 'Kenobi',
             'username': 'jedi_knight',
             'password1': 'qwerty777',
             'password2': 'qwerty777'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'User is successfully updated',
            'Пользователь успешно изменен',
        ])

    def test_user_update_no_permission(self):
        response = self.client.post(
            reverse_lazy('users_update', kwargs={'pk': 2}),
            {'first_name': 'Anakin',
             'last_name': 'Darth Vader',
             'username': 'red_saber_is_good',
             'password1': 'q1w2e3r4t5',
             'password2': 'Q1w2e3r4T5'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'You have no rights to change another user.',
            'У вас нет прав для изменения другого пользователя.',
        ])

    def test_user_update_no_login(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('users_update', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Вы не авторизованы! Пожалуйста, выполните вход.',
            'You are not logged in! Please log in.',
        ])


class UserDeleteTestCase(SetUpTestCase):
    def test_user_delete_view(self):
        response = self.client.get(reverse_lazy('users_delete',
                                                kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')

    def test_user_delete_success(self):
        response = self.client.post(
            reverse_lazy('users_delete', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'User successfully deleted',
            'Пользователь успешно удален',
        ])

    def test_user_delete_no_permission(self):
        response = self.client.post(
            reverse_lazy('users_delete', kwargs={'pk': 2}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'You have no rights to change another user.',
            'У вас нет прав для изменения другого пользователя.',
        ])

    def test_user_delete_no_login(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('users_delete', kwargs={'pk': 2}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Вы не авторизованы! Пожалуйста, выполните вход.',
            'You are not logged in! Please log in.',
        ])


class UserLoginTestCase(SetUpTestCase):
    def test_user_login_view(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/login.html')

    def test_user_login_post(self):
        incorrect_login = self.client.login(
            username='some_incorrect_username',
            password='some_incorrect_password',
        )
        self.assertFalse(incorrect_login)

        response = self.client.post(
            reverse_lazy('login'),
            {"username": "jedi",
             "password": "qwerty777"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), ['You are logged in', 'Вы залогинены'])


class UsersListViewTestCase(SetUpTestCase):
    def test_users_list_view_not_login(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users.html')

    def test_users_list_view_login(self):
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users.html')
