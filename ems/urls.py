from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    # Redirect the base URL to the dashboard.
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'), permanent=False)),

    url('', include('ems.crm.urls')),
    url('', include('ems.contracts.urls')),
    url('', include('ems.entries.urls')),
    url('', include('ems.reports.urls')),
]
