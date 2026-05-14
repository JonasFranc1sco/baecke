from django import forms
from .models import Questionnaire
from .choices import QUESTION_9_YES_OR_NO

class CleanRadioSelectMixin:
    fields: dict[str, forms.Field]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Garante que question_9_boolean e question_9_other_boolean comecem sem nada marcado
        # Não adicionamos uma opção vazia às choices dos RadioSelects — isso evitava
        # um rádio extra sem label. Em vez disso mantemos initial = None e forçamos
        # a validação em clean().
        for name in ['question_9_boolean', 'question_9_other_boolean']:
            if name in self.fields:
                field = self.fields[name]
                field.initial = None

        # Para os outros RadioSelects, apenas remove valores inválidos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.RadioSelect) and field_name not in ['question_9_boolean', 'question_9_other_boolean']:
                field.choices = [(val, label) for val, label in field.choices if val is not None and val != '']
                field.initial = None

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

class QuestionnaireForm(CleanRadioSelectMixin, forms.ModelForm):
    
    question_9_boolean = forms.TypedChoiceField(
        choices=(QUESTION_9_YES_OR_NO),
        coerce=lambda x: x == 'True', # Converte o valor do form ('True'/'False') para boolean
        widget=forms.RadioSelect,
        required=True, # A validação será feita no clean()
        label="9. Você pratica algum exercício físico?"
    )
    question_9_other_boolean = forms.TypedChoiceField(
        choices=QUESTION_9_YES_OR_NO,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect,
        required=False, # Este campo só aparece se o primeiro for 'Sim'
        label="9. Você pratica outro exercício físico?"
    )
    class Meta:
        model = Questionnaire
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6',
                  'question_7', 'question_8', 'question_9_boolean','question_9','question_9_time','question_9_proportion',
                  'question_9_other_boolean','question_9_other','question_9_other_time','question_9_other_proportion','question_10','question_11','question_12',
                  'question_13', 'question_14','question_15', 'question_16'] 
        widgets = {
            'question_1': forms.Select(),
            'question_2': forms.Select(),
            'question_3': forms.Select(),
            'question_4': forms.Select(),
            'question_5': forms.Select(),
            'question_6': forms.Select(),
            'question_7': forms.Select(),
            'question_8': forms.Select(),
            'question_9': forms.Select(),
            'question_9_time': forms.Select(),
            'question_9_proportion': forms.Select(),
            'question_9_other': forms.Select(),
            'question_9_other_time': forms.Select(),
            'question_9_other_proportion': forms.Select(),
            'question_10': forms.Select(),
            'question_11': forms.Select(),
            'question_12': forms.Select(),
            'question_13': forms.Select(),
            'question_14': forms.Select(),
            'question_15': forms.Select(),
            'question_16': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['question_9_boolean'].initial = None
        self.fields['question_9_other_boolean'].initial = None
        
        self.fields['question_9'].required = False
        self.fields['question_9_time'].required = False
        self.fields['question_9_proportion'].required = False
        self.fields['question_9_other'].required = False
        self.fields['question_9_other_time'].required = False
        self.fields['question_9_other_proportion'].required = False
        
        for field_name, field in self.fields.items():
            if hasattr(field, 'choices') and not isinstance(field.choices, list):
                field.choices = list(field.choices)      
        
        
    def clean(self):
        cleaned = super().clean()
        
        if 'question_9_boolean' not in cleaned or cleaned['question_9_boolean'] is None:
            self.add_error('question_9_boolean', "Este campo é obrigatório")
        
        groups = {
            'question_9': ['question_9', 'question_9_time', 'question_9_proportion'],
            'question_9_other': ['question_9_other', 'question_9_other_time', 'question_9_other_proportion'],
        }
        
        for group_name, fields in groups.items():
            bool_field = f"{group_name}_boolean"
            active = cleaned.get(bool_field)
            if active:
                for f in fields:
                    if not cleaned.get(f):
                        self.add_error(f, "Este campo é obrigatório quando a opção está ativa.")
            else:
                for f in fields:
                    if f in cleaned:
                        cleaned[f] = None
                    
        return cleaned
    
    def get_widget_type(self, field):
        return field.field.widget.__class__.__name__