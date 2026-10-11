---
name: universal-orchestrator
description: Orquestrar tarefas substanciais de implementação, correção, pesquisa, revisão ou criação de conteúdo com executores escolhidos dinamicamente do catálogo atual. O modelo desta conversa coordena e faz a crítica final; delegar somente trabalho delimitado e verificável, com quantidade adaptável e contexto mínimo. Use em pedidos de orquestração universal, Sol/Luna ou trabalho paralelo; pedidos triviais seguem execução direta.
---

# Universal Orchestrator

O **modelo ativo desta conversa é sempre o coordenador e crítico final**, qualquer que seja seu nome ou família. Ele entende o objetivo, define contratos, decide, integra, revisa e aceita. Esta skill não muda o modelo, esforço, permissões ou configuração global da conversa. Delegados são executores e consultores; nunca assumem essa autoridade.

Use o menor fluxo que entregue o resultado correto. A quantidade de agentes acompanha o trabalho: zero para trabalho trivial, geralmente um a três para entregas independentes; mais apenas com benefício concreto e capacidade. Respeite uma quantidade explicitamente solicitada pelo usuário quando viável.

## 1. Entenda e preserve o contexto

- Confirme objetivo, aceite, limites e autorização vigente. Inspecione estado/diff e instruções aplicáveis; busque símbolos, rotas e arquivos antes de ler trechos.
- Descubra tecnologia e ferramentas reais. Não assumir linguagem, framework, testes, provedor ou editor. Para pesquisa/conteúdo, descubra fontes, artefatos e critérios de qualidade.
- Reconstrua você mesmo o caminho relevante, interfaces, efeitos e falhas. Resolva decisões que bloqueiam a divisão; mantenha o caminho crítico avançando localmente.
- Congele um **contrato de qualidade (DQC)** curto: resultado, invariantes, interfaces, desenho, arquivos exclusivos e evidência de aceite. Registre estado no workspace quando houver delegação/continuação.
- Descubra e aplique as skills de domínio disponíveis somente na fase pertinente, por exemplo pesquisa, imagens ou documentos. Não inventar capacidade de imagens, navegador ou publicação dos delegados.

## 2. Resolva modelos pelo catálogo real

Leia [models.md](references/models.md) no primeiro despacho de um objetivo ou quando o catálogo mudar.

1. Descubra despacho e schema atual. Em functions.exec, procure ALL_TOOLS por multi_agent_v1__spawn_agent e operações associadas. Use nomes/prefixos reais em tools; nomes curtos aqui são operações, não chamadas universais.
2. Exporte modelos permitidos e esforços para snapshot mínimo no registro do objetivo, com origem/data. Execute scripts/resolve_models.py com esse catálogo local. O helper não usa rede nem altera configuração.
3. Executor econômico/rápido atende trabalho delimitado; revisão independente usa capacidade adequada quando útil. Sucessores Luna, Sol e novas famílias podem entrar pela descrição e versão do catálogo. Não prender a IDs nem confundir versão com qualidade medida.
4. Reconsulte em novo objetivo, retomada ou rejeição. Não trocar agentes em execução só porque há modelo novo. Exclua candidato rejeitado e tente alternativa suportada, preservando modelo explicitamente fixado pelo usuário.
5. O principal nunca entra nessa troca automática. Sem catálogo confiável/override, omita o override para herdar o modelo atual quando delegação fizer sentido. Sem delegação, execute localmente e registre a limitação.
6. Lançamento público não implica acesso nesta conta. Não inventar IDs, preços, limites ou percentuais de economia. Registre modelo solicitado/evidência; só afirmar modelo efetivo quando o runtime o informar.

## 3. Escolha a rota

| Rota | Quando | Execução |
|---|---|---|
| DIRECT | Pequeno, claro ou próximo passo urgente | Principal executa/verifica; nenhum delegado |
| ASSISTED | Ambíguo/acoplado, mas há investigação independente | Principal decide/implementa; apoio de leitura |
| DELEGATED | Contrato estável, escrita exclusiva e aceite independente | Executores aplicam patches; principal integra/revisa |
| CRITICAL | Risco relevante em contratos, estado, acesso ou efeitos | Principal mantém decisões/escritas sensíveis; apoio proporcional |

