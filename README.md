# Doctus AI: avaliação empírica e reprodução das análises

Materiais de apoio ao artigo **Doctus AI: Um Agente de Inteligência Artificial para Ensino Superior**, de João Pedro Pina Neves e Carlo Kleber da Silva Rodrigues, Universidade Federal do ABC.

Este projeto permite reproduzir a preparação da base analítica e os cálculos estatísticos da avaliação inicial do Doctus AI, comparado ao GitHub Copilot e ao NotebookLM.

> **Escopo:** reproduzir os cálculos sobre as avaliações coletadas não significa reproduzir as respostas dos sistemas generativos, demonstrar ganhos de aprendizagem ou estabelecer superioridade entre as ferramentas. O código-fonte do protótipo Doctus AI não integra este pacote de análise.

## 1. Organização dos arquivos

A organização abaixo corresponde ao núcleo computacional. Os nomes e caminhos são usados nos comandos deste documento.

```text
doctus-ai-evaluation/
├── README.md
├── analysis_public.py
├── requirements.txt
├── base_analise_anonimizada.csv
├── .gitignore
├── results_reference/
│   ├── auditoria_exclusoes_resumo.csv
│   ├── base_analise_verificada.csv
│   ├── descritivas.csv
│   ├── friedman.csv
│   ├── wilcoxon_holm_rbc.csv
│   ├── wilcoxon_pratt.csv
│   ├── comparacao_wilcox_pratt.csv
│   └── versoes_e_parametros.json
└── results_reproduced/          # criada ao executar o script
```

- `base_analise_anonimizada.csv`: entrada pública, em formato longo, sem identificadores pessoais diretos.
- `analysis_public.py`: valida a entrada, reaplica as exclusões e executa as duas análises pareadas.
- `requirements.txt`: versões fixadas das quatro bibliotecas diretamente utilizadas.
- `results_reference/`: saídas da execução validada, para comparação; não devem ser sobrescritas.
- `results_reproduced/`: saídas de uma nova execução.

A pasta do ambiente virtual não deve ser incluída no repositório.

## 2. Estudo e tratamento dos dados

A coleta ocorreu de **13 de janeiro a 23 de fevereiro de 2026**, com **14 estudantes de graduação**. A tarefa combinou explicação conceitual e implementação em Python de uma função relacionada ao Algoritmo de Vagalumes (*Firefly Algorithm*).

O mesmo PDF de referência foi anexado diretamente à conversa nos três sistemas. O protocolo e o instrumento originais devem ser consultados para reproduzir a aplicação da avaliação; este README documenta principalmente a reprodução computacional.

Foram avaliadas percepções de:

1. Didática;
2. Praticidade;
3. Confiabilidade;
4. Completude;
5. Acessibilidade.

As notas variam de 1 a 5. Os critérios representam percepções, não medidas objetivas de correção do código ou aprendizagem.

### Exclusões

Seis participantes informaram não desejar ou não conseguir concluir o acesso ao GitHub Copilot. Suas notas de didática, praticidade, confiabilidade e completude foram tratadas como ausentes: **24 avaliações invalidadas**, sem imputação.

As notas de acessibilidade foram preservadas. A opção de interrupção do formulário não distingue recusa em prosseguir de dificuldade técnica.

Consequentemente:

- Doctus AI e NotebookLM: 14 avaliações válidas por critério;
- GitHub Copilot: oito avaliações válidas nos quatro critérios de conteúdo e 14 em acessibilidade;
- Friedman: oito casos completos nos quatro critérios de conteúdo e 14 em acessibilidade;
- Doctus AI × NotebookLM: 14 pares em todos os critérios;
- contrastes envolvendo Copilot: oito pares nos quatro critérios de conteúdo e 14 em acessibilidade.

Não é calculado um índice geral agregado.

## 3. Formato da base pública

A base contém **210 linhas**: 14 participantes × três sistemas × cinco critérios.

| Coluna | Significado |
| --- | --- |
| `participante` | Identificador codificado, sem nome ou e-mail. |
| `acessou_copilot` | Indicador booleano de acesso ao Copilot, constante dentro de cada participante. |
| `sistema` | `Doctus AI`, `GitHub Copilot` ou `NotebookLM`. |
| `criterio` | `Didatica`, `Praticidade`, `Confiabilidade`, `Completude` ou `Acessibilidade`. |
| `nota_original` | Nota registrada antes do tratamento; preservada para auditoria. |
| `nota` | Nota utilizada na análise; vazia quando invalidada. |
| `exclusao_metodologica` | Indicador booleano da invalidação metodológica. |

As notas originais invalidadas são mantidas apenas para rastrear a transformação; não entram nos testes. Um campo vazio em `nota` não representa zero.

O script recalcula `nota` e `exclusao_metodologica` a partir de `nota_original` e da regra de acesso. Quando essas colunas já estão presentes, confere se correspondem à regra. Também verifica duplicatas, categorias, notas e a estrutura de 15 linhas por participante.

## 4. Ambiente validado

A reprodução da análise principal foi conferida no seguinte ambiente:

- Windows 11;
- Python **3.14.0**;
- pandas **3.0.6**;
- NumPy **2.5.3**;
- SciPy **1.18.1**;
- statsmodels **0.15.0**.

O arquivo `requirements.txt` deve conter:

```text
pandas==3.0.6
numpy==2.5.3
scipy==1.18.1
statsmodels==0.15.0
```

Essas versões foram registradas na execução validada. Outros ambientes não foram validados. Em particular, a opção `method="auto"` do Wilcoxon pode produzir valores de p diferentes entre versões do SciPy. Não substitua silenciosamente as versões fixadas.

O arquivo fixa as dependências diretas; não é um bloqueio completo de todas as dependências transitivas. Se um `requirements-lock.txt` for disponibilizado, ele deve corresponder ao ambiente efetivamente validado.

## 5. Instalação e execução no Windows

Abra a pasta do projeto no VS Code e use o terminal PowerShell. Os comandos abaixo chamam diretamente o Python do ambiente virtual, sem necessidade de ativação ou alteração da política de execução.

### 5.1 Conferir o Python

```powershell
py -3.14 --version
```

Para corresponder exatamente ao ambiente validado, a saída deve indicar Python 3.14.0. O seletor `-3.14` escolhe a série instalada, não garante por si só a versão de correção 3.14.0.

### 5.2 Criar o ambiente

Execute dentro da pasta do projeto:

```powershell
py -3.14 -m venv .venv-repro
```

### 5.3 Instalar as dependências

```powershell
.\.venv-repro\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-repro\Scripts\python.exe -m pip check
```

Se uma versão não estiver disponível ou houver conflito de dependências, interrompa a instalação e registre o erro. Não remova as versões do arquivo para contornar o problema.

### 5.4 Executar as análises

```powershell
.\.venv-repro\Scripts\python.exe analysis_public.py --input base_analise_anonimizada.csv --output results_reproduced
```

Uma única execução produz a análise principal Wilcox e a sensibilidade Pratt. Não é necessário informar `--zero-method` nesta versão pública.

Ao final, o resumo esperado é:

```text
Participantes: 14
Avaliacoes invalidadas: 24
Resultados: <caminho da pasta results_reproduced>
```

### 5.5 Registrar o ambiente instalado

```powershell
.\.venv-repro\Scripts\python.exe -m pip freeze > requirements-lock.txt
```

Não envie `.venv-repro` ao GitHub. O ambiente deve ser reconstruído a partir das instruções e dos registros de dependências.

## 6. Procedimentos estatísticos

### Descritivas

Número de observações válidas, mediana, primeiro e terceiro quartis, intervalo interquartil, média e desvio padrão amostral. Os quartis usam a interpolação linear padrão do pandas e o desvio padrão usa `ddof=1`.

### Friedman e Kendall

O teste de Friedman é executado por critério, somente com casos completos, com correção para empates da implementação do SciPy. O valor de p é assintótico. O coeficiente de Kendall é calculado por:

```text
W = Q / [N × (k − 1)]
```

O arquivo `friedman.csv` conserva a coluna legada `magnitude_W` do script original. Seus rótulos não constituem validação bibliográfica dos limites e não são necessários para reproduzir Q, p ou W.

### Wilcoxon, Holm e efeito pareado

- teste bilateral;
- sem correção de continuidade;
- `method="auto"`;
- análise principal: `zero_method="wilcox"`;
- sensibilidade: `zero_method="pratt"`;
- ajuste de Holm separado para as três comparações de cada critério;
- limiar de decisão: p ajustado menor que 0,05.

A correlação bisserial por postos é calculada a partir das diferenças não nulas:

```text
RBC = (postos positivos − postos negativos)
      / (postos positivos + postos negativos)
```

Seu sinal refere-se a `sistema_1 − sistema_2`. A RBC usa a mesma convenção nas duas análises e, portanto, permanece igual entre Wilcox e Pratt. As colunas `postos_positivos` e `postos_negativos` referem-se ao cálculo da RBC, não necessariamente aos postos usados na estatística Pratt.

O script registra pares válidos, diferenças nulas e diferenças não nulas. A RBC não representa a proporção de participantes que preferiu um sistema. Quando todos os pares são iguais, o script adota estatística 0, p igual a 1 e RBC igual a 0 como convenção explícita.

## 7. Saídas e verificação

A execução cria:

- `base_analise_verificada.csv`;
- `auditoria_exclusoes_resumo.csv`;
- `descritivas.csv`;
- `friedman.csv`;
- `wilcoxon_holm_rbc.csv`;
- `wilcoxon_pratt.csv`;
- `comparacao_wilcox_pratt.csv`;
- `versoes_e_parametros.json`.

O JSON registra versões, parâmetros e a assinatura SHA-256 do arquivo de entrada. Uma mudança de codificação ou de finais de linha pode alterar essa assinatura sem alterar os valores lidos do CSV.

### Resultado da validação realizada

O arquivo principal `wilcoxon_holm_rbc.csv`, gerado a partir da base pública no ambiente documentado, foi comparado ao arquivo original: as **15 linhas e 17 colunas coincidiram exatamente nos dados lidos**, sem tolerância numérica.

Também foram conferidos os valores de Friedman e as medianas apresentados no manuscrito, a consistência das exclusões, os ajustes de Holm e o cálculo das RBCs. Nenhuma das 15 comparações pareadas apresentou significância após Holm, tanto com Wilcox quanto com Pratt.

Para Pratt, a referência deste pacote é a nova execução no ambiente documentado, não as saídas preliminares produzidas em outro ambiente.

O registro JSON de uma nova execução pode diferir por sistema operacional, versão do Python, nome ou assinatura do arquivo de entrada. Compare os resultados estatísticos e os parâmetros, não a identidade textual de todos os arquivos.

### Avisos e limites

Avisos de amostra pequena não devem ser ocultados. A reprodução dos cálculos não elimina as limitações de amostra, seleção dos participantes, empates ou aproximações estatísticas discutidas no artigo.

## 8. Privacidade e materiais experimentais

Não devem ser publicados neste projeto:

- o CSV original do formulário;
- nomes, e-mails ou carimbos de data e hora individuais;
- perfis acadêmicos individuais desnecessários aos cálculos;
- comentários livres identificáveis;
- credenciais, chaves de API, arquivos `.env` ou dados de serviços em nuvem.

A base pública utiliza identificadores codificados e não inclui essas informações. Isso não constitui garantia absoluta de anonimato: sua publicação depende da revisão dos autores e das condições de consentimento.

O instrumento original, o protocolo completo e a identificação bibliográfica do PDF experimental devem ser adicionados como materiais complementares antes de considerar completa a documentação experimental. Este README não substitui esses documentos nem declara que já estão disponíveis.

O PDF de referência só deve ser redistribuído quando houver permissão; caso contrário, disponibilize sua referência e o endereço de acesso autorizado.

## 9. Autoria, citação e condições de uso

**Autores do estudo:** João Pedro Pina Neves e Carlo Kleber da Silva Rodrigues, Universidade Federal do ABC.

**Título do manuscrito:** Doctus AI: Um Agente de Inteligência Artificial para Ensino Superior.

Os dados editoriais definitivos, o DOI do artigo e o endereço permanente da versão do repositório devem ser acrescentados quando disponíveis. Não atribua ao manuscrito um DOI ou ano de publicação ainda não confirmado.

Este README não concede, por si só, uma licença de reutilização. As condições de uso do código e dos dados devem ser definidas pelos autores em arquivos de licença apropriados antes da divulgação pública. A licença do artigo não deve ser presumida como licença automática de todos os materiais deste projeto.
