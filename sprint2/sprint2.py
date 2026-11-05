# recurso -> coluna do CSV (valores em porcentagem, de 0 a 100)
RECURSOS = {
    "cpu": "cpu_util_percent",
    "memoria": "mem_util_percent",
    "disco": "disk_io_percent",
    "rede": "net_in",
}

LIMITE_PADRAO = 80.0


class TelemetryError(ValueError):
    """Erro de leitura ou validação do arquivo de dados."""


def load_telemetry(path):
    """Lê um arquivo .csv e retorna uma lista de registros (dicts com números)."""
    raise NotImplementedError


def compute_stats(records):
    """Retorna {machine_id: {recurso: {"media": ..., "pico": ...}}}."""
    raise NotImplementedError


def classify(stats, threshold=LIMITE_PADRAO):
    """Recebe {"media": ..., "pico": ...} e retorna 'OK', 'ATENCAO' ou 'CRITICO'."""
    raise NotImplementedError