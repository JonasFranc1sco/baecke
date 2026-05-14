# Relatório de Erro: Attribute "fields" is unknown em questionnaire/forms.py

## Descrição do Erro
O erro `Cannot access attribute "fields" for class "CleanRadioSelectMixin*". Attribute "fields" is unknown` ocorre porque a classe `CleanRadioSelectMixin` tenta acessar o atributo `self.fields` em seu método `__init__`, mas a classe não herda de nenhuma classe que possua esse atributo (como `forms.Form` ou `forms.ModelForm`).

Isso impede que ferramentas de análise estática (como Pyright, Pylance ou MyPy) confirmem que o atributo `fields` existirá em tempo de execução.

## Causa Raiz
No código atual:
```python
class CleanRadioSelectMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ...
        for name in ['question_9_boolean', 'question_9_other_boolean']:
            if name in self.fields:  # O analisador não sabe o que é self.fields
                # ...
```
Embora a mixin seja usada em classes que herdam de `forms.ModelForm` (que possui `fields`), a definição da mixin em si é isolada.

## Solução Proposta
A maneira mais simples e limpa de resolver isso, mantendo a compatibilidade com ferramentas de análise estática, é declarar o atributo `fields` na própria mixin ou usar anotações de tipo.

### Opção 1: Declaração de Atributo (Recomendada)
Adicionar a declaração do atributo com um tipo genérico ou específico para informar ao analisador:

```python
from django import forms

class CleanRadioSelectMixin:
    fields: dict[str, forms.Field]  # Informa ao analisador que 'fields' existe

    def __init__(self, *args, **kwargs):
        # ...
```

### Opção 2: Herança de BaseForm para Verificação de Tipo
Usar `typing.TYPE_CHECKING` para simular a herança durante a análise estática sem afetar o comportamento em tempo de execução:

```python
from typing import TYPE_CHECKING
from django import forms

if TYPE_CHECKING:
    _Base = forms.BaseForm
else:
    _Base = object

class CleanRadioSelectMixin(_Base):
    def __init__(self, *args, **kwargs):
        # ...
```

## Correção Aplicada
A correção recomendada é a **Opção 1**, por ser mais direta e legível. 

O arquivo `questionnaire/forms.py` deve ser atualizado para incluir a definição de tipo para `fields`.

## Erro de Operação: Decimal vs Float em questionnaire/models.py

### Descrição do Erro
O erro `TypeError: unsupported operand type(s) for +: 'float' and 'decimal.Decimal'` ocorria no método `total()` da classe `Question`. 

Em Python, não é permitido realizar operações aritméticas diretas entre objetos do tipo `float` e `decimal.Decimal` para evitar perdas de precisão implícitas.

### Causa Raiz
No método original:
```python
def total(self):
    return float(self.ALL()) + float(self.ELF()) + self.AFO()
```
Os métodos `ALL()` e `ELF()` eram convertidos para `float`, enquanto `AFO()` retornava um `Decimal` (resultado da divisão de uma soma de `Decimal` por um inteiro). A tentativa de somar `float + Decimal` causava a falha.

Além disso, o uso de `/ 8` ou `/ 4` com inteiros em Python 3 pode retornar um `float` se o operando não for explicitamente um `Decimal`.

### Solução Aplicada
A melhor forma de armazenar e calcular valores financeiros ou científicos no Django é utilizando o tipo `Decimal` em toda a cadeia de cálculo.

1.  **Padronização para Decimal**: Todos os valores padrão (`0`) foram substituídos por `Decimal('0')`.
2.  **Divisões Precisas**: As divisões agora utilizam divisores do tipo `Decimal` (ex: `Decimal('8')`), garantindo que o resultado permaneça como `Decimal`.
3.  **Remoção de Casts**: Os casts para `float()` foram removidos, mantendo a precisão total do cálculo até o salvamento no banco de dados.

O código foi atualizado para:
```python
def total(self):
    return self.ALL() + self.ELF() + self.AFO()
```
Isso garante que `total()` retorne um `Decimal`, que é perfeitamente compatível com o campo `total_calculated = models.DecimalField(...)`.

## Investigação: Campos não obrigatórios no QuestionnaireForm

### Problema
Os campos no `questionnaire_fields.html` (como `question_1` a `question_16`) não estão sendo renderizados com o atributo HTML `required` e permitem o envio do formulário sem seleção, mesmo quando deveriam ser obrigatórios.

### Causa Raiz
1.  **Definição no Model (`models.py`)**: A maioria dos campos de questões no modelo `Questionnaire` foi definida com `blank=True` e `null=True`. No Django, `blank=True` faz com que o `ModelForm` defina automaticamente o campo como `required=False`.
    ```python
    # Exemplo no models.py
    question_1 = DecimalField(..., null=True, blank=True)
    ```
2.  **Lógica do Template (`questionnaire_fields.html`)**: O template verifica explicitamente se o campo é obrigatório antes de adicionar o atributo `required`:
    ```html
    {% if field.field.required %}
        {% render_field field class="form-control" required="required" %}
    {% else %}
        {% render_field field class="form-control" %}
    {% endif %}
    ```
    Como o formulário considera os campos opcionais devido ao modelo, o atributo HTML não é inserido.

### Como Resolver
Existem duas abordagens possíveis:

1.  **Alteração no Model (Recomendado se os dados devem ser sempre obrigatórios no banco)**:
    Remover `blank=True` e `null=True` dos campos que devem ser obrigatórios no arquivo `questionnaire/models.py`.
    ```python
    question_1 = DecimalField(choices=QUESTION_1_VALUES, verbose_name="...", null=False, blank=False)
    ```

2.  **Alteração no Form (Se a obrigatoriedade for apenas na interface)**:
    Forçar o atributo `required=True` para os campos desejados no método `__init__` do `QuestionnaireForm` em `questionnaire/forms.py`.
    ```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exemplo para forçar obrigatoriedade em todos os campos
        for field_name, field in self.fields.items():
            field.required = True
    ```


