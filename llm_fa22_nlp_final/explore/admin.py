from django.contrib import admin

# Register your models here.

from .models import Corpus, Symptom, Medication

admin.site.register(Corpus)
admin.site.register(Symptom)
admin.site.register(Medication)