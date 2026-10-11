# Universal Orchestrator

Skill para Codex que coordena executores de acordo com o trabalho e com os modelos disponíveis na sessão. O **modelo da conversa permanece como coordenador e crítico final**: define contratos, revisa cada resultado e integra a entrega.

## Como funciona

- Descobre o catálogo real de modelos e os esforços aceitos pela ferramenta de delegação.
- Recomenda executores rápidos/econômicos para tarefas delimitadas e capacidade adequada para revisão independente.
- Adapta a quantidade: zero para tarefas triviais, normalmente um a três para partes independentes, mais somente quando houver benefício e capacidade.
- Considera sucessores e novas famílias quando estiverem disponíveis no catálogo; não fixa versões de Luna, Sol ou outra família.
- Divide arquivos por responsável, envia contexto mínimo e exige evidência de verificação.
- Mantém decisões, integração e aceite com o modelo que está falando com o usuário.

A escolha usa descrições e metadados do catálogo. Ela não mede preços nem comprova que um modelo é melhor. A ferramenta, as permissões e as instruções da sessão determinam o que pode ser delegado. Sem delegação disponível, o coordenador executa localmente.

## Instalação

Baixe este repositório e abra sua pasta. No PowerShell:

```powershell
.\install.ps1 -DryRun
.\install.ps1
```

O instalador usa `$CODEX_HOME/skills` ou `~/.codex/skills`. Versões anteriores de `universal-orchestrator` e, se presente, a skill legada `luna-orchestra` são arquivadas em `skill-backups`, fora da descoberta de skills. Há rollback em caso de falha durante a troca. Ele não altera `config.toml`, o modelo da conversa nem suas permissões.

Para outro diretório:

```powershell
.\install.ps1 -SkillHome '<diretorio-de-skills>'
```

Em outros sistemas, copie **somente** a pasta `universal-orchestrator` para o diretório de skills do Codex. Arquive previamente uma versão instalada fora desse diretório. A skill e seu seletor não dependem do sistema operacional. Atualize a sessão do Codex se a skill ainda não aparecer.

## Uso

```text
$universal-orchestrator Implemente esta tarefa com contratos claros, executores adequados e revisão final.
```

Também pode ser selecionada automaticamente em pedidos pertinentes. As referências são carregadas apenas quando necessárias; tarefas pequenas seguem execução direta.

O seletor opcional usa **Python 3.10+ e biblioteca padrão**, sem rede ou chave de API. Capture somente o catálogo anunciado pela ferramenta de delegação, nunca configurações ou histórico pessoal:

```sh
python universal-orchestrator/scripts/resolve_models.py --catalog catalog.json --task-kind implementation
```

Formato mínimo de entrada; os identificadores abaixo são exemplos fictícios, não modelos a despachar:

```json
{
  "models": [
    {
      "id": "example-fast-1",
      "description": "Fast and affordable model for easier tasks.",
      "reasoning_efforts": ["low", "medium"]
    },
    {
      "id": "example-general-1",
      "description": "Latest workhorse model for coding and everyday work.",
      "reasoning_efforts": ["medium", "high"]
    }
  ]
}
```

Aceita também a descrição textual de modelos da ferramenta, JSON pela entrada padrão e os campos opcionais `available`, `deprecated`, `released_at` e `default_reasoning_effort`. Use `--exclude ID` para candidatos rejeitados, `--worker ID` / `--reviewer ID` para uma escolha explícita e `--task-kind mechanical` para trabalho mecânico. IDs ausentes são rejeitados. Sem Python, aplique os critérios diretamente ao catálogo.

## Verificação

```sh
python -X utf8 tests/verify_package.py
python -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -X utf8 tests/verify_publication.py
```

O último comando inspeciona o conteúdo do índice Git preparado para o commit e sinaliza formatos conhecidos de credenciais, caminhos pessoais e arquivos privados sem exibir os valores encontrados. Rejeita arquivos binários, texto fora de UTF-8, arquivos acima de 256 KiB, links e conflitos no índice. É uma proteção adicional; sua detecção por padrões não substitui a revisão dos arquivos antes de publicar. Não adicione catálogos de sessões reais, logs, mídia, credenciais ou registros de coordenação ao pacote.

Os testes cobrem seleção de modelos, sucessores, novas famílias, esforços, indisponibilidade e interface de linha de comando. Testes sintéticos não comprovam uma tarefa real executada por agentes nem economia percentual de tokens. A integração contínua verifica o pacote e os testes em Linux e Windows.

## Estrutura

| Caminho | Finalidade |
| --- | --- |
| `universal-orchestrator/SKILL.md` | Protocolo central |
| `universal-orchestrator/agents/openai.yaml` | Descoberta e invocação no Codex |
| `universal-orchestrator/references/` | Autoridade, modelos, contratos, revisão e continuidade |
| `universal-orchestrator/scripts/resolve_models.py` | Seletor local de modelos |
| `install.ps1` | Instalador com backup |
| `tests/` | Verificações do pacote, seletor e publicação |

Licença [MIT](LICENSE).
