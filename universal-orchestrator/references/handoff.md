# Handoff com contrato, escopo e evidência

## Brief da tarefa

Cada brief tem no máximo 150 palavras e informa apenas o necessário:

- ID de continuação e papel; modelo escolhido do catálogo desta sessão, esforço efetivamente configurado e evidência dessa disponibilidade.
- Resultado esperado e abordagem/contratos definidos pelo principal.
- Contexto mínimo, dependências e invariantes.
- Leitura permitida e caminhos exclusivos de escrita; caminhos vedados.
- Verificação focal e condição de parada.

Não imponha ao principal outro modelo ou esforço. O delegado não cria subagentes, não inicia outra orquestração e executa somente a tarefa recebida. Para tarefa de leitura, nenhum caminho é gravável. Para escrita paralela, os caminhos de cada executor não se sobrepõem.

## Retorno conciso

STATUS: completo | parcial | bloqueado
ID: identificador da tarefa
MODELO/ESFORÇO: escolha real e evidência disponível
ESCOPO: caminhos lidos e escritos; desvios
RESULTADO: mudança ou achado, com referências concretas
VERIFICAÇÃO: comandos focais executados e resultados; itens não executados
INCERTEZAS: suposições e riscos ainda sem resolução
PRÓXIMO PASSO: decisão ou ação que cabe ao principal

O principal continua responsável: inspeciona o diff/artefato, confere as alegações decisivas e integra ou rejeita o resultado. Status declarado pelo delegado, isoladamente, não basta para aceite.