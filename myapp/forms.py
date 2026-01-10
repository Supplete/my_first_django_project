from django import forms
from .models import SparePart
from .models import MessageReply


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['name', 'price', 'in_stock', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }



class ReplyForm(forms.ModelForm):
    class Meta:
        model = MessageReply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }