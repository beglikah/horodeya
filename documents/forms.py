from django import forms
from documents.models import Document


class DocumentForm(forms.Form):
    class Neta:
        model = Document
        fields = [
            'title',
            'slug',
            'document'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class DocumentUpdateForm(forms.Form):
    class Neta:
        model = Document
        fields = [
            'title',
            'slug',
            'document'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