Delegue escrita somente com interface, escopo e critérios claros, sem colisão e com benefício. Não empurrar decisão de arquitetura mal definida a executor barato. Use [routing.md](references/routing.md) ou [authority.md](references/authority.md) quando necessário.

## 4. Despache sem duplicação

- Use o [brief e estado](references/handoff.md): entrega concreta, leitura mínima, escrita exclusiva, dependências resolvidas, invariantes, verificação real e condição de bloqueio.
- Use fork_context=false quando suportado. Passe caminhos e trechos indispensáveis; não copiar conversa inteira, todos os relatórios ou árvore do projeto.
- Executor não cria descendentes nem aplica esta skill de coordenação. Atribua papel útil: exploração, pesquisa, depuração, implementação, testes, revisão, segurança, desempenho, documentação ou integração.
- Agrupe despachos independentes; mantenha dependências/mutações compartilhadas sequenciais. Um recurso tem um escritor por lote; contrato compartilhado tem um responsável.
- Respeite capacidade: agentes concluídos ainda abertos podem ocupar vagas. Libere somente seus agentes quando dispensáveis. Não encher vagas nem consultar status em loop.
- Durante execução, avance fora dos escopos delegados. Aguarde em conjunto apenas quando o resultado for necessário ao próximo passo.
- Relatos de até150 palavras trazem caminhos, resultado, comandos/inspeção, riscos e próximo passo. Informação extensa fica em artefato referenciado, sem logs inteiros ou segredos.
- Reuse send_input para correção relacionada; resume_agent após fechamento se suportado. Se impossível retomar, substitua só a tarefa restante, registrando motivo e novo ID.

## 5. Revise e prove

O principal examina **todos os artefatos e diffs finais**, inclusive pareceres. Nenhum agente aprova o próprio trabalho. Fontes e afirmações são evidência a conferir.

- Compare entrega, contrato e limites. Verifique regressões/falhas pertinentes; rejeite remover testes/validações para obter resultado verde.
- Integre em ordem. Em workspace isolado, obtenha patch/artefato pelo mecanismo real e preserve alterações do usuário; teste o estado final integrado.
- Rode a menor verificação que cobre aceite/risco. Amplie a suíte por impacto, falha ou dúvida nova; não repetir teste verde sem motivo.
- Devolva defeitos ao responsável com reprodução, esperado e escopo. Em ambiguidade/repetição improdutiva, revise contrato e assuma o bloqueio localmente.
- Revisão independente serve como apoio quando a perspectiva distinta pode detectar risco concreto; o crítico final permanece nesta conversa. Use [quality.md](references/quality.md) proporcionalmente.
- Engenharia exige comportamento/interfaces corretos; pesquisa exige fontes verificadas; conteúdo exige inspeção real. Teste sintético/build/relato não comprova login, publicação, vídeo renderizado ou desempenho.

## 6. Continuidade e entrega

Atualize coordination/universal-orchestrator/<slug>/state.md quando um resultado chegar, contrato mudar ou antes de interrupção: objetivo, principal se conhecido, catálogo/seleção, IDs, contratos, artefatos, verificações e próximo passo.

Na retomada, confira estado e IDs/artefatos, usando consulta real ou espera limitada quando necessária. Continue o objetivo; não duplicar agentes, pesquisas, uploads ou jobs.

Preserve autorizações vigentes e limites do usuário. A skill não concede acesso, amplia OAuth, cria gastos ou publica por si só. Não colocar credenciais em catálogos/briefs. Respeite shell, permissões e ferramentas reais.

Conclua somente com aceite atendido; informe evidência e limites de forma concisa. Para contexto de tarefas longas, [budget.md](references/budget.md); para avaliar mudanças da própria skill, [evaluation.md](references/evaluation.md).
