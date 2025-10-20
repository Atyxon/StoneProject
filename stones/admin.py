from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from stones.models import Stone, Comment, FinderComment
from image_cropping import ImageCroppingMixin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('author', 'text', 'created_at')


@admin.register(FinderComment)
class FinderCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')


@admin.register(Stone)
class StoneAdmin(ImageCroppingMixin, admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin_crop_grid.css',)
        }
    list_display = ('title', 'public', 'found', 'view_stone_button')
    readonly_fields = ('generate_qr_button', 'view_stone_button')
    exclude = ('qr_code',)
    inlines = [CommentInline]

    def public(self, obj):
        return not obj.draft
    public.boolean = True
    public.short_description = "Public"

    def generate_qr_button(self, obj):
        if obj.pk:
            url = reverse('stone_qr', args=[obj.pk])
            return format_html(
                '<a href="{}" target="_blank">'
                '<button type="button">Generuj kod QR</button>'
                '</a>',
                url
            )
        return "-"
    generate_qr_button.short_description = "Kod QR"

    def view_stone_button(self, obj):
        if obj.pk:
            url = reverse('stone_detail', args=[obj.pk])
            return format_html(
                '<a href="{}" target="_blank">'
                '<button type="button">🌐 Otwórz stronę kamienia</button>'
                '</a>',
                url
            )
        return "-"
    view_stone_button.short_description = "Podgląd strony kamienia"
