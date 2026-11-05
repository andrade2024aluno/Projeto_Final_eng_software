"""Testes da Sprint 2.

Cada teste se chama test_h<história>_c<critério>: por exemplo, test_h2_c3 verifica
o 3º critério da História 2. Nesta sprint todos falham, pois as funções ainda
não foram implementadas (Sprint 3).

Execução: python -m unittest test_sprint2 -v
"""
import unittest

from sprint2 import TelemetryError, classify, compute_stats, load_telemetry

CSV = "amostra.csv"  # 3 servidores


# ---------- História 1: carregar os dados ----------
class TestHistoria1(unittest.TestCase):

    def test_h1_c1_csv_valido(self):
        """Critério 1: CSV válido gera uma entrada por linha, com valores numéricos."""
        registros = load_telemetry(CSV)
        self.assertEqual(len(registros), 30)
        self.assertEqual(registros[0]["cpu_util_percent"], 21.5)

    def test_h1_c2_coluna_ausente(self):
        """Critério 2: coluna ausente gera erro com o nome dela."""
        with self.assertRaises(TelemetryError) as erro:
            load_telemetry("invalido_sem_coluna.csv")  # sem a coluna net_in
        self.assertIn("net_in", str(erro.exception))

    def test_h1_c3_valor_nao_numerico(self):
        """Critério 3: valor que não é número gera erro com o número da linha."""
        with self.assertRaises(TelemetryError) as erro:
            load_telemetry("invalido_texto.csv")  # texto na linha 3
        self.assertIn("3", str(erro.exception))

    def test_h1_c4_valor_fora_de_0_a_100(self):
        """Critério 4: valor abaixo de 0 ou acima de 100 gera erro com o número da linha."""
        with self.assertRaises(TelemetryError) as erro:
            load_telemetry("invalido_fora_da_faixa.csv")  # valor 101 na linha 3
        self.assertIn("3", str(erro.exception))

    def test_h1_c5_arquivo_que_nao_e_csv(self):
        """Critério 5: arquivo que não seja .csv é recusado."""
        with self.assertRaises(TelemetryError):
            load_telemetry("dados.txt")


# ---------- História 2: média e pico por servidor ----------
class TestHistoria2(unittest.TestCase):

    def test_h2_c1_quatro_recursos_com_media_e_pico(self):
        """Critério 1: cada servidor traz 4 recursos, cada um com média e pico."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(set(stats["m_1"]), {"cpu", "memoria", "disco", "rede"})
        self.assertEqual(set(stats["m_1"]["cpu"]), {"media", "pico"})

    def test_h2_c2_media(self):
        """Critério 2: a média é calculada sobre todos os valores (m_2, CPU: 88,6)."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertAlmostEqual(stats["m_2"]["cpu"]["media"], 88.6, delta=0.1)

    def test_h2_c3_pico(self):
        """Critério 3: o pico é o maior valor (m_3, disco: 92,0)."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(stats["m_3"]["disco"]["pico"], 92.0)

    def test_h2_c4_servidores_separados(self):
        """Critério 4: cada servidor do arquivo é calculado separadamente."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(set(stats), {"m_1", "m_2", "m_3"})


# ---------- História 3: classificar cada recurso ----------
class TestHistoria3(unittest.TestCase):

    def test_h3_c1_media_alta_e_critico(self):
        """Critério 1: média >= 80 é CRITICO (m_2, CPU)."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(classify(stats["m_2"]["cpu"]), "CRITICO")

    def test_h3_c2_so_o_pico_alto_e_atencao(self):
        """Critério 2: média < 80 mas pico >= 80 é ATENCAO (m_3, disco)."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(classify(stats["m_3"]["disco"]), "ATENCAO")

    def test_h3_c3_tudo_baixo_e_ok(self):
        """Critério 3: pico < 80 é OK (m_1, CPU)."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(classify(stats["m_1"]["cpu"]), "OK")

    def test_h3_c4_limite_alteravel(self):
        """Critério 4: com limite 30, a memória do m_1 (média 38,9) vira CRITICO."""
        stats = compute_stats(load_telemetry(CSV))
        self.assertEqual(classify(stats["m_1"]["memoria"], threshold=30), "CRITICO")


if __name__ == "__main__":
    unittest.main()
