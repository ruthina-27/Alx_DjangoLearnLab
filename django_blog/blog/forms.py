from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }


class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts with tag functionality."""
    tags_input = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)',
            'data-toggle': 'tooltip',
            'title': 'Separate multiple tags with commas'
        }),
        help_text='Enter tags separated by commas. New tags will be created automatically.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 10
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Maximum 200 characters'
        self.fields['content'].help_text = 'Write your blog post content'
        
        # Pre-populate tags field if editing existing post
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit:
            self._save_tags(post)
        return post
    
    def _save_tags(self, post):
        """Process and save tags for the post."""
        tags_input = self.cleaned_data.get('tags_input', '')
        if tags_input:
            # Clear existing tags
            post.tags.clear()
            # Process new tags
            tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
            for tag_name in tag_names:
                if tag_name:  # Ensure tag name is not empty
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)


class CommentForm(forms.ModelForm):
    """Form for creating and updating comments with validation rules."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'minlength': '10',
                'maxlength': '1000'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].help_text = 'Share your thoughts about this post (10-1000 characters)'
        self.fields['content'].required = True
        
    def clean_content(self):
        """Custom validation for comment content."""
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 10:
                raise forms.ValidationError('Comment must be at least 10 characters long.')
            if len(content) > 1000:
                raise forms.ValidationError('Comment cannot exceed 1000 characters.')
            # Check for spam-like content
            if content.lower() in ['spam', 'test', 'hello', 'hi']:
                raise forms.ValidationError('Please write a meaningful comment.')
        return content
