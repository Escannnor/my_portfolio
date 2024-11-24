from django.contrib import admin
from .models import Project, Achievement, BlogPost


# Customizing how the Project model is displayed in the admin interface
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'file')  # Display key fields in the admin list view
    search_fields = ('title', 'description')  # Enable search by title and description
    list_filter = ('uploaded_at',)  # Add filters for uploaded date
    ordering = ('-uploaded_at',)  # Order projects by the most recent
    fieldsets = (  # Organize the admin form into sections
        ('Basic Information', {
            'fields': ('title', 'description', 'github_link')
        }),
        ('Additional', {
            'fields': ('file',)
        }),
    )

# Customizing how the Achievement model is displayed in the admin interface
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_awarded')
    search_fields = ('name', 'description')
    list_filter = ('date_awarded',)

# Customizing how the BlogPost model is displayed in the admin interface
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
