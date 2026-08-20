import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.filieres.models import Filiere
from apps.resultats.models import UE
from apps.imports.models import ImportFichier
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from decouple import config
from django.db.models import Count

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard_validateur(request):
    total_filieres = Filiere.objects.count()
    total_ues = UE.objects.count()
    imports_attente = ImportFichier.objects.filter(statut="en_attente").count()
    imports_total = ImportFichier.objects.count()
    
    admin_path = config('ADMIN_URL_PATH', default='super-secret-admin/')
    if not admin_path.endswith('/'):
        admin_path += '/'
    django_admin_url = f"/{admin_path}django/"
    
    context = {
        'total_filieres': total_filieres,
        'total_ues': total_ues,
        'imports_attente': imports_attente,
        'imports_total': imports_total,
        'django_admin_url': django_admin_url,
    }
    return render(request, "portail_admin/dashboard_validateur.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_superadmin(request):
    admin_path = config('ADMIN_URL_PATH', default='super-secret-admin/')
    if not admin_path.endswith('/'):
        admin_path += '/'
    django_admin_url = f"/{admin_path}django/"

    users = User.objects.all()
    accounts_data = []
    for u in users:
        role = "super-admin" if u.is_superuser else "validateur" if u.is_staff else "visiteur"
        accounts_data.append({
            "id": u.id,
            "name": u.nom or u.email.split('@')[0],
            "email": u.email,
            "role": role,
            "status": "active" if u.is_active else "inactive",
            "lastLogin": u.last_login.strftime("%d %b %Y, %H:%M") if u.last_login else "Jamais"
        })

    logs = LogEntry.objects.select_related('user').order_by('-action_time')[:15]
    activity_log = []
    for log in logs:
        role = "super-admin" if log.user.is_superuser else "validateur" if log.user.is_staff else "visiteur"
        
        if log.action_flag == 1:
            action = "CRÉATION"
        elif log.action_flag == 2:
            action = "MODIFICATION"
        else:
            action = "SUPPRESSION"
            
        activity_log.append({
            "id": log.id,
            "ts": log.action_time.strftime("%d/%m %H:%M"),
            "author": log.user.nom if getattr(log.user, 'nom', None) else log.user.email.split('@')[0],
            "role": role,
            "action": action,
            "entity": f"{log.content_type.name} {log.object_repr}",
            "ip": "-" # Django LogEntry doesn't store IP by default
        })

    context = {
        "accounts": accounts_data,
        "activityLog": activity_log,
        "djangoAdminUrl": django_admin_url,
    }

    return render(request, "portail_admin/super_admin.html", context)
