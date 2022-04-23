from django import forms
from documents.models import Document


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Document
        fields = ['title', 'document']
