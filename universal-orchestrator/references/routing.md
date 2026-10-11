# Roteamento adaptável por tarefa e sessão

## Escolha do caminho

Avalie simplicidade, ambiguidade, risco, acoplamento, possibilidade de verificação e independência entre partes. O modelo principal permanece o modelo desta conversa, com seu esforço atual. Consulte `models.md` para selecionar delegados do catálogo real e das capacidades disponíveis nesta sessão; não fixe nomes de modelo, famílias ou esforço imposto.

- DIRETO: tarefa trivial ou coesa; principal executa, zero delegados.
- ASSISTIDO: incerteza ou risco; principal decide e executa, podendo solicitar análise independente de leitura.
- DELEGADO: contrato estável, escopo separável e evidência focal; delegados podem executar partes exclusivas e limitadas.
- SENSÍVEL: decisões de segurança, dados, dinheiro, interfaces críticas ou efeitos externos ficam com o principal; assistência costuma ser de leitura.

A quantidade é adaptável: zero para trivial, um a três quando útil; mais somente quando a independência real e a capacidade da sessão sustentarem a divisão. Disponibilidade de perfis não é meta de utilização.

## Autorização de escrita delegada

Delegue escrita apenas quando o principal puder definir resultado, abordagem e caminhos de escrita exclusivos; contratos estiverem claros; houver verificação proporcional; e a integração permanecer sob controle do principal. Se alguma condição falhar, mantenha a execução com o principal ou limite a ajuda à leitura. Não permita que delegados criem agentes descendentes ou apliquem a orquestração em cascata.

## Paralelismo e continuação

Paralelize somente partes independentes, com donos de escrita distintos. Serialize alterações em recursos compartilhados e integração. Ao continuar trabalho delegado, retome pelos IDs de tarefa existentes e leia seu estado; não recrie tarefas concluídas ou em andamento. Se a ferramenta não permitir continuação, prossiga sequencialmente e registre a limitação.

## Fallback

Sem capacidade de delegação ou modelo auxiliar adequado no catálogo desta sessão, o principal prossegue por conta própria. Reduza a divisão, não a qualidade necessária para o resultado. Use a skill de domínio pertinente quando a tarefa envolver uma área especializada, em qualquer disciplina ou tipo de artefato.