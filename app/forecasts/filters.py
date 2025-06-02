from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext as _
from django.forms import CheckboxInput, Select

from .models import Forecast
from ..users.models import User


WIDGET = Select(attrs={'class': 'form-control bg-dark text-white'})


class ForecastFilter(FilterSet):
    author = ModelChoiceFilter(
        label=_('Author'),
        queryset=User.objects.all(),
        widget=WIDGET,
    )
    only_mine_tasks = BooleanFilter(
        label=_('Only my forecasts'),
        method='get_my_forecasts',
        widget=CheckboxInput,
    )

    class Meta:
        model = Forecast
        fields = ['author']

    def get_my_forecasts(self, queryset, _, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset
