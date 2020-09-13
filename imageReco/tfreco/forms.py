from django import forms
from tfreco.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields =('document',)
