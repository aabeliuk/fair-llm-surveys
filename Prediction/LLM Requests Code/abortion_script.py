import pandas as pd
from requester_script import Exp_Request
from matrix_aborto import index_matrix
import dictionaries
import numpy as np
from index_matrix import index_matrix

df = pd.read_csv('exp2_inputs_filtrado.csv')
#df = df.iloc[315:]#151#315


#data = pd.read_csv('exp1_inputs.csv')
fewshotexamples_df = pd.read_csv('exp_100_inputs.csv')
#fewshotexamples_df = pd.read_csv('fewshot_inputscsv')
anes_df =  pd.read_csv("anes_2020_660_v1.csv")
anes_100_df =  pd.read_csv('anes_2020_100_v1.csv')

# Definir la clase derivada (clase hija) que hereda de Animal
class Abortion_Requester(Exp_Request):
 
  def __init__(self, model, b, chat, name, eng=False, prompting_estructure = "normal", prompt_type="", with_context = True, spec = False,translate= False, ablation = False, finetuned=False, random_fewshot =False, nsamples = 0):
    # Llama al constructor de la clase padre usando super()
    #model_llama
    if random_fewshot:
      examples_df = fewshotexamples_df
    else: 
      examples_df = []

    if eng:
      dictionary = dictionaries.aborto_eng
    else:
      dictionary = dictionaries.aborto

    if nsamples < 50:
      imatrix = index_matrix
    else:
      imatrix = np.loadtxt('matrix_50.txt', dtype=int).tolist()
      print(imatrix)
    jsonl_name = './' + model + '_abortion_' + b + 'b' +name + '.jsonl'
    if finetuned:
      jsonl_name = './abortion_' +name + '.jsonl'
    
    #####################   Prompts   ######################
    #if finetuned:
    #  task= "Analiza el perfil de la siguiente persona y entrega la respuesta que probablemente daría dicha persona a la pregunta que se hará.\n "
      #inst = ""
    #  end= ""
    if not eng:
      #task="Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en la segunda vuelta presidencial de Chile del 2021. Debes responder siempre con tan solo una palabra de entre las siguientes opciones: Boric, Kast o Nulo.\n "
      task = "Eres un modelo predictor. Tu tarea es predecir las respuestas de una persona a cierta pregunta basándote en sus características sociodemográficas. Las características sociodemográficas estarán delimitadas con triple backsticks, la pregunta estará delimitada con los siguientes símbolos < >, y las alternativas de respuesta por [ ]."
      context = " La pregunta que se te hará será sobre la segunda vuelta de la elección presidencial de 2021, en esta elección habían 2 candidatos. Gabriel Boric, de izquierda. José Antonio Kast Rist, de derecha. Y como siempre los ciudadanos podían anular el voto si no les gustaba ninguno de los 2 candidatos.\n"
      end_JSON = "Genera solo un JSON (sin palabras ni explicaciones extras) con las siguientes llaves: 'prediccion' que muestre solo la opción elegida de entre las alternativas que se te darán, y 'explicacion' (en máximo 100 palabras) conteniendo la razón por la que elegiste dicha alternativa."
      #end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes llaves: 'prediccion' conteniendo la alternativa elegida para responder a la pregunta, 'explicación' (en no más de 100 palabras) explicando por qué elegiste esa alternativa."
      end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes llaves: 'explicacion' (EN MÁXIMO 100 PALABRAS) donde explicarás la cadena de razonamientos que sigues para responder a la pregunta y 'respuesta' que muestre el candidato por el cual votaría la persona con dichas características. "
      #end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes llaves: 'explicacion' (EN MÁXIMO 100 PALABRAS) donde responderás ¿Por qué no elegiste al otro candidato?¿Hace sentido tu respuesta con la ideología (izquierda-derecha) de la persona?, y 'respuesta' que muestre solo la opción elegida de entre las alternativas que se te darán. "
      #end = "A continuación se presenta una pregunta con las opciones de respuesta. Entrega un JSON con las siguientes 3 llaves: 'kast' donde responderás ¿Votaría esta persona por Kast para ser presidente y por qué? , 'boric' donde responderás ¿Votaría esta persona por Boric para ser presidente y por qué?, y 'respuesta' que muestre a cuál de los 2 elegiría de presidente."
      end = " Entrega un JSON con las siguientes llaves: 'explicacion' (EN MÁXIMO 100 PALABRAS) donde irás escribiendo tu razonamiento para responder a la pregunta, y 'respuesta' que muestre la alternativa elegida para responder a la pregunta."
    else:
      task = "Your job is to be an assistant who will help predict the opinion of certain people regarding abortion. You must always respond with just one of the following options: Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case. \n"
      context =  "First I'm going to give you a little context in which you should place yourself. The presidential election of Chile for the period 2022-2026 was held on November 21, 2021, the second electoral round, meanwhile, took place on December 19, 2021.\n The result of the first presidential round places José Antonio Kast in first place with 27.91% of the votes, Gabriel Boric Font in second place with 25.83% of the votes, the rest of the candidates failed to obtain more than 12% of the votes. Therefore, Gabriel Boric and José Antonio Kast were the candidates who went to the second round.\n Thus, Chileans had to choose between a left-wing candidate and a right-wing candidate respectively. The main focus of Gabriel Boric's candidacy was gender equality, social security and sustainability. On the other hand, the candidate José Antonio Kast carried out a campaign focused on security, order, reduction of the State and establishing himself as an opponent of the events related to the social outbreak of 2019.\n"
      end = "Now analyze the profile of the following person and answer the question that will be asked of you. \n"
      inst = ""
    if prompting_estructure=="json":
      task = "You are a predictive model. Your task is to predict a person's answers to a certain question based on their sociodemographic characteristics. The sociodemographic characteristics will be delimited with triple backsticks, the question will be delimited with the following symbols < >, and the response alternatives by [ ]."
      inst = " Deliver a JSON with the following keys: 'explanation' (IN MAXIMUM 100 WORDS) where you will write your reasoning to answer the question, and 'answer' that shows the alternative chosen to answer the question."
  
    if not with_context:
      context = ""

    
    super().__init__(3, model, b, chat, jsonl_name, task,"" , "", inst, dictionary, eng, prompting_estructure, prompt_type,translate, ablation, finetuned, nsamples, random_fewshot, imatrix )
  

