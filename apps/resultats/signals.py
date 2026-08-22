from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django_q.tasks import async_task
from django.conf import settings
from .models import UE

def envoyer_notification_publication(ue_id):
    ue = UE.objects.select_related('session__semestre__filiere').get(id=ue_id)
    # Récupérer les étudiants liés à cette UE via les résultats
    etudiants = ue.resultats.select_related('etudiant').all()
    emails = [res.etudiant.email for res in etudiants if res.etudiant.email]
    
    if not emails:
        return

    sujet = f"ENA - Publication des résultats pour {ue.code} ({ue.nom})"
    message = (
        f"Bonjour,\n\n"
        f"Les résultats de l'UE {ue.code} - {ue.nom} viennent d'être publiés officiellement.\n"
        f"Vous pouvez consulter votre procès-verbal sur la plateforme de résultats de l'ENA.\n\n"
        f"Cordialement,\n"
        f"La Direction de l'ENA"
    )

    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=True,
    )


@receiver(pre_save, sender=UE)
def ue_pre_save_notification(sender, instance, **kwargs):
    if instance.pk:
        # Check if statut changed to 'publie'
        old_instance = UE.objects.get(pk=instance.pk)
        if old_instance.statut != 'publie' and instance.statut == 'publie':
            # Run in background via django-q
            async_task('apps.resultats.signals.envoyer_notification_publication', instance.pk)
