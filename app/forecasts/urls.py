from django.urls import path

from . import views


urlpatterns = [
    path('', views.ForecastsView.as_view(), name='forecasts'),
    path(
        'create/',
        views.ForecastCreateView.as_view(),
        name='forecast_create',
    ),
    path(
        '<int:pk>/',
        views.ForecastView.as_view(),
        name='forecast',
    ),
    path(
        '<int:pk>/delete/',
        views.ForecastDeleteView.as_view(),
        name='forecast_delete',
    ),
]
