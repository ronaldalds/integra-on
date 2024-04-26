from django.apps import AppConfig


class NotificacaoExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.notificacao_expenses'

    def ready(self) -> None:
        from apscheduler.schedulers.background import BackgroundScheduler
        from .integracao import NotificacaoVexpenses
        from apscheduler.triggers.cron import CronTrigger
        integracao = NotificacaoVexpenses()
        sheduler: BackgroundScheduler = BackgroundScheduler(daemon=True)
        jobs = sheduler.get_jobs()
        if jobs:
            sheduler.shutdown()
        sheduler.configure(timezone="america/fortaleza")
        trigger=CronTrigger(hour='8,13', day_of_week='mon-fri', timezone="america/fortaleza")
        sheduler.add_job(integracao.notificar, trigger=trigger)
        sheduler.start()