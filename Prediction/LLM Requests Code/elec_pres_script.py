import pandas as pd
import numpy as np
#from requester_v import Exp_Request
from requester_script import Exp_Request
from index_matrix import index_matrix
import dictionaries


df1 = pd.read_csv('exp2_inputs_filtrado.csv')
#df1 = df1.drop(df1.index[:440])
#data = pd.read_csv('exp1_inputs.csv')
#fewshot_df = pd.read_csv('./prompt-dataframes/prompt_dataset_presidencial_fewshot.csv')
#fewshotexamples_df = pd.read_csv('./prompt-dataframes/prompt_dataset_presidencial_fewshotexamples.csv')
fewshotexamples_df = pd.read_csv('exp_100_inputs.csv')
anes_df =  pd.read_csv("anes_2020_660.csv")
anes_100_df =  pd.read_csv('anes_2020_100.csv')




# Definir la clase derivada (clase hija) que hereda de Animal
class Elecpres_Requester(Exp_Request):
  #model,
  def __init__(self, model, b, chat, name, eng=False, prompting_estructure = "normal", prompt_type="",with_context = True, spec = False,translate= False, ablation = False, finetuned=False, random_fewshot =False, nsamples = 0):
    # Llama al constructor de la clase padre usando super()
    
    #model_llama
    if random_fewshot:
      examples_df = fewshotexamples_df
    else: 
      examples_df = []

    if prompt_type == "anes":
      dictionary = dictionaries.voto_anes
    else:
      dictionary = dictionaries.voto_eng

    dictionary = dictionaries.voto_anes
    
    if nsamples < 50:
      imatrix = index_matrix
    else:
      imatrix = np.loadtxt('matrix_50.txt', dtype=int).tolist()
    
    jsonl_name = './' + model + '_elecpres_' + b + 'b' +name + '.jsonl'
    #llama_elecpres_13bllama_json_inverted_rfewshot_5
    if finetuned:
      jsonl_name = './elecpres' +name + '.jsonl'
    
    #####################   Prompts   ######################
    #if finetuned:
    #  task= "Analiza el perfil de la siguiente persona y entrega la respuesta que probablemente daría dicha persona a la pregunta que se hará.\n "
      #inst = ""
    #  end= ""
    if not eng:
      task="Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en la segunda vuelta presidencial de Chile del 2021. Debes responder siempre con tan solo una palabra de entre las siguientes opciones: Boric, Kast o Nulo.\n "
      task_json = "Eres un modelo predictor. Tu tarea es predecir las respuestas de una persona a cierta pregunta basándote en sus características sociodemográficas. Las características sociodemográficas estarán delimitadas con triple backsticks, la pregunta estará delimitada con los siguientes símbolos < >, y las alternativas de respuesta por [ ]."
      context = "Primero te voy a dar un poco de contexto en el que debes situarte. La elección presidencial de Chile para el período 2022-2026 se realizó el 21 de noviembre de 2021, la segunda vuelta electoral, en tanto, tuvo lugar el 19 de diciembre de 2021.\n El resultado de la primera vuelta presidencial ubica a José Antonio Kast en primer lugar con un 27,91% de los votos, a Gabriel Boric Font en segundo lugar con un 25.83% de los votos, el resto de los candidatos no lograron obtener más de un 12% de los votos. Por lo tanto, Gabriel Boric y José Antonio Kast fueron los candidatos que pasaron a la segunda vuelta.\n Así los chilenos debían elegir entre un candidato de izquierda y otro de derecha respectivamente. El enfoque principal de la candidatura de Gabriel Boric era igualdad de género, seguridad social y sustentabilidad. Por otro lado el candidato José Antonio Kast realizó una campaña centrada en seguridad, orden, disminución del Estado e instalándose como opositor a los sucesos relacionados con el estallido social del 2019.\n"
      end = "Ahora analiza el perfil de la siguiente persona y responde a la pregunta que se te hará. \n "
      inst = "Recuerda responder en solo 1 palabra. \n"
      #context = " La pregunta que se te hará será sobre la segunda vuelta de la elección presidencial de 2021, en esta elección habían 2 candidatos. Gabriel Boric, de izquierda. José Antonio Kast Rist, de derecha. Y como siempre los ciudadanos podían anular el voto si no les gustaba ninguno de los 2 candidatos.\n"
      inst_json = "Entrega un JSON con las siguientes llaves: 'explicación' (EN MAXIMO 100 PALABRAS)  donde darás el razonamiento para responder a la pregunta, y 'respuesta' que mostrará la alternativa que elegiste para responder."
      #end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes llaves: 'prediccion' conteniendo la alternativa elegida para responder a la pregunta, 'explicación' (en no más de 100 palabras) explicando por qué elegiste esa alternativa."
      #end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes llaves: 'explicacion' (EN MÁXIMO 100 PALABRAS) donde explicarás la cadena de razonamientos que sigues para responder a la pregunta y 'respuesta' que muestre el candidato por el cual votaría la persona con dichas características. "
      
    else:
      task =  "Your job is to be an assistant who will help predict the vote of certain people in the 2021 Chilean presidential second round. You must always respond with just one of the following options (without extra explanations): Gabriel Boric, José Antonio Kast or null.\n"
      #context =  "First I'm going to give you a little context in which you should place yourself. The presidential election of Chile for the period 2022-2026 was held on November 21, 2021, the second electoral round, meanwhile, took place on December 19, 2021.\n The result of the first presidential round places José Antonio Kast in first place with 27.91% of the votes, Gabriel Boric Font in second place with 25.83% of the votes, the rest of the candidates failed to obtain more than 12% of the votes. Therefore, Gabriel Boric and José Antonio Kast were the candidates who went to the second round.\n Thus, Chileans had to choose between a left-wing candidate and a right-wing candidate respectively. The main focus of Gabriel Boric's candidacy was gender equality, social security and sustainability. On the other hand, the candidate José Antonio Kast carried out a campaign focused on security, order, reduction of the State and establishing himself as an opponent of the events related to the social outbreak of 2019.\n"
      context = "\n First I'm going to give you a little context in which you should place yourself. The 2020 United States presidential election took place on November 3 and featured several candidates. The main contenders were Joe Biden from the Democratic Party and incumbent President Donald Trump from the Republican Party. Joe Biden, with Kamala Harris as his vice-presidential candidate, focused his campaign on managing the COVID-19 pandemic, criticizing Trump's response, and proposing a more scientific and coordinated approach. He also emphasized social and racial justice, proposing police reforms and greater equity, as well as tackling climate change by promising to rejoin the Paris Agreement and develop ambitious environmental policies. Additionally, Biden advocated for greater economic stimulus to support working families and small businesses affected by the pandemic. Donald Trump, with Mike Pence as his vice-presidential candidate, defended his handling of the pandemic, highlighting the rapid development of vaccines, and adopted a 'law and order' stance in response to racial justice protests. Trump also emphasized his economic growth record before the pandemic and promised a swift economic recovery, while continuing his policies of environmental deregulation and support for the fossil fuel industry. \n In addition to Biden and Trump, there were other minor party candidates. Jo Jorgensen from the Libertarian Party advocated for reducing the size of the government, lowering taxes, legalizing drugs, and withdrawing U.S. troops from overseas conflicts. Howie Hawkins from the Green Party centered his campaign on the Green New Deal, an ambitious agenda to address climate change and promote social and economic justice, as well as proposing the expansion of public healthcare and electoral reform."
      end = "\n Now analyze the profile of the following person and answer the question that will be asked of you. "
      inst = "Remember to answer just in 1 word. \n"

    if spec:
      inst = " Por favor también responde en a lo más 200 palabras por qué crees que la persona eligiría esa opción y en qué variables te fijaste al hacer la predicción. Usa la primera palabra para indicar la opción elegida y el resto de palabras para explicar el por qué."


    if prompting_estructure=="json":
      task = "You are a predictive model. Your task is to predict a person's answers to a certain question based on their sociodemographic characteristics. The sociodemographic characteristics will be delimited with triple backsticks, the question will be delimited with the following symbols < >, and the response alternatives by [ ].\n"
      inst = " Deliver a JSON with the following keys: 'explanation' (IN MAXIMUM 100 WORDS) where you will write your reasoning to answer the question, and 'answer' that shows the alternative chosen to answer the question."

    if prompt_type == "anes" and not prompting_estructure=="json":
      task = "Your job is to be an assistant who will help predict the vote of certain people in the 2020 presidential election of the United States. You must always respond with just one of the following options: Joe Biden, Donald Trump, Jo Jorgensen, Howie Hawkins. \n"
    if not with_context:
      context = ""

    #inst="¿Por quién votó esta persona en las elecciones presidenciales de Chile del 2021?¿Gabriel Boric, José Antonio Kast, o nulo?"
    super().__init__(1, model, b, chat, jsonl_name,  task ,"", "", inst, dictionary, eng, prompting_estructure, prompt_type,translate, ablation, finetuned, nsamples, random_fewshot, imatrix )
              # exp, model_name, b,chat,jsonl_name, task, context, end , inst, dictionary, eng, prompt_type ,translate,ablation, finetuned, nsamples, random_fewshot, index_matrix
              

