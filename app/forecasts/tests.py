from dotenv import load_dotenv

from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy

from .models import Forecast
from ..users.models import User
from ..pyown_api import weather_manager


load_dotenv()


class SetUpTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Alice', last_name='Wang',
            username='alice_wang',
        )
        self.user.set_password('dfGt30jBY3')
        self.user.save()

        self.user2 = User.objects.create(
            first_name='Bob', last_name='Brown',
            username='bob_brown',
        )
        self.user2.set_password('hk70XhHG0D')
        self.user2.save()

        alice_forecast_place = "Пермь"
        self.alice_forecast = Forecast.objects.create(
            place=alice_forecast_place,
            author=self.user,
            forecast_today=weather_manager.get_weather_today(
                alice_forecast_place
            ),
            forecast_tomorrow=weather_manager.get_weather_tomorrow(
                alice_forecast_place
            ),
        )
        self.alice_forecast.save()

        bob_forecast_place = "Москва"
        self.bob_forecast = Forecast.objects.create(
            place=bob_forecast_place,
            author=self.user2,
            forecast_today=weather_manager.get_weather_today(
                bob_forecast_place
            ),
            forecast_tomorrow=weather_manager.get_weather_tomorrow(
                bob_forecast_place
            ),
        )
        self.bob_forecast.save()

        self.client.login(
            username='alice_wang', password='dfGt30jBY3',
        )


class ForecastCreateTestCase(SetUpTestCase):
    def test_forecasts_list_view(self):
        response = self.client.get(reverse_lazy('forecasts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='forecasts/forecasts.html',
        )

    def test_forecast_create_view(self):
        response = self.client.get(reverse_lazy('forecast_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='forecasts/create.html',
        )

    def test_forecast_create_success(self):
        some_valid_place = "Монако"
        response = self.client.post(
            reverse_lazy('forecast_create'),
            {
                'place': some_valid_place,
                'forecast_today': weather_manager.get_weather_today(
                    some_valid_place
                ),
                'forecast_tomorrow': weather_manager.get_weather_tomorrow(
                    some_valid_place
                ),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy('forecast', kwargs={'pk': 3})
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Forecast successfully created',
            'Прогноз успешно создан',
        ])

        new_task = Forecast.objects.get(place=some_valid_place)
        self.assertIsNotNone(new_task)

    def test_forecast_create_fail_not_logged_in(self):
        self.client.logout()

        response = self.client.post(reverse_lazy('forecast_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'You are not logged in! Please log in.',
            'Вы не авторизованы! Пожалуйста, выполните вход.',
        ])


class ForecastDeleteTestCase(SetUpTestCase):
    def test_forecast_delete_view(self):
        response = self.client.get(reverse_lazy(
            'forecast_delete', kwargs={'pk': 1}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='forecasts/delete.html',
        )

    def test_task_delete_success(self):
        response = self.client.post(
            reverse_lazy('forecast_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('forecasts'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Forecast successfully deleted',
            'Прогноз успешно удален',
        ])

        with self.assertRaises(Forecast.DoesNotExist):
            Forecast.objects.get(pk=1)

    def test_forecast_delete_fail_user_not_author(self):
        response = self.client.post(
            reverse_lazy('forecast_delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('forecasts'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'The forecast can be deleted only by its author',
            'Прогноз может удалить только его автор',
        ])

    def test_forecast_delete_fail_task_not_exist(self):
        response = self.client.post(
            reverse_lazy('forecast_delete', kwargs={'pk': 42})
        )
        self.assertEqual(response.status_code, 404)

    def test_forecast_delete_fail_not_logged_in(self):
        self.client.logout()

        response = self.client.post(reverse_lazy(
            'forecast_delete', kwargs={'pk': 2}
        ))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'You are not logged in! Please log in.',
            'Вы не авторизованы! Пожалуйста, выполните вход.',
        ])
