from django.apps import AppConfig


class OstConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.ost'

    def ready(self):
        from .integracao import Notificacao
        from apscheduler.schedulers.background import BackgroundScheduler
        sheduler = BackgroundScheduler(daemon=True)
        notificacao = Notificacao()
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(notificacao.notificacao_sla, 'interval', minutes=10)
        sheduler.add_job(notificacao.notificacao_agendamento, 'interval', minutes=15)
        sheduler.start()