########################################### Función Requests ###################################################
b = str(13)

#r=Abortion_Requester("llama","13", True, "_json_ablation_rfs5", eng = True, prompting_estructure="json", prompt_type="",ablation = True, translate=False, random_fewshot = True, nsamples = 5)
#r.ablation_request(df)

r=Abortion_Requester("llama","13", True, "_json_wpv_anes_rfs5", eng = True, prompting_estructure="json", prompt_type="wpv",ablation = False, translate=False, random_fewshot = True, nsamples = 5)
r.answers_generator(anes_df)

r=Abortion_Requester("llama","13", True, "_json_onlypol_anes_rfs5", eng = True, prompting_estructure="json", prompt_type="onlypol",ablation = False, translate=False, random_fewshot = True, nsamples = 5)
r.answers_generator(anes_df)


#r= Abortion_Requester("llama","13", True, "_list_anes_rfs5",eng = True, prompting_estructure="list", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

# r= Abortion_Requester("llama","13", True, "_text_anes_rfs5",eng = True, prompting_estructure="text", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
# r.answers_generator(anes_df)

# r= Abortion_Requester("llama","13", True, "_oom_anes_rfs5",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
# r.answers_generator(anes_df)

#r= Abortion_Requester("mistral","v0.2", True, "_list_anes_rfs5",eng = True, prompting_estructure="list", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r= Abortion_Requester("mistral","v0.2", True, "_text_anes_rfs5",eng = True, prompting_estructure="text", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r= Abortion_Requester("mistral","v0.2", True, "_oom_anes_rfs5",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r= Abortion_Requester("mistral","v0.2", True, "_json_anes_rfs5",eng = True, prompting_estructure="json", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)
#llama_abortion_13b_original_anes_rfs5

#r = Abortion_Requester("llama","13", True, "_json_anes_rfs5",eng = True, prompting_estructure="json", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df.drop(anes_df.index[:271]))

#r = Abortion_Requester("llama","13", True, "_original_anes_rfs5",eng = True, prompting_estructure="normal", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r = Abortion_Requester("mistral","v0.2", True, "_original_anes_rfs5",eng = True, prompting_estructure="normal", prompt_type="anes", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#r = Abortion_Requester("llama", "13", True, "_oom_anes_rfs0",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot = False, nsamples = 5)
#r.answers_generator(anes_df)

#r = Abortion_Requester("mistral","v0.2", True, "_oom_anes_rfs0",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot = False, nsamples = 5)
#r.answers_generator(anes_df.drop(anes_df.index[:539])) #539

#r = Abortion_Requester("t0","", True, "_oom_anes_rfs5",eng = True, prompting_estructure="oom", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

# r = Abortion_Requester("t0","", True, "_text_anes_rfs5",eng = True, prompting_estructure="text", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
# r.answers_generator(anes_df) #539