########################################### Función Requests ###################################################
b = str(7)

################################################### Original ###################################################

#llama_elecpres_13b_json_anes_ablation_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_anes_ablation_rfs5", eng = True, prompting_estructure="json", prompt_type="anes", translate=False,  ablation = True, random_fewshot =True, nsamples = 5)
#r.ablation_request(anes_df)

#llama_elecpres_13b_json_onlypolwpv_final_rfs5.jsonl
r=Elecpres_Requester("llama","13", True, "_json_onlypolwpv_final_rfs5", eng = True, prompting_estructure="json", prompt_type="wpv",translate=False, random_fewshot = True, nsamples = 5)
r.answers_generator(anes_df)

#mistral_elecpres_v0.2b_originalprompt_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_originalprompt_rfs5", eng = True, prompting="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_originalprompt_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_originalprompt_rfs5", eng = True, prompting="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_originalprompt_withoutcontext_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_originalprompt_withoutcontext_rfs5", eng = True, prompting="normal", random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_originalprompt_withoutcontext_rfs5.jsonl - REVISADO
#r=Elecpres_Requester("mistral","v0.2", True, "_originalprompt_withoutcontext_rfs5", eng = True, prompting="normal", random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_oom_taskend_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_oom_taskend_rfs5", eng = True, prompting="oom", random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)


