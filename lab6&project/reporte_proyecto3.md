# Proyecto #3 — Clasificador SPAM/HAM con Naive Bayes
**CC3085 Inteligencia Artificial**

---

## a. Análisis de Datos Exploratorio (EDA)

### Dataset

| Característica | Valor |
| :--- | :--- |
| Total de mensajes | 5,565 |
| HAM (legítimos) | 4,819 (86.6%) |
| SPAM | 746 (13.4%) |
| Columnas | `Label`, `SMS_TEXT` |

El dataset presenta un **desbalance marcado**: hay aproximadamente 6.5 mensajes ham por cada spam. Este desbalance es importante considerarlo al interpretar métricas como la accuracy, ya que un modelo que prediga siempre ham alcanzaría un 86.6% de acierto sin aprender nada útil.

### Longitud de mensajes

| Clase | Media (chars) | Mediana (chars) |
| :--- | :--- | :--- |
| HAM | ~67 | ~52 |
| SPAM | ~139 | ~149 |

Los mensajes de spam son, en promedio, **el doble de largos** que los ham. Esto sugiere que la longitud del mensaje por sí sola es un indicador útil: el spam tiende a incluir más información promocional, instrucciones de acción y términos legales pequeños al pie.

### Palabras más frecuentes (sin limpiar)

En los datos crudos, las palabras más frecuentes en ambas clases son conectores comunes: *to*, *I*, *the*, *a*, *you*. Estas palabras aparecen en proporciones similares en ham y spam, por lo que no aportan poder discriminativo.

### Palabras exclusivas del Top-20 (post-preprocesamiento)

| Solo SPAM | Solo HAM |
| :--- | :--- |
| `free`, `txt`, `mobil`, `prize`, `claim`, `win`, `stop`, `cash`, `urgent`, `repli`, `servic`, `tone`, `nokia`, `uk`, `week`, `www`, `send`, `min` | `ok`, `good`, `love`, `home`, `time`, `day`, `go`, `come`, `know`, `like`, `got`, `lor`, `lt`, `one`, `need`, `take`, `want` |

El SPAM usa vocabulario **persuasivo y orientado a la acción** (premios, dinero, urgencia). El HAM usa vocabulario **conversacional y relacional** (emociones, lugares, rutinas).

---

## b. Limpieza de Datos

### Pipeline de preprocesamiento (en orden de aplicación)

#### Paso 1 — Tokenización con expresiones regulares
```
re.findall(r'\b[a-zA-Z]{2,}\b', text)
```
Extrae solo secuencias de letras de 2 o más caracteres. Esto elimina implícitamente números, símbolos, emojis y caracteres especiales sin necesidad de un paso separado. El umbral de 2 caracteres evita que iniciales sueltas (como "I" o "a") entren al vocabulario.

#### Paso 2 — Conversión a minúsculas
```
text.lower()
```
Unifica variantes como `FREE`, `Free` y `free` en un solo token. Sin este paso, el modelo trataría estas formas como palabras distintas, fragmentando el conteo y perdiendo señal estadística.

#### Paso 3 — Eliminación de puntuación
La tokenización por regex ya descarta automáticamente puntuación, comillas y signos de exclamación. No se necesita un paso adicional con `string.punctuation`.

#### Paso 4 — Eliminación de *stopwords* (NLTK, inglés)
```python
STOP_WORDS = set(stopwords.words('english'))  # 198 palabras
tokens = [t for t in tokens if t not in STOP_WORDS]
```
Remueve artículos, preposiciones, pronombres y conjunciones que aparecen en cualquier texto sin importar la clase. Esto reduce el vocabulario y dirige la atención del modelo a palabras con real poder discriminativo.

> **Limitación**: eliminar stopwords borra la negación. El texto "not free" pierde el "not" y queda solo "free", siendo interpretado erróneamente como señal de spam.

#### Paso 5 — Stemming con PorterStemmer
```python
stemmer = PorterStemmer()
tokens = [stemmer.stem(t) for t in tokens]
```
Reduce palabras a su raíz morfológica usando reglas heurísticas. Ejemplos:
- `prizes`, `prize`, `prizing` → `prize`
- `calling`, `called`, `calls` → `call`
- `competition`, `compete` → `compet`

**¿Por qué stemming y no lemmatización?** La lemmatización (WordNetLemmatizer) requiere descarga de recursos adicionales y es más lenta. Para Naive Bayes, ambos métodos producen resultados similares ya que el modelo trabaja con frecuencias de tokens, no con semántica profunda.

### Resultado del preprocesamiento

| Métrica | SPAM | HAM |
| :--- | :--- | :--- |
| Vocabulario raw | 1,909 palabras | 6,343 palabras |
| Vocabulario limpio (stems) | 1,584 palabras (−17%) | 5,116 palabras (−19%) |
| Longitud media original | 139 chars | 67 chars |
| Longitud media limpia | 13.4 tokens | 7.0 tokens |

