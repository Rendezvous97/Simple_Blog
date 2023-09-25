from django import forms
from blog.models import Post, Comment



class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'author': forms.Select(attrs={'style': 'margin-bottom: 5px;'}),
            'title': forms.TextInput(attrs={'class':'textinputclass', 'style': 'margin-bottom: 5px;'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent border',
                                          'style': 'margin-bottom: 20px; min-height: 100px; padding: 10px; font-size: 15px;'}),
        }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }

