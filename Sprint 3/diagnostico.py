import csv
import json
import sys

RECURSOS = {
    "cpu": "cpu_util_percent",
    "memoria": "mem_util_percent",
    "disco": "disk_io_percent",
    "rede": "net_in"
}

COLUNAS_OBRIGATORIAS = [
    "machine_id",
    "cpu_util_percent",
    "mem_util_percent",
    "disk_io_percent",
    "net_in"
]


class ErroTelemetria(Exception):
    pass


def validar_colunas(colunas):
    faltando = []
    for col in COLUNAS_OBRIGATORIAS:
        if col not in colunas:
            faltando.append(col)
    if len(faltando) > 0:
        raise ErroTelemetria(f"Colunas faltando no arquivo: {', '.join(faltando)}")


def carregar_dados(caminho):
    # Verifica se a extensao e valida
    if not (caminho.endswith(".csv") or caminho.endswith(".json")):
        raise ErroTelemetria("Formato de arquivo invalido. Use .csv ou .json")

    linhas_brutas = []

    try:
        if caminho.endswith(".csv"):
            with open(caminho, mode="r", encoding="utf-8") as arq:
                leitor = csv.DictReader(arq)
                if leitor.fieldnames is None:
                    raise ErroTelemetria("Arquivo CSV vazio")
                validar_colunas(leitor.fieldnames)

                num_linha = 2
                for linha in leitor:
                    linhas_brutas.append((num_linha, linha))
                    num_linha += 1
        else:
            with open(caminho, mode="r", encoding="utf-8") as arq:
                dados = json.load(arq)
                if len(dados) > 0:
                    validar_colunas(dados[0].keys())

                num_linha = 1
                for item in dados:
                    linhas_brutas.append((num_linha, item))
                    num_linha += 1
    except ErroTelemetria:
        raise
    except Exception as e:
        raise ErroTelemetria(f"Erro ao ler o arquivo: {e}")

    registros = []
    for num_linha, item in linhas_brutas:
        validar_colunas(item.keys())
        id_maquina = str(item["machine_id"]).strip()
        if id_maquina == "":
            raise ErroTelemetria(f"Linha {num_linha}: machine_id vazio")

        registro = {"machine_id": id_maquina}
        for nome_col in RECURSOS.values():
            try:
                registro[nome_col] = float(item[nome_col])
            except (ValueError, TypeError):
                raise ErroTelemetria(f"Linha {num_linha}: valor invalido na coluna {nome_col}")

        registros.append(registro)

    if len(registros) == 0:
        raise ErroTelemetria("Nenhum dado encontrado no arquivo")

    return registros


def calcular_estatisticas(registros):
    agrupado = {}

    # Separa as leituras por servidor e por recurso
    for reg in registros:
        maquina = reg["machine_id"]
        if maquina not in agrupado:
            agrupado[maquina] = {
                "cpu": [],
                "memoria": [],
                "disco": [],
                "rede": []
            }

        for nome_recurso, coluna_csv in RECURSOS.items():
            agrupado[maquina][nome_recurso].append(reg[coluna_csv])

    # Calcula a media e o pico de cada recurso
    resultado = {}
    for maquina, recursos in agrupado.items():
        resultado[maquina] = {}
        for nome_recurso, lista_valores in recursos.items():
            media = sum(lista_valores) / len(lista_valores)
            pico = max(lista_valores)
            resultado[maquina][nome_recurso] = {
                "media": media,
                "pico": pico
            }

    return resultado


def classificar(dados_recurso, limite=80.0):
    if dados_recurso["media"] >= limite:
        return "CRITICO"
    elif dados_recurso["pico"] >= limite:
        return "ATENCAO"
    else:
        return "OK"


def mostrar_relatorio(estatisticas, limite=80.0):
    print(f"Limite configurado: {limite}%\n")
    for maquina in sorted(estatisticas.keys()):
        print(f"Servidor: {maquina}")
        for recurso, valores in estatisticas[maquina].items():
            status = classificar(valores, limite)
            media = valores["media"]
            pico = valores["pico"]
            print(f"  - {recurso}: media = {media:.1f}% | pico = {pico:.1f}% -> {status}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python diagnostico.py <arquivo> [limite]")
        sys.exit(1)

    arquivo = sys.argv[1]
    limite_uso = 80.0
    if len(sys.argv) >= 3:
        limite_uso = float(sys.argv[2])

    try:
        dados = carregar_dados(arquivo)
        estatisticas = calcular_estatisticas(dados)
        mostrar_relatorio(estatisticas, limite_uso)
    except ErroTelemetria as erro:
        print(f"Erro: {erro}")
        sys.exit(1)