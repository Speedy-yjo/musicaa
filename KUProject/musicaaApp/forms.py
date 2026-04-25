from django import forms
from .model.form import Form

class SongRequestForm(forms.ModelForm):
    singerIsMale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    prompt = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your song idea...'}))
    mood = forms.ChoiceField(required=False, choices=Form.Mood.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(required=False, choices=Form.Genre.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    occasion = forms.ChoiceField(required=False, choices=Form.Occasion.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    length_str = forms.CharField(
        required=True, 
        initial='03:00',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '03:00', 'pattern': '^[0-5]?[0-9]:[0-5][0-9]$'})
    )

    class Meta:
        model = Form
        fields = ['name', 'prompt', 'mood', 'genre', 'occasion', 'singerIsMale']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for your song'}),
            'prompt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your song idea...'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'occasion': forms.Select(attrs={'class': 'form-control'}),
            'singerIsMale': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_length_str(self):
        val = self.cleaned_data.get('length_str')
        try:
            parts = val.split(':')
            minutes = int(parts[0])
            seconds = int(parts[1])
            total_seconds = minutes * 60 + seconds
            if not (120 <= total_seconds <= 360):
                raise forms.ValidationError("Length must be between 02:00 and 06:00")
            return total_seconds
        except (ValueError, IndexError):
            raise forms.ValidationError("Invalid format. Use mm:ss")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.lengthInSeconds = self.cleaned_data.get('length_str', 180)
        if commit:
            instance.save()
        return instance