################################################################################

#llama_elecpres_13b_oom_prompt_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_oom_prompt_rfs5", eng = True, prompting="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_oom_prompt_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_oom_prompt_rfs5", eng = True, prompting="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#t0_elecpres_b_oom_prompt_rfs5.jsonl
#t0_elecpres_b_original_withoutcontext_prompt_rfs5.jsonl
#r=Elecpres_Requester("t0","", True, "_original_withoutcontext_prompt_rfs5", eng = True, prompting_estructure="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)


####################################################################################

#llama_elecpres_13b_json_inverted_final_esp_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_final_esp_rfs5",eng = False, prompting="json",translate=False, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_json_inverted_final_esp_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_inverted_final_esp_rfs5",eng = False, prompting_estructure="json",translate=False, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_json_inverted_final_rfs0.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_inverted_final_rfs0",eng = True, prompting_estructure="json",translate=False, random_fewshot =False, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_json_inverted_final_rfs0.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_final_rfs0",eng = True, prompting="json",translate=False, random_fewshot = False, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_json_inverted_final_rfs50.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_final_rfs50",eng = True, prompting_estructure="json",translate=False, random_fewshot = True, nsamples = 50)
#r.answers_generator(df1)

#llama_elecpres_13b_json_inverted_final_rfs50.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_inverted_final_rfs50",eng = True, prompting_estructure="json",translate=False, random_fewshot = True, nsamples = 50)
#r.answers_generator(df1)

