# Protocolo experimental

## Status e escopo

Este documento registra o procedimento descrito pelos autores para a avaliação inicial do Doctus AI em comparação com GitHub Copilot e NotebookLM. Não é um protocolo pré-registrado. As informações não disponíveis estão explicitamente indicadas.

A reprodução das análises sobre os dados coletados é documentada no README e no script público. Uma nova aplicação da tarefa não garante respostas idênticas dos sistemas generativos.

## Objetivo

Investigar as percepções de estudantes sobre o suporte oferecido pelos três sistemas em uma tarefa que combina explicação conceitual e implementação em Python.

## Participantes e período

- Participação voluntária de 14 estudantes de graduação.
- Amostra por conveniência.
- Coleta entre 13 de janeiro e 23 de fevereiro de 2026.
- Apresentação do Termo de Consentimento Livre e Esclarecido antes do preenchimento do formulário.

Este documento não declara aprovação ou dispensa de apreciação ética não documentada.

## Sistemas e tarefa

Sistemas avaliados: Doctus AI, GitHub Copilot e NotebookLM.

Tema: Inteligência de Enxame, especificamente a função de atratividade do Algoritmo de Vagalumes (Firefly Algorithm).

Material: um mesmo artigo técnico em PDF, anexado diretamente à conversa em cada um dos três sistemas, conforme informado pelo responsável pela coleta. A identificação bibliográfica do documento deve ser completada em `material_de_referencia.md`.

A padronização do anexo não implica processamento interno idêntico pelos sistemas.

## Comando de entrada

A versão atualmente apresentada no manuscrito é:

> Explique didaticamente por que a atratividade diminui com a distância e Forneça o código Python implementando a função de Atratividade (beta) apresentada no texto.

## Procedimento

1. Disponibilização do material de referência e das instruções da tarefa aos participantes.
2. Anexação do mesmo PDF diretamente à conversa em cada sistema.
3. Inserção do comando padronizado e interação com o sistema, quando o acesso foi concluído.
4. Registro das percepções em formulário eletrônico, segundo os cinco critérios descritos abaixo.

As interfaces e condições próprias de acesso, autenticação e configuração foram preservadas. Não houve controle da ordem de utilização nem repetições sistemáticas, conforme as limitações descritas no manuscrito.

O número exato de mensagens adicionais, a duração das sessões e as configurações detalhadas dos sistemas não estão documentados nos materiais fornecidos para este arquivo. Não se presume que tenham sido iguais.

## Avaliação

Escala de cinco pontos, de 1 (percepção mais negativa) a 5 (percepção mais positiva).

- Didática: clareza e compreensão da explicação.
- Praticidade: percepção sobre o código apresentado.
- Confiabilidade: percepção de correção e fidelidade ao material.
- Completude: integração entre explicação e implementação.
- Acessibilidade: condições de acesso e utilização.

Essas descrições são sínteses analíticas, não transcrições literais das perguntas. A redação original deve constar em `questionario.md`.

## Interrupções de acesso e preparação da base

Todos os itens de avaliação foram configurados como obrigatórios. Seis participantes informaram não desejar ou não conseguir concluir a ativação do Copilot, mas preencheram as avaliações.

As 24 notas desses participantes para o Copilot em didática, praticidade, confiabilidade e completude foram invalidadas e convertidas em ausentes, sem imputação. As notas originais foram preservadas para auditoria. As avaliações de acessibilidade foram mantidas.

A opção do formulário agrupava recusa e dificuldade de ativação; não é possível separar os motivos a partir da base.

## Reprodução computacional

O script público lê a base sem identificadores pessoais diretos, reaplica a regra de exclusão e produz descritivas, Friedman, Kendall, Wilcoxon, Holm e correlação bisserial por postos. Executa Wilcox e Pratt na mesma chamada.

Consulte `README.md`, `data_dictionary.md` e `results_reference/` para comandos, versões, parâmetros e resultados de referência.