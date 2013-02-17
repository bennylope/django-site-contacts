# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import get_model
from django.template import loader, Context, RequestContext
from django.utils.translation import ugettext as _

from .models import get_user_model, Recipient


class RecipientForm(forms.ModelForm):
    """
    Form class for choosing contact recipients via the admin site.
    """
    user = forms.ModelChoiceField(queryset=get_user_model().objects.filter(is_staff=True))

    class Meta:
        model = get_model('contact_form', 'contactrecipient')


class ContactMixin(object):
    """
    Mixin for contact forms providing reusable methods irrespective of form
    class.
    """
    subject_template_name = "contact/email_subject.html"
    message_template_name = 'contact/email_body.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [manager[1] for manager in settings.MANAGERS]

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets any attributes as passed to the form as
        keyword arguments.
        """
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
        super(ContactMixin, self).__init__(*args, **kwargs)

    def get_subject_template_name(self):
        return self.subject_template_name

    def get_message_template_name(self):
        return self.message_template_name

    def recipient_list(self):
        """
        Returns a list of the email addresses for the site managers
        """
        return self.recipients

    def message(self):
        """
        Render the body of the message to a string.
        """
        return loader.render_to_string(self.get_message_template_name(),
                self.get_context())

    def subject(self):
        """
        Render the subject of the message to a string.
        """
        subject = loader.render_to_string(self.get_subject_template_name(),
                self.get_context())
        return ''.join(subject.splitlines())

    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.
        """
        return Context(dict(self.cleaned_data))

    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.

        By default, the following values are returned:

        * ``from_email``

        * ``message``

        * ``recipient_list``

        * ``subject``
        """
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('from_email', 'message', 'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = callable(attr) and attr() or attr
        return message_dict

    def send(self, fail_silently=False):
        """
        Build and send the email message.
        """
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


class RecipientsMixin(object):
    """
    A mixin for sending the results to a list of recipients.
    """
    def recipient_list(self):
        emails = [recipient.user.email for recipient in
                Recipient.objects.all().select_related('user') if
                recipient.user.email]
        return emails if emails else [manager[1] for manager in settings.MANAGERS]


class RequestContactMixin(object):
    """
    Base functionality from which all contact forms inherit. This
    form class does not use the RequestContext, and so has no need
    for the request object.
    """
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ContactMixin, self).__init__(*args, **kwargs)
        self.request = request

    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.

        By default, this context includes:

        * All of the validated values in the form, as variables of the
          same names as their fields.

        * The current ``Site`` object, as the variable ``site``.

        * Any additional variables added by context processors (this
          will be a ``RequestContext``).

        """
        return RequestContext(self.request,
                dict(self.cleaned_data, site=Site.objects.get_current()))


class AkismetMixin(object):
    """
    Contact form which doesn't add any extra fields, but does add an
    Akismet spam check to the validation routine.

    Requires the setting ``AKISMET_API_KEY``, which should be a valid
    Akismet API key.

    """
    def clean_body(self):
        """
        Perform Akismet validation of the message.

        """
        if 'body' in self.cleaned_data and getattr(settings, 'AKISMET_API_KEY', ''):
            from akismet import Akismet
            from django.utils.encoding import smart_str
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                    blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = {
                    'comment_type': 'comment',
                    'referer': self.request.META.get('HTTP_REFERER', ''),
                    'user_ip': self.request.META.get('REMOTE_ADDR', ''),
                    'user_agent': self.request.META.get('HTTP_USER_AGENT', '')
                }
                if akismet_api.comment_check(smart_str(self.cleaned_data['body']), data=akismet_data, build_data=True):
                    raise forms.ValidationError(_("Akismet thinks this message is spam"))
        return self.cleaned_data['body']


class ContactForm(RecipientsMixin, ContactMixin, forms.Form):
    """
    Base functionality from which all contact forms inherit. This
    form class does not use the RequestContext, and so has no need
    for the request object.
    """
    name = forms.CharField(max_length=100, label=_('Your name'))
    email = forms.EmailField(max_length=100, label=_('Your email address'))
    body = forms.CharField(widget=forms.Textarea(), label=_('Your message'))
