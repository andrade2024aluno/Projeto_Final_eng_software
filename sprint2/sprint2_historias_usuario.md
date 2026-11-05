# Sprint 2: Histórias de Usuário

Dados de entrada (Sintéticos), com 5 colunas: `machine_id` (servidor), `cpu_util_percent`(cpu), `mem_util_percent`(memória), `disk_io_percent`(Disco) e `net_in`(Rede)

---

## História 1: Carregar os dados dos servidores
Como administrador de sistemas, eu quero carregar um arquivo CSV/JSON com os dados de monitoramento, para que o sistema confira se está tudo certo antes de analisar, sem eu precisar revisar o arquivo na mão.

Critérios de aceitação:

* Ao carregar um CSV/JSON válido, o sistema lê uma entrada para cada linha de dados, com os valores já como números.
* Se faltar uma coluna, o sistema mostra um erro dizendo qual coluna está faltando.
* Se algum valor não for um número, o sistema mostra um erro dizendo em qual linha está o problema.
* Arquivos que não sejam CSV/JSON são recusados com um erro.

Prioridade: Alta

---

## História 2: Calcular a média e o pico de cada servidor
Como administrador de sistemas, eu quero ver a média e o pico de uso de CPU, memória, disco e rede de cada servidor, para ter uma visão resumida sem fazer conta manualmente.

Critérios de aceitação:

* Para cada servidor, o resultado traz os 4 recursos, e cada um mostra a média e o pico.
* A média é calculada sobre todos os valores do servidor (ex.: 50, 70 e 90 dão 70).
* O pico é o maior valor do servidor (ex.: 20, 95 e 40 dão 95).
* Quando o arquivo tem mais de um servidor, cada um é calculado separadamente.

Prioridade: Média

---

## História 3: Classificar o estado de cada recurso
Como administrador de sistemas, eu quero que cada recurso de cada servidor apareça como OK, ATENCAO ou CRITICO, para achar o problema rapidamente sem precisar interpretar os números.

Critérios de aceitação:

* Se a média for 80% ou mais, o recurso é CRITICO.
* Se a média for menor que 80%, mas o pico for 80% ou mais, o recurso é ATENCAO.
* Se o pico for menor que 80%, o recurso é OK.
* O limite de 80% pode ser alterado pelo usuário (ex.: com limite 50, média 60 vira CRITICO).

Prioridade: Alta

---

## Relação entre testes e critérios

Os critérios de cada história são numerados na ordem em que aparecem (1º, 2º...). Os testes em `test_sprint2.py` seguem o padrão `test_h<história>_c<critério>`: por exemplo, `test_h2_c3` verifica o 3º critério da História 2 (o pico é o maior valor).

| História | Testes |
|----------|--------|
| 1 | test_h1_c1 a test_h1_c4 |
| 2 | test_h2_c1 a test_h2_c4 |
| 3 | test_h3_c1 a test_h3_c4 |
