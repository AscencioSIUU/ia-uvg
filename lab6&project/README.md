# Laboratorio: Spam/Ham — Análisis Exploratorio y Preprocesamiento

Instrucciones para ejecutar el notebook en un entorno virtual limpio.

---

## Requisitos previos

- Python 3.9 o superior
- `pip` actualizado

---

## Configuración del entorno

### 1. Clonar o descargar el proyecto

Asegúrate de tener los siguientes archivos en la misma carpeta:

```
laboratorio_spam_ham/
├── laboratorio_spam_ham.ipynb
├── spam_ham.csv
└── README.md
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

Sabrás que está activo porque el prompt mostrará `(venv)` al inicio.

### 4. Instalar las dependencias

```bash
pip install --upgrade pip
pip install notebook pandas numpy matplotlib seaborn nltk wordcloud
```

### 5. Descargar los recursos de NLTK

Ejecuta esto **una sola vez** desde la terminal (con el venv activo):

```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 6. Iniciar Jupyter Notebook

```bash
jupyter notebook
```

Se abrirá el navegador automáticamente. Abre `laboratorio_spam_ham.ipynb` y ejecuta las celdas con **Run All** (`Kernel → Restart & Run All`).

---

## Desactivar el entorno al terminar

```bash
deactivate
```

---

## Dependencias utilizadas

| Paquete | Propósito |
|---------|-----------|
| `notebook` | Servidor de Jupyter |
| `pandas` | Carga y manipulación del dataset |
| `numpy` | Operaciones numéricas |
| `matplotlib` | Gráficas y visualizaciones |
| `seaborn` | Gráficas de densidad (KDE) |
| `nltk` | Tokenización, stopwords y stemming |
| `wordcloud` | Generación de nubes de palabras |