---

## c. Modelo — Naive Bayes con Teorema de Bayes

### Fundamento teórico

El clasificador asume que, **dada la clase**, las palabras son condicionalmente independientes entre sí. Esto simplifica el cálculo del producto de probabilidades y es el supuesto "ingenuo" (*naive*) que da nombre al método.

### División del dataset

| Conjunto | Mensajes | SPAM | HAM |
| :--- | :--- | :--- | :--- |
| Training (80%) | 4,452 | 596 | 3,856 |
| Testing (20%) | 1,113 | 150 | 963 |

La división es **estratificada** para preservar la proporción 86.6%/13.4% en ambos subconjuntos.

### Paso 1 — Probabilidades a priori

$$P(S) = \frac{\text{mensajes SPAM en training}}{\text{total training}} \approx 0.1339$$

$$P(H) = \frac{\text{mensajes HAM en training}}{\text{total training}} \approx 0.8661$$

### Paso 2 — Verosimilitudes con suavizado de Laplace

Para cada palabra $W$ en el vocabulario:

$$P(W|S) = \frac{n_{W,S} + \alpha}{N_S + 2\alpha} \qquad P(W|H) = \frac{n_{W,H} + \alpha}{N_H + 2\alpha}$$

Donde:
- $n_{W,S}$ = número de documentos SPAM que contienen $W$
- $N_S$ = total de documentos SPAM en training
- $\alpha = 1$ (suavizado de Laplace)

El suavizado de Laplace garantiza que ninguna probabilidad sea exactamente 0, evitando que una sola palabra desconocida anule toda la predicción.

### Paso 3 — P(S|W) por palabra (fórmula del Anexo)

$$P(S|W) = \frac{P(W|S)\,P(S)}{P(W|S)\,P(S) + P(W|H)\,P(H)}$$

Este valor se calcula para cada palabra del vocabulario durante el entrenamiento. Palabras como `free`, `prize`, `claim`, `win` obtienen valores cercanos a 1.0, mientras que palabras como `love`, `home`, `ok` obtienen valores cercanos a 0.

### Paso 4 — P(S|W₁…Wₙ) para un mensaje completo (fórmula del Anexo)

$$P(S|\mathbf{W}) = \frac{P_1 P_2 \cdots P_n}{P_1 P_2 \cdots P_n + (1-P_1)(1-P_2)\cdots(1-P_n)}$$

Donde $P_i = P(S|W_i)$ para cada token único del mensaje.

**Implementación en log-espacio** para evitar underflow numérico con mensajes largos:

```python
log_spam = sum(log(Pi) for Pi in ps)
log_ham  = sum(log(1 - Pi) for Pi in ps)
prob_spam = exp(log_spam) / (exp(log_spam) + exp(log_ham))
```

### Ejemplo de cálculo

Para el mensaje: `"FREE entry WIN a cash prize!"`

Tokens preprocesados: `['free', 'entri', 'win', 'cash', 'prize']`

| Token | P(S\|W) |
| :--- | :--- |
| `free` | ~0.97 |
| `entri` | ~0.85 |
| `win` | ~0.94 |
| `cash` | ~0.96 |
| `prize` | ~0.98 |

Resultado: $P(S|\mathbf{W}) \approx 0.999$ → **SPAM**

---

## d. Pruebas de Rendimiento

### Métricas con threshold = 0.5

Evaluado sobre **1,113 mensajes de prueba** (149 spam, 964 ham):

| Métrica | Valor |
| :--- | :--- |
| Accuracy | **96.14%** |
| Precisión | **95.69%** |
| Recall | **74.50%** |
| F1-Score | **83.77%** |

**Matriz de confusión (threshold=0.5):**

```
                Pred HAM   Pred SPAM
  Real HAM :      959           5
  Real SPAM:       38         111
```

- **TP=111** — spam detectado correctamente
- **TN=959** — ham correctamente ignorado
- **FP=5** — ham filtrado como spam (crítico: mensajes legítimos perdidos)
- **FN=38** — spam que pasó desapercibido

### Exploración de thresholds

| Threshold | Precisión | Recall | F1 | Accuracy | FP | FN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.25 | 0.8741 | 0.7919 | 0.8310 | 95.69% | 17 | 31 |
| 0.30 | 0.9070 | 0.7852 | 0.8417 | 96.05% | 12 | 32 |
| 0.35 | 0.9355 | 0.7785 | 0.8498 | 96.32% | 8 | 33 |
| **0.40** | **0.9431** | **0.7785** | **0.8529** | **96.41%** | **7** | **33** |
| 0.45 | 0.9576 | 0.7584 | 0.8464 | 96.32% | 5 | 36 |
| 0.50 | 0.9569 | 0.7450 | 0.8377 | 96.14% | 5 | 38 |
| 0.60 | 0.9821 | 0.7383 | 0.8429 | 96.32% | 2 | 39 |
| 0.70 | 0.9818 | 0.7248 | 0.8340 | 96.14% | 2 | 41 |
| 0.80 | 0.9907 | 0.7181 | 0.8327 | 96.14% | 1 | 42 |

