
from django.core.management.base import BaseCommand, CommandError

from questionnaire.models import Question, ChoiceSet


class Command(BaseCommand):
    help = "Popula as perguntas dinâmicas do questionário de Baecke"

    QUESTIONS = [
        {
            "code": "question_1",
            "text": "1. Qual a sua ocupação principal?",
            "choice_set": "QUESTION_1",
            "order": 1,
        },
        {
            "code": "question_2",
            "text": "2. No trabalho, eu fico sentado:",
            "choice_set": "QUESTION_2",
            "order": 2,
        },
        {
            "code": "question_3",
            "text": "3. No trabalho, eu fico em pé:",
            "choice_set": "QUESTION_3",
            "order": 3,
        },
        {
            "code": "question_4",
            "text": "4. No trabalho, eu ando:",
            "choice_set": "QUESTION_4",
            "order": 4,
        },
        {
            "code": "question_5",
            "text": "5. No trabalho, eu levanto objetos pesados:",
            "choice_set": "QUESTION_5",
            "order": 5,
        },
        {
            "code": "question_6",
            "text": "6. Depois do trabalho, eu me sinto cansado:",
            "choice_set": "QUESTION_6",
            "order": 6,
        },
        {
            "code": "question_7",
            "text": "7. No trabalho, eu suo:",
            "choice_set": "QUESTION_7",
            "order": 7,
        },
        {
            "code": "question_8",
            "text": (
                "8. Em comparação com o trabalho de outras pessoas "
                "da minha idade, o meu trabalho é fisicamente:"
            ),
            "choice_set": "QUESTION_8",
            "order": 8,
        },

        # Pergunta 9: exercício principal e segundo exercício.
        {
            "code": "question_9_boolean",
            "text": "9. Você pratica algum exercício físico?",
            "choice_set": "QUESTION_9_YES_OR_NO",
            "order": 9,
        },
        {
            "code": "question_9",
            "text": "Qual exercício?",
            "choice_set": "QUESTION_9",
            "order": 10,
        },
        {
            "code": "question_9_time",
            "text": "Quantas horas por semana você pratica esse exercício?",
            "choice_set": "QUESTION_9_TIME",
            "order": 11,
        },
        {
            "code": "question_9_proportion",
            "text": "Quantos meses por ano você pratica esse exercício?",
            "choice_set": "QUESTION_9_PROPORTION",
            "order": 12,
        },
        {
            "code": "question_9_other_boolean",
            "text": "Você pratica um segundo exercício físico?",
            "choice_set": "QUESTION_9_YES_OR_NO",
            "order": 13,
        },
        {
            "code": "question_9_other",
            "text": "Qual é o segundo exercício?",
            "choice_set": "QUESTION_9",
            "order": 14,
        },
        {
            "code": "question_9_other_time",
            "text": "Quantas horas por semana você pratica esse segundo exercício?",
            "choice_set": "QUESTION_9_TIME",
            "order": 15,
        },
        {
            "code": "question_9_other_proportion",
            "text": "Quantos meses por ano você pratica esse segundo exercício?",
            "choice_set": "QUESTION_9_PROPORTION",
            "order": 16,
        },

        {
            "code": "question_10",
            "text": (
                "10. Em comparação com outras pessoas da minha idade, "
                "minha atividade física durante os momentos de lazer é:"
            ),
            "choice_set": "QUESTION_10",
            "order": 17,
        },
        {
            "code": "question_11",
            "text": "11. Durante os momentos de lazer eu suo:",
            "choice_set": "QUESTION_11",
            "order": 18,
        },
        {
            "code": "question_12",
            "text": (
                "12. Durante os momentos de lazer, eu pratico "
                "atividades físicas:"
            ),
            "choice_set": "QUESTION_12",
            "order": 19,
        },
        {
            "code": "question_13",
            "text": "13. Durante os momentos de lazer, eu assisto televisão:",
            "choice_set": "QUESTION_13",
            "order": 20,
        },
        {
            "code": "question_14",
            "text": "14. Durante os momentos de lazer, eu ando:",
            "choice_set": "QUESTION_14",
            "order": 21,
        },
        {
            "code": "question_15",
            "text": "15. Durante os momentos de lazer, eu ando de bicicleta:",
            "choice_set": "QUESTION_15",
            "order": 22,
        },
        {
            "code": "question_16",
            "text": (
                "16. Quantos minutos você caminha e/ou anda de bicicleta "
                "por dia para ir ou voltar do trabalho, escola ou shopping?"
            ),
            "choice_set": "QUESTION_16",
            "order": 23,
        },
    ]

    def handle(self, *args, **options):
        missing = sorted({
            item["choice_set"]
            for item in self.QUESTIONS
            if not ChoiceSet.objects.filter(
                code=item["choice_set"]
            ).exists()
        })

        if missing:
            raise CommandError(
                "Os seguintes ChoiceSets não existem: "
                + ", ".join(missing)
                + ". Execute primeiro o comando de seed dos ChoiceSets."
            )

        created_count = 0
        updated_count = 0

        for item in self.QUESTIONS:
            choice_set = ChoiceSet.objects.get(
                code=item["choice_set"]
            )

            question, created = Question.objects.update_or_create(
                code=item["code"],
                defaults={
                    "text": item["text"],
                    "choice_set": choice_set,
                    "order": item["order"],
                    "required": False,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Criada: {question.code}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    f"Atualizada: {question.code}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Concluído: {created_count} criadas, "
                f"{updated_count} atualizadas."
            )
        )