#elecpresf_10000_1e6_01_1_json_inverted_final_rfs0.jsonl
#r=Elecpres_Requester("f_10000_1e6_01_1","", True, "f_10000_1e6_01_1_json_inverted_final_rfs0",eng = True, prompting_estructure="json",translate=False, finetuned = True, random_fewshot = False, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_json_inverted_final_context_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_final_context_rfs5", eng = True, prompting="json",translate=False, random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_json_inverted_final_context_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_inverted_final_context_rfs5", eng = True, prompting_estructure="json",translate=False, random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_json_inverted_wpv_final_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_wpv_final_rfs5", eng = True, prompting_estructure="json", prompt_type="onlypol",translate=False, random_fewshot = True, nsamples = 5)
#r.answers_generator(df1)


#llama_elecpres_13b_json_inverted_final_ablation_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_inverted_final_ablation_rfs5", eng = True, prompting="json", translate=False,  ablation = True, random_fewshot =True, nsamples = 5)
#r.ablation_request(df1.drop(df1.index[:193]))



#mistral_elecpres_v0.2b_json_inverted_final_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_inverted_final_rfs5",eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#t0_elecpres_b_json_inverted_final_rfs5.jsonl
#r=Elecpres_Requester("t0","", True, "_json_inverted_final_rfs5", eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#####################################################################################

#llama_elecpres_13b_text_template_final_rfs5.jsonl
#llama_elecpres_13b_list_template_final_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_list_template_final_rfs5",eng = True, prompting_estructure="list",random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#mistral_elecpres_v0.2b_text_template_final_rfs5.jsonl
#mistral_elecpres_v0.2b_list_template_final_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_list_template_final_rfs5",eng = True, prompting_estructure="list", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#t0_elecpres_b_text_template_final_rfs5.jsonl
#r=Elecpres_Requester("t0","", True, "_text_template_final_rfs5", prompting_estructure="text", random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#t0_elecpres_b_list_template_final_rfs5.jsonl
#r=Elecpres_Requester("t0","", True, "_list_template_final_rfs5", prompting="list",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1.drop(df1.index[:576]))

################################################## RANDOM FEWSHOT ###################################################
#r = Elecpres_Requester(b, "_rfewshot", random_fewshot =True, examples_df = fewshotexamples_df)
#r.answers_generator(fewshot_df) #3, 6
#r=Elecpres_Requester("llama-2-13b-chat_v15_ENG_NORMAL_EVAL_5000_inverted",str(13), True, "llama_v15_NORMAL_ENG_5000_eval_inverted_rfewshot_5", translate=True,finetuned = True,  random_fewshot =True, nsamples = 5)
#r=Elecpres_Requester("llama",str(13), True, "llama_json_inverted_rfewshot_5", translate=True, random_fewshot =True, nsamples = 5)
#r=Elecpres_Requester("finetuning-mistral-0.2-inst_v2_ENG_NORMAL_EVAL_5000_inverted/checkpoint-700", "v0.2", True, "_mistral_finetuned_v2_rfewshot_10", translate=True,finetuned = True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#r = Elecpres_Requester("t0","", True, "_text_anes_rfs5",eng = True, prompting_estructure="text", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

#r = Elecpres_Requester("t0","", True, "_list_anes_rfs5",eng = True, prompting_estructure="list", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df.drop(anes_df.index[:200])) #539

#r = Elecpres_Requester("t0","", True, "_oom_anes_rfs5",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

#r = Elecpres_Requester("t0","", True, "_original_anes_rfs5",eng = True, prompting_estructure="normal", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

#r = Elecpres_Requester("t0","", True, "_json_anes_rfs5",eng = True, prompting_estructure="json", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#
# 
# 
# r.answers_generator(anes_df) #539

################################################### SPEC ###################################################
#answers_generator(dataset, b, task, context, end, spec, name = "_spec")

###################################################  WPV  ###################################################
#answers_generator(dataset_wpv, b, task, context, end, inst, name = "_wpv")

