from django.core.management.base import BaseCommand

from questionnaire.models import ChoiceSet, Choice, Question
from questionnaire.choices import (
    SEX_CHOICES,
    QUESTION_VALUES,
    QUESTION_VALUES_REVERSE,
    QUESTION_VALUES_WEIGHT,
    QUESTION_VALUES_EQUAL,
    QUESTION_1_VALUES,
    QUESTION_9_VALUES,
)


class Command(BaseCommand):
    help = "Popula o questionário Baecke"

    def handle(self, *args, **options):
        self.create_choice_set(
            code="SEX",
            name="Sexo",
            category="ALL",
            choices=SEX_CHOICES,
        )

        self.create_choice_set(
            code="QUESTION_VALUES",
            name="Escala de frequência",
            category="AFO",
            choices=QUESTION_VALUES,
        )

        self.create_choice_set(
            code="QUESTION_VALUES_REVERSE",
            name="Escala de frequência invertida",
            category="ALL",
            choices=QUESTION_VALUES_REVERSE,
        )

        self.create_choice_set(
            code="QUESTION_VALUES_WEIGHT",
            name="Escala de peso",
            category="AFO",
            choices=QUESTION_VALUES_WEIGHT,
        )

        self.create_choice_set(
            code="QUESTION_VALUES_EQUAL",
            name="Escala de comparação",
            category="AFO",
            choices=QUESTION_VALUES_EQUAL,
        )

        self.create_choice_set(
            code="QUESTION_1_VALUES",
            name="Atividades ocupacionais",
            category="AFO",
            choices=QUESTION_1_VALUES,
        )

        self.create_choice_set(
            code="QUESTION_9_VALUES",
            name="Atividades físicas",
            category="ELF",
            choices=QUESTION_9_VALUES,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "ChoiceSets e Choices criados com sucesso!"
            )
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