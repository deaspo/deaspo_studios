from django.contrib import admin
from deaspo.models import Project, Product
#add search and related projects functionality
class ProductSearch(admin.ModelAdmin):
    list_display = ['pname']
    search_fields = ['pname']
    filter_horizontal = ['prel', 'pproj']

class ProjectSearch(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# Register your models here.
admin.site.register(Product, ProductSearch)
admin.site.register(Project, ProjectSearch)

