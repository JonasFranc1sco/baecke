from django.core.management.base import BaseCommand

from questionnaire.models import ChoiceSet, Choice, Question
from questionnaire.choices2 import (
    SEX_CHOICES,
    QUESTION_1,
    QUESTION_2,
    QUESTION_3,
    QUESTION_4,
    QUESTION_5,
    QUESTION_6,
    QUESTION_7,
    QUESTION_8,
    QUESTION_9,
    QUESTION_10,
    QUESTION_11,
    QUESTION_12,
    QUESTION_13,
    QUESTION_14,
    QUESTION_15,
    QUESTION_16,
)

class Command(BaseCommand):
    help = "Popula o questionário Baecke"
    
    def handle(self, *args, **options):
        self.create_choice_set(
            code="SEX",
            name="Sexo",
            category="PSL",
            choices=SEX_CHOICES,
        )
        
        self.create_choice_set(
            code="QUESTION_1",
            name="Qual a sua ocupação principal?",
            category="AFO",
            choices=QUESTION_1,
        )
        
        self.create_choice_set(
            code="QUESTION_2",
            name="No trabalho, eu fico sentado:",
            category="AFO",
            choices=QUESTION_2,
        )
        
        self.create_choice_set(
            code="QUESTION_3",
            name="No trabalho, eu fico em pé:",
            category="AFO",
            choices=QUESTION_3,
        )
        
        self.create_choice_set(
            code="QUESTION_4",
            name="No trabalho, eu ando:",
            category="AFO",
            choices=QUESTION_4,
        )
        
        self.create_choice_set(
            code="QUESTION_5",
            name="No trabalho, eu levanto objetos pesados:",
            category="AFO",
            choices=QUESTION_5,
        )
        
        self.create_choice_set(
            code="QUESTION_6",
            name="Depois do trabalho, eu me sinto cansado:",
            category="AFO",
            choices=QUESTION_6,
        )
        
        self.create_choice_set(
            code="QUESTION_7",
            name="No trabalho, eu suo:",
            category="AFO",
            choices=QUESTION_7,
        )
        self.create_choice_set(
            code="QUESTION_8",
            name="Em comparação com o trabalho de outras pessoas da minha idade, o meu trabalho é fisicamente:",
            category="AFO",
            choices=QUESTION_8,
        )
        
        self.create_choice_set(
            code="QUESTION_9",
            name="Qual exercício?",
            category="ELF",
            choices=QUESTION_9,
        )
        
        self.create_choice_set(
            code="QUESTION_10",
            name="Em comparação com outras pessoas da minha idade, minha atividade física durante os momentos de lazer é:",
            category="ELF",
            choices=QUESTION_10,
        )
        
        self.create_choice_set(
            code="QUESTION_11",
            name="Durante os momentos de lazer eu suo:",
            category="ELF",
            choices=QUESTION_11,
        )
        
        self.create_choice_set(
            code="QUESTION_12",
            name="Durante os momentos de lazer, eu pratico atividades físicas:",
            category="ELF",
            choices=QUESTION_12,
        )
        
        self.create_choice_set(
            code="QUESTION_13",
            name="Durante os momentos de lazer, eu assisto televisão:",
            category="ALL",
            choices=QUESTION_13,
        )
        
        self.create_choice_set(
            code="QUESTION_14",
            name="Durante os momentos de lazer, eu ando:",
            category="ALL",
            choices=QUESTION_14,
        )
        
        self.create_choice_set(
            code="QUESTION_15",
            name="Durante os momentos de lazer, eu ando de bicicleta:",
            category="ALL",
            choices=QUESTION_15,
        )
        
        self.create_choice_set(
            code="QUESTION_16",
            name="Quantos minutos você caminha e/ou anda de bicicleta por dia para ir ou voltar do trabalho, escola ou shopping?",
            category="ALL",
            choices=QUESTION_16,
        )

        
    def create_choice_set(self, code, name, category, choices):
        choice_set, created = ChoiceSet.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "category": category,
            },
        )
        
        for order, (value, label) in enumerate(choices, start=1):
            Choice.objects.update_or_create(
                choice_set=choice_set,
                order=order,
                defaults={
                    "value": str(value),
                    "label": label,
                },
            )
            
        if created:
            self.stdout.write(
                f"ChoiceSet criado: {name}"
            )
        else:
            self.stdout.write(
                f"ChoiceSet atualizado: {name}"
            )