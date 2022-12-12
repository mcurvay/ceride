from django.contrib import admin

from .models import Event, Step

# TODO: Admin panelin tema, dil, yerleşim ayarları yapılacak. Model netleştikten sonra.

class StepInline(admin.TabularInline):
  model = Step
  extra = 1


class EventAdmin(admin.ModelAdmin):
  inlines = [StepInline]
  readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

  def save_model(self, request, obj, form, change):
    if obj.pk is None:
      obj.created_by = request.user
    else:
      obj.updated_by = request.user

    super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)