from django import forms

class DocumentForm(form.Form):
    docfile = forms.FileField(
        label = 'Select a file',
        help_text = 'max. 42 megabytes'
        )