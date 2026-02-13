import pandas as pd
from chatgpt_aux import *
import dictionaries
from index_matrix import index_matrix
#anes_df =  pd.read_csv("anes_2020_660.csv")
#anes_100_df =  pd.read_csv('anes_2020_100.csv')

anes_df =  pd.read_csv("anes_2020_660_v1.csv")
anes_100_df =  pd.read_csv('anes_2020_100_v1.csv')

#df1 = pd.read_csv('exp1_fewshot_inputs.csv')
#fewshotexamples_df = pd.read_csv('prompt_dataset_presidencial_fewshotexamples.csv')
#exp1_complete_df = pd.read_csv('exp1_inputs.csv')

data = pd.read_csv('exp2_inputs_filtrado.csv')
n_exp = 3
eng = True
#print(data)
#print(n_exp)

############################### PROMPTS ##############################
if not eng:
  task = "Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en la segunda vuelta presidencial de Chile del 2021. Debes responder siempre con tan solo una palabra de entre las siguientes opciones: Boric, Kast o Nulo.\n "
  end = "Ahora analiza el perfil de la siguiente persona y responde a la pregunta que se te hará. "
else:
  end = "Now analyze the profile of the following person and answer the question that will be asked of you."

task_eng = "Your job is to be an assistant who will help predict the vote of certain people in the 2021 Chilean presidential second round. You must always respond with just one word from the following options: Boric, Kast or Null. \n"
task_anes_eng = "Your job is to be an assistant who will help predict the vote of certain people in the 2020 presidential election of the United States. You must always respond with just one of the following options: Joe Biden, Donald Trump, Jo Jorgensen, Howie Hawkins. \n"

inst_eng = "Remember to answer in just 1 word. "

spec = " Por favor también responde en a lo más 200 palabras por qué crees que la persona eligiría esa opción y en qué variables te fijaste al hacer la predicción. Usa la primera palabra para indicar la opción elegida y el resto de palabras para explicar el por qué."
inst = "Recuerda responder tan solo en 1 palabra. \n"

inst = "Who did this person vote for in the 2021 Chilean presidential elections? Gabriel Boric, José Antonio Kast, or null?"

task_json = "You are a predictive model. Your task is to predict a person's answers to a certain question based on their sociodemographic characteristics. The sociodemographic characteristics will be delimited with triple backsticks, the question will be delimited with the following symbols < >, and the response alternatives by [ ]."
inst_json = "Deliver a JSON with the following keys: 'explanation' (IN MAXIMUM 100 WORDS) where you will write your reasoning to answer the question, and 'answer' that shows the alternative chosen to answer the question."

task_json_esp = "Eres un modelo predictor. Tu tarea es predecir las respuestas de una persona a cierta pregunta basándote en sus características sociodemográficas. Las características sociodemográficas estarán delimitadas con triple backsticks, la pregunta estará delimitada con los siguientes símbolos < >, y las alternativas de respuesta por [ ]."
inst_json_esp = "Entrega un JSON con las siguientes llaves: 'explicación' (EN MÁXIMO 100 PALABRAS)  donde darás el razonamiento para responder a la pregunta, y 'respuesta' que mostrará la alternativa que elegiste para responder."

if n_exp==1:
  context = "Primero te voy a dar un poco de contexto en el que debes situarte. La elección presidencial de Chile para el período 2022-2026 se realizó el 21 de noviembre de 2021, la segunda vuelta electoral, en tanto, tuvo lugar el 19 de diciembre de 2021.\n El resultado de la primera vuelta presidencial ubica a José Antonio Kast en primer lugar con un 27,91% de los votos, a Gabriel Boric Font en segundo lugar con un 25.83% de los votos, el resto de los candidatos no lograron obtener más de un 12% de los votos. Por lo tanto, Gabriel Boric y José Antonio Kast fueron los candidatos que pasaron a la segunda vuelta.\n Así los chilenos debían elegir entre un candidato de izquierda y otro de derecha respectivamente. El enfoque principal de la candidatura de Gabriel Boric era igualdad de género, seguridad social y sustentabilidad. Por otro lado el candidato José Antonio Kast realizó una campaña centrada en seguridad, orden, disminución del Estado e instalándose como opositor a los sucesos relacionados con el estallido social del 2019.\n"
  context_eng     =  "First I'm going to give you a little context in which you should place yourself. The presidential election of Chile for the period 2022-2026 was held on November 21, 2021, the second electoral round, meanwhile, took place on December 19, 2021.\n The result of the first presidential round places José Antonio Kast in first place with 27.91% of the votes, Gabriel Boric Font in second place with 25.83% of the votes, the rest of the candidates failed to obtain more than 12% of the votes. Therefore, Gabriel Boric and José Antonio Kast were the candidates who went to the second round.\n Thus, Chileans had to choose between a left-wing candidate and a right-wing candidate respectively. The main focus of Gabriel Boric's candidacy was gender equality, social security and sustainability. On the other hand, the candidate José Antonio Kast carried out a campaign focused on security, order, reduction of the State and establishing himself as an opponent of the events related to the social outbreak of 2019.\n"
