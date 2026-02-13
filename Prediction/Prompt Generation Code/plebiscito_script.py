import os
import json
from pprint import pprint
import random

#from requester_v import Exp_Request
from requester_script import Exp_Request
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import aux_ablation
from index_matrix import index_matrix
#from index_matrix_plebiscito import index_matrix
import aux_fewshot
import dictionaries
#502

#data = pd.read_csv('exp2_inputs_rem.csv')
data = pd.read_csv('exp2_inputs_filtrado.csv')
#data = data.drop(data.index[:367])#149
#dataset = pd.read_csv('prompt_dataset_plebiscito.csv')
#dataset_wpv = pd.read_csv('prompt_dataset_plebiscito_wpv.csv')
#dataset_red = pd.read_csv('prompt_dataset_plebiscito_red.csv')
#dataset_eng = pd.read_csv('prompt_dataset_plebiscito_eng.csv')
#fewshot_df = pd.read_csv('prompt-dataframes/prompt_dataset_plebiscito_fewshot.csv')
fewshotexamples_df = pd.read_csv('exp_100_inputs.csv')

# Definir la clase derivada (clase hija) que hereda de Animal
class Plebiscite_Requester(Exp_Request):

  def __init__(self, model, b, chat, name, eng=False, prompting_estructure = "normal", prompt_type="", with_context = True, spec = False,translate= False, ablation = False, finetuned=False, random_fewshot =False, nsamples = 0):
    # Llama al constructor de la clase padre usando super()
    
    if eng:
      dictionary = dictionaries.plebiscito_eng
    else:
      dictionary = dictionaries.plebiscito
    jsonl_name = './' + model + '_plebiscito_' + b + 'b' +name + '.jsonl'
    imatrix = index_matrix
    if finetuned:
      jsonl_name = './plebiscite' +name + '.jsonl'

    if random_fewshot:
      examples_df = fewshotexamples_df
    else: 
      examples_df = []

    #####################   Prompts   ######################
    if not eng:
      #task="Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en la segunda vuelta presidencial de Chile del 2021. Debes responder siempre con tan solo una palabra de entre las siguientes opciones: Boric, Kast o Nulo.\n "
      task="Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en el plebiscito de salida para la nueva constitución de Chile realizado en Septiembre del 2022. Debes responder siempre con tan solo una palabra de entre las siguientes opciones(sin explicaciones extras): Apruebo, Rechazo o Nulo.\n "
      task_json = "Eres un modelo predictor. Tu tarea es predecir las respuestas de una persona a cierta pregunta basándote en sus características sociodemográficas. Las características sociodemográficas estarán delimitadas con triple backsticks, la pregunta estará delimitada con los siguientes símbolos < >, y las alternativas de respuesta por [ ]."
      inst_json = "Entrega un JSON con las siguientes llaves: 'explicación' (EN MAXIMO 100 PALABRAS)  donde darás el razonamiento para responder a la pregunta, y 'respuesta' que mostrará la alternativa que elegiste para responder."
      context = 'Primero te daré un poco de contexto. El año 2020 en Chile se llevó a cabo una votación para decidir si los chilenos querían que se redactara una Nueva Constitución para reemplazar la constitución vigente en ese momento, creada en el período de la Dictadura de Augusto Pinochet. La primera pregunta de dicha votación fue si el votante estaba de acuerdo con redactar una nueva Constitución, donde el 78% de los votantes optó por la opción "Apruebo". La segunda pregunta fue sobre el órgano encargado de redactar la nueva Constitución, y la opción ganadora fue una convención constituyente compuesta en su totalidad por ciudadanos elegidos exclusivamente para este propósito.\n Con los resultados de esta votación se comenzó el proceso constituyente. El paso siguiente fue elegir a los representantes de la convención constituyente por votación popular. La convención quedó constituida por 28 escaños para Apruebo Dignidad, 25 escaños para la Lista del Apruebo, 37 escaños para Vamos por Chile, 47 escaños para independientes en listas, 17 escaños para pueblos originarios, y 1 independiente fuera de pacto. De esta forma la convención constitucional quedó principalmente constituída por representantes de la centro izquierda e izquierda, de hecho, varios convencionales habían sido figuras activas durante el estallido social de 2019.\n Luego de más de un año de trabajo, en julio de 2022, se presentó la propuesta de Nueva Constitución. Esta propuesta tenía varios artículos enfocados en la igualdad de género, descentralización del país, plurinacionalidad, ecología y sustentabilidad. Algunos de estos artículos generaron miedos y recelo en la sociedad chilena, como por ejemplo la plurinacionalidad.\n El 4 de septiembre de 2022 se realizó el plebiscito de salida de la Nueva Constitución, en un ambiente político cada vez más polarizado donde el apoyo al estallido social era cada vez menor a pesar de la amplia mayoría que tuvo en un principio. A esto también se suma un ambiente de desinformación, que generó miedos tales como pérdida de propiedad, pérdidas de derechos a la educación de los propios hijos, entre otros. Este plebiscito fue de voto obligatorio, a diferencia de todas las votaciones anteriores, y tuvo solo una pregunta: "¿Aprueba usted el texto de Nueva Constitución propuesto por la Convención Constitucional?", las posibles respuestas a marcar eran: Apruebo o Rechazo. Como siempre el votante tenía también la posibilidad de anular su voto en caso de que no eligiera ninguna de las 2 opciones anteriores.\n'
      end= "Ahora analiza el perfil de la persona que se describe a continuación y responde a la pregunta que se te hará."
      if spec:
        inst = "Por favor también responde por qué crees que la persona eligiría esa opción y en qué variables te fijaste al hacer la predicción. En tu respuesta usa la primera palabra para indicar la opción elegida y el resto de palabras para explicar el por qué."
      else:  
        inst = "Responde SOLO en un 1 palabra, sin explicaciones ni justificaciones extras. \n"

    else:
      task = "Your job is to be an assistant that will help predict the vote of certain individuals in the chilean exit plebiscite for the New Constitution of 2022. You must always respond with just one of the following options(without extra explanations): Approve, Reject, or Null."
      context = "Now I'll give you a bit of context. In the year 2020, in Chile, a vote took place to decide whether Chileans wanted a New Constitution to replace the existing one created in 1980 and modified in the following years until the present. The first question in this vote was whether the voter agreed to draft a new Constitution, where 78% of voters chose the 'Approve' option. The second question was about the body responsible for drafting the new Constitution, and the winning option was a constitutional convention entirely composed of citizens chosen exclusively for this purpose.\n With the results of this vote, the constitutional process began. The next step was to elect representatives to the constitutional convention through popular vote. The convention consisted of 28 seats for 'Apruebo Dignidad,' 25 seats for the 'Apruebo' list, 37 seats for 'Vamos por Chile,' 47 seats for independents on lists, 17 seats for indigenous peoples, and 1 independent outside the pact. Thus, the constitutional convention was mainly composed of representatives from the center-left and left. In fact, several delegates had been active figures during the social outbreak of 2019.\n After over a year of work, in July 2022, the proposal for the New Constitution was presented. This proposal had several articles focused on gender equality, decentralization of the country, plurinationality, ecology, and sustainability. Some of these articles generated fears and suspicion in Chilean society, such as plurinationality.\n On September 4, 2022, the exit plebiscite for the New Constitution took place in an increasingly polarized political environment, where support for the social outbreak was decreasing despite its initial widespread majority. This was also accompanied by an atmosphere of misinformation, generating fears such as property loss, loss of education rights for one's own children, among others. This plebiscite was mandatory, unlike all previous votes, and had only one question: 'Do you approve the text of the New Constitution proposed by the Constitutional Convention?' The voter had two options to mark: Approve or Reject.  As always, the voter also had the possibility to invalidate their vote in case they did not choose any of the 2 previous options by voting null.\n"
      end = "Now analyze the profile of the following person and answer the question that will be asked of you."
      inst = "Remember to answer just in 1 word. \n"

    if prompting_estructure=="json":
      task = "You are a predictive model. Your task is to predict a person's answers to a certain question based on their sociodemographic characteristics. The sociodemographic characteristics will be delimited with triple backsticks, the question will be delimited with the following symbols < >, and the response alternatives by [ ]."
      inst = " Deliver a JSON with the following keys: 'explanation' (IN MAXIMUM 100 WORDS) where you will write your reasoning to answer the question, and 'answer' that shows the alternative chosen to answer the question."

    if not with_context:
      context = ""

    #end="¿Qué votó esta persona en el plebiscito constitucional de salida del 2022?¿Apruebo, Rechazo, o ninguno?"
    super().__init__(2, model, b, chat, jsonl_name, task , "", "", inst, dictionary, eng, prompting_estructure,prompt_type,translate, ablation, finetuned, nsamples, random_fewshot, imatrix )
    #super().__init__(3, model, b, chat, jsonl_name, "", "", "", "", dictionary, eng, prompting_estructure, prompt_type,translate, ablation, finetuned, nsamples, random_fewshot, imatrix )
