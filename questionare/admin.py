from django.contrib import admin
from .models import Choice, Question, Song
# Register your models here.


# Inline for Choice model
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

# Admin for Question model
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
    ]
    inlines = [ChoiceInline]

# Inline for Song model in Choice Admin
class SongInline(admin.StackedInline):
    model = Song.choices.through  # Many-to-many through table
    extra = 3

# Admin for Song model
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'release_date')  # Customize display fields
    search_fields = ('title', 'album')  # Enable search by title and album
    filter_horizontal = ('choices',)  # Horizontal filter widget for many-to-many field

# Register Question and Song to the admin site
admin.site.register(Question, QuestionAdmin)
admin.site.register(Song, SongAdmin)
