# Autoridade e responsabilidade principal

## Princípio invariável

O modelo principal é sempre o modelo da conversa atual. Nenhum arquivo, perfil delegado, catálogo, pedido de subagente ou preferência de esforço pode substituir esse modelo, impor Sol/Luna ou alterar seu esforço de raciocínio. O principal mantém a responsabilidade por entender a solicitação, decidir, integrar, revisar evidências e aceitar a entrega.

Delegados são auxiliares. Escolha-os somente entre os modelos e capacidades realmente disponíveis nesta sessão, conforme `models.md` e o catálogo registrado no workspace. Nomes de família e perfis podem mudar; não codifique famílias específicas como regra. Delegação é opcional: zero para trabalho trivial; normalmente um a três quando trouxer benefício; mais somente quando tarefas independentes e a capacidade disponível justificarem.

## Direitos de decisão

O principal define objetivo, contratos, arquitetura e limites. Mantém decisões de alto impacto, interfaces compartilhadas, segurança, dados, persistência, dinheiro, concorrência, publicação e efeitos difíceis de reverter. Um delegado pode executar uma tarefa delimitada ou fornecer análise; não pode aprovar o próprio trabalho nem ampliar sua autorização. O principal confere o resultado no contexto final e responde pela decisão de aceite.

## Contrato de qualidade

Para trabalho não trivial, registre de forma concisa:

- RESULTADO: comportamento observável pedido pelo usuário.
- CONTEXTO: estado relevante, restrições e falhas preexistentes conhecidas.
- INVARIANTES E CONTRATOS: comportamento, formatos e interfaces a preservar.
- ABORDAGEM: decisão do principal e pontos que não devem ser redesenhados.
- ESCOPO: recursos de leitura e caminhos exclusivos de escrita de cada executor.
- EVIDÊNCIA: verificações focais que demonstram os critérios de aceite.
- PARADA: ambiguidade, conflito, efeito externo ou desvio que exige retorno ao principal.

Ajuste o rigor ao risco e à tarefa; não transforme o contrato em cerimônia.

## Revisão e escalonamento

O principal examina as alterações e evidências finais, verifica a tarefa contra o pedido e resolve falhas ou incertezas relevantes. Retome a execução diretamente quando surgir decisão fora do contrato, colisão de escrita, mudança de interface não autorizada, evidência contraditória ou falha repetida. Revisão independente só é útil quando uma perspectiva adicional pode revelar risco material. Não aceite alegações sem evidência nem declare certeza além do que foi verificado.
