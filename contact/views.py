from django.core.urlresolvers import reverse
from django.views.generic import FormView

from .forms import ContactForm


class ContactViewMixin(object):
    """
    Renders the contact form
    """
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get_success_url(self):
        """
        Rreturns the URL to which a user should be redirected after successful
        form submission
        """
        return reverse("contact_success")

    def form_valid(self, form):
        """
        Sends the contact message and sends the user to the 'sent' page.
        """
        form.send()
        return super(ContactViewMixin, self).form_valid(form)


class SimpleContactView(ContactViewMixin, FormView):
    pass