""" r = Elecpres_Requester("mistral", "v0.2", "_sys_wpv", sys=True)
r.answers_generator(df1)

r = Elecpres_Requester("mistral", "v0.2", "_wpv")
r.answers_generator(df1)
 """

###################################################  REDUCED  ###################################################
""" #answers_generator(dataset_red, b, task, context, end, inst, name = "_red")
r = Elecpres_Requester("mistral", "v0.2", "_sys_red", sys=True)
r.answers_generator(df1)

r = Elecpres_Requester("mistral", "v0.2", "_red")
r.answers_generator(df1) """
###################################################  ENG  ###################################################
#answers_generator(dataset_eng, b, task_eng, context_eng, end_eng, "", name = "_eng", random_fewshot=True, nsamples = 1)
#r = Elecpres_Requester("mistral", "v0.2", "_sys_red", sys=True, with_context = False )
#r.answers_generator(df1)

# r=Elecpres_Requester("respuestas", str(7), "_eng", eng =True)
# r.answers_generator(df1)

# r=Elecpres_Requester("respuestas", str(13), "_eng", eng =True)
# r.answers_generator(df1)

#r = Elecpres_Requester("mistral", "v0.2", "_eng_resto", eng= True)
#r.answers_generator(df1)
############################################## WITHOUT CONTEXT ####################################
# r = Elecpres_Requester("llama", b, "_withoutcontext", with_context = False)
# r.answers_generator(df1) #3, 6 

#r = Elecpres_Requester("mistral", "v0.2", "_sys_withoutcontext", sys=True, with_context = False )
#r.answers_generator(df1)

#r = Elecpres_Requester("mistral", "v0.2", "_withoutcontext", with_context = False)
#r.answers_generator(df1) 

###################################################  ABLATION  ###################################################
#r = Elecpres_Requester(str(7), "_ablation", ablation = True)
#r.ablation_request(df1) #3, 6

#r = Elecpres_Requester(str(13), "_ablation", ablation = True)
#r.ablation_request(df1) #3, 6

###################################################### ANES ###################################################

#llama_elecpres_13b_json_anes_context_rfs5.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_anes_context_rfs5",eng = True, prompting_estructure="json", prompt_type="anes",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df.drop(anes_df.index[:612]))

#t0_elecpres_json_anes_rfs5.jsonl
#r=Elecpres_Requester("t0","13", True, "_json_anes_rfs5",eng = True, prompting_estructure="json", prompt_type="anes",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#mistral_elecpres_v0.2b_json_anes_context_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_json_anes_context_rfs5",eng = True, prompting_estructure="json", prompt_type="anes",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df.drop(anes_df.index[:546]))#137

#t0_elecpres_b_json_inverted_final_rfs5.jsonl
#r=Elecpres_Requester("t0","", True, "_json_inverted_final_rfs5", eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df1)

#llama_elecpres_13b_text_template_final_rfs5.jsonl
#llama_elecpres_13b_list_template_final_rfs5.jsonl
#mistral_elecpres_v0.2banes_json_rfs0.jsonl
#llama_elecpres_13banes_json_ablacion_rfs5.jsonl#llama_elecpres_13banes_json_rfs0.jsonl
#r=Elecpres_Requester("llama","13", True, "_json_ablation_rfs5_final_v2",eng = True, prompting_estructure="json", translate=False,  ablation = True, random_fewshot =True, nsamples = 5)
#r.ablation_request(df1.drop(df1.index[:252]))

#mistral_elecpres_v0.2b_text_template_final_rfs5.jsonl
#mistral_elecpres_v0.2b_list_template_final_rfs5.jsonl
#r=Elecpres_Requester("mistral","v0.2", True, "_oom_template_final_rfs5",eng = True, prompting_estructure="oom", prompt_type="anes", random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r=Elecpres_Requester("mistral","v0.2", True, "anes_json_rfs0",eng = True, prompting_estructure="json", prompt_type="anes", random_fewshot =False, nsamples = 5)
#r.answers_generator(anes_df)