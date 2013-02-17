from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from .views import SimpleContactView


urlpatterns = patterns('',
    url(r'^$', view=SimpleContactView.as_view(), name="contact_form"),
    url(r'^sent/$',
        view=TemplateView.as_view(template_name="contact/contact_success.html"),
        name="contact_success"),
)
