# Material de referência da tarefa

## Identificação do documento utilizado

- **Título apresentado no documento:** O Algoritmo de Enxame de Vagalumes (Firefly Algorithm).
- **Nome do arquivo fornecido:** `O Algoritmo de Enxame de Vagalumes (Firefly Algorithm).pdf`.
- **Extensão:** três páginas.
- **Natureza:** material explicativo adaptado para o experimento, conforme declaração na introdução do próprio documento.
- **Responsável pela adaptação:** João Pedro Pina Neves, conforme confirmação do próprio responsável. O PDF original não apresenta essa identificação no corpo do documento.
- **Data da adaptação:** janeiro de 2026, conforme confirmação do responsável. Essa data não consta no corpo do PDF original.
- **Periódico, evento, editora ou repositório:** não identificados no documento.
- **DOI ou endereço de publicação:** não identificados no documento.

O documento menciona Xin-She Yang e 2008 ao apresentar a origem do algoritmo. Essa menção não identifica a autoria nem a data de elaboração deste material adaptado.

## Conteúdo e localização

1. **Página 1:** introdução, conceitos centrais e regras de comportamento.
2. **Página 2:** formulação matemática da distância, da atratividade e do movimento.
3. **Página 3:** explicação dos termos do movimento, pseudocódigo e aplicações.

A seção diretamente relacionada à tarefa é **“Equação 2: A Atratividade (Beta)”**, na página 2, que apresenta:

```text
β(r) = β₀ · exp(−γr²)
```

O material descreve a atratividade base, o coeficiente de absorção e o quadrado da distância.

## Utilização no estudo

O mesmo PDF foi anexado diretamente à conversa no Doctus AI, no GitHub Copilot e no NotebookLM, conforme informado pelo responsável pela coleta. Foi utilizado como contexto para a tarefa de explicação da diminuição da atratividade com a distância e implementação da função em Python.

O documento deve ser identificado no artigo como material explicativo adaptado para o experimento. Não há elementos no PDF fornecido que permitam classificá-lo como artigo científico publicado.

## Preservação da versão experimental

Para documentar o experimento, deve ser preservada a cópia efetivamente fornecida aos participantes. Eventuais revisões posteriores devem ser identificadas como novas versões, sem substituir silenciosamente o material original.

A identificação deste arquivo não constitui uma validação técnica integral de seu conteúdo ou de suas equações.

## Disponibilização

Antes de incluir o PDF no repositório público, os responsáveis devem confirmar sua autoria, procedência e permissão de redistribuição. Não se presume uma licença a partir da ausência de indicação no documento.

Caso a publicação seja autorizada, recomenda-se armazenar a cópia original em:

```text
materials/O Algoritmo de Enxame de Vagalumes (Firefly Algorithm).pdf
```

## Identificação da cópia

Para registrar a assinatura SHA-256 da cópia utilizada, execute no PowerShell, dentro da pasta que contém o PDF:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "O Algoritmo de Enxame de Vagalumes (Firefly Algorithm).pdf"
```

- **SHA-256:** a preencher com a saída do comando sobre a cópia original.

A assinatura identifica os bytes do arquivo, não comprova autoria e não concede permissão de redistribuição.

## Pendências

- Confirmar a permissão de publicação da cópia original.
- Registrar a assinatura SHA-256.

## Fontes informadas pelo responsável pela adaptação

O responsável informou os três endereços abaixo como fontes utilizadas na preparação do material. São publicações distintas; não constituem a identificação bibliográfica do PDF adaptado.

1. **Couto, Deylon Carlo Fidelis; Silva, Carlos Alexandre.** Algoritmo Colônia de Vaga-lumes Aplicado na Otimização de Funções N-dimensionais. *Proceeding Series of the Brazilian Society of Computational and Applied Mathematics*, v. 3, n. 2, 2015. DOI: https://doi.org/10.5540/03.2015.003.02.0109. Registro: https://proceedings.sbmac.org.br/sbmac/article/view/1006.
2. **Desenvolvimento de um Algoritmo Multi-Populacional Auto-Adaptativo para a Resolução de Problemas de Otimização.** *Revista Cereus*, v. 10, n. 2, p. 252–275. DOI: https://doi.org/10.18605/2175-7275/cereus.v10n2p252-275. PDF informado: https://ojs.unirg.edu.br/index.php/1/article/download/2216/639/7688. A autoria completa deve ser conferida no registro editorial antes de gerar uma entrada bibliográfica definitiva.
3. **Paiva, F. A. P.; Leite, I. V. O.; Marcone, M. H. F.** Um breve estudo sobre os algoritmos do vaga-lume e do morcego para otimização de funções de referência. *HOLOS*, 2018. DOI: https://doi.org/10.15628/holos.2018.5487. PDF informado: https://www2.ifrn.edu.br/ojs/index.php/HOLOS/article/download/5487/pdf/19826.

As datas dessas fontes não determinam a data de elaboração da adaptação. A inclusão dos endereços não implica autorização para redistribuir os textos das publicações.