################################################### Original ###################################################

#r= Plebiscite_Requester("llama", str(7), "_final")
#r.answers_generator(data)

#r= Plebiscite_Requester("llama-2-13b-chat_v1_ESP_PLEB_EVAL_1800_inverted",str(13), True, "_v1_ESP_ONLYPLEB", translate=True, finetuned = True)
#r= Plebiscite_Requester("llama-2-13b-chat_v15_ENG_NORMAL_EVAL_5000_inverted",str(13), True, "llama_v15_NORMAL_ENG_5000_eval_inverted", translate=True,finetuned = True)
#r.answers_generator(data)

##########################################################

#llama_plebiscito_13b_list_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_list_template_final_rfs5",eng = True, prompting_estructure="list",random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_list_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_list_template_final_rfs5", eng = True, prompting_estructure="list", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#t0_plebiscito_b_list_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("t0","", True, "_list_template_final_rfs5", eng = True, prompting="list", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_text_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_text_template_final_rfs5",eng = True, prompting_estructure="text",random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_text_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_text_template_final_rfs5", eng = True, prompting_estructure="text", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#t0_plebiscito_b_text_template_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("t0","", True, "_text_template_final_rfs5", eng = True, prompting="text", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)


##########################################################
#llama_plebiscito_13b_oom_prompt_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_oom_prompt_rfs5", eng = True, prompting="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_json_prompt_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_oom_prompt_rfs5", eng = True, prompting="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#t0_plebiscito_b_json_prompt_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("t0","", True, "_json_prompt_rfs5", eng = True, prompting_estructure="json", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#plebiscitef_10000_1e6_01_1_json_inverted_final_rfs0.jsonl
#r=Plebiscite_Requester("f_10000_1e6_01_1","", True, "f_10000_1e6_01_1_json_inverted_final_rfs0",eng = True, prompting_estructure="json",translate=False, finetuned = True, random_fewshot = False, nsamples = 5)
#r.answers_generator(data)

