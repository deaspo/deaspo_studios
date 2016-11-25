from django.contrib import admin
from deaspo.models import Project, Product, Plan, EmailPlan, ProductWebOrder
#add search and related projects functionality
class ProductSearch(admin.ModelAdmin):
    list_display = ['pname']
    search_fields = ['pname']
    filter_horizontal = ['prel', 'pproj', 'plan']

class ProjectSearch(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# Register your models here.
admin.site.register(Product, ProductSearch)
admin.site.register(Project, ProjectSearch)
admin.site.register(Plan)
admin.site.register(ProductWebOrder)
admin.site.register(EmailPlan)