if n_exp==2:
  if eng:
    task = "Your job is to be an assistant that will help predict the vote of certain individuals in the chilean exit plebiscite for the New Constitution of 2022. You must always respond with just one of the following options(without extra explanations): Approve, Reject, or Null."
    context = " Now I'll give you a bit of context. In the year 2020, in Chile, a vote took place to decide whether Chileans wanted a New Constitution to replace the existing one created in 1980 and modified in the following years until the present. The first question in this vote was whether the voter agreed to draft a new Constitution, where 78% of voters chose the 'Approve' option. The second question was about the body responsible for drafting the new Constitution, and the winning option was a constitutional convention entirely composed of citizens chosen exclusively for this purpose.\n With the results of this vote, the constitutional process began. The next step was to elect representatives to the constitutional convention through popular vote. The convention consisted of 28 seats for 'Apruebo Dignidad,' 25 seats for the 'Apruebo' list, 37 seats for 'Vamos por Chile,' 47 seats for independents on lists, 17 seats for indigenous peoples, and 1 independent outside the pact. Thus, the constitutional convention was mainly composed of representatives from the center-left and left. In fact, several delegates had been active figures during the social outbreak of 2019.\n After over a year of work, in July 2022, the proposal for the New Constitution was presented. This proposal had several articles focused on gender equality, decentralization of the country, plurinationality, ecology, and sustainability. Some of these articles generated fears and suspicion in Chilean society, such as plurinationality.\n On September 4, 2022, the exit plebiscite for the New Constitution took place in an increasingly polarized political environment, where support for the social outbreak was decreasing despite its initial widespread majority. This was also accompanied by an atmosphere of misinformation, generating fears such as property loss, loss of education rights for one's own children, among others. This plebiscite was mandatory, unlike all previous votes, and had only one question: 'Do you approve the text of the New Constitution proposed by the Constitutional Convention?' The voter had two options to mark: Approve or Reject.  As always, the voter also had the possibility to invalidate their vote in case they did not choose any of the 2 previous options by voting null.\n"
  else:
    task="Tu trabajo es ser un asistente que ayudará a predecir el voto de ciertas personas en el plebiscito de salida para la nueva constitución de Chile realizado en Septiembre del 2022. Debes responder siempre con tan solo una palabra de entre las siguientes opciones(sin explicaciones extras): Apruebo, Rechazo o Nulo.\n "
if n_exp == 3:
  if eng:
    task = "Your job is to be an assistant who will help predict the opinion of certain people regarding abortion. You must always respond with just one of the following options: Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case. \n"

context_anes = "\n First I'm going to give you a little context in which you should place yourself. The 2020 United States presidential election took place on November 3 and featured several candidates. The main contenders were Joe Biden from the Democratic Party and incumbent President Donald Trump from the Republican Party. Joe Biden, with Kamala Harris as his vice-presidential candidate, focused his campaign on managing the COVID-19 pandemic, criticizing Trump's response, and proposing a more scientific and coordinated approach. He also emphasized social and racial justice, proposing police reforms and greater equity, as well as tackling climate change by promising to rejoin the Paris Agreement and develop ambitious environmental policies. Additionally, Biden advocated for greater economic stimulus to support working families and small businesses affected by the pandemic. Donald Trump, with Mike Pence as his vice-presidential candidate, defended his handling of the pandemic, highlighting the rapid development of vaccines, and adopted a 'law and order' stance in response to racial justice protests. Trump also emphasized his economic growth record before the pandemic and promised a swift economic recovery, while continuing his policies of environmental deregulation and support for the fossil fuel industry. \n In addition to Biden and Trump, there were other minor party candidates. Jo Jorgensen from the Libertarian Party advocated for reducing the size of the government, lowering taxes, legalizing drugs, and withdrawing U.S. troops from overseas conflicts. Howie Hawkins from the Green Party centered his campaign on the Green New Deal, an ambitious agenda to address climate change and promote social and economic justice, as well as proposing the expansion of public healthcare and electoral reform."

