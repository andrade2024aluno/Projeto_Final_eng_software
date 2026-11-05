import os
import tempfile
import unittest

from sprint2 import TelemetryError, classify, compute_stats, load_telemetry

COLUNAS = ["machine_id", "cpu_util_percent", "mem_util_percent", "disk_io_percent", "net_in"]


def registro(**campos):
    dados = {"machine_id": "m_1", "cpu_util_percent": 10, "mem_util_percent": 10,
             "disk_io_percent": 10, "net_in": 10}
    dados.update(campos)
    return dados


def salvar_csv(pasta, nome, registros, colunas=COLUNAS):
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(",".join(colunas) + "\n")
        for r in registros:
            f.write(",".join(str(r[c]) for c in colunas) + "\n")
    return caminho



class TestHistoria1(unittest.TestCase):

    def test_h1_c1_csv_valido(self):
        """Critério 1: CSV válido gera uma entrada por linha, com valores numéricos."""
        with tempfile.TemporaryDirectory() as pasta:
            caminho = salvar_csv(pasta, "d.csv", [registro(cpu_util_percent=50), registro()])
            resultado = load_telemetry(caminho)
            self.assertEqual(len(resultado), 2)
            self.assertEqual(resultado[0]["cpu_util_percent"], 50.0)

    def test_h1_c2_coluna_ausente(self):
        """Critério 2: coluna ausente gera erro com o nome dela."""
        colunas = [c for c in COLUNAS if c != "net_in"]
        with tempfile.TemporaryDirectory() as pasta:
            caminho = salvar_csv(pasta, "d.csv", [registro()], colunas)
            with self.assertRaises(TelemetryError) as erro:
                load_telemetry(caminho)
            self.assertIn("net_in", str(erro.exception))

    def test_h1_c3_valor_nao_numerico(self):
        """Critério 3: valor que não é número gera erro com o número da linha."""
        with tempfile.TemporaryDirectory() as pasta:
            caminho = salvar_csv(pasta, "d.csv", [registro(), registro(cpu_util_percent="abc")])
            with self.assertRaises(TelemetryError) as erro:
                load_telemetry(caminho)
            self.assertIn("3", str(erro.exception))  # cabeçalho=1, ok=2, inválido=3

    def test_h1_c4_valor_fora_de_0_a_100(self):
        """Critério 4: valor abaixo de 0 ou acima de 100 gera erro com o número da linha."""
        for valor in (-1, 101):
            with tempfile.TemporaryDirectory() as pasta:
                caminho = salvar_csv(pasta, "d.csv", [registro(), registro(disk_io_percent=valor)])
                with self.assertRaises(TelemetryError) as erro:
                    load_telemetry(caminho)
                self.assertIn("3", str(erro.exception))

    def test_h1_c5_arquivo_que_nao_e_csv(self):
        """Critério 5: arquivo que não seja .csv é recusado."""
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "d.txt")
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("qualquer coisa")
            with self.assertRaises(TelemetryError):
                load_telemetry(caminho)


# ---------- História 2: média e pico por servidor ----------
class TestHistoria2(unittest.TestCase):

    def test_h2_c1_quatro_recursos_com_media_e_pico(self):
        """Critério 1: cada servidor traz 4 recursos, cada um com média e pico."""
        resultado = compute_stats([registro()])["m_1"]
        self.assertEqual(set(resultado), {"cpu", "memoria", "disco", "rede"})
        self.assertEqual(set(resultado["cpu"]), {"media", "pico"})

    def test_h2_c2_media(self):
        """Critério 2: a média é calculada sobre todos os valores (50, 70, 90 -> 70)."""
        registros = [registro(cpu_util_percent=v) for v in (50, 70, 90)]
        self.assertEqual(compute_stats(registros)["m_1"]["cpu"]["media"], 70)

    def test_h2_c3_pico(self):
        """Critério 3: o pico é o maior valor (20, 95, 40 -> 95)."""
        registros = [registro(mem_util_percent=v) for v in (20, 95, 40)]
        self.assertEqual(compute_stats(registros)["m_1"]["memoria"]["pico"], 95)

    def test_h2_c4_servidores_separados(self):
        """Critério 4: com mais de um servidor, cada um é calculado separadamente."""
        registros = [registro(machine_id="m_1", cpu_util_percent=20),
                     registro(machine_id="m_2", cpu_util_percent=80)]
        resultado = compute_stats(registros)
        self.assertEqual(resultado["m_1"]["cpu"]["media"], 20)
        self.assertEqual(resultado["m_2"]["cpu"]["media"], 80)


# ---------- História 3: classificar cada recurso ----------
class TestHistoria3(unittest.TestCase):

    def test_h3_c1_media_alta_e_critico(self):
        """Critério 1: média >= 80 é CRITICO."""
        self.assertEqual(classify({"media": 80, "pico": 90}), "CRITICO")

    def test_h3_c2_so_o_pico_alto_e_atencao(self):
        """Critério 2: média < 80 mas pico >= 80 é ATENCAO."""
        self.assertEqual(classify({"media": 40, "pico": 95}), "ATENCAO")

    def test_h3_c3_tudo_baixo_e_ok(self):
        """Critério 3: pico < 80 é OK."""
        self.assertEqual(classify({"media": 30, "pico": 79}), "OK")

    def test_h3_c4_limite_alteravel(self):
        """Critério 4: com limite 50, média 60 é CRITICO."""
        self.assertEqual(classify({"media": 60, "pico": 70}, threshold=50), "CRITICO")


if __name__ == "__main__":
    unittest.main()