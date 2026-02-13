
# LLM Request Code

Contiene los archivos que generan las predicciones. En particular tenemos 3 archivos distintons, uno para aborto, otro para plebiscito y otro para eleccion presidencial. Cada uno setea las variables que necesita y luego llama al requester_script.py que es el que opera de igual forma para los 3 experimentos. Este último archivo hace todo el trabajo de convertir a prompt legible, hacer las predicciones con el LLM y guardar los resultados en un dataframe.

# Prompt Generation Code

Esta carpeta contiene los archivos que se usan para convertir el dataframe crudo en un prompt. El archivo prompt_generator.py tiene muchas funciones, las cuales corresponden a cada uno de los diferentes prompts utilizados (en distintos formatos e idiomas).

dictionary.py tiene algunos diccionarios con los significados de los códigos en las encuestas (para ANES y para CEP).