**Mejor threshold por F1-Score: 0.40** (F1=0.8529)

**Interpretación del trade-off:**
- Bajar el threshold captura más spam (mayor recall) pero genera más falsos positivos (ham clasificado como spam).
- Subir el threshold es más conservador: casi elimina los FP pero deja pasar más spam (FN aumenta).
- El threshold 0.40 es el punto óptimo: equilibra precisión (~94%) y recall (~78%) con el menor F1 posible.

---

## e. Discusión de Resultados

### Significado práctico de las métricas

Con threshold=0.5, el modelo alcanza **96.14% de accuracy**, **95.69% de precisión** y **74.50% de recall**. El perfil "alta precisión / recall moderado" es característico de este tipo de clasificador: cuando el modelo dice "esto es spam", acierta en 19 de cada 20 casos. Sin embargo, deja pasar 38 spams de 149 (25.5%) sin detectar.

Los **5 falsos positivos** son el costo más crítico: 5 mensajes legítimos que un usuario jamás vería. En términos de usuario, **casi no perderás mensajes legítimos** pero algo de spam llegará a tu bandeja.

**Para un filtro de correo en producción**, threshold=0.40 es la elección óptima (mejor F1=85.29%): captura más spam con solo 2 FP adicionales respecto al umbral 0.50. Si el contexto fuera seguridad crítica (phishing bancario), convendrían umbrales aún más bajos (~0.25-0.30) priorizando recall sobre precisión.

### Impacto del preprocesamiento en el rendimiento

| Decisión | Impacto positivo | Impacto negativo |
| :--- | :--- | :--- |
| Stemming | Agrupa variantes → mayor frecuencia de señales de spam | Pierde matices semánticos |
| Eliminar stopwords | Elimina ruido, señales más limpias | Pierde contexto de negación |
| Suavizado de Laplace | Evita crash con palabras nuevas | Suaviza palabras raras, reduce su impacto |
| Tokenización por regex | Elimina símbolos y números automáticamente | Pierde señales de `$`, `%`, `!!!` |

### Limitaciones del modelo

1. **Supuesto de independencia**: Las palabras no son independientes en lenguaje natural. "Win money" juntas tienen más peso que la suma de "win" y "money" por separado.
2. **Desbalance de clases**: Con 86.6% ham, el modelo tiende a favorecer ham. El suavizado no corrige completamente este sesgo.
3. **Vocabulario fijo**: Palabras no vistas en training reciben P(S) como probabilidad por defecto, lo que puede ser impreciso.
4. **Evasión de spam**: Un spammer que conoce el modelo puede evitar palabras típicas y usar sinónimos o errores tipográficos deliberados.

### Conclusión

El clasificador Naive Bayes con el preprocesamiento aplicado logra un rendimiento sólido para una implementación desde cero sin librerías de ML. La clave del éxito está en el preprocesamiento: sin él, las stopwords dominan el vocabulario y el modelo pierde señal discriminativa. Con el pipeline completo, palabras como `free`, `prize`, `win` y `cash` emergen como fuertes indicadores de spam, mientras que `love`, `home` y `ok` caracterizan el ham con alta confianza.

---

## Módulo interactivo (presentación en vivo)

```python
spam_classifier("FREE entry WIN a cash prize! Text NOW to claim your reward")
```

**Salida:**
```
=======================================================
   CLASIFICADOR SPAM/HAM — Naive Bayes
=======================================================
  Texto    : FREE entry WIN a cash prize! Text NOW to claim your reward
  Threshold: 0.40
  P(SPAM)  : 1.0000  (100.0%)
  [████████████████████████████████████████]
  Resultado: ** SPAM **

  Top-3 palabras con mayor P(S|W) en este mensaje:
    1. claim           P(S|W)=0.9890  [███████████████████░]
    2. prize           P(S|W)=0.9840  [███████████████████░]
    3. entri           P(S|W)=0.9410  [██████████████████░░]
=======================================================
```

El módulo acepta cualquier texto, aplica el mismo pipeline de preprocesamiento y retorna la probabilidad de spam junto con las 3 palabras más discriminativas del mensaje.

---

*Dataset: SMS Spam Collection — 5,565 mensajes etiquetados como spam/ham.*
*Modelo: Naive Bayes con suavizado de Laplace, implementado desde cero en Python.*
