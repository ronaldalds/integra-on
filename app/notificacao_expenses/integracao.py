from utils.vexpenses.drive import Vexpenses
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from pydantic import BaseModel
from telebot import TeleBot
from .models import Notificar, UserVexpenses, LogNotificacao
from time import sleep


class NotificacaoDTO(BaseModel):
    usuario: int
    data_avulso: list[dict] = []
    data_aberto: list[dict] = []


class NotificacaoVexpenses:
    def __init__(self):
        self.vexpense = Vexpenses()

    def __lista_datas(self, data: datetime) ->  list:
        lista_datas = []
        data_inicial = data - timedelta(days=60)
        print(data_inicial)
        while data.strftime("%Y-%m-%d") >= data_inicial.strftime("%Y-%m-%d"):
            lista_datas.append(data)
            data = data - timedelta(days=1)
        return lista_datas

    def extracao_dados(self):
        datas = self.__lista_datas(datetime.now())
        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(self.vexpense.list_expenses, datas)
        expenses = list(chain.from_iterable(result))

        notificacoes: list[NotificacaoDTO] = []
        distinct_user_ids = {expense['user_id'] for expense in expenses}
        for usuario in distinct_user_ids:
            notificacao = NotificacaoDTO(usuario=usuario)
            for expense in expenses:
                if usuario == expense.get("user_id"):
                    if not expense.get("expense_id"):
                        notificacao.data_avulso.append(expense)
                    elif expense["report"]["data"] and expense["report"]["data"]["status"] == "ABERTO":
                        notificacao.data_aberto.append(expense)
            notificacoes.append(notificacao)
        return notificacoes

    def usuario_separador(self, list_user: list[UserVexpenses]):
        list_user_ids = [user.id for user in list_user]
        result = list(filter(lambda x: x.usuario in list_user_ids, self.extracao_dados()))
        return result

    def enviar_notificacao(self, expense: NotificacaoDTO, telegram: TeleBot, chat_id_send: int):
        usuario = UserVexpenses.objects.filter(id=expense.usuario).first()
        if (len(expense.data_avulso) == 0) and (len(expense.data_aberto) == 0):
            return
        msg_1 = f"🔴 🟡 🟢\n\nOlá {usuario.nome}."
        msg_2 = f"Falta prestação de conta {len(expense.data_avulso)}" if len(expense.data_avulso) != 0 else ""
        msg_3 = f"Falta enviar {len(expense.data_aberto)}" if len(expense.data_aberto) != 0 else ""
        txt_msg = f"{msg_1}\n\n\r{msg_2}\n\r{msg_3}"
        telegram.send_message(chat_id=chat_id_send, text=txt_msg)
        log_telegram = LogNotificacao()
        log_telegram.user_id = usuario
        log_telegram.grupo = chat_id_send
        log_telegram.avulso = len(expense.data_avulso)
        log_telegram.aberto = len(expense.data_aberto)
        log_telegram.save()
        sleep(5)

    def notificar(self):
        notificacao = Notificar.objects.all()
        if not notificacao:
            return
        for grupo in notificacao:
            bot_telegram = TeleBot(grupo.token_bot, parse_mode=None)
            lista_usuarios = UserVexpenses.objects.filter(
                gestor_id=grupo.gestor_id,
                ativo=True,
                operacao=grupo.operacao
            )
            expenses = self.usuario_separador(lista_usuarios)
            for expense in expenses:
                self.enviar_notificacao(expense, bot_telegram, grupo.grupo)
