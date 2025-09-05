from django import forms
from .models import Review


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }