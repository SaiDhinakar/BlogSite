# home/forms.py
from django import forms
from .models import Post, Comment, Category
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    # Add TinyMCE widget for content field
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text='Write your post content here.'
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        required=True
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'categories', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '3'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write your comment here...',
                'maxlength': '500'
            })
        }
        labels = {
            'content': 'Comment'
        }
        error_messages = {
            'content': {
                'required': 'Please enter a comment',
                'max_length': 'Comment cannot exceed 500 characters'
            }
        }