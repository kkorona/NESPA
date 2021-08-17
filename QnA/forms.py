from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__( self, *args, **kwargs ):
        super(CommentForm, self).__init__( *args, **kwargs )
        self.fields['text'].label = False

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={'class': 'form-control', 
                                            'id': 'textAreaExample',
                                            'rows': 4,
                                            'placeholder': '댓글을 입력해주세요'})}