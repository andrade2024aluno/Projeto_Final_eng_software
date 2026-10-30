# Sprint 1 — Definição da proposta

**Projeto:** NodeDiag — Diagnóstico de saúde e identificação de gargalos em servidores

## 1. Integrantes

1. Lucas Gabriel Rodrigues de Moraes
2. Vinicius Gonçalves de Andrade
3. [Nome Completo do Integrante 3]

## 2. Descrição do sistema

O sistema auxiliará na identificação de gargalos de desempenho e esgotamento de recursos físicos (processamento, memória e disco) em servidores Linux.
Seu público-alvo será composto por administradores de infraestrutura, desenvolvedores que mantêm serviços próprios (self-hosting) e operadores de pequenos ambientes em nuvem.
A entrada será um arquivo estruturado (CSV ou JSON) com registros temporais de telemetria do servidor, contendo leituras como:
2026-10-27T14:10:00;host=srv-app01;cpu_pct=42.5;load_1m=4.80;mem_used_pct=94.2;swap_in_kb=1840;iowait_pct=31.4
A saída reunirá os períodos críticos diagnosticados e a relação entre os recursos afetados, conforme o exemplo:
Servidor analisado: srv-app01 (4 vCPUs, 8 GB RAM)
Período crítico: 27/10, das 14:08 às 14:15
Ocorrências: 8 leituras consecutivas com uso de memória acima de 90% e escrita ativa em Swap
Diagnóstico: Saturação de memória RAM com paginação em disco (Swap thrashing), elevando o tempo de espera de I/O (iowait médio de 29,8%).
Severidade: 9/10, conforme os limiares de saturação configurados para o perfil do servidor.

## 3. Pesquisa e justificativa da relevância

A pesquisa utilizou duas fontes: a documentação do Método USE, de Brendan Gregg, e o capítulo sobre monitorização do livro Site Reliability Engineering (SRE), da Google. Uma fundamenta como detetar gargalos de hardware, enquanto a outra justifica a análise estruturada de métricas para encontrar a causa de lentidões.

Brendan Gregg propõe avaliar três indicadores em cada recurso físico: Utilização, Saturação e Erros (USE). O autor destaca que olhar apenas a média de uso (como a percentagem de CPU ou RAM) esconde sinais de saturação — quando o recurso começa a acumular trabalho em fila, como processos a aguardar por leitura de disco (I/O wait) ou trocas constantes entre RAM e Swap. Esses fenómenos travam os serviços mesmo quando o processador parece livre.

O livro de SRE da Google aponta que a análise manual de grandes volumes de telemetria é ineficiente e que a monitorização deve separar sintomas de causas reais, diferenciando picos isolados de uma degradação contínua. Embora o livro trate de infraestruturas de grande escala, a dificuldade de cruzar várias colunas de métricas ao longo do tempo também afeta quem gere servidores menores sem ferramentas pagas.

Com base nisto, o NodeDiag propõe filtrar os registos de coleta e cruzar métricas de utilização e saturação para destacar o que exige atenção, reduzindo o trabalho de inspecionar tabelas brutas manualmente. Esse ganho é uma hipótese da proposta, ainda não medida. Picos rápidos serão tratados como variações normais de carga e apenas eventos contínuos gerarão alertas, cabendo ao administrador decidir a correção a aplicar.

## 4. Referências

[1] GREGG, Brendan. **The USE Method**. Brendan Gregg's Homepage, [s.d.]. Disponível em: <https://www.brendangregg.com/usemethod.html>. Acesso em: 29 out. 2026. Seções consultadas: *Introduction*, *Summary*, *Resource List* e *Interpretation*.

[2] EWASCHUK, Rob. **Monitoring Distributed Systems**. In: BEYER, Betsey et al. (org.). *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. Cap. 6. Disponível em: <https://sre.google/sre-book/monitoring-distributed-systems/>. Acesso em: 29 out. 2026. Seções consultadas: *Definitions*, *Why Monitor?* e *Symptoms Versus Causes*.
