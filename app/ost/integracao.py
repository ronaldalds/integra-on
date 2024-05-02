import time
import telebot
from datetime import datetime
from utils.mkat.drive import Mkat
from .models import (
    UserTelegram,
    TipoOs,
    TempoSla,
    InformacaoOs,
    Log,
    TecnicoMensagem,
    ErrorOs,
    BotTelegram
)


class Notificacao:
    def __init__(self, mk: int):
        self.mk = mk
        self.mkat = Mkat()

    def informacaoes(self, tipo_os: str) -> list[InformacaoOs]:
        tipo = TipoOs.objects.filter(tipo=tipo_os).first()
        informacao = InformacaoOs.objects.filter(id_tipo_os=tipo)
        if informacao:
            return informacao
        else:
            return InformacaoOs.objects.filter(id_tipo_os=TipoOs.objects.filter(tipo="PADRAO").first().pk)

    def enviar_messagem(self, nome_bot: str, nome_chat: str, message: str):
        token = BotTelegram.objects.filter(nome=nome_bot, ativo=True).first().token
        chat_id = UserTelegram.objects.filter(nome=nome_chat, mk=self.mk).first().chat_id
        bot_telegram = telebot.TeleBot(token, parse_mode=None)
        bot_telegram.send_message(chat_id=chat_id, text=message)

    def notificacao_agendamento(self) -> None:
        agendamentos = self.mkat.agenda_os(mk=self.mk)
        for agenda in agendamentos:
            ordem_servico: dict = agenda.get("os", {})
            encerrado: bool = ordem_servico.get("encerrado", False)
            operador: str = ordem_servico.get("operador_abertura", "Sem Operador")
            if not encerrado and (operador != "bot.sistemas"):
                self.verificar_os(ordem_servico)

    def verificar_os(self, ordem_servico: dict) -> None:
        motivo: str = ordem_servico.get("motivo", "")
        tipo_os: dict = ordem_servico.get("tipo_os", {})
        descricao_tipo_os: str = tipo_os.get("descricao", "PADRAO")
        informacoes_os = self.informacaoes(descricao_tipo_os)
        detalhes = []
        for detalhe in informacoes_os:
            if detalhe.nome.replace(":", "") not in motivo:
                detalhes.append(detalhe.nome)

        if not detalhes: return
        cod = ordem_servico.get('cod')
        operador_abertura = ordem_servico.get('operador_abertura', '')
        msg_os = f"OS {cod} - {descricao_tipo_os}."
        msg_operador = f"Operador {operador_abertura}."
        msg_detalhe = f"Falta detalhe {detalhes} no motivo da O.S."
        msg = f"🔴 🟡 🟢\n\n{msg_os}\n{msg_operador}\n{msg_detalhe}"
        if not ErrorOs.objects.filter(os=ordem_servico.get('cod')).exists():
            error = ErrorOs(
                os=ordem_servico.get('cod', ''),
                tipo=descricao_tipo_os,
                operador=ordem_servico.get('operador_abertura', ''),
                detalhe=msg
            )
            error.save()
        self.enviar_messagem(
            nome_bot="TELEGRAM_OST",
            nome_chat=f"GRUPO_NOTIFICACAO_OST",
            message=msg
        )
        time.sleep(7)

    def sla_os(self, Tipo_OS) -> int | None:
        tipo = TipoOs.objects.filter(tipo=Tipo_OS, ativo=True).first()
        if tipo:
            return tipo.sla
        else:
            return None

    def tempo_de_aviso(self) -> list:
        tempo_aviso = TempoSla.objects.all()
        return sorted([x.sla for x in tempo_aviso], reverse=True)

    def notificar(
        self,
        Cod_OS,
        ID_Tecnico,
        Tempo_Aviso,
        Nome_Tecnico: str,
        Tipo_OS,
        data_abertura: datetime,
    ) -> None:
        mensagens = TecnicoMensagem.objects.filter(
            nome_tecnico=Nome_Tecnico,
            cod_os=Cod_OS,
            chat_id=ID_Tecnico,
            sla=Tempo_Aviso,
            envio=True
        )
        horario = data_abertura.strftime("%d/%m/%Y %H:%M")
        Nome_Tecnico_Formatado = Nome_Tecnico.replace('.', ' ').title()
        msg_1 = f"🔴 🟡 🟢\n\nOlá {Nome_Tecnico_Formatado}."
        msg_2 = f"Falta menos de {Tempo_Aviso} "
        msg_3 = "horas para a seguinte O.S. expirar."
        msg_4 = f"Cód O.S. : {Cod_OS}"
        msg_5 = f"Tipo O.S : {Tipo_OS}"
        msg_6 = f"Data Abertura : {horario}"
        msg = f"{msg_1}\n\n\r{msg_2}{msg_3}\n\n\r{msg_4}\n{msg_5}\n{msg_6}"
        if not mensagens.exists():
            print(msg)
            tm = TecnicoMensagem(
                nome_tecnico=Nome_Tecnico,
                chat_id=ID_Tecnico,
                mensagem=msg,
                sla=Tempo_Aviso,
                cod_os=Cod_OS,
            )
            try:
                self.enviar_messagem(nome_bot="TELEGRAM_OST", nome_chat=Nome_Tecnico, message=msg)
                tm.envio = True
                tm.save()
            except Exception:
                self.enviar_messagem(nome_bot="TELEGRAM_OST", nome_chat="ADMINISTRADOR", message=msg)
                tm.envio = False
                tm.save()
            time.sleep(7)

    def diferenca_hora(self, data_abertura: datetime):
        agora = datetime.now()
        diferenca = agora - data_abertura
        return diferenca.total_seconds() / 3600

    def notificacao_sla(self):
        print('Rodando : ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        lista_tecnicos = UserTelegram.objects.filter(ativo=True, mk=self.mk)
        for tecnico in lista_tecnicos:
            print(f"id: {tecnico.chat_id} Nome: {tecnico.nome}")
            agenda_tecnico = self.mkat.agenda_tecnico(tecnico=tecnico.nome, mk=self.mk)
            tempo_aviso = self.tempo_de_aviso()
            for agenda in agenda_tecnico:
                data_obj = datetime.strptime(agenda['os']['data_abertura'], "%Y-%m-%dT%H:%M:%S.%fZ")
                hora_obj = datetime.strptime(agenda['os']['hora_abertura'].split(".")[0], "%H:%M:%S")
                horario_abertura = data_obj.replace(
                    hour=hora_obj.hour,
                    minute=hora_obj.minute,
                    second=hora_obj.second,
                    microsecond=hora_obj.microsecond
                )
                encerrado = agenda['os']['encerrado']
                cod_os = agenda['codos']
                tipo_os = agenda['os']['tipo_os']['descricao']
                hora_passada = self.diferenca_hora(horario_abertura)
                sla_max = self.sla_os(tipo_os)

                if encerrado: continue
                if not sla_max: continue
                for aviso in tempo_aviso:
                    sla_1 = (sla_max - hora_passada) >= 0
                    sla_2 = (sla_max - hora_passada) <= aviso
                    if sla_1 and sla_2:
                        self.notificar(cod_os, tecnico.chat_id, aviso, tecnico.nome, tipo_os, horario_abertura)
                        Log.objects.create()
