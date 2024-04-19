from utils.desk.drive import Desk
from django.db.models import Max, Count, F
from .models import Chamado, Interacao
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class CargaIndicadores:
    def __init__(self):
        self.desk = Desk()

    def atualizar(self):
        novo = self.desk.total_chamados()
        atual = Chamado.objects.aggregate(Max('chave'))['chave__max']
        print(f"[{datetime.now()}] Atualizando chamados...")
        if not atual:
            atual = 0
        if (atual - 2) < 0:
            inicio = 0
        else:
            inicio = atual - 2
        if novo > atual:
            chamados_novos = self.desk.lista_chamados(chave=inicio, direcao="true")
            with ThreadPoolExecutor(max_workers=1) as executor_novo:
                executor_novo.map(self.chamado, chamados_novos.get("root"))
            executor_novo.shutdown()
        chamados_em_aberto = self.desk.lista_chamados(ativo="EmAberto")
        print(len(chamados_em_aberto.get("root")))
        self.atualizar_chamado(chamados_em_aberto.get("root"))
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.map(self.modificar, chamados_em_aberto.get("root"))
        print(f"[{datetime.now()}] Finalizado chamados...")

    def tempo_atendimento(self, tempo: str):
        if tempo in ["0", "00:00:00", ""]:
            return 0.0 if tempo == "0" else None
        negative = "-" in tempo
        if negative:
            tempo = tempo.replace("-", "")
        tempo_str = tempo.split(":")
        horas = int(tempo_str[0])
        minutos = int(tempo_str[1])
        segundos = int(tempo_str[2]) if tempo_str[2] == "" else 0
        total = horas + minutos / 60 + segundos / 3600
        return round(total * (-1 if negative else 1), 2)

    def modificar(self, data: dict):
        chamado = Chamado.objects.filter(chave=data.get('Chave')).first()
        if not chamado:
            return
        chamado.andamento = True
        chamado.nome_grupo = data.get("NomeGrupo")
        chamado.nome_operador = data.get("NomeOperador", "")
        chamado.nome_status = data.get("NomeStatus", "")
        chamado.nome_sla_status_atual = data.get("NomeSlaStatusAtual", "")
        chamado.first_call = data.get("FirstCall", "")
        chamado.sla_1_expirado = data.get("Sla1Expirado")
        chamado.sla_2_expirado = data.get("Sla2Expirado")
        chamado.total_horas_1_atendimento = self.tempo_atendimento(str(data.get("TempoUtilAtPrimeiroAtendimento")))
        chamado.total_horas_1_2_atendimento = self.tempo_atendimento(str(data.get("TotalHorasPrimeiroSegundoAtendimento")))
        chamado.tempo_restante_1 = self.tempo_atendimento(str(data.get("TempoRestantePrimeiroAtendimento")))
        chamado.tempo_restante_2 = self.tempo_atendimento(str(data.get("TempoRestanteSegundoAtendimento")))
        chamado.nome_sistema = data.get("_203471", "")
        chamado.qnt_interacao = data.get("TAcoes")
        chamado.save(update_fields=[
            "andamento",
            "nome_grupo",
            "nome_operador",
            "nome_status",
            "nome_sla_status_atual",
            "first_call",
            "sla_1_expirado",
            "sla_2_expirado",
            "total_horas_1_atendimento",
            "total_horas_1_2_atendimento",
            "tempo_restante_1",
            "tempo_restante_2",
            "nome_sistema",
            "qnt_interacao",
        ])

    def chamado(self, data: dict) -> None:
        chamado = Chamado.objects.filter(chave=data.get('Chave')).first()
        if not chamado:
            chamado = Chamado()
        chamado.andamento = False
        chamado.chave = data.get("Chave", "")
        chamado.cod_chamado = data.get("CodChamado", "")
        chamado.nome_grupo = data.get("NomeGrupo", "")
        chamado.nome_categoria = data.get("NomeCategoria", "")
        chamado.assunto = data.get("Assunto", "")
        chamado.data_criacao = datetime.strptime(data.get("DataCriacao"), "%Y-%m-%d")
        if data.get("DataFinalizacao", "") == "0000-00-00":
            chamado.data_finalizacao = None
        else:
            chamado.data_finalizacao = datetime.strptime(data.get("DataFinalizacao", ""), "%Y-%m-%d")
        chamado.nome_operador = data.get("NomeOperador", "")
        chamado.nome_status = data.get("NomeStatus", "")
        chamado.possui_sla = data.get("PossuiSla", "")
        chamado.nome_sla_status_atual = data.get("NomeSlaStatusAtual", "")
        chamado.first_call = data.get("FirstCall", "")
        chamado.sla_1_expirado = data.get("Sla1Expirado", "")
        chamado.sla_2_expirado = data.get("Sla2Expirado", "")
        chamado.total_horas_1_atendimento = self.tempo_atendimento(str(data.get("TempoUtilAtPrimeiroAtendimento")))
        chamado.total_horas_1_2_atendimento = self.tempo_atendimento(str(data.get("TotalHorasPrimeiroSegundoAtendimento")))
        chamado.tempo_restante_1 = self.tempo_atendimento(str(data.get("TempoRestantePrimeiroAtendimento")))
        chamado.tempo_restante_2 = self.tempo_atendimento(str(data.get("TempoRestanteSegundoAtendimento")))
        chamado.nome_sistema = data.get("_203471", "")
        chamado.qnt_interacao = data.get("TAcoes")
        chamado.save()

    def carga_chamado_faltante(self):
        valores_coluna = Chamado.objects.values_list('chave', flat=True)
        valores_ordenados = sorted(valores_coluna)
        numeros_ausentes = []
        ultimo_valor = None
        for valor in valores_ordenados:
            if ultimo_valor is not None:
                numeros_ausentes.extend(range(ultimo_valor + 1, valor))
            ultimo_valor = valor
        numeros_ausentes.remove(11)
        numeros_ausentes.remove(12)
        if numeros_ausentes:
            for i in numeros_ausentes:
                chamados = self.desk.lista_chamados(chave_filtro=i, direcao="true")
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(self.chamado, chamados.get("root"))

    def atualizar_chamado(self, data: list):
        chamados_andamento = Chamado.objects.filter(andamento=True)
        chamados_atualizados = list(map(lambda x: x["CodChamado"], data))
        lista = [item.cod_chamado for item in chamados_andamento if item.cod_chamado not in chamados_atualizados]
        print(lista)
        if lista:
            chamados = self.desk.lista_chamados(pesquisa=",".join(lista))
            print(chamados.get("root"))
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.map(self.chamado, chamados.get("root"))

    def carga_interacao(self):
        chamados = Chamado.objects.annotate(
            numero_interacao=Count("interacao")
        ).filter(numero_interacao__lt=F('qnt_interacao')).order_by("-chave")
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.atualizar_interacao, chamados)

    def atualizar_interacao(self, chamado: Chamado):
        interacoes = self.desk.lista_interacao(chamado.chave)
        if interacoes.get("root"):
            for interacao in interacoes.get("root"):
                interacao["chamado"] = chamado
                self.interacao(interacao)

    def interacao(self, data: dict) -> None:
        print(data)
        interacao = Interacao()
        interacao.chave = data.get("Chave")
        interacao.chamado = data.get("chamado")
        interacao.seguencia = data.get("Sequencia")
        interacao.status_acao_nome_relatorio = data.get("Status")[0].get("text")
        interacao.fantasia_fornecedor = data.get("FantasiaFornecedor", "")
        interacao.chamado_aprovadores = data.get("ChamadoAprovadores", "")
        interacao.tempo_corrido_interacao = self.tempo_atendimento(str(data.get("TempoCorridoAcoes")))
        interacao.save()