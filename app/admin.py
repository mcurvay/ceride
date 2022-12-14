from django.contrib import admin

from .models import Event, Step


class StepInline(admin.TabularInline):
    model = Step
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [StepInline]
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    fieldsets = [
        (None, {'fields': ['title', 'description', 'dateTime']}),
        ('Tespit', {'fields': ['detection_method', 'detection_method_text', 'detection_by']}),
        ('Etki', {'fields': ['level', 'type', 'type_text']}),
        ('Çözüm', {'fields': ['solved_at', 'failure_source', 'solution_by', 'notes']}),
        ('Kayıt Bilgileri', {'fields': ['created_by', 'created_at', 'updated_by', 'updated_at']})]
    list_display = ('title', 'dateTime', 'solved_at')
    list_filter = ['dateTime', 'solved_at']
    search_fields = ['title', 'description']

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)
