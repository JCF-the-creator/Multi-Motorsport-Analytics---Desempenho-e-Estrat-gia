# Multi Motorsport Analytics — Desempenho e Estratégia

**Repositório:** [github.com/JCF-the-creator/Multi_Motorsport_Analytics_Desempenho_e_Estrategia](https://github.com/JCF-the-creator/Multi_Motorsport_Analytics_Desempenho_e_Estrategia)  
**Dashboard interativo:** [multi-motorsport.lovable.app](https://multi-motorsport.lovable.app/)  
**Versão:** 1.0 — Executive Edition  
**Autor:** James Candido Ferreira, Erick Jonathas Lima dos Santos, Matheus Silva, Arlindo Dos Santos Lima, Luan Da Costa e Lucas Herbet Brito
**Linguagens principais:** Python (97.2% Jupyter Notebook · 2.7% .py) · TypeScript/React (frontend)

---

## 1. Visão Geral

O **Multi Motorsport Analytics** é uma plataforma de inteligência de dados que centraliza, transforma e visualiza indicadores de desempenho de três modalidades do automobilismo mundial:

| Modalidade | Cobertura de dados |
|---|---|
| **Fórmula 1** | 1950 – 2024 (histórico completo) |
| **MotoGP** | Temporadas recentes (base estruturada) |
| **Rally dos Sertões** | Resultados acumulados por etapa e categoria |

O projeto cobre todo o ciclo de dados — da extração e transformação em Python/Jupyter até a entrega em um dashboard web interativo — e serve como portfólio técnico na intersecção de engenharia de dados, análise exploratória e desenvolvimento front-end.

---

## 2. Estrutura do Repositório

```
Multi_Motorsport_Analytics_Desempenho_e_Estrategia/
│
├── Codigo_PY_MotoGP/          # Notebooks e scripts de ETL para MotoGP
├── Codigo_Py_F1/              # Notebooks e scripts de ETL para Fórmula 1
├── Resultados_Rally_2025_Completo - Copia/   # Dados brutos do Rally dos Sertões (JSON/CSV)
└── README.md
```

### 2.1 `Codigo_Py_F1/`
Pipeline de processamento de dados da Fórmula 1. Responsabilidades principais:

- Leitura de resultados de corridas em formato CSV
- Limpeza e normalização de campos (tempos, nomes de pilotos, construtoras)
- Cálculo de métricas derivadas: pontuações acumuladas, médias de tempo de pit stop, correlação grid × resultado final
- Preparação dos dados para consumo pelo dashboard

### 2.2 `Codigo_PY_MotoGP/`
Pipeline de processamento de dados da MotoGP. Responsabilidades principais:

- Manipulação de colunas de tempo de volta (`timedelta`, conversões para segundos)
- Mapeamento de nomes fictícios/alternativos de pilotos
- Cálculo da coluna `GAP` (diferença para o líder por corrida)
- Extração de tabelas de classificação a partir de PDFs com `pdfplumber` e validação por calibração de eixo X
- Geração de relatórios PDF com `ReportLab` integrando pandas e Matplotlib

### 2.3 `Resultados_Rally_2025_Completo/`
Conjunto de dados brutos do Rally dos Sertões 2025. Contém:

- Arquivos JSON por etapa (Special Stages — SS)
- Resultados por categoria: RC2, RC5, RC5L, MT1, MT2, UTU e outras
- Convertidos para CSV via batch converter Python (injeção de metadados de cabeçalho nos registros)

---

## 3. Pipeline de Dados

```
Fontes brutas
  ├── CSVs de corridas F1 (resultados históricos 1950–2024)
  ├── PDFs/CSVs de classificação MotoGP
  └── JSONs por etapa do Rally dos Sertões
         │
         ▼
  Transformação (Python/Jupyter)
  ├── Limpeza e normalização
  ├── Cálculo de métricas (GAP, pontuação, médias)
  ├── Exportação para CSV estruturado
  └── Geração de relatórios PDF
         │
         ▼
  Dashboard Web (React + TypeScript)
  └── Visualizações interativas (Recharts)
      Exportação CSV e PDF diretamente pelo browser
```

---

## 4. Dashboard Web — Funcionalidades

O dashboard está disponível em [multi-motorsport.lovable.app](https://multi-motorsport.lovable.app/) e oferece as seguintes seções e recursos:

### 4.1 Visão Executiva (Página Inicial)

Painel consolidado com indicadores de todas as modalidades:

| KPI | Valor atual |
|---|---|
| Eventos Totais | 2.296 |
| Pilotos Totais | 1.087 |
| Equipes/Categorias | 250 |
| Vitórias F1 | 1.128 |

Inclui gráficos de evolução de eventos por temporada, distribuição por modalidade e ranking geral de vitórias na F1.

### 4.2 Fórmula 1

Análise histórica completa (1950–2024):

| KPI | Valor |
|---|---|
| Corridas | 1.125 |
| Pilotos | 861 |
| Equipes | 211 |
| Vitórias registradas | 1.128 |
| Poles | 494 |
| Pódios | 3.397 |

**Visualizações disponíveis:**
- Ranking de pilotos por vitórias acumuladas (top 15)
- Ranking de equipes por pontuação
- Evolução de pontos por temporada (top 6 pilotos)
- Correlação Grid × Resultado (posição final média por largada, 2020+)
- Tempo médio de pit stop por temporada (mediana em segundos)
- Performance por circuito (top por número de corridas)
- Tabela detalhada com vitórias, pódios, pontos e participações — paginada e com busca

### 4.3 MotoGP

| KPI | Valor |
|---|---|
| Corridas | 178 |
| Pilotos | 15 (temporadas recentes) |
| Equipes | 10 |
| Vitórias | 163 |
| Pódios | 440 |
| Pole Positions | 144 |
| Melhor Piloto | Marc Márquez |
| Melhor Equipe | Ducati Lenovo |

**Visualizações disponíveis:**
- Ranking de pilotos por pontuação acumulada
- Ranking de equipes
- Evolução de pontos por temporada (top 6)
- Posições por corrida (temporada atual)
- Performance por circuito
- Evolução por temporada: corridas, pilotos e equipes
- Top 10 vitórias e pódios por piloto
- Gráfico radar de comparação multidimensional entre pilotos (top 5)
- Tendência de performance: média de pontos e velocidade máxima

### 4.4 Rally dos Sertões

| KPI | Valor |
|---|---|
| Eventos | 10 |
| Categorias | 29 |
| Pilotos | 211 |
| Melhor Tempo Acumulado | 0h 25m 10s |

**Categorias cobertas:** RC2, RC5, RC5L, MT1, MT2, UTU, MB, UB e outras.

**Visualizações disponíveis:**
- Ranking geral (top 10 por menor tempo acumulado)
- Ranking por categoria (volume de pilotos e eventos)
- Evolução por etapa/SS (participantes registrados)
- Diferença para o líder (gap em segundos — top 10)
- Performance por evento: pilotos e categorias
- Tabela detalhada: tempo total, gap e posição na categoria

### 4.5 Comparativos

Visão cruzada entre as três modalidades, permitindo análises comparativas de volume de eventos, evolução histórica e desempenho relativo.

### 4.6 Recursos Transversais

Todos os recursos abaixo estão disponíveis em qualquer seção do dashboard:

- **Filtro global de modalidade** (Todas / F1 / MotoGP / Rally)
- **Seletor de temporada** (cobertura de 1950 a 2024)
- **Exportação CSV** — download direto dos dados filtrados
- **Exportação PDF** — relatório formatado da visualização atual
- **Tema claro/escuro** (toggle persistente)
- **Cards KPI animados**
- **Gráficos interativos** (hover, zoom, filtro por legenda)
- **Tabelas com ordenação, busca e paginação**
- **Layout responsivo** (desktop e mobile)

---

## 5. Stack Tecnológica

### Back-end / ETL (Python)

| Biblioteca | Uso no projeto |
|---|---|
| `pandas` | Manipulação de DataFrames, limpeza, cálculos agregados |
| `pdfplumber` | Extração de tabelas de PDFs de classificação MotoGP |
| `ReportLab` | Geração de relatórios PDF |
| `Matplotlib` | Visualizações embarcadas nos relatórios PDF |
| `json` / `csv` | Leitura e escrita dos arquivos de dados brutos |
| `re` (regex) | Parsing de colunas de tempo e nomes de pilotos |

### Front-end (Dashboard Web)

| Tecnologia | Uso |
|---|---|
| React 19 + TypeScript | Framework e tipagem do frontend |
| TanStack Router + Vite | Roteamento SPA e bundling |
| Recharts | Gráficos interativos |
| Tailwind CSS v4 + Shadcn UI | Estilização e componentes |

---

## 6. Técnicas e Padrões Aplicados

- **Calibração de coluna X** no pdfplumber para extração precisa de colunas em tabelas de PDFs com layout variável
- **Batch converter JSON → CSV** com injeção de metadados de cabeçalho nos registros de saída (Rally)
- **Manipulação de tempo** com `timedelta` e conversões para segundos para cálculos de GAP
- **Mapeamento de entidades** (nomes fictícios/alternativos de pilotos) para normalização de chaves
- **Princípio DRY** aplicado na refatoração dos notebooks (funções reutilizáveis para leitura, transformação e exportação)
- **Pipeline reprodutível**: cada módulo (F1, MotoGP, Rally) é independente e executável isoladamente

---

## 7. Dados e Cobertura

| Fonte | Tipo | Período |
|---|---|---|
| Resultados oficiais F1 | CSV | 1950 – 2024 |
| Classificações MotoGP | PDF / CSV | Temporadas recentes |
| Rally dos Sertões | JSON por etapa | 2025 (etapas completas) |

> **Nota:** Os dados de MotoGP do dashboard utilizam base estruturada até a integração com a fonte oficial da organização.

---

## 8. Como Executar o ETL Localmente

### Pré-requisitos

```bash
pip install pandas pdfplumber reportlab matplotlib
```

### F1

```bash
cd Codigo_Py_F1/
jupyter notebook
# Abrir e executar os notebooks na ordem indicada
```

### MotoGP

```bash
cd Codigo_PY_MotoGP/
jupyter notebook
# Os notebooks incluem as etapas de extração PDF e geração de relatório
```

### Rally

```bash
cd "Resultados_Rally_2025_Completo - Copia/"
python batch_converter.py  # converte JSONs para CSV com metadados injetados
```

---

## 9. Acesso ao Dashboard

O dashboard está publicado e acessível publicamente:

**URL:** [https://multi-motorsport.lovable.app](https://multi-motorsport.lovable.app)

Seções disponíveis:

| URL | Conteúdo |
|---|---|
| `/` | Visão executiva consolidada |
| `/f1` | Análise completa de Fórmula 1 |
| `/motogp` | Análise de MotoGP |
| `/rally` | Análise do Rally dos Sertões |
| `/comparativo` | Cruzamento entre modalidades |
| `/sobre` | Informações técnicas do projeto |

---

## 10. Autores e Contato

**James Candido Ferreira**  
- GitHub: [github.com/JCF-the-creator](https://github.com/JCF-the-creator)
- LinkedIn: [linkedin.com/in/jamescandidoferreira](https://linkedin.com/in/jamescandidoferreira)


**Erick Jonathas Lima dos Santos**  
- GitHub: [github.com/Erickzyz](github.com/Erickzyz)
- LinkedIn: [www.linkedin.com/in/erick-jonathas-santos](www.linkedin.com/in/erick-jonathas-santos)


**Matheus Silva**  
- GitHub: [github.com/Silva15m](github.com/Silva15m)
- LinkedIn: [https://www.linkedin.com/in/matheus-silva-data/](https://www.linkedin.com/in/matheus-silva-data/)


**Arlindo Dos Santos Lima**  
- GitHub: [github.com/Arlindo21](github.com/Arlindo21)
- LinkedIn: [https://www.linkedin.com/in/arlindo-lima-ti/](https://www.linkedin.com/in/arlindo-lima-ti/)


**Luan Da Costa**  
- GitHub: [github.com/Asproz21](github.com/Asproz21)
- LinkedIn: [https://www.linkedin.com/in/luan-da-costa-9590b224b/](https://www.linkedin.com/in/luan-da-costa-9590b224b/)


**Lucas Herbet Brito**  
- GitHub: [github.com/herbertbrito4](github.com/herbertbrito4)
- LinkedIn: [https://www.linkedin.com/in/lucas-h-brito/](https://www.linkedin.com/in/lucas-h-brito/)

---