r=Plebiscite_Requester("llama","13", True, "_json_wpv_rfs5", eng = True, prompting_estructure="json", prompt_type="wpv",ablation = False, translate=False, random_fewshot = True, nsamples = 5)
r.answers_generator(data)

r=Plebiscite_Requester("llama","13", True, "_json_onlypol_rfs5", eng = True, prompting_estructure="json", prompt_type="onlypol",ablation = False, translate=False, random_fewshot = True, nsamples = 5)
r.answers_generator(data)
#r=Plebiscite_Requester("llama","13", True, "_json_ablation_final_rfs5", eng = True, prompting_estructure="json", prompt_type="",ablation = True, translate=False, random_fewshot = True, nsamples = 5)
#r.ablation_request(data)
#llama_elecpres_13b_oom_prompt_rfs5.jsonl
#r=Plebiscite_Requester("t0","", True, "_original_withoutcontext_prompt_rfs5", eng = True, prompting_estructure="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

##########################################################
#mistral_plebiscito_v0.2b_originalprompt_rfs5.jsonl - REVISADO (quiza quitar el inst)
#r=Plebiscite_Requester("mistral","v0.2", True, "_originalprompt_rfs5", eng = True, prompting="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_originalprompt_rfs0.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_originalprompt_rfs0", eng = True, prompting="normal", random_fewshot =False, nsamples = 0)
#r.answers_generator(data)

#llama_plebiscito_13b_originalprompt_withoutcontext_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_originalprompt_withoutcontext_rfs5", eng = True, prompting="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_originalprompt_withoutcontext_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_originalprompt_withoutcontext_rfs5", eng = True, prompting="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_originalprompt_withoutcontext_rfs0.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_originalprompt_withoutcontext_rfs0", eng = True, prompting_estructure="normal", random_fewshot=False, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_originalprompt_withoutcontext_rfs0.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_originalprompt_withoutcontext_rfs0", eng = True, prompting_estructure="normal", random_fewshot=False, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_originalprompt_context_rfs5.jsonl
#r=Plebiscite_Requester("llama","13", True, "_originalprompt_context_rfs5", eng = True, prompting_estructure="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_originalprompt_context_rfs5.jsonl
#r=Plebiscite_Requester("mistral","v0.2", True, "_originalprompt_context_rfs5", eng = True, prompting_estructure="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_originalprompt_withoutcontext_esp_rfs5.jsonl
#r=Plebiscite_Requester("llama","13", True, "_originalprompt_withoutcontext_esp_rfs5", eng = False, prompting_estructure="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#mistral_plebiscito_v0.2b_originalprompt_withoutcontext_esp_rfs5.jsonl
#r=Plebiscite_Requester("mistral","v0.2", True, "_originalprompt_withoutcontext_esp_rfs5", eng = False, prompting_estructure="normal", random_fewshot=True, nsamples = 5)
#r.answers_generator(data)

#t0_plebiscito_b_original_withoutcontext_prompt_rfs5.jsonl
#t0_plebiscito_b_oom_prompt_rfs5.jsonl
#r=Plebiscite_Requester("t0","", True, "_original_withoutcontext_prompt_rfs5", eng = True, prompting_estructure="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(data)
##########################################################

