from django.contrib import admin

from .models import Event, Step

admin.site.register(Event)
admin.site.register(Step)

# TODO: Daha sonra bu dosyayı kullanarak admin panelindeki görünümü değiştireceğiz.
