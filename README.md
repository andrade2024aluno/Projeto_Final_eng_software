# Sprint 1 — Definição da proposta

**Projeto:** NodeDiag — Diagnóstico de saúde e identificação de gargalos em servidores

## 1. Integrantes

1. Lucas Gabriel Rodrigues de Moraes
2. Vinicius Gonçalves de Andrade
3. [Nome do Integrante 3]

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

A pesquisa usou duas fontes: o Método USE, de Brendan Gregg [1], e o capítulo sobre monitoramento do livro *Site Reliability Engineering* (SRE), do Google [2].

Gregg propõe avaliar Utilização, Saturação e Erros em cada recurso físico. Olhar só a média de uso (CPU ou RAM) esconde a saturação, que ocorre quando o recurso acumula trabalho em fila, como I/O wait ou trocas constantes entre RAM e Swap. Isso trava serviços mesmo com o processador aparentemente livre.

O livro de SRE aponta que analisar telemetria manualmente é ineficiente e que o monitoramento deve separar sintomas de causas e picos isolados de degradações contínuas. Embora trate de grande escala, o problema de cruzar várias métricas ao longo do tempo também afeta quem administra servidores menores sem ferramentas pagas.

Com base nisso, o NodeDiag cruza métricas de utilização e saturação para destacar o que exige atenção, reduzindo a inspeção manual de tabelas. Esse ganho é uma hipótese ainda não medida. Picos rápidos serão tratados como variação normal e só eventos contínuos gerarão alertas, cabendo ao administrador decidir a correção.

## 4. Referências

[1] GREGG, Brendan. **The USE Method**. Brendan Gregg's Homepage, [s.d.]. Disponível em: <https://www.brendangregg.com/usemethod.html>. Acesso em: 29 out. 2026. Seções consultadas: *Introduction*, *Summary*, *Resource List* e *Interpretation*.

[2] EWASCHUK, Rob. **Monitoring Distributed Systems**. In: BEYER, Betsey et al. (org.). *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. Cap. 6. Disponível em: <https://sre.google/sre-book/monitoring-distributed-systems/>. Acesso em: 29 out. 2026. Seções consultadas: *Definitions*, *Why Monitor?* e *Symptoms Versus Causes*.
