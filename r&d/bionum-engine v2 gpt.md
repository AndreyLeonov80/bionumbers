Ниже — архитектура **Bionum Engine v2**: от сырого биотекста/биоданных → к графу смыслов → к генерации гипотез.

---

# Bionum Engine v2

Архитектурная формула:

[
Entity \rightarrow Text \rightarrow BioNum \rightarrow Graph \rightarrow Pattern \rightarrow Hypothesis
]

Идея:

обычные биоданные превращаются в **числово-семантическую топологию**.

---

# 1. Core Layers

```text
┌─────────────────────────┐
│ Input Layer             │
│ BioNumbers / PubMed     │
│ Genes / Proteins / GO   │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ Parsing Layer           │
│ extract entities        │
│ normalize units         │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ BioNum Layer            │
│ calculate(text)         │
│ digital root            │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ Semantic Layer          │
│ embeddings              │
│ ontology                │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ Graph Layer             │
│ entity graph            │
│ bionum graph            │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ Pattern Engine          │
│ clusters                │
│ anomalies               │
│ transitions             │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│ Hypothesis Engine       │
│ prediction              │
│ unknown links           │
└─────────────────────────┘
```

---

# 2. CSV Schema

Файл: `entities.csv`

```csv
id,name,type,description,bionum,embedding_id
1,ATP,molecule,energy carrier,7,vec_001
2,Mitochondria,organelle,cell energy generator,7,vec_002
3,DNA Repair,process,genome repair mechanism,3,vec_003
4,Apoptosis,process,programmed cell death,9,vec_004
```

---

Файл: `relations.csv`

```csv
source_id,target_id,relation,weight
1,2,powered_by,0.92
3,4,regulates,0.77
2,4,inhibits,0.44
```

---

Файл: `facts.csv`

```csv
fact_id,text,question_bionum,answer_bionum,fact_bionum
1,ATP powers mitochondria,4,7,7
2,DNA repair prevents apoptosis,3,9,3
```

---

# 3. JSON Schema

## Entity

```json
{
  "id": "gene_001",
  "name": "TP53",
  "type": "gene",
  "description": "tumor suppressor",
  "bionum": 8,
  "semantic_class": "repair"
}
```

---

## Relation

```json
{
  "source": "TP53",
  "target": "DNA Repair",
  "relation": "activates",
  "weight": 0.91
}
```

---

## Hypothesis

```json
{
  "hypothesis_id": "H-001",
  "trigger_pattern": [8,3,8],
  "predicted_relation": "TP53 may regulate apoptosis indirectly",
  "confidence": 0.74
}
```

---

# 4. Graph Model

Есть 2 графа:

---

## A. Semantic Graph

```text
ATP ───── powers ─────► Mitochondria
 │
 │
 └──── supports ─────► Respiration
```

---

## B. BioNum Graph

```text
7 ─────► 7
│
├────► 3
│
└────► 9
```

Это уже **граф переходов числовых состояний**.

Можно считать:

[
P(next_bionum|current_bionum)
]

---

# 5. Pattern Engine

---

## Cluster Finder

Ищет:

```text
same bionum + similar embedding
```

Пример:

```text
ATP
Mitochondria
NADH
Respiration
```

все = 7

→ энергетический кластер.

---

## Transition Matrix

```text
Q-BioNum → A-BioNum
```

матрица:

| Q | A | freq |
| - | - | ---- |
| 7 | 4 | 88   |
| 3 | 8 | 43   |
| 9 | 9 | 67   |

---

## Density Analyzer

Ищет:

* где bionum перенасыщен
* где редок
* где выбросы

Это потенциальные открытия.

---

# 6. Hypothesis Engine

Логика:

если:

A связан с B
B связан с C
A и C имеют одинаковый bionum

но прямой связи нет:

→ propose relation.

---

Пример:

```text
TP53 → DNA Repair
DNA Repair → Genome Stability

TP53 = 8
Genome Stability = 8
```

Нет прямого ребра.

Гипотеза:

```text
TP53 directly stabilizes genome architecture
```

---

# 7. Novelty Detector

Формула:

[
Novelty = Rare(BioNumPattern) × HighSemanticDistance × HighConnectivityPotential
]

ищет:

редкие, но сильные комбинации.

---

# 8. Discovery Modes

---

## Mode 1: Find constants

ищет стабильные биочисла.

---

## Mode 2: Find scaling laws

ищет:

[
Y=aX^b
]

---

## Mode 3: Find anomalies

ищет:

редкие bionum в обычных классах.

---

## Mode 4: Find missing links

ищет:

недостающие рёбра графа.

---

## Mode 5: Predict unknown biology

предсказывает:

* новые функции генов
* новые связи белков
* скрытые паттерны старения

---

# 9. Storage

```text
/data
   entities.csv
   relations.csv
   facts.csv
   hypotheses.json
   transitions.json
   embeddings.vec
```

---

# 10. Minimal API

```python
engine.ingest(data)
engine.build_graph()
engine.find_clusters()
engine.find_anomalies()
engine.find_missing_links()
engine.generate_hypotheses()
engine.export()
```

---

Это уже полноценная **числово-семантическая исследовательская машина**, которую можно натравить на:

* Genetics
* Systems Biology
* Proteomics
* Neuroscience
* Cancer
* Aging

Следующий логичный шаг: построить **Bionum Engine v2 DSL** (язык запросов типа `find where bionum=8 and relation=repair`). Это сильно ускорит исследования.
