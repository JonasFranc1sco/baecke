from django.contrib import admin
from .models import (
    ChoiceSet,
    Choice,
    Question,
    Answer,
    Participant,
    Questionnaire,
)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    ordering = ("order",)
    
@admin.register(ChoiceSet)
class ChoiceSetAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category")
    search_fields = ("name", "code")
    list_filter = ("category",)
    inlines = [ChoiceInline]
    
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "choice_set", "order")
    list_filter = ("choice_set",)
    search_fields = ("label",)
    ordering = ("choice_set", "order")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "code", "text", "choice_set", "required")
    list_display_links = ("code", "text")
    list_filter = ("choice_set", "required")
    search_fields = ("code", "text")
    ordering = ("order",)
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("questionnaire", "question", "choice")
    list_filter = ("question",)
    search_fields = ("questionnaire__uuid", "question__code", "question__text",)
    
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("hash_identify", "created_date")
    search_fields = ("hash_identify",)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("uuid", "participant", "age", "sex", "height", "weight", "total_calculated",)
    search_fields = ("uuid", "participant__hash_identify")
    readonly_fields = ("uuid", "total_calculated")