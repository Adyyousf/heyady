from django.contrib import admin
from blog.models import Blog, Contact

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/main.css",)
        }

        js = ("js/blog.js",)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact)
