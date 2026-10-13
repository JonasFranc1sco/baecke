from django import forms
from .models import Question, Questionnaire, ChoiceSet

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
        
        choice_set = ChoiceSet.objects.get(code="SEX")
        
        sex_choices = [
            (str(choice.value), choice.label)
            for choice in choice_set.choices.all().order_by("order")
        ]
        
        self.fields["sex"] = forms.ChoiceField(
            choices=[("", "Selecionar")] + sex_choices,
            label="Sexo",
            required=True,
            widget=forms.Select(attrs={
                "class": "form-control",
            }),
        )

class QuestionnaireForm(forms.Form):
    BOOLEAN_QUESTIONS = {
        "question_9_boolean",
        "question_9_other_boolean",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        questions = (
            Question.objects
            .prefetch_related("choice_set__choices")
            .order_by("order")
        )
        for question in questions:
            if question.choice_set is None:
                continue

            choices = [
                (choice.code, choice.label)
                for choice in question.choice_set.choices.all().order_by("order")
            ]

            if question.code in self.BOOLEAN_QUESTIONS:
                self.fields[question.code] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    required=question.required,
                    widget=forms.RadioSelect(
                        attrs={"class": "form-check-input"}
                    ),
                )
            else:
                self.fields[question.code] = forms.ChoiceField(
                    label=question.text,
                    choices=[("", "Selecionar"), *choices],
                    required=question.required,
                    widget=forms.Select(
                        attrs={"class": "form-control"}
                    ),
                )

    