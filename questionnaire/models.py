from django.db import models
from decimal import Decimal
import uuid

# Create your models here.
class Participant(models.Model):
    hash_identify = models.CharField(max_length=64, unique=True, db_index=True, help_text="Hash SHA-256 for user email")
    created_date = models.DateField(auto_now_add=True)
    
class DecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 4)
        kwargs.setdefault('decimal_places', 2)
        super().__init__(*args, **kwargs)

# ChoiceSet representa um conjunto de escolhas.
class ChoiceSet(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=3)
        
    def __str__(self):
        return self.name

# Choice representa uma única escolha que deve estar em um conjunto.
class Choice(models.Model):
    choice_set = models.ForeignKey(ChoiceSet, on_delete=models.CASCADE, related_name="choices")
    
    value = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.label

# Question representa uma pergunta com um conjunto de escolhas.
class Question(models.Model):
    code = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    
    choice_set = models.ForeignKey(ChoiceSet, on_delete=models.PROTECT, related_name="questions", null=True, blank=True)
    
    order = models.PositiveIntegerField(default=0)
    required = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Questionnaire(models.Model):
    participant = models.OneToOneField(Participant, verbose_name=("email"), on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Questões de Baecke ordenadas, sem precisar serem criadas no Admin
    age = models.IntegerField(verbose_name="Sua idade")
    sex = models.CharField(max_length=10)
    height = models.FloatField(max_length=3, verbose_name="Sua altura")
    weight = models.FloatField(max_length=700, verbose_name="Seu peso")
    #question_1 = DecimalField(choices=QUESTION_1_VALUES, verbose_name="1. Qual a sua ocupação principal?", null=True, blank=True)
    #question_2 = DecimalField(choices=QUESTION_VALUES, verbose_name="2. No trabalho, eu fico sentado:", null=True, blank=True)
    #question_3 = DecimalField(choices=QUESTION_VALUES, verbose_name="3. No trabalho, eu fico em pé:", null=True, blank=True)
    #question_4 = DecimalField(choices=QUESTION_VALUES, verbose_name="4. No trabalho, eu ando:", null=True, blank=True)
    #question_5 = DecimalField(choices=QUESTION_VALUES, verbose_name="5. No trabalho, eu levanto objetos pesados:", null=True, blank=True)
    #question_6 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="6. Depois do trabalho, eu me sinto cansado:", null=True, blank=True)
    #question_7 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="7. No trabalho, eu suo:", null=True, blank=True)
    #question_8 = DecimalField(choices=QUESTION_VALUES_WEIGHT, verbose_name="8. Em comparação com o trabalho de outras pessoas da minha idade, o meu trabalho é fisicamente:", null=True, blank=True)
    #question_9_boolean = models.BooleanField(choices=QUESTION_9_YES_OR_NO, verbose_name="9. Você pratica algum exercício físico?", null=True, blank=True, default=None)
    #question_9 = DecimalField(choices=QUESTION_9_VALUES, verbose_name="Qual exercício?", null=True, blank=True)
    #question_9_time = DecimalField(choices=QUESTION_9_TIME, verbose_name="Quantas horas por semana você pratica esse exercício", null=True, blank=True)
    #question_9_proportion = DecimalField(choices=QUESTION_9_PROPORTION, verbose_name="Quantos meses por ano?", null=True, blank=True)
    #question_9_other_boolean = models.BooleanField(choices=QUESTION_9_YES_OR_NO, verbose_name="Você pratica um segundo exercício físico?", null=True, blank=True, default=None)
    #question_9_other = DecimalField(choices=QUESTION_9_VALUES, verbose_name="Qual exercício?", null=True, blank=True)
    #question_9_other_time = DecimalField(choices=QUESTION_9_TIME, verbose_name="Quantas horas por semana você pratica esse exercício?", null=True, blank=True)
    #question_9_other_proportion = DecimalField(choices=QUESTION_9_PROPORTION, verbose_name="Quantos meses por ano?", null=True, blank=True)
    #question_10 = DecimalField(choices=QUESTION_VALUES_EQUAL, verbose_name="10. Em comparação com outras pessoas da minha idade, minha atividade física durante os momentos de lazer é:", null=True, blank=True)
    #question_11 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="11. Durante os momentos de lazer eu suo:", null=True, blank=True)
    #question_12 = DecimalField(choices=QUESTION_VALUES, verbose_name="12. Durante os momentos de lazer, eu pratico atividades físicas:", null=True, blank=True)
    #question_13 = DecimalField(choices=QUESTION_VALUES, verbose_name="13. Durante os momentos de lazer, eu assisto televisão:", null=True, blank=True)
    #question_14 = DecimalField(choices=QUESTION_VALUES, verbose_name="14. Durante os momentos de lazer, eu ando:", null=True, blank=True)
    #question_15 = DecimalField(choices=QUESTION_VALUES, verbose_name="15. Durante os momentos de lazer, eu ando de bicicleta:", null=True, blank=True)
    #question_16 = DecimalField(choices=QUESTION_16, verbose_name="16. Quantos minutos você caminha e/ou anda de bicicleta por dia para ir ou voltar do trabalho, escola ou shopping?", null=True, blank=True)
    total_calculated = models.DecimalField(default=Decimal(0), editable=False, decimal_places=4, max_digits=8)

    def calculate_question_9(self):
        answers = self._get_answers_by_category("ELF")
        
        values = {
            answer.question.code: Decimal(answer.choice.value)
            for answer in answers
        }
        
        exercise_1 = (
            values.get("question_9_other", Decimal("0"))
            * values.get("question_9_other_time", Decimal("0"))
            * values.get("question_9_other_proportion", Decimal("0"))
        )
        
        exercise_2 = (
            values.get("question_9", Decimal("0"))
            * values.get("question_9_time", Decimal("0"))
            * values.get("question_9_proportion", Decimal("0"))
        )
        
        total = exercise_1 + exercise_2
        
        if total == 0:
            return Decimal("1")
        elif total < 4:
            return Decimal("2")
        elif total < 8:
            return Decimal("3")
        elif total < 12:
            return Decimal("4")
        else:
            return Decimal("5")

    def _getanswers_by_category(self, category):
        return self.answers.filter(question__choice_set__category=category).select_related("question", "choice")
    
    def _get_values(self, category):
        return[
            Decimal(answer.choice.value)
            for answer in self._getanswers_by_category(category)
        ]
        
    def calculate_afo(self):
        answers = self._getanswers_by_category("AFO")
        values = []
        
        for answer in answers:
            value = Decimal(answer.choice.value)
            if answer.question.code == "question_2":
                value = Decimal("6") - value
            values.append(value)
        
        if not values:
            return Decimal("0")
        
        return sum(values) / Decimal(len(values))
    
    def calculate_elf(self):
        answers = self._get_answers_by_category("ELF")
        
        values = {
            answer.question.code: Decimal(answer.choice.value)
            for answer in answers
        }
        
        q9 = self.calculate_question_9()
        q10 = values.get("question_10", Decimal("0"))
        q11 = values.get("question_11", Decimal("0"))
        q12 = values.get("question_12", Decimal("0"))
        
        return (
            q9 + q10 + q11 + q12
        ) / Decimal("4")
    
    def calculate_all(self):
        answers = self._getanswers_by_category("ALL")
        
        values = []
        
        for answer in answers:
            value = Decimal(answer.choice.value)
            if answer.question.code == "question_13":
                value = Decimal("6") - value
            values.append(value)
        
        if not values:
            return Decimal("0")
        
        return sum(values) / Decimal(len(values))
    
    def total(self):
        return (
            self.caltulate_afo() + self.calculate_elf() + self.calculate_all()
        )
    
    def save(self, *args, **kwargs):
        self.total_calculated = self.total()
        super().save(*args, **kwargs)
        
class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="answers")
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT, related_name="answers")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["questionnaire", "question"], name="unique_questionnaire_question")
        ]