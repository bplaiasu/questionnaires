from django.contrib import admin
from .models import Category, Question, Answer

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'simulation_exam_a', 'sim_ex_a_questions')
    list_display_links = ('id', 'name')
    list_editable = ('is_active', 'simulation_exam_a')

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('id', 'text', 'category')
    list_display_links = ('id', 'text')
    list_filter = ('category',)
    search_fields = ('text',)
    list_per_page = 20

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
