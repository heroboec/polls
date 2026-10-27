from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from apps.core.models import Answer, AnswerStatistic, Poll, PollStatistic, Profile, Question

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class ProfileUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('sort_index', 'title')
    extra = 1
    show_change_link = True


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('sort_index', 'title', 'is_open_answer')
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('-id',)
    autocomplete_fields = ('author',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'poll', 'sort_index')
    list_select_related = ('poll',)
    autocomplete_fields = ('poll',)
    inlines = [AnswerInline]


@admin.register(PollStatistic)
class PollStatisticAdmin(admin.ModelAdmin):
    list_display = ('poll', 'started', 'completed', 'total_duration_sec')
    list_select_related = ('poll',)
    raw_id_fields = ('poll',)


@admin.register(AnswerStatistic)
class AnswerStatisticAdmin(admin.ModelAdmin):
    list_display = ('answer', 'choices_count')
    list_select_related = ('answer',)
    raw_id_fields = ('answer',)
