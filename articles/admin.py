from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))

        if main_count == 0:
            raise ValidationError('Должен быть указан один основной раздел.')
        elif main_count > 1:
            raise ValidationError('Основной раздел может быть только один.')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
