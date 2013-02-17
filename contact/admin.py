from django.contrib import admin

from .models import Recipient
from .forms import RecipientForm


class RecipientAdmin(admin.ModelAdmin):
    form = RecipientForm


admin.site.register(Recipient, RecipientAdmin)
