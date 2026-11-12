import unittest
from diagnostico import ErroTelemetria, carregar_dados, calcular_estatisticas, classificar

ARQUIVO_CSV = "amostra.csv"


class TestLeituraDados(unittest.TestCase):

    def test_csv_valido(self):
        registros = carregar_dados(ARQUIVO_CSV)
        self.assertEqual(len(registros), 30)
        self.assertEqual(registros[0]["cpu_util_percent"], 21.5)

    def test_coluna_ausente(self):
        with self.assertRaises(ErroTelemetria) as contexto:
            carregar_dados("invalido_sem_coluna.csv")
        self.assertIn("net_in", str(contexto.exception))

    def test_valor_nao_numerico(self):
        with self.assertRaises(ErroTelemetria) as contexto:
            carregar_dados("invalido_texto.csv")
        self.assertIn("3", str(contexto.exception))

    def test_arquivo_formato_invalido(self):
        with self.assertRaises(ErroTelemetria):
            carregar_dados("invalido_dados.txt")


class TestEstatisticas(unittest.TestCase):

    def test_quatro_recursos_com_media_e_pico(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(set(estatisticas["m_1"].keys()), {"cpu", "memoria", "disco", "rede"})
        self.assertEqual(set(estatisticas["m_1"]["cpu"].keys()), {"media", "pico"})

    def test_calculo_media(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertAlmostEqual(estatisticas["m_2"]["cpu"]["media"], 88.6, delta=0.1)

    def test_calculo_pico(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(estatisticas["m_3"]["disco"]["pico"], 92.0)

    def test_servidores_separados(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(set(estatisticas.keys()), {"m_1", "m_2", "m_3"})


class TestClassificacao(unittest.TestCase):

    def test_media_alta_critico(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(classificar(estatisticas["m_2"]["cpu"]), "CRITICO")

    def test_apenas_pico_alto_atencao(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(classificar(estatisticas["m_3"]["disco"]), "ATENCAO")

    def test_valores_baixos_ok(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(classificar(estatisticas["m_1"]["cpu"]), "OK")

    def test_limite_personalizado(self):
        estatisticas = calcular_estatisticas(carregar_dados(ARQUIVO_CSV))
        self.assertEqual(classificar(estatisticas["m_1"]["memoria"], limite=30), "CRITICO")


if __name__ == "__main__":
    unittest.main()