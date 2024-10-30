from django.contrib import admin
from .models import Availability, Consultation, NutritionPlan, ClientProgress
# Register your models here.
admin.site.register(Availability)
admin.site.register(Consultation)
admin.site.register(NutritionPlan)

from django.utils.html import format_html

class ClientProgressAdmin(admin.ModelAdmin):
    list_display = ('dietitian', 'client', 'progress_bar', 'date_updated')
    
    # Method to render progress bar as HTML
    def progress_bar(self, obj):
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 4px;">'
            '<div style="width: {}%; background: #007bff; padding: 2px; color: white; border-radius: 4px; text-align: center;">'
            '{}%</div></div>',
            obj.progress,
            obj.progress
        )
    progress_bar.short_description = "Progress"

admin.site.register(ClientProgress, ClientProgressAdmin)