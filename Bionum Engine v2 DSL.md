Хорошо. Построим **Bionum Engine v2 DSL** как предметно-ориентированный язык для запросов к bionum-графу.

Идея:

не писать SQL/Python, а думать в терминах:

* сущностей
* биочисел
* переходов
* закономерностей
* аномалий
* гипотез

---

# Bionum DSL v2

Базовая форма:

```text
FIND <object>
WHERE <conditions>
RETURN <projection>
```

---

# 1. Primitive types

---

## ENTITY

Биологический объект.

Примеры:

```text
gene
protein
pathway
process
molecule
cell
organ
disease
```

---

## BIONUM

Число:

```text
1..9
```

---

## RELATION

Тип связи:

```text
activates
inhibits
binds
repairs
powers
transcribes
translates
mutates
causes
stabilizes
```

---

## FACT

Текстовая единица знания.

---

# 2. Core grammar

---

## Поиск сущностей

```text
FIND entity WHERE bionum = 8
```

пример:

```text
FIND gene WHERE bionum = 8
```

---

## Поиск по типу

```text
FIND protein WHERE type = repair
```

---

## Комбинированный поиск

```text
FIND gene
WHERE bionum = 8
AND semantic = regeneration
```

---

# 3. Relation Queries

---

## Все связи

```text
LINKS OF TP53
```

---

## Конкретный тип

```text
LINKS OF TP53 WHERE relation = activates
```

---

## Обратные связи

```text
INCOMING TO apoptosis
```

---

# 4. Path Queries

Поиск путей.

---

## Путь между объектами

```text
PATH TP53 -> apoptosis
```

---

## Ограничение длины

```text
PATH TP53 -> aging MAX 4
```

---

## Только определённые отношения

```text
PATH TP53 -> cancer
USING activates, inhibits
```

---

# 5. Pattern Queries

---

## Кластеры

```text
CLUSTER WHERE bionum = 7
```

---

## Семантически похожие

```text
CLUSTER AROUND mitochondria
```

---

## Повторяющиеся шаблоны

```text
PATTERN FIND [8 -> 3 -> 8]
```

---

# 6. Transition Queries

---

## Частоты переходов

```text
TRANSITIONS FROM 7
```

вывод:

```text
7 -> 4 (42%)
7 -> 8 (31%)
7 -> 9 (18%)
```

---

## Матрица

```text
TRANSITION MATRIX
```

---

## Самый частый переход

```text
MOST COMMON TRANSITION
```

---

# 7. Anomaly Queries

---

## Аномалии внутри класса

```text
ANOMALIES IN repair
```

---

## Редкие bionum

```text
RARE bionum IN metabolism
```

---

## Сильные выбросы

```text
OUTLIERS WHERE bionum = 9
```

---

# 8. Missing Link Queries

---

## Отсутствующие связи

```text
MISSING LINKS FOR TP53
```

---

## Потенциальные связи

```text
PREDICT LINKS FOR mitochondria
```

---

# 9. Hypothesis Queries

---

## Генерация гипотез

```text
HYPOTHESIZE ON aging
```

---

## Только сильные

```text
HYPOTHESIZE ON cancer
WHERE confidence > 0.8
```

---

## Через паттерн

```text
HYPOTHESIZE FROM [8 -> 3 -> 9]
```

---

# 10. Resonance Queries

Это уникальная часть DSL.

---

## Поиск одинаковых bionum

```text
RESONANCE OF TP53
```

найдёт:

все сущности с тем же bionum.

---

## Перекрёстный резонанс

```text
RESONANCE BETWEEN aging AND regeneration
```

---

## Максимальный резонанс

```text
MAX RESONANCE IN genome
```

---

# 11. Discovery Queries

---

## Биоконстанты

```text
DISCOVER CONSTANTS
```

---

## Законы масштабирования

```text
DISCOVER SCALING
```

---

## Скрытые циклы

```text
DISCOVER CYCLES
```

---

## Неизвестные классы

```text
DISCOVER UNKNOWN CLUSTERS
```

---

# 12. Temporal Layer

Для времени.

---

## Эволюция

```text
EVOLVE TP53 OVER dataset
```

---

## Изменение bionum

```text
TRACK bionum OF cancer
```

---

# 13. Meta Queries

---

## Объяснение

```text
EXPLAIN TP53
```

вернёт:

* bionum
* связи
* кластеры
* аномалии
* гипотезы

---

## Почему?

```text
WHY TP53 -> apoptosis
```

---

# 14. Example Session

```text
FIND gene WHERE bionum = 8
LINKS OF TP53
PATH TP53 -> apoptosis
CLUSTER AROUND TP53
ANOMALIES IN repair
PREDICT LINKS FOR TP53
HYPOTHESIZE ON aging
RESONANCE OF TP53
DISCOVER CONSTANTS
```

---

# Execution model

DSL parser:

```text
Query
 ↓
Lexer
 ↓
Parser
 ↓
AST
 ↓
Graph Executor
 ↓
Pattern Engine
 ↓
Hypothesis Engine
 ↓
Result
```

---

Минимальный Python API:

```python
engine.query("FIND gene WHERE bionum = 8")
engine.query("PATH TP53 -> apoptosis")
engine.query("HYPOTHESIZE ON aging")
```

Это уже превращает Bionum Engine в **исследовательский язык**, а не просто библиотеку. Следующий уровень — добавить **Bionum Logic Rules**:

```text
IF same_bionum AND shared_neighbor THEN probable_relation
```

Это даст полноценный inferencing engine.