# r = Abortion_Requester("t0","", True, "_list_anes_rfs5",eng = True, prompting_estructure="list", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
# r.answers_generator(anes_df) #539

#r = Abortion_Requester("t0","", True, "_json_anes_rfs5",eng = True, prompting_estructure="json", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

#r = Abortion_Requester("t0","", True, "_normal_anes_rfs5",eng = True, prompting_estructure="normal", prompt_type="anes", translate=True, random_fewshot = True, nsamples = 5)
#r.answers_generator(anes_df) #539

#mistral_abortion_v0.2b_oom_wpv_prompt_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_anes_oom_wpv_prompt_rfs5", eng = True, prompting_estructure="oom", prompt_type="red", random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)

#llama_abortion_13b_anes_oom_wpv_prompt_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_anes_oom_wpv_prompt_rfs5", eng = True, prompting_estructure="oom", prompt_type="wpv", random_fewshot =True, nsamples = 5)
#r.answers_generator(anes_df)
################################################### Original ###################################################
#r = Abortion_Requester("llama",str(7), "_final", random_fewshot=True,  nsamples=1)
#r.answers_generator(df)
#r = Abortion_Requester("llama",str(13), "_final", random_fewshot=True,  nsamples=1)
#r.answers_generator(df)


#llama_abortion_13b_json_inverted_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_json_inverted_final_rfs5",eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_json_inverted_final_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_json_inverted_final_rfs5",eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#t0_abortion_b_json_inverted_final_rfs5.jsonl
#r=Abortion_Requester("t0","", True, "_json_inverted_final_rfs5", eng = True, prompting="json",translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df.drop(df.index[:600]))
 
######################################################################

#llama_abortion_13b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_list_template_final_rfs5",eng = True, prompting_estructure="list",random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_list_template_final_rfs5", eng = True, prompting_estructure="list", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#t0_abortion_b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("t0","", True, "_list_template_final_rfs5", eng = True, prompting_estructure="list", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#llama_abortion_13b_text_template_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_text_template_final_rfs5",eng = True, prompting_estructure="text",random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_text_template_final_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_text_template_final_rfs5", eng = True, prompting_estructure="text", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#t0_abortion_b_text_template_final_rfs5.jsonl
#r=Abortion_Requester("t0","", True, "_text_template_final_rfs5", eng = True, prompting_estructure="text", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

##################################################################################



#llama_abortion_13b_list_template_final_rfs0.jsonl
#r=Abortion_Requester("llama","13", True, "_list_template_final_rfs0",eng = True, prompting_estructure="list",random_fewshot =False, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_list_template_final_rfs0.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_list_template_final_rfs0", eng = True, prompting_estructure="list", random_fewshot =False, nsamples = 5)
#r.answers_generator(df)

#llama_abortion_13b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_list_template_final_rfs50",eng = True, prompting_estructure="list",random_fewshot =True, nsamples = 50)
#r.answers_generator(df)

#mistral_abortion_v0.2b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_list_template_final_rfs50", eng = True, prompting_estructure="list", random_fewshot =True, nsamples = 50)
#r.answers_generator(df)


#llama_abortion_13b_oom_template_esp_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_oom_template_esp_final_rfs5",eng = False, prompting_estructure="oom",random_fewshot =True, nsamples = 50)
#r.answers_generator(df)

#mistral_abortion_v0.2b_oom_template_esp_final_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_oom_template_esp_final_rfs5", eng = False, prompting_estructure="oom", random_fewshot =True, nsamples = 50)
#r.answers_generator(df)

#llama_abortion_13b_oom_ablation_rfs5_final_v2.jsonl
#r=Abortion_Requester("llama","13", True, "_oom_ablation_rfs5_final_v2", eng = True, prompting_estructure="oom", translate=False,  ablation = True, random_fewshot =True, nsamples = 5)
#r.ablation_request(df)

#llama_abortion_13b_list_template_final_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_list_template_final_rfs50",eng = True, prompting_estructure="list",random_fewshot =True, nsamples = 50)
#r.answers_generator(df)

#######################################################################

#llama_abortion_13b_oom_prompt_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_oom_esp_prompt_rfs5", eng = False, prompting_estructure="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_oom_prompt_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_oom_esp_prompt_rfs5", eng = False, prompting_estructure="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#llama_abortion_13b_oom_onlypol_prompt_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_oom_onlypol_prompt_rfs5", eng = True, prompting_estructure="oom", prompt_type="onlypol", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)




