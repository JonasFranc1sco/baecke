
from django.core.management.base import BaseCommand
from questionnaire.models import ChoiceSet, Choice
from questionnaire.choices import (
    SEX_CHOICES,
    QUESTION_9_YES_OR_NO,
    QUESTION_9_TIME,
    QUESTION_9_PROPORTION,
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
    help = "Popula as escolhas do questionário de Baecke"

    CHOICE_SETS = [
        (
            "SEX",
            "Sexo",
            "PSL",
            SEX_CHOICES,
        ),
        (
            "QUESTION_1",
            "Qual a sua ocupação principal?",
            "AFO",
            QUESTION_1,
        ),
        (
            "QUESTION_2",
            "No trabalho, eu fico sentado:",
            "AFO",
            QUESTION_2,
        ),
        (
            "QUESTION_3",
            "No trabalho, eu fico em pé:",
            "AFO",
            QUESTION_3,
        ),
        (
            "QUESTION_4",
            "No trabalho, eu ando:",
            "AFO",
            QUESTION_4,
        ),
        (
            "QUESTION_5",
            "No trabalho, eu levanto objetos pesados:",
            "AFO",
            QUESTION_5,
        ),
        (
            "QUESTION_6",
            "Depois do trabalho, eu me sinto cansado:",
            "AFO",
            QUESTION_6,
        ),
        (
            "QUESTION_7",
            "No trabalho, eu suo:",
            "AFO",
            QUESTION_7,
        ),
        (
            "QUESTION_8",
            "Em comparação com o trabalho de pessoas da minha idade, meu trabalho é fisicamente:",
            "AFO",
            QUESTION_8,
        ),
        (
            "QUESTION_9",
            "Qual exercício?",
            "ELF",
            QUESTION_9,
        ),
        (
            "QUESTION_10",
            "Em comparação com outras pessoas da minha idade, minha atividade física durante o lazer é:",
            "ELF",
            QUESTION_10,
        ),
        (
            "QUESTION_11",
            "Durante os momentos de lazer eu suo:",
            "ELF",
            QUESTION_11,
        ),
        (
            "QUESTION_12",
            "Durante os momentos de lazer, eu pratico atividades físicas:",
            "ELF",
            QUESTION_12,
        ),
        (
            "QUESTION_13",
            "Durante os momentos de lazer, eu assisto televisão:",
            "ALL",
            QUESTION_13,
        ),
        (
            "QUESTION_14",
            "Durante os momentos de lazer, eu ando:",
            "ALL",
            QUESTION_14,
        ),
        (
            "QUESTION_15",
            "Durante os momentos de lazer, eu ando de bicicleta:",
            "ALL",
            QUESTION_15,
        ),
        (
            "QUESTION_16",
            "Quantos minutos você caminha e/ou anda de bicicleta por dia para ir ou voltar do trabalho, escola ou shopping?",
            "ALL",
            QUESTION_16,
        ),
        (
            "QUESTION_9_YES_OR_NO",
            "Sim ou não",
            "BOL",
            QUESTION_9_YES_OR_NO,
        ),
        (
            "QUESTION_9_TIME",
            "Horas por semana de exercício",
            "ELF",
            QUESTION_9_TIME,
        ),
        (
            "QUESTION_9_PROPORTION",
            "Meses por ano de exercício",
            "ELF",
            QUESTION_9_PROPORTION,
        ),
    ]

    def handle(self, *args, **options):
        for code, name, category, choices in self.CHOICE_SETS:
            self.create_choice_set(
                code=code,
                name=name,
                category=category,
                choices=choices,
            )

        self.stdout.write(
            self.style.SUCCESS("Seed de escolhas concluído.")
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
            # Identificador da opção, diferente da sua pontuação.
            choice_code = f"choice_{order:03d}"

            Choice.objects.update_or_create(
                choice_set=choice_set,
                code=choice_code,
                defaults={
                    "value": str(value),
                    "label": label,
                    "order": order,
                },
            )

        status = "criado" if created else "atualizado"
        self.stdout.write(f"ChoiceSet {status}: {name}")
