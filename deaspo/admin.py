from django.contrib import admin
from deaspo.models import Project, Product, Plan, EmailPlan, ProductWebOrder, UserProfile, Comment, Contact, Staff, Social
#add search and related projects functionality
class ProductSearch(admin.ModelAdmin):
    list_display = ['pname']
    search_fields = ['pname']
    filter_horizontal = ['prel', 'pproj', 'plan']

class ProjectSearch(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','email','approved']

class StaffSearch(admin.ModelAdmin):
    list_display =['name']
    search_fields = ['name','position']

class SocialAdmin(admin.ModelAdmin):
    list_display = ['get_category_display']



# Register your models here.
admin.site.register(Product, ProductSearch)
admin.site.register(Project, ProjectSearch)
admin.site.register(Plan)
admin.site.register(ProductWebOrder)
admin.site.register(EmailPlan)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Staff, StaffSearch)
admin.site.register(Social, SocialAdmin)