#llama_abortion_13b_oom_prompt_rfs0.jsonl
#r=Abortion_Requester("llama","13", True, "_oom_prompt_rfs0", eng = True, prompting_estructure="oom", random_fewshot =False, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_oom_prompt_rfs0.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_oom_prompt_rfs0", eng = True, prompting_estructure="oom", random_fewshot =False, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_oom_prompt_rfs5.jsonl
#r=Abortion_Requester("t0","", True, "_oom_prompt_rfs5", eng = True, prompting_estructure="oom", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#llama_abortion_13b_original_withoutcontext_prompt_rfs5.jsonl
#r=Abortion_Requester("llama","13", True, "_original_withoutcontext_prompt_rfs5", eng = True, prompting_estructure="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#mistral_abortion_v0.2b_original_withoutcontext_prompt_rfs5.jsonl
#r=Abortion_Requester("mistral","v0.2", True, "_original_withoutcontext_prompt_rfs5", eng = True, prompting_estructure="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

#t0_abortion_b_oom_prompt_rfs5.jsonl
#r=Abortion_Requester("t0","", True, "_original_prompt_rfs5", eng = True, prompting_estructure="normal", random_fewshot =True, nsamples = 5)
#r.answers_generator(df)
###################################################SPEC###################################################
#answers_generator(dataset, b, task, fin, spec, name = "_spec", few_shot=True )

###################################################  WPV  ###################################################

# r = Abortion_Requester(str(13), "_wpv", wpv = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)
# r = Abortion_Requester(str(7), "_wpv", wpv = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)

###################################################  REDUCED  ###################################################
""" r = Abortion_Requester(str(13), "_red", red = True, fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.answers_generator(df)

r = Abortion_Requester(str(7), "_red", red = True, fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.answers_generator(df)
 """

# r = Abortion_Requester(str(13), "_red", red = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)
# r = Abortion_Requester(str(7), "_red", red = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)

##################################################  ENG  ###################################################
""" r = Abortion_Requester("str(13), "_eng", eng = True, fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.answers_generator(df)

r = Abortion_Requester(str(7), "_eng", eng = True, fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.answers_generator(df) """

#r = Abortion_Requester("mistral", "v0.2", "_eng_final", eng = True, random_fewshot=True, nsamples=1)
#r.answers_generator(df) 
# r = Abortion_Requester(str(13), "_eng", eng = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)
# r = Abortion_Requester(str(7), "_eng", eng = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
# r.answers_generator(df)

    
################################################## RANDOM FEWSHOT ###################################################
""" r = Abortion_Requester(str(13), "_rfewshot", random_fewshot=True, examples_df = fewshotexamples_df )
r.answers_generator(df)

r = Abortion_Requester(str(7), "_rfewshot", random_fewshot=True, examples_df = fewshotexamples_df )
r.answers_generator(df)  """
#r=Elecpres_Requester("llama-2-13b-chat_v15_ENG_NORMAL_EVAL_5000_inverted",str(13), True, "llama_v15_NORMAL_ENG_5000_eval_inverted_rfewshot_5", translate=True,finetuned = True,  random_fewshot =True, nsamples = 5)
#r=Abortion_Requester("llama-2-13b-chat_v15_ENG_NORMAL_EVAL_5000_inverted",str(13), True, "llama_v15_NORMAL_ENG_5000_eval_inverted_rfewshot_5", translate=True,finetuned = True,  random_fewshot =True, nsamples = 5)
#r=Abortion_Requester("llama",str(13), True, "llama_json_inverted_rfewshot_5", translate=True, random_fewshot =True, nsamples = 5)
#r.answers_generator(df)

###################################################  FEWSHOT  ###################################################
#answers_generator(dataset, b, task, fin, inst, name = "_fewshot", few_shot = True)

################################################### ABLATION ###################################################
""" r = Abortion_Requester(str(7), "_ablation", ablation = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.ablation_request(df) #3, 6

r = Abortion_Requester(str(13), "_ablation", ablation = True, random_fewshot=True, examples_df = fewshotexamples_df , nsamples=1)
r.ablation_request(df) #3, 6 """

#r=Abortion_Requester("f_10000_1e6_01_1","", True, "f_10000_1e6_01_1_json_inverted_final_rfs0",eng = True, prompting_estructure="json",translate=False, finetuned = True, random_fewshot = False, nsamples = 5)
#r.answers_generator(df)

#r=Abortion_Requester("f_1000_1e6_01_1","", True, "f_1000_1e6_01_1_json_inverted_final_rfs0",eng = True, prompting_estructure="json",translate=False, finetuned = True, random_fewshot = False, nsamples = 5)
#r.answers_generator(df.drop(df.index[:510]))

