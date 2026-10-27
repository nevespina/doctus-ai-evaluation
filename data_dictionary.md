# Dicionário dos dados

## 1. Arquivo e unidade de observação

Este documento descreve `base_analise_anonimizada.csv`, entrada do script público `analysis_public.py`, e `base_analise_verificada.csv`, saída que contém os mesmos campos após a validação e a reaplicação das regras de preparação.

Cada linha representa **a avaliação de um sistema por um participante em um critério**. A chave composta é:

```text
participante + sistema + criterio
```

Não deve existir mais de uma linha com a mesma combinação. A base do estudo contém **210 linhas e sete colunas**, correspondentes a 14 participantes, três sistemas e cinco critérios. As linhas cujas notas foram invalidadas permanecem na base para preservar a estrutura e a rastreabilidade.

## 2. Formato do arquivo

- Formato: CSV.
- Separador de campos: vírgula (`,`).
- Codificação utilizada nas exportações: UTF-8 com BOM (`utf-8-sig`).
- Separador decimal: ponto (`.`).
- Booleanos exportados: `True` e `False`.
- Ausência de nota: campo vazio, interpretado como `NaN` pelo pandas.
- As notas podem aparecer como `5.0`, mas representam categorias inteiras de 1 a 5.
- Os nomes das colunas e os valores de `sistema` e `criterio` devem ser preservados exatamente como definidos abaixo.

## 3. Definição das variáveis

| Variável | Tipo lógico | Valores permitidos | Ausência na base do estudo | Definição |
| --- | --- | --- | --- | --- |
| `participante` | Texto; identificador codificado | `P01` a `P14` nesta base | Não | Identifica o mesmo participante nas avaliações dos três sistemas e dos cinco critérios. Não contém nome ou e-mail. |
| `acessou_copilot` | Booleano | `True`, `False` | Não | Indica se o participante prosseguiu com o acesso ao GitHub Copilot segundo a codificação do formulário. É constante nas 15 linhas do participante. |
| `sistema` | Categoria nominal | `Doctus AI`, `GitHub Copilot`, `NotebookLM` | Não | Sistema ao qual a avaliação se refere. |
| `criterio` | Categoria nominal | `Didatica`, `Praticidade`, `Confiabilidade`, `Completude`, `Acessibilidade` | Não | Dimensão de percepção avaliada. |
| `nota_original` | Categoria ordinal, armazenada numericamente | 1, 2, 3, 4 ou 5 | Não | Nota registrada no formulário antes do tratamento metodológico. Inclui notas posteriormente invalidadas. |
| `nota` | Categoria ordinal, armazenada numericamente | 1, 2, 3, 4, 5 ou campo vazio | Sim: 24 campos vazios | Nota efetivamente utilizada nas estatísticas. É igual à nota original, exceto nas avaliações invalidadas. |
| `exclusao_metodologica` | Booleano | `True`, `False` | Não | Indica se a nota daquela linha foi invalidada pela regra de não acesso ao Copilot. Não significa exclusão integral do participante. |

### 3.1 Identificador do participante

O código permite parear avaliações sem publicar identificadores pessoais diretos. A numeração não deve ser interpretada como característica acadêmica, classificação ou desempenho.

A codificação não garante anonimato absoluto. Não se deve publicar uma tabela de correspondência entre códigos e identidades, nem associar estes códigos a perfis acadêmicos ou comentários identificáveis.

### 3.2 Indicador de acesso ao Copilot

- `True`: participante codificado como tendo prosseguido com a tarefa do Copilot.
- `False`: participante informou não desejar ou não conseguir concluir a ativação.

Na conversão original do formulário, a ausência de marcação na opção de interrupção foi interpretada como continuidade da tarefa. Portanto, o indicador deriva da resposta ao formulário, não de logs independentes de autenticação ou utilização.

A opção de interrupção agrupava recusa e dificuldade de ativação; a base não permite distinguir esses motivos. O indicador refere-se somente ao Copilot, mesmo quando aparece em uma linha do Doctus AI ou do NotebookLM.

### 3.3 Escala das notas

A escala varia de **1, percepção mais negativa, a 5, percepção mais positiva**. Não se atribuem neste dicionário rótulos intermediários que não tenham sido confirmados no instrumento original.

As notas representam percepções dos participantes, não medidas diretas de aprendizagem, correção técnica ou desempenho dos sistemas.

## 4. Critérios avaliados

As descrições abaixo sintetizam o significado analítico dos critérios. Não substituem a redação literal das perguntas do instrumento original.

| Valor no CSV | Nome no artigo | Significado analítico |
| --- | --- | --- |
| `Didatica` | Didática | Percepção de clareza e facilidade de compreensão da explicação. |
| `Praticidade` | Praticidade | Percepção sobre a funcionalidade e a correção do código apresentado. |
| `Confiabilidade` | Confiabilidade | Percepção de correção e fidelidade ao material de referência. |
| `Completude` | Completude | Percepção de equilíbrio e integração entre explicação conceitual e implementação. |
| `Acessibilidade` | Acessibilidade | Percepção das condições de acesso e utilização do sistema, incluindo a etapa de ativação. |

## 5. Regra de preparação e exclusão

A regra aplica-se quando as condições abaixo ocorrem simultaneamente:

