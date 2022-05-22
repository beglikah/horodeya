from django.contrib import admin
from . import models as my_models


class QuestionnaireAdmin(admin.ModelAdmin):
    model = my_models.Questionnaire
    fieldsets = [
        (None,               {'fields': ['title']}),
        # ('Date information', {
        #     'fields': ['pub_date'], 'classes': ['collapse']
        # }),
    ]
    list_display = ['title', 'pub_date']


# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3


class ChoiceInline(admin.TabularInline):
    model = my_models.Choice
    extra = 3
    classes = ['collapse']


class QuestionAdmin(admin.ModelAdmin):
    model = my_models.Question


class QuestionChoiceAdmin(admin.ModelAdmin):
    model = my_models.QuestionChoice
    fieldsets = [
        (None, {'fields': ['questionnaire']}),
        (None, {
            'fields': ['question_type'],
        }),
        (None, {'fields': ['question_text']}),
        ('Position', {'fields': ['position']}),
    ]
    classes = ['collapse']
    inlines = [ChoiceInline]
    readonly_fields = ['question_type']



class ShortAnswerAdmin(admin.ModelAdmin):
    fields = [
        'questionnaire',
        'question_type',
        'question_text',
        'position'
    ]
    readonly_fields = ['question_type']
    list_display = [
        'questionnaire',
        'position',
        'question_text',
        'question_type',
    ]


class QuestionChoiceInline(admin.StackedInline):
    model = my_models.QuestionChoice
    extra = 1
    fields = [
        'question_type',
        'question_text',
        'position'
    ]

    inlines = [ChoiceInline]
    classes = ['collapse']
    readonly_fields = ['question_type']


class ShortAnswerInline(admin.StackedInline):
    model = my_models.ShortAnswer
    extra = 1
    fields = [
        'question_type',
        'question_text',
        'position'
    ]
    readonly_fields = ['question_type']


class LongAnswerInline(admin.StackedInline):
    model = my_models.LongAnswer
    extra = 1
    fields = [
        'question_type',
        'question_text',
        'position'
    ]
    readonly_fields = ['question_type']


class FileAnswerInline(admin.StackedInline):
    model = my_models.FileAnswer
    extra = 1
    fields = [
        'question_type',
        'question_text',
        'position'
    ]
    readonly_fields = ['question_type']


class QuestionnaireAdmin(admin.ModelAdmin):
    model = my_models.Questionnaire
    fieldsets = [
        (None,               {'fields': ['title']}),
        # ('Date information', {
        #     'fields': ['pub_date'], 'classes': ['collapse']
        # }),
    ]
    inlines = [ShortAnswerInline, LongAnswerInline, QuestionChoiceInline, FileAnswerInline]
    classes = ['collapse']
    list_display = ['title', 'pub_date']


admin.site.register(my_models.Questionnaire, QuestionnaireAdmin)
admin.site.register(my_models.Question, QuestionAdmin)
admin.site.register(my_models.QuestionChoice, QuestionChoiceAdmin)
admin.site.register(my_models.ShortAnswer, ShortAnswerAdmin)
admin.site.register(my_models.LongAnswer)
admin.site.register(my_models.FileAnswer)
