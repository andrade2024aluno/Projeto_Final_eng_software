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

A pesquisa baseou-se em duas referências técnicas de engenharia de sistemas: a documentação do Método USE, de Brendan Gregg, e o capítulo sobre monitoramento de sistemas do livro Site Reliability Engineering (SRE), do Google. A primeira fundamenta como identificar gargalos de hardware, enquanto a segunda justifica a necessidade de filtrar métricas brutas para encontrar a causa de lentidões.

Brendan Gregg propõe que a investigação de desempenho em servidores deve avaliar três métricas para cada componente físico: Utilização, Saturação e Erros (USE). O autor aponta que administradores costumam observar apenas a média de utilização (como percentual de CPU ou memória ocupada), deixando passar sinais de saturação — o ponto em que o recurso passa a enfileirar trabalho, como processos aguardando leitura de disco (I/O wait) ou trocas constantes entre RAM e Swap. Segundo o guia, esses gargalos conseguem travar aplicações mesmo quando o processador aparenta estar ocioso.

O livro de SRE do Google, no capítulo escrito por Rob Ewaschuk, aborda o problema de analisar grandes volumes de coletas de telemetria manualmente. O texto destaca que o monitoramento eficaz precisa traduzir dados brutos de máquina em relação de sintoma e causa, diferenciando oscilações momentâneas de uma degradação sustentada que exige intervenção. Embora as práticas do Google sejam voltadas a infraestruturas de grande porte, o problema de cruzar múltiplas colunas de métricas ao longo do tempo também afeta quem administra poucos servidores sem ferramentas pagas de observabilidade.

A partir dessas referências, o NodeDiag propõe processar históricos de coleta de recursos e aplicar regras que cruzam utilização e saturação para apontar onde está o gargalo real da máquina. A redução no tempo de diagnóstico em comparação à leitura manual de tabelas é uma premissa do projeto, limitada à qualidade e ao intervalo dos dados fornecidos na entrada. Picos isolados de uso e variações normais de carga serão diferenciados de gargalos persistentes por meio de janelas de tempo configuráveis, cabendo ao administrador decidir se a solução envolve ajuste de software ou ampliação de hardware.

## 4. Referências

[1] GREGG, Brendan. **The USE Method**. Brendan Gregg's Homepage, [s.d.]. Disponível em: <https://www.brendangregg.com/usemethod.html>. Acesso em: 29 out. 2026. Seções consultadas: *Introduction*, *Summary*, *Resource List* e *Interpretation*.

[2] EWASCHUK, Rob. **Monitoring Distributed Systems**. In: BEYER, Betsey et al. (org.). *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. Cap. 6. Disponível em: <https://sre.google/sre-book/monitoring-distributed-systems/>. Acesso em: 29 out. 2026. Seções consultadas: *Definitions*, *Why Monitor?* e *Symptoms Versus Causes*.
