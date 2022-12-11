from django.contrib import admin

from .models import Event, Step


class EventAdmin(admin.ModelAdmin):
    # readonly_fields alanları sadece okunabilir olacak, değiştirilemeyecek
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

    # Kaydetme işleminden önce bu fonksiyon çalışacak
    def save_model(self, request, obj, form, change):
        # obj.pk değeri None ise yeni bir kayıt oluşturuluyor
        if obj.pk is None:
            # created_by alanına veri giren kullanıcı atanıyor
            obj.created_by = request.user
        # obj.pk değeri None değilse var olan bir kaydın güncelleniyor
        else:
            # updated_by alanına veriyi güncelleyen kullanıcı atanıyor
            obj.updated_by = request.user

        # Kaydetme işlemini yap
        super().save_model(request, obj, form, change)


class StepAdmin(admin.ModelAdmin):
    # readonly_fields alanları sadece okunabilir olacak, değiştirilemeyecek
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

    # Kaydetme işleminden önce bu fonksiyon çalışacak
    def save_model(self, request, obj, form, change):
        # obj.pk değeri None ise yeni bir kayıt oluşturuluyor
        if obj.pk is None:
            # created_by alanına veri giren kullanıcı atanıyor
            obj.created_by = request.user
        # obj.pk değeri None değilse var olan bir kaydın güncelleniyor
        else:
            # updated_by alanına veriyi güncelleyen kullanıcı atanıyor
            obj.updated_by = request.user

        # Kaydetme işlemini yap
        super().save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)
admin.site.register(Step, StepAdmin)

# TODO: Daha sonra bu dosyayı kullanarak admin panelindeki görünümü değiştireceğiz.
