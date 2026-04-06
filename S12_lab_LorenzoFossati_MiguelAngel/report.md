# Analizador de texto multilingue con LLM local

**Asignatura:** Procesamiento del Lenguaje Natural
**Alumno:** Miguel Ángel Lorenzo Fossati

---

## 1. Descripcion del problema

En esta practica se pide disenar e implementar una pequeña aplicacion que use un modelo de lenguaje grande ejecutado en local para resolver una tarea relacionada con el lenguaje. He desarrollado una aplicacion que analiza textos escritos en diferentes idiomas y devuelve un resumen en espanol junto con una estimacion del tono del texto.

La aplicacion incluye varias etapas: una fase de preprocesamiento del texto, una llamada al modelo para generar un resumen y una segunda llamada para clasificar el tono. Todo se presenta mediante una interfaz grafica pensada para un usuario final.

---

## 2. Diseno del sistema y flujo de trabajo

La aplicacion está dividida en tres pasos:

1. El usuario escribe o pega un texto en la interfaz.
2. El sistema limpia el texto y detecta su idioma.
3. El modelo local genera un resumen en español y clasifica el tono.

### Preprocesamiento

Se elimina ruido del texto (URLs, espacios repetidos) usando expresiones regulares.
El idioma se detecta automaticamente con la libreria langdetect.

### Procesamiento con el LLM

Se hacen dos llamadas separadas al modelo:

- Una para generar un resumen en 3-5 puntos clave en espanol.
- Otra para clasificar el tono y devolver la respuesta en formato JSON.

Separar las tareas permite usar un prompt especifico para cada una y controlar mejor la salida.

### Interfaz grafica

Implementada con Streamlit. Muestra el idioma detectado, numero de palabras, resumen generado y tono del texto.

![alt text](image.png)

---

## 3. Seleccion del modelo y justificacion

Modelo: Llama 3.2 (3B parametros) ejecutado con Ollama

| Criterio    | Decision                              |
|-------------|---------------------------------------|
| Ejecucion   | 100% local, sin API externa           |
| Tamaño      | 2 GB, manejable en hardware estandar  |
| Idiomas     | Soporte multilingue nativo            |
| Velocidad   | Respuestas en pocos segundos en CPU   |
| Licencia    | Meta Llama 3 Community License        |

Se descarto el modelo de 1B por menor capacidad de seguir instrucciones. Se descarto el de 7B por sus mayores requisitos de RAM. La version de 3B ofrece un equilibrio razonable entre calidad y coste computacional.

---

## 4. Implementacion

Toda la logica esta concentrada en un unico archivo app.py.

### Herramientas usadas

| Componente        | Herramienta        | Version |
|-------------------|--------------------|---------|
| LLM local         | Ollama + Llama 3.2 | 0.6.1   |
| Interfaz grafica  | Streamlit          | 1.56.0  |
| Deteccion idioma  | langdetect         | 1.0.9   |
| Limpieza texto    | re (stdlib Python) | --      |
| Lenguaje          | Python             | 3.10+   |

### Estructura del proyecto

texto-analisis/
 - app.py
 - requirements.txt

### Prompt engineering

Se definieron dos system prompts distintos:

Para el resumen:
"Resume el texto en 3-5 puntos clave en espanol. Usa formato de lista con guiones. Solo los puntos, sin introduccion."

Para el tono:
"Responde: {"tono": "positivo/negativo/neutro/mixto", "razon": "frase corta"}"

---

## 5. Resultados, limitaciones y mejoras

### Resultados

La aplicacion funciona correctamente para textos de longitud media en multiples idiomas.

Ejemplo de uso:
- Entrada: "Im very comfortable here and it is a beautifull place" (ingles)
- Idioma detectado: en
- Resumen: puntos clave en espanol con las ideas principales
- Tono: positivo / mixto
  
  ![alt text](image-1.png)

### Limitaciones

- Textos cortos: langdetect puede dar resultados incorrectos con menos de 10 palabras.
- Clasificacion del tono: el modelo a veces clasifica como mixto textos claramente positivos. Esto es una limitacion habitual de modelos pequeños en tareas de clasificacion subjetiva.
- Velocidad: dos llamadas al modelo implican entre 10 y 30 segundos por analisis en CPU.
- Sin historial: la aplicacion no guarda resultados anteriores entre sesiones.

### Posibles mejoras

- Anadir few-shot prompting en la clasificacion del tono.
- Reducir las categorias a positivo, negativo y neutro.
- Permitir elegir el modelo desde la interfaz.
- Guardar historial.
- Exportar resultados a .txt.