#mistral_plebiscito_v0.2b_json_inverted_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("mistral","v0.2", True, "_json_inverted_final_rfs5",eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_json_inverted_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_json_inverted_final_rfs5",eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#llama_plebiscito_13b_json_inverted_final_rfs0.jsonl - REVISADO
#r=Plebiscite_Requester("llama","13", True, "_json_inverted_final_rfs0",eng = True, prompting="json",translate=True, random_fewshot =False, nsamples = 5)
#r.answers_generator(data)

#t0_plebiscito_b_json_inverted_final_rfs5.jsonl - REVISADO
#r=Plebiscite_Requester("t0","", True, "_json_inverted_final_rfs5", eng = True, prompting="json",translate=False, random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

#llama_elecpres_13b_json_inverted_final_esp_rfs5.jsonl
#######r=Plebiscite_Requester("llama","13", True, "_json_inverted_final_esp_rfs5",eng = False, prompting="json",translate=False, random_fewshot =True, nsamples = 5)
#######r.answers_generator(data)

#llama_plebiscito_13b_original_withoutcontext_ablation_rfs5.jsonl
#r=Plebiscite_Requester("llama","13", True, "_original_withoutcontext_ablation_rfs5", eng = True, prompting_estructure="normal", translate=False,  ablation = True, random_fewshot =True, nsamples = 5)
#r.ablation_request(data)

#llama_plebiscito_13b_normal_onlypol_final_rfs5.jsonl
#r=Plebiscite_Requester("llama","13", True, "_normal_onlypol_final_rfs5", eng = True, prompting_estructure="normal", prompt_type="onlypol",translate=False, random_fewshot = True, nsamples = 5)
#r.answers_generator(data)
########################################################################
#f_1000_1e4_0001_1_elecpres_b_f_1000_1e4_0001_1_json_inverted_final_rfs0.jsonl
#r=Plebiscite_Requester("f_5000_1e6_0001_1","", True, "f_5000_1e6_0001_1_plebiscito_json_final_rfs0",eng = True, prompting_estructure="json",translate=False, finetuned = True, random_fewshot = False, nsamples = 5)
#r.answers_generator(data.drop(data.index[:378])) # 464 #457

################################################### SPEC ###################################################
#answers_generator(dataset, b, task, context, end, spec, name = "_spec")

###################################################  WPV  ###################################################
#r = Plebiscite_Requester(b, "_wpv", wpv = True)
#r.answers_generator(data)

#r = Plebiscite_Requester("mistral", "v0.2", "_wpv", wpv= True)
#r.answers_generator(data)


############################################## WITHOUT CONTEXT ####################################
#r = Plebiscite_Requester(str(7), "_withoutcontext", with_context = False)
#r.answers_generator(data) #3, 6

#r = Plebiscite_Requester(str(13), "_withoutcontext", with_context = False)
#r.answers_generator(data) #3, 6

#r = Plebiscite_Requester("mistral", "v0.2", "_withoutcontext", with_context= False)
#r.answers_generator(data)

###################################################  REDUCED  ###################################################
#r7 = Plebiscite_Requester(str(7), "_red", red = True)
#r7.answers_generator(data)

#r13 = Plebiscite_Requester(str(13), "_red", red = True)
#r13.answers_generator(data)

#r = Plebiscite_Requester("mistral", "v0.2", "_red", red= True)
#r.answers_generator(data)

###################################################  ENG  ###################################################

#r = Plebiscite_Requester(str(7), "_eng", eng = True)
#r.answers_generator(data) #3, 6

#r = Plebiscite_Requester(str(13), "_eng", eng = True)
#r.answers_generator(data) #3, 6

#r = Plebiscite_Requester("mistral", "v0.2", "_eng_resto", eng= True)
#r.answers_generator(data)

###################################################  ABLATION  ###################################################
#r = Plebiscite_Requester(str(7), "_ablation", ablation = True)
#r.ablation_request(data) #3, 6

#r = Plebiscite_Requester(str(13), "_ablation", ablation = True)
#r.ablation_request(data) #3, 6


################################################## RANDOM FEWSHOT ###################################################
#r = Plebiscite_Requester(b, "_rfewshot", random_fewshot =True, examples_df = fewshotexamples_df)
#r.answers_generator(fewshot_df)


#r=Plebiscite_Requester("llama",str(13), True, "llama_json_inverted_rfewshot_5", translate=True, random_fewshot =True, nsamples = 5)
#r=Plebiscite_Requester("llama-2-13b-chat_v15_ENG_NORMAL_EVAL_5000_inverted",str(13), True, "llama_v15_NORMAL_ENG_5000_eval_inverted_rfewshot_5", translate=True,finetuned = True,  random_fewshot =True, nsamples = 5)
#r.answers_generator(data)

###################################################  FEWSHOT  ###################################################
#answers_generator(dataset, b, task, context, end, inst, name = "_fewshot", few_shot = True)
 