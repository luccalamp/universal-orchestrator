# Modelos sem versões fixas

O catálogo de despacho desta sessão determina disponibilidade; anúncio público/cache de outra conversa não o substitui. A escolha automática vale só para delegados. O principal permanece nesta conversa. Não editar config.toml nem mudar modelo/esforço principal.

## Captura e execução

Em functions.exec, busque ALL_TOOLS por spawn_agent e leia schema/overrides/esforços. Exporte somente esse catálogo para coordination/universal-orchestrator/<slug>/model-catalog.txt; registre origem/data. Não exportar ambiente, configuração privada ou histórico.

Use Python disponível e caminhos absolutos:
Se Python não estiver disponível, aplique os critérios diretamente ao catálogo
real; o helper é uma conveniência, não motivo para instalar software ou bloquear.

    python <skill>/scripts/resolve_models.py --catalog <workspace>/coordination/universal-orchestrator/<slug>/model-catalog.txt --task-kind implementation

Para tarefa mecânica, task-kind mechanical. O JSON propõe worker, reviewer, esforços, motivos e avisos. Aplique somente campos aceitos pelo schema real. São recomendações, não duas instâncias obrigatórias. O crítico final nunca é substituído pelo reviewer.

Entrada aceita descrição textual da ferramenta ou JSON com models contendo id, description e reasoning_efforts. available/deprecated, released_at e default_reasoning_effort são opcionais, somente se a fonte fornecer. Também aceita objeto exportado com description. Sem rede.

## Critérios

- Elegibilidade: só IDs anunciados, disponíveis e não excluídos.
- Executor: descrição econômica/rápida. O principal mantém trabalho difícil/acoplado ou escolhe capacidade adequada à tarefa.
- Revisor: capacidade geral/avançada, somente quando independência beneficiar.
- Atualização: dentro da mesma família, compare versões numericamente (6.10 depois de6.2). Entre famílias distintas, priorize indicação atual/antiga e data de lançamento anunciada; seus números podem ser incomparáveis. Nova família entra por descrição/metadados, sem precisar se chamar Luna/Sol.
- Metadados insuficientes: escolha estável com aviso, julgamento pelo principal. Isso não comprova melhor qualidade/preço.
- Esforço low mecânico, medium implementação, high revisão, somente se anunciado. Sem lista, omita para herdar; não inventar esforço.

Modelo rejeitado: registre motivo e resolva de novo com --exclude <id>, uma vez por candidato. Escolha explícita pode usar --worker/--reviewer; ausência causa falha clara, sem substituição silenciosa.

Refresque em novos objetivos/retomadas e quando catálogo mudar. Modelo novo só entra automaticamente após ficar disponível a esta conta. ID retornado por spawn confirma despacho; não confirma modelo efetivo sem esse metadado. Registre separadamente.
