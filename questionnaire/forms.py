from django import forms
from .models import Questionnaire
from .choices import QUESTION_9_YES_OR_NO

class ParticipantForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Seu e-mail")

    class Meta:
        model = Questionnaire
        fields = ['sex', 'age', 'height', 'weight']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-label', 'placeholder': 'Digite sua idade'}),
            'height': forms.NumberInput(attrs={'class': 'form-label', 'placeholder': 'Digite sua altura'}),
            'weight': forms.NumberInput(attrs={'class': 'form-label', 'placeholder': 'Digite seu peso'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-label', 'placeholder': 'Digite seu email'})
        if 'sex' in self.fields:
            self.fields['sex'].choices = [('', 'Selecionar')] + [c for c in self.fields['sex'].choices if c[0]]

class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        questions = Question.objects.prefetch_related("choice_set__choices").order_by("order")
        
        for question in questions:
            choices = [
                (choice.value, choice.label)
                for choice in question.choice_set.choices.all()
            ]
            
            self.fields[question.code] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                required=question.required,
                widget=forms.Select(),
            )
    
    