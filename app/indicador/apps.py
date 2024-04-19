from django.apps import AppConfig


class IndicadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.indicador'

    def ready(self) -> None:
        from apscheduler.schedulers.background import BackgroundScheduler
        from .carga import CargaIndicadores
        carga = CargaIndicadores()
        sheduler: BackgroundScheduler = BackgroundScheduler(daemon=True)
        jobs = sheduler.get_jobs()
        if jobs:
            sheduler.shutdown()
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(carga.atualizar, 'interval', minutes=0.35)
        sheduler.add_job(carga.carga_chamado_faltante, 'interval', minutes=60)
        sheduler.add_job(carga.carga_interacao, 'interval', minutes=0.5)

        sheduler.start()
