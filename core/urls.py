from django.urls import path, re_path, include

from .views import HelpPageView

app_name = 'core'

urlpatterns = [
    re_path(
        r'^help/',
        view=HelpPageView.as_view(),
        name='help',
    ),
]
