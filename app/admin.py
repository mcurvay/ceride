from django.contrib import admin

from .models import Event, EventStep

admin.site.register(Event)
admin.site.register(EventStep)

# TODO: Daha sonra bu dosyayı kullanarak admin panelindeki görünümü değiştireceğiz.
