from django import forms
from .models import UploadFileModel

# https://cjh5414.github.io/django-file-upload/

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields=('title','file')

    def __init(self, *args, *kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
