from django import forms
from .model.form import Form

class SongRequestForm(forms.ModelForm):
    singerIsMale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    prompt = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your song idea...'}))
    mood = forms.ChoiceField(required=False, choices=Form.Mood.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(required=False, choices=Form.Genre.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    occasion = forms.ChoiceField(required=False, choices=Form.Occasion.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Form
        fields = ['name', 'prompt', 'mood', 'genre', 'occasion', 'singerIsMale', 'lengthInSeconds']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for your song'}),
            'prompt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your song idea...'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'occasion': forms.Select(attrs={'class': 'form-control'}),
            'lengthInSeconds': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 300, 'value': 120}),
            'singerIsMale': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
