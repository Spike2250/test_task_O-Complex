from typing import Dict

from django.views.generic import CreateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from django_filters.views import FilterView


from .forms import ForecastForm
from .models import Forecast
from ..utils import AuthorizationCheckMixin, ForecastPermissionsMixin
from ..forecasts.filters import ForecastFilter
from ..pyown_api import weather_manager


class ForecastView(AuthorizationCheckMixin,
                   DetailView):
    model = Forecast
    template_name = 'forecasts/forecast.html'


class ForecastsView(AuthorizationCheckMixin,
                    FilterView):
    model = Forecast
    filterset_class = ForecastFilter
    context_object_name = 'forecasts'
    template_name = 'forecasts/forecasts.html'


class ForecastCreateView(AuthorizationCheckMixin,
                         SuccessMessageMixin,
                         CreateView):
    form_class = ForecastForm
    template_name = 'forecasts/create.html'
    # success_url = reverse_lazy('forecast', kwargs={'pk': self.object.pk})
    success_message = _('Forecast successfully created')

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user

        forecasts = weather_manager.get_weather(form.instance.place)
        if all((
            isinstance(forecasts["today"], Dict),
            isinstance(forecasts["tomorrow"], Dict),
        )):
            form.instance.forecast_today = forecasts["today"]
            form.instance.forecast_tomorrow = forecasts["tomorrow"]
        else:
            form.instance.forecast_today = {"error": forecasts["today"]}
            form.instance.forecast_tomorrow = {"error": forecasts["tomorrow"]}

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forecast', kwargs={'pk': self.object.pk})


class ForecastDeleteView(AuthorizationCheckMixin,
                         ForecastPermissionsMixin,
                         SuccessMessageMixin,
                         DeleteView):
    model = Forecast
    template_name = 'forecasts/delete.html'
    success_url = reverse_lazy('forecasts')
    success_message = _('Forecast successfully deleted')
