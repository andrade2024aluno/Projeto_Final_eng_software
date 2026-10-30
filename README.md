# Sprint 1

**Projeto:** Diagnóstico de saúde e identificação de gargalos em servidores

## 1. Integrantes

1. Lucas Gabriel Rodrigues de Moraes
2. Vinicius Gonçalves de Andrade
3.

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


## 3. Pesquisa e justificativa da relevância

A pesquisa usou fonte: o Método USE, de Brendan Gregg 

Gregg propõe avaliar Utilização, Saturação e Erros em cada recurso físico. Olhar só a média de uso (CPU ou RAM) esconde a saturação, que ocorre quando o recurso acumula trabalho em fila, como I/O wait ou trocas constantes entre RAM e Swap. Isso trava serviços mesmo com o processador aparentemente livre.

Com base nisso, o projeto cruza métricas de utilização e saturação para destacar o que exige atenção, reduzindo a inspeção manual de tabelas. Esse ganho é uma hipótese ainda não medida. Picos rápidos serão tratados como variação normal e só eventos contínuos gerarão alertas, cabendo ao administrador decidir a correção.

## 4. Referências

GREGG, Brendan. **The USE Method**. Brendan Gregg's Homepage, [s.d.]. Disponível em: <https://www.brendangregg.com/usemethod.html>. Acesso em: 29 out. 2026. Seções consultadas: *Introduction*, *Summary*, *Resource List* e *Interpretation*.