1. `acessou_copilot` é `False`;
2. `sistema` é `GitHub Copilot`;
3. `criterio` é `Didatica`, `Praticidade`, `Confiabilidade` ou `Completude`;
4. `nota_original` está preenchida.

Nessas linhas:

```text
nota = campo vazio
exclusao_metodologica = True
```

Nas demais linhas da base do estudo:

```text
nota = nota_original
exclusao_metodologica = False
```

O script público recalcula esses dois campos a partir das colunas de origem. Se os campos já estiverem presentes no CSV, confere sua concordância com a regra e interrompe a execução em caso de divergência.

### 5.1 Efeito da regra na base

- Seis participantes foram codificados como não tendo prosseguido com o Copilot.
- Quatro notas de conteúdo foram invalidadas por participante, totalizando **24 notas**.
- As **14 avaliações de acessibilidade do Copilot foram mantidas**.
- As notas de Doctus AI e NotebookLM não foram alteradas.
- Nenhuma linha ou participante foi integralmente removido.
- Não houve imputação de valores.
- `nota_original` permanece preenchida para permitir auditoria, mas os cálculos usam exclusivamente `nota`.

## 6. Valores ausentes e interpretação

Nesta base, os 24 campos vazios em `nota` decorrem exclusivamente da regra metodológica descrita acima. Não representam nota zero, recusa em avaliar todos os sistemas ou ausência de participação no estudo.

A manutenção das notas de acessibilidade não significa que os seis participantes tenham utilizado integralmente o Copilot. Essas notas foram preservadas porque o processo de entrada integra a interpretação do critério. Seus significados podem ser heterogêneos, como discutido no artigo.

Não se deve preencher os campos vazios com zero, com a média ou com a nota original invalidada.

## 7. Contagens esperadas

### 7.1 Estrutura geral

| Verificação | Valor esperado |
| --- | ---: |
| Participantes distintos | 14 |
| Sistemas distintos | 3 |
| Critérios distintos | 5 |
| Linhas por participante | 15 |
| Total de linhas | 210 |
| Notas originais preenchidas | 210 |
| Notas válidas para análise | 186 |
| Notas invalidadas | 24 |
| Participantes com `acessou_copilot=False` | 6 |

### 7.2 Notas válidas por sistema

| Critério | Doctus AI | GitHub Copilot | NotebookLM |
| --- | ---: | ---: | ---: |
| Didática | 14 | 8 | 14 |
| Praticidade | 14 | 8 | 14 |
| Confiabilidade | 14 | 8 | 14 |
| Completude | 14 | 8 | 14 |
| Acessibilidade | 14 | 14 | 14 |

### 7.3 Conjuntos utilizados nos testes

- **Friedman:** oito participantes com observações completas nos quatro critérios de conteúdo e 14 em acessibilidade.
- **Doctus AI × NotebookLM:** 14 pares em todos os critérios.
- **Contrastes envolvendo Copilot:** oito pares nos quatro critérios de conteúdo e 14 em acessibilidade.

As estatísticas descritivas usam todas as notas válidas de cada sistema e critério. Por isso, suas composições amostrais podem diferir das comparações globais por casos completos.

## 8. Verificações de integridade

Para a base deste estudo, devem ser verificadas:

- unicidade da chave `participante + sistema + criterio`;
- presença das 15 combinações de sistema e critério por participante;
- ausência de identificadores vazios;
- constância de `acessou_copilot` dentro de cada participante;
- notas originais inteiras entre 1 e 5;
- correspondência entre `nota`, `nota_original` e o indicador de exclusão;
- exatamente 24 exclusões e 24 notas ausentes;
- preservação das notas de acessibilidade;
- ausência de dados pessoais diretos e de colunas adicionais desnecessárias à análise.

O script valida a estrutura e a regra de transformação. As contagens específicas de 14 participantes e 24 exclusões também devem ser conferidas ao comparar com a versão publicada do estudo; o script não deve ser interpretado como impondo esses números a qualquer nova pesquisa.

## 9. Relação com os arquivos de resultados

- `auditoria_exclusoes_resumo.csv`: agrega as contagens por sistema e critério.
- `descritivas.csv`: descreve a distribuição de `nota` entre observações válidas.
- `friedman.csv`: usa casos completos por critério.
- `wilcoxon_holm_rbc.csv`: análise principal com procedimento Wilcox.
- `wilcoxon_pratt.csv`: análise de sensibilidade com procedimento Pratt.
- `comparacao_wilcox_pratt.csv`: compara valores de p, RBC e decisões após Holm.
- `versoes_e_parametros.json`: registra o ambiente, os parâmetros e a assinatura do arquivo de entrada.

Este dicionário descreve a base de avaliações, não substitui a documentação das colunas estatísticas desses resultados. Para comandos de execução e parâmetros, consulte o `README.md` e o script.

## 10. Privacidade e limites de utilização

A base não contém nomes, e-mails, carimbos de data e hora, instituições, cursos, semestres ou comentários livres. O CSV original do formulário e qualquer correspondência entre identificadores e pessoas devem permanecer fora do repositório público.

A publicação deve observar o consentimento e a revisão dos autores. Este documento não concede uma licença de reutilização nem constitui garantia absoluta de anonimato. As condições de uso devem ser definidas separadamente no repositório.
