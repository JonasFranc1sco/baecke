from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import ParticipantForm, QuestionnaireForm
from .models import Questionnaire, Participant, Question, Choice, Answer
from django.contrib import messages
from django.db.models import Avg, Count
import json
import hashlib
# Create your views here.

def personalView(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            email_raw = form.cleaned_data['email']
            email_normalized = email_raw.strip().lower()
            hash_obj = hashlib.sha256(email_normalized.encode('utf-8'))
            hash_hex = hash_obj.hexdigest()
            participant, created = Participant.objects.get_or_create(hash_identify=hash_hex)
            
            data_save = form.cleaned_data
            del data_save['email']
            
            question_obj, created = Questionnaire.objects.update_or_create(
                participant=participant,
                defaults=data_save
            )
            messages.success(request, 'Informações básicas salvas com sucesso!')
            return redirect('questionnaire-view-uuid', uuid=question_obj.uuid)
        else:
            messages.error(request, 'Erro ao salvar informações. Verifique os campos abaixo.')
    else:
        form = ParticipantForm()
    return render(request, 'personal_fields.html', {'form': form})

def questionnaireView(request, uuid=None):
    if uuid is None:
        return redirect('personal')
    questionnaire = get_object_or_404(Questionnaire, uuid=uuid)
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                questionnaire.answers.all().delete()
                
                questions = Question.objects.select_related("choice_set").filter(code__in=form.cleaned_data.keys())
                
                questions_by_code = {
                    question.code: question
                    for question in questions
                }
                
                for code, selected_value in form.cleaned_data.items():
                    if selected_value == "":
                        continue
                    
                    question = questions_by_code[code]
                    choice = Choice.objects.get(choice_set=question.choice_set, code=selected_value,)
                    
                    Answer.objects.create(
                        questionnaire=questionnaire,
                        question=question,
                        choice=choice,
                    )
                    
            questionnaire.total_calculated = questionnaire.total()
            questionnaire.save(update_fields=["total_calculated"])
            messages.success(request, 'Questionário enviado com sucesso!')
            return redirect('result', uuid=questionnaire.uuid)
        messages.error(request, 'Erro ao enviar o questionário. Verifique se todas as perguntas foram respondidas.')
    else:
        form = QuestionnaireForm()
    return render(request, 'questionnaire_fields.html', {'form': form})

def resultView(request, uuid):
    questionnaire = get_object_or_404(Questionnaire, uuid=uuid)
    total = questionnaire.total_calculated if questionnaire.total_calculated else questionnaire.total()
    afo = questionnaire.calculate_afo()
    elf = questionnaire.calculate_elf()
    all_score = questionnaire.calculate_all()
    context = {
        'questionnaire': questionnaire,
        'total': total,
        'afo': afo,
        'elf': elf,
        'all_score': all_score,
    }
    return render(request, "result_page.html", context)

def homeView(request):
    return render(request, "home_page.html")

def aboutView(request):
    return render(request, "about_page.html")

def chartsView(request):
    total_media = Questionnaire.objects.aggregate(media=Avg('total_calculated'))['media']
    total_media = float(total_media) if total_media else 0.0
    
    sex_data = Questionnaire.objects.values('sex').annotate(total=Count('sex'))
    labels_sex = [item['sex'] for item in sex_data]
    values_sex = [item['total'] for item in sex_data]

    context = {
        'media_total_json': json.dumps(total_media),        
        'labels_sex_json': json.dumps(labels_sex),
        'values_sex_json': json.dumps(values_sex),
        'total_answers': Questionnaire.objects.count()
    }
    
    return render(request, "charts_page.html", context)