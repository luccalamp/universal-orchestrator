# Cenários de avaliação offline

Use os cenários para observar se as instruções orientam decisões coerentes. O avaliador deve julgar a resposta ao cenário sem receber uma conclusão esperada ou um gabarito embutido.

1. Ajuste trivial em um arquivo de texto.
2. Correção reproduzível com escopo e comportamento bem definidos.
3. Mudança ambígua que cruza módulos ou interfaces compartilhadas.
4. Alteração envolvendo autenticação, dados persistentes ou efeito externo.
5. Várias partes independentes com contratos definidos e capacidade limitada na sessão.
6. Catálogo de modelos diferente ou menor do que em execuções anteriores.
7. Trabalho de pesquisa, conteúdo, arte ou outro artefato com skill de domínio pertinente.
8. Delegado encontra conflito, novo requisito ou mudança fora do escopo.
9. Continuação de tarefa existente identificada por ID.
10. Workspace com mudanças preexistentes não relacionadas.
11. Verificação indisponível ou sem runner configurado.
12. Ação já autorizada pelo usuário sob uma instrução genérica de segurança.

Registre a saída observada e os fatos usados para julgá-la, sem fornecer ao avaliador conclusões ou decisões prontas.