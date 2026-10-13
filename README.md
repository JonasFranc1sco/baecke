# Baecke Saúde

> **Plataforma web para avaliação epidemiológica e cálculo automatizado do Questionário de Atividade Física Habitual de Baecke.**

O **Baecke Saúde** é uma aplicação completa desenvolvida em **Django** que digitaliza e automatiza a aplicação do *Questionário de Atividade Física Habitual* formulado originalmente por **Baecke, Burema e Frijters (1982)** e adaptado e validado transculturalmente para a população brasileira no estudo de referência de **Florindo et al. (2004)** (documentado detalhadamente em [`reference.md`](reference.md)), além das contribuições de **Guedes et al. (2005)**.

A aplicação fornece um fluxo intuitivo para participantes responderem às questões com busca rápida em centenas de ocupações e modalidades esportivas, calcula com precisão científica os três índices de movimento dos últimos 12 meses, garante a privacidade dos participantes através de anonimização criptográfica (SHA-256) e disponibiliza gráficos coletivos com métricas epidemiológicas.

---

## Sumário

- [Visão Geral e Embasamento Científico](#-visão-geral-e-embasamento-científico)
- [Documento de Referência Base (Florindo et al., 2004)](#-documento-de-referência-base-florindo-et-al-2004)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Linha de Execução e Fluxo de Dados](#-linha-de-execução-e-fluxo-de-dados)
- [Metodologia e Fórmulas de Cálculo Detalhadas](#-metodologia-e-fórmulas-de-cálculo-detalhadas)
- [Rotas da Aplicação (Endpoints)](#-rotas-da-aplicação-endpoints)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Rodar o Projeto](#-como-rodar-o-projeto)
- [Comandos de Seed e População do Banco](#-comandos-de-seed-e-população-do-banco)
- [Referências Bibliográficas](#-referências-bibliográficas)

---

## Visão Geral e Embasamento Científico

O Questionário de Baecke investiga a atividade física habitual realizada nos últimos 12 meses através de **três domínios independentes**:

1. **Índice de Atividade Física Ocupacional (AFO / IT):** Mede as demandas físicas da rotina laboral (tempo sentado, em pé, caminhada, transporte de cargas, fadiga após o trabalho, suor e esforço comparativo).
2. **Índice de Exercício Físico no Lazer (ELF / IE):** Mede a prática sistemática de modalidades esportivas e exercícios programados, ponderando a intensidade metabólica do esporte (METs), horas semanais e meses por ano.
3. **Índice de Atividade Física de Lazer e Locomoção (ALL / IL):** Mede a movimentação nas horas vagas e deslocamento ativo (assistir TV de forma sedentária, caminhada de lazer, andar de bicicleta e tempo diário de transporte ativo a pé/bicicleta).

A soma desses três índices resulta no **Escore Global de Baecke**, variando de **3,00 (mínimo)** a **15,00 (máximo)**.

---

## Documento de Referência Base (Florindo et al., 2004)

Este projeto baseia-se diretamente no artigo científico contido em [`reference.md`](reference.md):

> **FLORINDO, Alex Antonio et al.** *Metodologia para a avaliação da atividade física habitual em homens com 50 anos ou mais*. Revista de Saúde Pública / Faculdade de Saúde Pública da USP & Hospital Heliópolis, v. 38, n. 4, p. 578-586, 2004.

### 1. Processo de Tradução e Adaptação Transcultural
- **Autorização Prévia:** Permissão concedida formalmente pelos autores originais (Baecke et al., 1982).
- **Tradução e Consenso:** Dupla tradução independente do inglês para o português por pesquisadores experientes, com versão de consenso.
- **Back-Translation:** Retrotradução realizada por dois professores nativos anglófonos (Estados Unidos e Inglaterra).
- **Adaptações Verbais:** Ajustes linguísticos e culturais nas questões 1, 6, 8 e 9, apresentados e validados com os autores holandeses.

### 2. Validação e Propriedades Psicométricas no Brasil
- **Reprodutibilidade:** Teste-reteste em intervalo de 45 dias com coeficientes de correlação intraclasse **superiores a 0,69**, demonstrando alta consistência temporal.
- **Validade Concorrente:** Correlações estatisticamente significativas com índices fisiológicos e percentagem de decréscimo da frequência cardíaca.
- **Consistência Interna ($\alpha$ de Cronbach):**
  - Escore AFO: $\alpha = 0,52$
  - Escore EFL: $\alpha = 0,52$ (com destaque para o tipo de exercício físico na $Q_9$, com $\alpha = 0,85$)
  - Escore ALL: $\alpha = 0,62$
- **Correlação dos Domínios com o Escore Total (ET):**
  - ALL $\leftrightarrow$ ET: $r = 0,78$ ($r_{ajustado} = 0,77$)
  - AFO $\leftrightarrow$ ET: $r = 0,70$ ($r_{ajustado} = 0,67$)
  - EFL $\leftrightarrow$ ET: $r = 0,60$ ($r_{ajustado} = 0,67$)
  *(Correlações parciais mantidas mesmo após ajuste por idade, escolaridade e Índice de Massa Corporal - IMC).*
- **Aplicabilidade Prática:** Tempo de resposta ágil (entre **5 e 10 minutos**), com excelente compreensão por indivíduos de diferentes níveis de escolaridade através da escala Likert (1 a 5).

---

## Funcionalidades Principais

- **Privacidade por Design (LGPD):** O e-mail do participante é normalizado e convertido em um hash **SHA-256**, garantindo total anonimização dos dados biométricos e respostas no banco.
- **Formulário em 2 Etapas com Indicador de Progresso:**
  1. *Identificação e Biometria:* E-mail, sexo, idade, altura e peso.
  2. *Questionário Dinâmico:* 16 perguntas principais com subquestões condicionais para esportes.
- **Questões e Alternativas Dinâmicas no Banco:** Modelos `Question`, `ChoiceSet` e `Choice` desacoplados, permitindo fácil manutenção sem alterar schemas do banco.
- **Busca Rápida com Select2:** Facilita a localização entre centenas de profissões cadastradas (Q1) e atividades físicas (Q9).
- **Campos Condicionais Inteligentes:** JavaScript (`hidden.js`) exibe ou oculta campos de esportes complementares automaticamente com base na resposta sim/não.
- **Cálculo Preciso com `Decimal`:** Evita imprecisões de ponto flutuante durante as divisões e ponderações de METs.
- **Relatório de Resultados Visual:**
  - Gráfico em medidor circular animado (SVG Gauge).
  - Classificação categórica imediata (*Levemente Ativo / Sedentário*, *Moderadamente Ativo*, *Altamente Ativo*).
  - Barras segmentadas para cada um dos 3 índices (1,00 a 5,00).
- **Dashboard Epidemiológico:** Painel com estatísticas coletivas anonimizadas utilizando **Chart.js** (média geral do escore e distribuição por sexo).
- **Painel Administrativo Completo:** Django Admin configurado com filtros, inlines e visualizações otimizadas para monitoramento dos dados.

---

## Estrutura do Projeto

```text
baecke/
│
├── config/                         # Configurações globais do Django
│   ├── __init__.py
│   ├── asgi.py                     # Ponto de entrada ASGI
│   ├── settings.py                 # Definições do projeto, apps instalados, DB e Tailwind
│   ├── urls.py                     # Mapeamento central de rotas/URLs
│   └── wsgi.py                     # Ponto de entrada WSGI
│
├── questionnaire/                  # Aplicação principal (Questionário Baecke)
│   ├── admin.py                    # Customizações do Django Admin
│   ├── apps.py                     # Configuração da app questionnaire
│   ├── choices.py                  # Dicionários de alternativas, ocupações e esportes (METs)
│   ├── forms.py                    # ParticipantForm e QuestionnaireForm dinâmico
│   ├── models.py                   # Modelos: Participant, ChoiceSet, Choice, Question, Questionnaire, Answer
│   ├── views.py                    # Lógica das views (home, personal, questionnaire, result, charts, about)
│   ├── migrations/                 # Migrações do banco de dados
│   │   └── 0001_initial.py
│   ├── management/
│   │   └── commands/               # Comandos customizados do manage.py
│   │       ├── seed_choices.py     # Popula os ChoiceSets e Choices no banco
│   │       └── seed_questions.py   # Popula as Question dinâmicas no banco
│   ├── static/                     # Arquivos estáticos da aplicação
│   │   ├── css/                    # Estilos complementares (forms, home, result, style)
│   │   ├── js/
│   │   │   ├── charts.js           # Renderização dos gráficos com Chart.js
│   │   │   ├── hidden.js           # Controle de visibilidade das perguntas condicionais de esporte
│   │   │   └── select2-init.js     # Inicialização dos campos com Select2
│   │   └── img/                    # Imagens e ilustrações vetoriais (SVG)
│   ├── templates/                  # Templates HTML em Django Template Language
│   │   ├── base.html               # Layout base com Tailwind, navbar e mensagens
│   │   ├── home_page.html          # Página inicial de apresentação
│   │   ├── personal_fields.html    # Etapa 1: Dados biométricos e e-mail
│   │   ├── questionnaire_fields.html # Etapa 2: Perguntas do Questionário Baecke
│   │   ├── result_page.html        # Página de exibição do resultado e índices
│   │   ├── charts_page.html        # Página de gráficos epidemiológicos
│   │   └── about_page.html         # Fundamentação teórica e referências ABNT
│   └── templatetags/
│       └── form_extras.py          # Filtros customizados para templates
│
├── theme/                          # App django-tailwind com o tema visual
│   ├── apps.py
│   ├── static/
│   │   └── css/dist/styles.css     # CSS compilado do Tailwind pronto para uso
│   ├── static_src/                 # Código fonte e configuração do Tailwind / PostCSS
│   │   ├── package.json
│   │   ├── tailwind.config.js
│   │   └── src/styles.css
│   └── templates/
│       └── base.html
│
├── reference.md                    # Artigo científico na íntegra de referência (Florindo et al., 2004)
├── db.sqlite3                      # Banco de dados SQLite local
├── manage.py                       # Utilitário CLI do Django
└── requirements.txt                # Dependências Python do projeto
```

---

## Linha de Execução e Fluxo de Dados

1. **Acesso à Página Inicial (`homeView`):** O usuário conhece o questionário e clica em *Iniciar Avaliação*.
2. **Dados Pessoais (`personalView`):** Informa e-mail, sexo, idade, peso e altura. O e-mail é convertido em SHA-256 e o participante é salvo gerando um `UUID` único.
3. **Questionário (`questionnaireView`):** O sistema recupera as 16 perguntas do banco de dados ordenadas. `select2` permite selecionar a ocupação e esportes entre centenas de opções.
4. **Processamento e Persistência:**
   - Em transação atômica (`transaction.atomic`), as respostas anteriores daquele questionário são renovadas pelas novas instâncias de `Answer`.
   - O método `total()` executa os cálculos aritméticos das três dimensões conforme a Tabela 1 de [`reference.md`](reference.md).
   - O resultado final é persistido em `total_calculated`.
5. **Apresentação do Resultado (`resultView`):** Mostra o escore total e o detalhamento de cada índice com orientações de atividade física.

---

## Metodologia e Fórmulas de Cálculo Detalhadas

As fórmulas e critérios adotados na aplicação seguem rigorosamente a **Tabela 1** do estudo de Florindo et al. (2004) descrita em [`reference.md`](reference.md):

### 1. Índice de Atividade Física Ocupacional (AFO)

$$AFO = \frac{Q_1 + (6 - Q_2) + Q_3 + Q_4 + Q_5 + Q_6 + Q_7 + Q_8}{8}$$

- **$Q_1$ (Tipo de Ocupação):** Classificada segundo o Compêndio de Atividades Físicas de Ainsworth:
  - *Gasto leve:* valor **1,0**
  - *Gasto moderado:* valor **3,0**
  - *Gasto vigoroso:* valor **5,0**
  - *Casos especiais documentados:* Para aposentados ou licenciados sem 2ª ocupação regular, adota-se o escore padrão **1,000**. Para atividades domésticas, adota-se o nível moderado (**3,0**).
- **$Q_2$ (Ficar sentado):** Possui pontuação invertida ($6 - Q_2$), pois sentar é indicador de inatividade física (no estudo de validação, apresentou forte correlação inversa com o escore: $r = -0,72$).
- **$Q_3$ a $Q_8$:** Respostas em escala de Likert de 1 a 5 (ficar em pé, andar, carregar peso, cansaço após o trabalho, suor e trabalho fisicamente pesado comparado a pares).

---

### 2. Índice de Exercício Físico no Lazer (ELF)

$$ELF = \frac{Q_9 + Q_{10} + Q_{11} + Q_{12}}{4}$$

#### Cálculo Específico da Questão 9 ($Q_9$):
Avalia a prática regular de até **duas modalidades esportivas** baseada na tríade da fisiologia do exercício (intensidade, tempo e frequência):

$$Modalidade = Intensidade \times Tempo \times Propor\text{ç}\tilde{a}o$$

- **Intensidade metabólica (Compêndio de Ainsworth):**
  - *Leve:* **0,76**
  - *Moderada:* **1,26**
  - *Vigorosa:* **1,76**
- **Tempo (Horas por semana):**
  - $< 1$ h/semana: **0,5**
  - Entre $1$ e $< 2$ h/semana: **1,5**
  - Entre $2$ e $< 3$ h/semana: **2,5**
  - Entre $3$ e $\le 4$ h/semana: **3,5**
  - $> 4$ h/semana: **4,5**
- **Proporção (Meses por ano):**
  - $< 1$ mês/ano: **0,04**
  - De $1$ a $3$ meses/ano: **0,17**
  - De $4$ a $6$ meses/ano: **0,42**
  - De $7$ a $9$ meses/ano: **0,67**
  - $> 9$ meses/ano: **0,92**

#### Total da Questão 9:
$$Total_{Q9} = Modalidade_1 + Modalidade_2$$

Conversão do valor final para escore de 1 a 5:
- **Sem exercício físico** ou $Total_{Q9} = 0 \implies Q_9 = \mathbf{1}$
- Entre $0,01$ e $< 4,00 \implies Q_9 = \mathbf{2}$
- Entre $4,00$ e $< 8,00 \implies Q_9 = \mathbf{3}$
- Entre $8,00$ e $< 12,00 \implies Q_9 = \mathbf{4}$
- $\ge 12,00 \implies Q_9 = \mathbf{5}$

As questões $Q_{10}$ a $Q_{12}$ seguem a escala Likert de 1 a 5 (comparação física com pessoas da mesma idade, suor nas horas de lazer e frequência geral de exercícios).

---

### 3. Índice de Atividades de Lazer e Locomoção (ALL)

$$ALL = \frac{(6 - Q_{13}) + Q_{14} + Q_{15} + Q_{16}}{4}$$

- **$Q_{13}$ (Assistir televisão):** Pontuação invertida ($6 - Q_{13}$), representando comportamento sedentário de tela (apresentou forte correlação inversa com o escore: $r = -0,88$).
- **$Q_{14}$ e $Q_{15}$:** Caminhada e ciclismo nas horas de lazer (escala de 1 a 5).
- **$Q_{16}$ (Transporte ativo diário):** Minutos por dia caminhando ou pedalando para ir e voltar do trabalho, escola ou compras:
  - $< 5$ min/dia: 1
  - $5$ a $15$ min/dia: 2
  - $15$ a $30$ min/dia: 3
  - $30$ a $45$ min/dia: 4
  - $> 45$ min/dia: 5

---

### 4. Escore Total de Baecke (ET)

$$Escore\,Total = AFO + ELF + ALL \quad (3,00 \text{ a } 15,00)$$

**Classificação do Perfil do Participante:**
- $\ge 9,00$: **Altamente Ativo**
- $\ge 6,00$ e $< 9,00$: **Moderadamente Ativo**
- $< 6,00$: **Levemente Ativo / Sedentário**

---

## Rotas da Aplicação (Endpoints)

| Rota | View | Nome da URL | Descrição |
|---|---|---|---|
| `/` | `homeView` | `home` | Página inicial com apresentação e chamada para ação |
| `/baecke/info/` | `personalView` | `personal` | Formulário de identificação anônima e biometria |
| `/baecke/questionnaire/` | `questionnaireView` | `questionnaire-view` | Redireciona para preenchimento de dados pessoais |
| `/baecke/questionnaire/<uuid>/` | `questionnaireView` | `questionnaire-view-uuid` | Formulário dinâmico com as questões de Baecke |
| `/baecke/result/<uuid>/` | `resultView` | `result` | Painel de resultado com escore total e índices parciais |
| `/baecke/graficos/` | `chartsView` | `charts` | Dashboard epidemiológico com dados consolidados |
| `/baecke/sobre/` | `aboutView` | `about` | Página explicativa, metodologia e referências científicas |
| `/admin/` | `admin.site.urls` | `admin` | Painel administrativo do Django |

---

## Tecnologias Utilizadas

- **Linguagem & Backend:** [Python 3.10+](https://www.python.org/) & [Django](https://www.djangoproject.com/)
- **Estilização & UI:** [Tailwind CSS](https://tailwindcss.com/) integrado via [django-tailwind](https://django-tailwind.readthedocs.io/)
- **Ícones & Tipografia:** [Google Fonts (Inter)](https://fonts.google.com/specimen/Inter) e [Material Symbols Outlined](https://fonts.google.com/icons)
- **Componentes Interativos:**
  - [Select2](https://select2.org/) para busca e seleção rápida de ocupações e esportes
  - [Chart.js](https://www.chartjs.org/) para visualização gráfica das métricas epidemiológicas
  - [jQuery](https://jquery.com/) para manipulação dinâmica da visibilidade dos campos
  - [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) para customização de inputs
- **Banco de Dados:** SQLite (padrão de desenvolvimento)

---

## Como Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/JonasFranc1sco/baecke.git
cd baecke
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
# Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

# Windows:
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Aplicar as Migrações do Banco de Dados
```bash
python manage.py migrate
```

### 5. Popular o Banco de Dados (Seeds Obrigatórios)
O projeto depende dos conjuntos de escolhas e perguntas populados no banco:
```bash
# 1º: Popula os ChoiceSets e as Choices (opções, profissões e esportes)
python manage.py seed_choices

# 2º: Popula as Perguntas dinâmicas associando aos ChoiceSets
python manage.py seed_questions
```

### 6. Criar um Superusuário (Opcional, para acessar o Admin)
```bash
python manage.py createsuperuser
```

### 7. (Opcional) Compilar o Tailwind CSS
O projeto já conta com o arquivo `theme/static/css/dist/styles.css` pré-compilado e pronto para execução. Caso queira modificar as classes do Tailwind:
```bash
python manage.py tailwind install
python manage.py tailwind start
```

### 8. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Acesse no navegador: **[http://localhost:8000](http://localhost:8000)**

---

## Referências Bibliográficas

- **FLORINDO, A. A.; LATORRE, M. R. D. O.; JAIME, P. C.; TANAKA, T.; ZERBINI, C. A. F.** Metodologia para a avaliação da atividade física habitual em homens com 50 anos ou mais. *Revista de Saúde Pública*, São Paulo, v. 38, n. 4, p. 578-586, 2004. Disponível no projeto em [`reference.md`](reference.md).
- **BAECKE, J. A.; BUREMA, J.; FRIJTERS, J. E.** A short questionnaire for the measurement of habitual physical activity in epidemiological studies. *The American Journal of Clinical Nutrition*, v. 36, n. 5, p. 936-942, 1982.
- **AINSWORTH, B. E. et al.** Compendium of physical activities: an update of activity codes and MET intensities. *Medicine & Science in Sports & Exercise*, v. 32, n. 9, p. S498-S504, 2000.
- **GUEDES, D. P.; LOPES, C. C.; GUEDES, J. E. R. P.** Reprodutibilidade e validade do Questionário Habitual de Atividade Física de Baecke. *Revista Brasileira de Medicina do Esporte*, v. 11, n. 2, p. 151-158, 2005.

---

Desenvolvido para apoio à pesquisa epidemiológica e promoção da saúde física e bem-estar.