############################## SEGMENTACION #########################

def df_joiner(df_list):
  df = pd.concat(df_list, ignore_index=True)
  df.drop(['Unnamed: 0'], axis = 'columns', inplace=True)
  return df

############################## SEGMENTACION #########################


def requester(df, n, context, inst, dictionary, var_to_remove=False):
  df_list = []
  i=0

  while i+n < len(df):
    print(i)
    print(len(df))
    print(var_to_remove)
    #model="gpt-4-turbo", "gpt-3.5-turbo-0125
    i_df = vote_prediction(df, dictionary, context, inst, start=i, n = n, model="gpt-4-turbo",  exp = n_exp, prompting = "json", prompt_type="anes", eng= eng, ablation = var_to_remove, random_fewshot= True, n_samples=5, index_matrix=index_matrix)
    df_list.append(i_df)
    i+= n
    #i_df.to_csv("resultados_gpt_prompting_final/expanes_chatgpt3_text_rfs5" + str(i) +".csv")
  if i < len(df):
    i_df = vote_prediction(df, dictionary, context, inst, start=i, n = len(df)-i, model="gpt-4-turbo", exp = n_exp, prompting = "json", prompt_type="anes", eng= eng, ablation = var_to_remove, random_fewshot= True, n_samples=5, index_matrix=index_matrix)
    df_list.append(i_df)
    i = len(df)
    #i_df.to_csv("resultados_gpt_prompting_final/expanes_chatgpt3_list_context_rfs5" + str(i) +".csv") 
  return df_list


def ablation_requester(df, n, context, dictionary):
  variables = ["gender"]
  for var in variables:
    df_list = requester(df, n, context, dictionary, var_to_remove=var)
    joined_df = df_joiner(df_list)
    df = joined_df

  return df

#exp1_complete_rest = exp1_complete_df.copy(deep=True)
#exp1_complete_rest = exp1_complete_rest.iloc[range(800,814)]



#df_list = requester(data, 100, "task+context+end", dictionaries.voto) #normal
#df_list = requester(data, 100, task_eng + context_eng + end_eng, dictionaries.voto) #normal

#df_list = requester(data, 100, task_json, end_json, dictionaries.voto) #normal
#df_list = requester(data, 100, task + end_eng , "" , dictionaries.voto_eng) #normal
#df_list = requester(data, 100, task + end_eng , "" , dictionaries.plebiscito_eng) #normal
#df_list = requester(data, 100, task_json , inst_json ,  dictionaries.voto_eng) #normal
#df_list = requester(data, 100, task+context+end_eng , "" ,  dictionaries.plebiscito_eng)
#df_list = requester(anes_df, 100, task_json, inst_json, dictionaries.aborto_eng) #normal
df_list = requester(anes_df, 100, task_json, inst_json, dictionaries.aborto_eng) #normal

#df_list = requester(data, 100, "" , "" , dictionaries.aborto_eng) #normal

joined_df = df_joiner(df_list)
#joined_df.to_csv("resultados_gpt_prompting_final/expanes_chatgpt4_oom_rfs0.csv")
joined_df.to_csv("resultados_gpt_prompting_final/exp3anes_chatgpt4_json_rfs5.csv")
print(joined_df)


# df_r= ablation_requester(exp1_complete_rest, 14, task+context+end, dictionaries.voto)
# df_r.to_csv("exp1_chatgpt_sinsexo_rest.csv")
# print(df_r)


#ABORTO
# corri json gpt3
# corii list en llama mistral y gpt
# corri text en llama mistral y gpt
# corri oom en llama mistral y gpt