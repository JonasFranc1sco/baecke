from django.db import models
from decimal import Decimal
import uuid
from .choices import SEX_CHOICES, QUESTION_1_VALUES, QUESTION_VALUES, QUESTION_VALUES_REVERSE, QUESTION_VALUES_WEIGHT, QUESTION_VALUES_EQUAL, QUESTION_9_VALUES, QUESTION_9_YES_OR_NO, QUESTION_9_TIME, QUESTION_9_PROPORTION, QUESTION_16

# Create your models here.
class Participant(models.Model):
    hash_identify = models.CharField(max_length=64, unique=True, db_index=True, help_text="Hash SHA-256 for user email")
    created_date = models.DateField(auto_now_add=True)
    
class DecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 4)
        kwargs.setdefault('decimal_places', 2)
        super().__init__(*args, **kwargs)



class Questionnaire(models.Model):
    participant = models.OneToOneField(Participant, verbose_name=("email"), on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Questões de Baecke ordenadas, sem precisar serem criadas no Admin
    age = models.IntegerField(verbose_name="Sua idade")
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    height = models.FloatField(max_length=3, verbose_name="Sua altura")
    weight = models.FloatField(max_length=700, verbose_name="Seu peso")
    question_1 = DecimalField(choices=QUESTION_1_VALUES, verbose_name="1. Qual a sua ocupação principal?", null=True, blank=True)
    question_2 = DecimalField(choices=QUESTION_VALUES, verbose_name="2. No trabalho, eu fico sentado:", null=True, blank=True)
    question_3 = DecimalField(choices=QUESTION_VALUES, verbose_name="3. No trabalho, eu fico em pé", null=True, blank=True)
    question_4 = DecimalField(choices=QUESTION_VALUES, verbose_name="4. No trabalho, eu ando:", null=True, blank=True)
    question_5 = DecimalField(choices=QUESTION_VALUES, verbose_name="5. No trabalho, eu levanto objetos pesados:", null=True, blank=True)
    question_6 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="6. Depois do trabalho, eu me sinto cansado:", null=True, blank=True)
    question_7 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="7. No trabalho, eu suo:", null=True, blank=True)
    question_8 = DecimalField(choices=QUESTION_VALUES_WEIGHT, verbose_name="8. Em comparação com o trabalho de outras pessoas da minha idade, o meu trabalho é fisicamente:", null=True, blank=True)
    question_9_boolean = models.BooleanField(choices=QUESTION_9_YES_OR_NO, verbose_name="9. Você pratica algum exercício físico?", null=True, blank=True, default=None)
    question_9 = DecimalField(choices=QUESTION_9_VALUES, verbose_name="Qual exercício?", null=True, blank=True)
    question_9_time = DecimalField(choices=QUESTION_9_TIME, verbose_name="Quantas horas por semana você pratica esse exercício", null=True, blank=True)
    question_9_proportion = DecimalField(choices=QUESTION_9_PROPORTION, verbose_name="Quantos meses por ano?", null=True, blank=True)
    question_9_other_boolean = models.BooleanField(choices=QUESTION_9_YES_OR_NO, verbose_name="Você pratica um segundo exercício físico?", null=True, blank=True, default=None)
    question_9_other = DecimalField(choices=QUESTION_9_VALUES, verbose_name="Qual exercício?", null=True, blank=True)
    question_9_other_time = DecimalField(choices=QUESTION_9_TIME, verbose_name="Quantas horas por semana você pratica esse exercício?", null=True, blank=True)
    question_9_other_proportion = DecimalField(choices=QUESTION_9_PROPORTION, verbose_name="Quantos meses por ano?", null=True, blank=True)
    question_10 = DecimalField(choices=QUESTION_VALUES_EQUAL, verbose_name="10. Em comparação com outras pessoas da minha idade, minha atividade física durante os momentos de lazer é:", null=True, blank=True)
    question_11 = DecimalField(choices=QUESTION_VALUES_REVERSE, verbose_name="11. Durante os momentos de lazer eu suo:", null=True, blank=True)
    question_12 = DecimalField(choices=QUESTION_VALUES, verbose_name="12. Durante os momentos de lazer, eu pratico atividades físicas:", null=True, blank=True)
    question_13 = DecimalField(choices=QUESTION_VALUES, verbose_name="13. Durante os momentos de lazer, eu assisto televisão:", null=True, blank=True)
    question_14 = DecimalField(choices=QUESTION_VALUES, verbose_name="14. Durante os momentos de lazer, eu ando:", null=True, blank=True)
    question_15 = DecimalField(choices=QUESTION_VALUES, verbose_name="15. Durante os momentos de lazer, eu ando de bicicleta:", null=True, blank=True)
    question_16 = DecimalField(choices=QUESTION_16, verbose_name="16. Quantos minutos você caminha e/ou anda de bicicleta por dia para ir ou voltar do trabalho, escola ou shopping?", null=True, blank=True)
    total_calculated = models.DecimalField(default=Decimal(0), editable=False, decimal_places=4, max_digits=8)

    def _safe_sum(self, fields):
        return sum((getattr(self, f) or Decimal('0')) for f in fields)

# Cálculo questões categoria AFO    
    def AFO(self):
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7', 'question_8']
        return self._safe_sum(fields) / Decimal('8')
        
# Cálculo questões categoria ELF
    def ELF(self):
        q9 = self.question_9 or Decimal('0')
        q9_time = self.question_9_time or Decimal('0')
        q9_prop = self.question_9_proportion or Decimal('0')
        
        q10 = self.question_10 or Decimal('0')
        q11 = self.question_11 or Decimal('0')
        q12 = self.question_12 or Decimal('0')
        
        totalELF = (
            (q9 + q9_time + q9_prop) +
            q10 + q11 + q12
        ) / Decimal('4')
        return totalELF

# Cálculo questões categoria ALL
    def ALL(self):
        q13 = self.question_13 or Decimal('0')
        q14 = self.question_14 or Decimal('0')
        q15 = self.question_15 or Decimal('0')
        q16 = self.question_16 or Decimal('0')
        
        val_q13 = (Decimal('6') - q13) if q13 > Decimal('0') else Decimal('0')
        
        totalALL = (
            val_q13 +
            q14 +
            q15 +
            q16
        ) / Decimal('4')
        return totalALL
    
    def total(self):
        return self.ALL() + self.ELF() + self.AFO()
    
    def save(self, *args, **kwargs):
        self.total_calculated = self.total()
        super(Questionnaire, self).save(*args, **kwargs)