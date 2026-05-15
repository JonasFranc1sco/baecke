from django.shortcuts import render, redirect, get_object_or_404
from .forms import ParticipantForm, QuestionnaireForm
from .models import Questionnaire, Participant
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
    question_obj = get_object_or_404(Questionnaire, uuid=uuid)
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=question_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Questionário enviado com sucesso!')
            return redirect('result', uuid=question_obj.uuid)
        else:
            messages.error(request, 'Erro ao enviar o questionário. Verifique se todas as perguntas foram respondidas.')
    else:
        form = QuestionnaireForm(instance=question_obj)
    return render(request, 'questionnaire_fields.html', {'form': form})

def resultView(request, uuid):
    question = get_object_or_404(Questionnaire, uuid=uuid)
    total = question.total()
    return render(request, "result_page.html", {'total': total})

def homeView(request):
    return render(request, "home_page.html")

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