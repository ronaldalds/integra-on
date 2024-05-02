from django.apps import AppConfig


class OstConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.ost'

    def ready(self):
        from .integracao import Notificacao
        from apscheduler.schedulers.background import BackgroundScheduler
        sheduler = BackgroundScheduler(daemon=True)
        notificacao_1 = Notificacao(mk=1)
        notificacao_3 = Notificacao(mk=3)
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(notificacao_1.notificacao_sla, 'interval', minutes=30)
        sheduler.add_job(notificacao_3.notificacao_sla, 'interval', minutes=30)
        sheduler.add_job(notificacao_1.notificacao_agendamento, 'interval', minutes=15)
        sheduler.add_job(notificacao_3.notificacao_agendamento, 'interval', minutes=15)
        sheduler.start()
