from django import forms
from stones.models import Comment, FinderComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "text"]
        widgets = {
            "author": forms.TextInput(attrs={"placeholder": "Twoja nazwa", "class": "form-control", "id": "author-input"}),
            "text": forms.Textarea(attrs={"placeholder": "Dodaj komentarz", "rows": 3, "class": "form-control"}),
        }


class FinderCommentForm(forms.ModelForm):
    class Meta:
        model = FinderComment
        fields = ["author", "text", "image"]
        widgets = {
            "author": forms.TextInput(attrs={"placeholder": "Twoja nazwa", "class": "form-control", "id": "author-input"}),
            "text": forms.Textarea(attrs={"placeholder": "Dodaj komentarz", "rows": 3, "class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control-file",
                "accept": "image/*",
                "id": "image"
            })
        }
