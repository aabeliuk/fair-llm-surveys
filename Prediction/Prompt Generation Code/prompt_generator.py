from dictionaries import *
import pandas as pd
import random

def non_political_prompt(person):
  p_edad_sexo = ""
  p_region = ""
  p_gse_esc = ""
  p_religion = ""
  p_orig= ""

  #AGE AND GENDER
  p_edad_sexo = f"Persona de {str(person["edad"])} años, de sexo {dict_sexo[person["sexo"]]}. "

  #REGION
  if person["zona_u_r"] == 1:
    p_region =  f"Vive en la región {person["nom_region"]} en Chile, en una zona urbana. "

  else:
    p_region =  f"Vive en la región {person["nom_region"]} en Chile, en una zona rural. "

  # ECONOMIC LEVEL aND SCHOLARITY
  p_gse_esc = f"Su nivel socioeconómico es {gse[str(int(person["gse"]))]} y su nivel de escolaridad es {escolaridad[str(int(person["esc_nivel_1"]))]}. "

  # NATIVE PEOPLE
  if person["info_enc_58"] == 1:
    if person["info_enc_30"]!=0 and person["info_enc_30"] != 11 and person["info_enc_30"] != 88  and person["info_enc_30"] != 888 and person["info_enc_30"] != 999:
      p_orig = f"Pertenece al pueblo originario {pueblo[person["info_enc_30"]]}. "
    else:
      p_orig = "Pertenece a un pueblo originario. "


  # RELIGION
  if person["religion_82"] == 88 or person["religion_82"] == 99:
    p_religion = ""
  elif person["religion_82"] == 9: # NONE
    p_religion =  "No se siente cercana a ninguna religión. "
  elif person["religion_82"] == 10 or person["religion_82"] == 11 :
    p_religion = f"En cuanto a la religión, se considera {religion[str(int(person["religion_82"]))]}. "
  else:
    p_religion = f"En cuanto a la religión, se considera una persona más cercana a la religión {religion[str(int(person["religion_82"]))]}. "

  return p_edad_sexo + p_region + p_gse_esc  + p_orig + p_religion



def political_prompt(person, prompting):
  #PROMPT WITH IDEOLOGY - PARTY - INTEREST
  
  p_ideo_part_inter = "En cuanto a la política"
  

  if person["iden_pol_2"] != 88 and person["iden_pol_2"] != 99 and person["iden_pol_2"] != ' ':
    p_ideo_part_inter += f", en la escala izquierda - derecha se siente más cercana a la {izq_der[str(int(person["iden_pol_2"]))]}"
  if person["iden_pol_3"] != 99 and person["iden_pol_3"]!= 88:
    if person["iden_pol_3"] == 15:
      p_ideo_part_inter += ", no simpatiza ni se siente cercana a ningún partido"
    else:
      p_ideo_part_inter += f", el partido con el que más simpatiza es el {party[str(int(person["iden_pol_3"]))]}"
  if person["interes_pol_1_b"]!= 88 and person["interes_pol_1_b"] != 99:
    p_ideo_part_inter += f", está {interes[str(int(person["interes_pol_1_b"]))]} en política"

    
  if p_ideo_part_inter == "En cuanto a la política":
    p_ideo_part_inter = "En cuanto a sus intereses o tendencias políticas no proporciona ninguna información"

  p_ideo_part_inter += ". "

  if prompting == "red":
    p_ideo_part_inter = "Persona que " + p_ideo_part_inter.lower()

  return p_ideo_part_inter




#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la que se escribe)
def prompt_generator(person, prompting_estructure, exp, prompting_type=""):

  if prompting_estructure == "list":
    return list_template_esp(person, exp)
  
  elif prompting_estructure == "text":
    return text_template_esp(person, exp)
  
  elif prompting_estructure == "oom":
    return oom_generator_esp(person, exp)
  
  else: # Chain of thought

    p_notpolitical = ""
    if prompting_type != "red":
      p_notpolitical += non_political_prompt(person)
  
    p_ideo_part_inter =""
    if prompting_type != "wpv":
      p_ideo_part_inter += political_prompt(person, prompting_type)
    
    question = question_dict[exp]
    alternatives = alternatives_dict[exp]

    if prompting_estructure == "json":
      return  " Características de la persona: ``` " + p_notpolitical + p_ideo_part_inter + " ```. Pregunta: < "+ question + ">. Alternativas: [ " + alternatives + "]."
    else:
      return p_notpolitical + p_ideo_part_inter + question


def list_template_ablation(person, exp, var_to_remove):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""- country: Chile
{'- gender: ' + dict_sexo_eng[person["sexo"]] if var_to_remove != 'gender' else ''}
{'- age: ' + str(person["edad"]) if var_to_remove != 'age' else ''}
{'- region of residence: ' + region if var_to_remove != 'region' else ''}
{'- zone type: ' + zona_eng[person["zona_u_r"]] if var_to_remove != 'region' else ''}
{'- socioeconomic status: ' + gse[str(int(person["gse"]))] if var_to_remove != 'gse' else ''}
{'- level of scholarity: ' + escolaridad_eng[str(int(person["esc_nivel_1"]))] if var_to_remove != 'scholarity' else ''}
{'- indigenous community: ' + pueblo_eng[person["info_enc_30"]] if var_to_remove != 'indigenous' else ''}
{'- religion: ' + religion_eng[str(int(person["religion_82"]))] if var_to_remove != 'religion' else ''}
{'- political ideology: ' + izq_der_eng[str(int(person["iden_pol_2"]))] if var_to_remove != 'ideology' else ''}
{'- political party:' + party_eng[str(int(person["iden_pol_3"]))] +'.' if var_to_remove != 'party' else ''}
{'- political interest:' + interes_eng[str(int(person["interes_pol_1_b"]))] +'.' if var_to_remove != 'interest' else ''}
{question_dict_list[exp]}
"""

  return list_prompt 

def list_template(person, exp):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""- country: Chile
- gender: {dict_sexo_eng[person["sexo"]]}
- age: {str(int(person["edad"]))}
- region of residence: {region}
- zone type: {zona_eng[person["zona_u_r"]]}
- socioeconomic status: {gse[str(int(person["gse"]))]}
- level of scholarity: {escolaridad_eng[str(int(person["esc_nivel_1"]))]}
- indigenous community: {pueblo_eng[person["info_enc_30"]]}
- religion: {religion_eng[str(int(person["religion_82"]))]}
- political ideology: {izq_der_eng[str(int(person["iden_pol_2"]))]}
- political party: {party_eng[str(int(person["iden_pol_3"]))]}.
{question_dict_list[exp]}
"""
  return list_prompt 

def list_template_anes(person, exp):
  print("LIST ANES")
  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""- country: United States
- gender: {sexo_anes[person["sexo"]]}
- age: {str(person["edad"])}
- region of residence: {region_anes[int(person["nom_region"])]}
- zone type: {zona_anes[person["zona_u_r"]]}
- socioeconomic status: {gse_anes[int(person["gse"])]}
- level of scholarity: {escolaridad_anes[int(person["esc_nivel_1"])]}
- race: {pueblo_anes[person["race"]]}
- religion: {religion_anes[int(person["religion_82"])]}
- political ideology: {izq_der_anes[int(person["iden_pol_2"])]}
- political party: {party_anes[int(person["iden_pol_3"])]}.
- political interest: {interes_anes[int(person["interes_pol_1_b"])]}.
{question_dict_list_anes[exp]}
"""

  return list_prompt 

def list_template_esp(person, exp):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""- país: Chile
- sexo: {dict_sexo[person["sexo"]]}
- edad: {str(person["edad"])}
- región de residencia: {region}
- tipo de zona: {zona[person["zona_u_r"]]}
- estatus socioeconómico: {gse[str(int(person["gse"]))]}
- nivel de escolaridad: {escolaridad[str(int(person["esc_nivel_1"]))]}
- comunidad indígena: {pueblo[person["info_enc_30"]]}
- religión: {religion[str(int(person["religion_82"]))]}
- ideología política: {izq_der[str(int(person["iden_pol_2"]))]}
- partido político: {party[str(int(person["iden_pol_3"]))]}
- interés político: {interes[str(int(person["interes_pol_1_b"]))]}.
{question_dict_list_esp[exp]}
"""

  return list_prompt 



def text_template_anes(person, exp):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  text_prompt = (f'The gender is {sexo_anes[person["sexo"]]}. '
    f'The age is {str(person["edad"])}. '
    f'The country is United States. '
    f'The region of residence is {region_anes[int(person["nom_region"])]}. '
    f'The type of zone is {zona_anes[person["zona_u_r"]]}. '
    f'The socioeconomic status is {gse_anes[int(person["gse"])]}. '
    f'The level of scholarity is {escolaridad_anes[int(person["esc_nivel_1"])]}. '
    f'The race is {pueblo_anes[person["race"]]}. '
    f'The religion is {religion_anes[person["religion_82"]]}. '
    f'The political ideology is {izq_der_anes[int(person["iden_pol_2"])]}. '
    f'The political party is {party_anes[int(person["iden_pol_3"])]}. '
    f'The political interest is {interes_anes[int(person["interes_pol_1_b"])]}.'
  )
  text_prompt = text_prompt + "\n" + question_dict_list_anes[exp]
  return text_prompt 

def text_template(person, exp):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  text_prompt = (f'The gender is {dict_sexo_eng[person["sexo"]]}. '
    f'The age is {str(int(person["edad"]))}. '
    f'The country is Chile. '
    f'The region of residence is {region}. '
    f'The type of zone is {zona_eng[person["zona_u_r"]]}. '
    f'The socioeconomic status is {gse[str(int(person["gse"]))]}. '
    f'The level of scholarity is {escolaridad_eng[str(int(person["esc_nivel_1"]))]}. '
    f'The indigenous community is {pueblo_eng[person["info_enc_30"]]}. '
    f'The religion is {religion_eng[str(int(person["religion_82"]))]}. '
    f'The political ideology is {izq_der_eng[str(int(person["iden_pol_2"]))]}. '
    f'The political party is {party_eng[str(int(person["iden_pol_3"]))]}. '
  )
  text_prompt = text_prompt + "\n" + question_dict_list[exp]
  return text_prompt 

def text_template_esp(person, exp):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  text_prompt = (f'El sexo es {dict_sexo_eng[person["sexo"]]}. '
    f'La edad es {str(int(person["edad"]))}. '
    f'El país es Chile. '
    f'La región de residencia es {region}. '
    f'El tipo de zona en la que vive es {zona_eng[person["zona_u_r"]]}. '
    f'El estatus socioeconómico {gse[str(int(person["gse"]))]}. '
    f'El nivel de escolaridad {escolaridad_eng[str(int(person["esc_nivel_1"]))]}. '
    f'La comunidad indígena es {pueblo_eng[person["info_enc_30"]]}. '
    f'La religion es {religion_eng[str(int(person["religion_82"]))]}. '
    f'La ideología política es {izq_der_eng[str(int(person["iden_pol_2"]))]}. '
    f'El partido político es {party_eng[str(int(person["iden_pol_3"]))]}. '
  )
  text_prompt = text_prompt + "\n" + question_dict_list[exp]
  return text_prompt 


################# ESTOS SON PARA EMBEDDINGS #################

def char_list_generator_anes(person, exp):
  print("CHAR LIST ANES")
  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""country: United States
gender: {sexo_anes[person["sexo"]]}
age: {str(person["edad"])}
region of residence: {region_anes[int(person["nom_region"])]}
zone type: {zona_anes[person["zona_u_r"]]}
socioeconomic status: {gse_anes[int(person["gse"])]}
level of scholarity: {escolaridad_anes[int(person["esc_nivel_1"])]}
race: {pueblo_anes[person["race"]]}
religion: {religion_anes[int(person["religion_82"])]}
political ideology: {izq_der_anes[int(person["iden_pol_2"])]}
political party: {party_anes[int(person["iden_pol_3"])]}.
political interest: {interes_anes[int(person["interes_pol_1_b"])]}.
"""
  return list_prompt

def char_generator(person):
  p_notpolitical = non_political_prompt(person)
  p_ideo_part_inter = political_prompt(person, False)
  prompt =   p_notpolitical + p_ideo_part_inter
  return prompt

def char_generator_anes(person):
  p_notpolitical = non_political_prompt_anes(person)
  p_ideo_part_inter = political_prompt_anes(person)
  prompt =   p_notpolitical + p_ideo_part_inter
  return prompt


def char_list_generator_eng(person):
  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  list_prompt = f"""country: Chile
gender: {dict_sexo_eng[person["sexo"]]}
age: {str(int(person["edad"]))}
region of residence: {region}
zone type: {zona_eng[person["zona_u_r"]]}
socioeconomic status: {gse[str(int(person["gse"]))]}
level of scholarity: {escolaridad_eng[str(int(person["esc_nivel_1"]))]}
indigenous community: {pueblo_eng[person["info_enc_30"]]}
religion: {religion_eng[str(int(person["religion_82"]))]}
political ideology: {izq_der_eng[str(int(person["iden_pol_2"]))]}
political party: {party_eng[str(int(person["iden_pol_3"]))]}.
"""
  
  return list_prompt

def char_list_generator(person):

  try:
    region = region_dict[int(person["nom_region"])]

  except:
    region = person["nom_region"]

  char_list = f"""país: Chile
sexo: {dict_sexo[person["sexo"]]},
edad: {str(int(person["edad"]))},
región de residencia: {region},
tipo de zona: {zona[person["zona_u_r"]]},
nivel socioeconómico: {gse[str(int(person["gse"]))]},
nivel de escolaridad: {escolaridad[str(int(person["esc_nivel_1"]))]},
pueblo originario: {pueblo[person["info_enc_30"]] if person["info_enc_58"] == 1 else "No pertenece"},
religión: {religion[str(int(person["religion_82"]))]},
ideología política: {izq_der[str(int(person["iden_pol_2"]))]},
partido político con el que simpatiza: {party[str(int(person["iden_pol_3"]))]}"""


  return char_list


#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def rag_prompt_generator(person, exp, wpv, red):

  p_notpolitical = ""
  if not red:
    p_notpolitical += non_political_prompt(person)
 
  p_ideo_part_inter =""
  if not wpv:
    p_ideo_part_inter += political_prompt(person, red)
  
  question = question_dict[exp]
  alternatives = alternatives_dict[exp]

  prompt =  " Características de la persona: " + p_notpolitical + p_ideo_part_inter + " Pregunta: "+ question + ". Alternativas: [ " + alternatives + " ]."
  return prompt

def non_political_prompt_english(person):

  p_edad_sexo = ""
  p_region = ""
  p_gse_esc = ""
  p_religion = ""

  #EDAD y SEXO
  if person["sexo"] == 2:
    subject = "She "
    s2 = "her"
    s3 = "herself"
    p_edad_sexo =  str(int(person["edad"])) + " year old woman. "
  else:
    subject = "He "
    s2 = "his"
    s3 = "himself"
    p_edad_sexo = str(int(person["edad"])) + " year old man. "


  #REGION
  try:
    if person["zona_u_r"] == 1:
      p_region = subject + "lives in " +  person["nom_region"] + " region in Chile, in an urban area. "

    else:
      p_region =  subject + "lives in " +  person["nom_region"] + " region in Chile, in a rural area. "
  except:
    if person["zona_u_r"] == 1:
      p_region = subject + "lives in " +  region_dict[int(person["nom_region"])] + " region in Chile, in an urban area. "

    else:
      p_region =  subject + "lives in " +  region_dict[int(person["nom_region"])] + " region in Chile, in a rural area. "

  #GSE NIVEL DE ESTUDIOS
  p_gse_esc = s2.capitalize() + " socioeconomic level is gse "+ gse[str(int(person["gse"]))] + " and " + s2 + " level of schooling is "+ escolaridad_eng[str(int(person["esc_nivel_1"]))] + ". "


  if person["info_enc_58"] == 1:
    if person["info_enc_30"]!=0 and person["info_enc_30"] != 11 and person["info_enc_30"] != 88  and person["info_enc_30"] != 888 and person["info_enc_30"] != 999:
      p_orig =subject + "belongs to the " + pueblo_eng[person["info_enc_30"]] + " indigenous people. "
    else:
      p_orig = subject + "belongs to an indigenous people. "
  else:
    p_orig = subject + "does not belong to any indigenous people. "

  #RELIGIÓN
  if person["religion_82"] == 88 or person["religion_82"] == 99:
    p_religion = ""
  elif person["religion_82"] == 9: #ninguna
    p_religion =  subject+ "does not feel close to any religion. "
  elif person["religion_82"] == 10 or person["religion_82"] == 11 :
    p_religion = "In terms of religion, " + subject.lower() + "considers " + s3 + " to be " + religion_eng[str(int(person["religion_82"]))] + ". "
  else:
    p_religion = "In terms of religion, " + subject.lower() + "considers " + s3 + " a person closer to the "+ religion_eng[str(int(person["religion_82"]))] + " religion. "
  
  return p_edad_sexo + p_region + p_gse_esc  + p_orig + p_religion

def non_political_prompt_anes(person):
  
  p_edad_sexo = ""
  p_region = ""
  p_gse_esc = ""
  p_religion = ""

  #EDAD y SEXO
  if person["sexo"] == 2:
    subject = "She "
    s2 = "her"
    s3 = "herself"
    p_edad_sexo =  str(person["edad"]) + " year old woman. "
  else:
    subject = "He "
    s2 = "his"
    s3 = "himself"
    p_edad_sexo = str(person["edad"]) + " year old man. "


  #REGION
  if person["zona_u_r"] == 1:
    p_region = subject + "lives in " + region_anes[int(person["nom_region"])] + ", United States, in an urban area. "

  else:
    p_region =  subject + "lives in " +  region_anes[int(person["nom_region"])] + ", United States, in a rural area. "

  #GSE NIVEL DE ESTUDIOS
  p_gse_esc = s2.capitalize() + " socioeconomic level is "+ gse_anes[person["gse"]] + " and " + s2 + " level of schooling is "+ escolaridad_anes[person["esc_nivel_1"]] + ". "


  p_orig = ""
  if person["race"] != 88  and person["race"] != -8 and person["race"] != 99 and person["race"] != -9:
    p_orig = s2.capitalize() + " race is " + pueblo_anes[person["race"]] + ". "
  elif person["race"] == 88  and person["race"] == -8:
    p_orig = subject+ "doesn't know " + s2 + " race. "


  #RELIGIÓN
  if person["religion_82"] == 88 or person["religion_82"] == 99 and person["religion_82"] == -8 or person["religion_82"] == -9:
    p_religion = ""
  elif person["religion_82"] == 12: #ninguna
    p_religion =  subject+ "does not feel close to any religion. "
  elif person["religion_82"] == 9 or person["religion_82"] == 10 :
    p_religion = "In terms of religion, " + subject.lower() + "considers " + s3 + " to be " + religion_anes[person["religion_82"]] + ". "
  else:
    p_religion = "In terms of religion, " + subject.lower() + "considers " + s3 + " a person closer to the "+ religion_anes[person["religion_82"]] + " religion. "
  
  return p_edad_sexo + p_region + p_gse_esc  + p_orig + p_religion


def political_prompt_english(person):
  #EDAD y SEXO
  if person["sexo"] == 2:
    subject = "She "
    s2 = "her"
    s3 = "herself"
    p_edad_sexo =  str(person["edad"]) + " year old woman. "
  else:
    subject = "He "
    s2 = "his"
    s3 = "himself"
    p_edad_sexo = str(person["edad"]) + " year old man. "


  #IDEOLOGIA - PARTIDO - INTERES
  p_ideo_part_inter = "Regarding politics"
  if person["iden_pol_2"] != 88 and person["iden_pol_2"] != 99 and person["iden_pol_2"] != ' ':
    p_ideo_part_inter += ", on the left-right scale " +  subject.lower() + "feels closer to the " + izq_der_eng[str(int(person["iden_pol_2"]))]
  if person["iden_pol_3"] != 99 and person["iden_pol_3"]!= 88 and person["iden_pol_3"] != 15:
    p_ideo_part_inter += ", the party with which " + subject.lower() + "sympathizes most is "+  party_eng[str(int(person["iden_pol_3"]))]
  elif person["iden_pol_3"]== 15:
    p_ideo_part_inter += ", " + subject.lower() + "does not sympathize or feel close to any party"
  #if person["interes_pol_1_b"]!= 88 and person["interes_pol_1_b"] != 99 :
  #  p_ideo_part_inter += ", " + subject.lower()  + " is " +  interes_eng[str(int(person["interes_pol_1_b"]))] + " in politics"
  

  if p_ideo_part_inter == "Regarding politics":
    p_ideo_part_inter = "Regarding politics, " + subject.lower() + " does not provide any information"

  p_ideo_part_inter += ". "
  return p_ideo_part_inter

def political_prompt_anes(person):
  #EDAD y SEXO
  if person["sexo"] == 2:
    subject = "She "
    s2 = "her"
    s3 = "herself"
    p_edad_sexo =  str(person["edad"]) + " year old woman. "
  else:
    subject = "He "
    s2 = "his"
    s3 = "himself"
    p_edad_sexo = str(person["edad"]) + " year old man. "


  #IDEOLOGIA - PARTIDO - INTERES
  p_ideo_part_inter = "Regarding politics"
  if person["iden_pol_2"] != 88 and person["iden_pol_2"] != 99 and person["iden_pol_2"] != -9 and person["iden_pol_2"] != -8:
    p_ideo_part_inter += ", on the left-right scale " +  subject.lower() + "feels closer to the " + izq_der_anes[person["iden_pol_2"]]
  if person["iden_pol_3"] != 99 and person["iden_pol_3"]!= 88 and person["iden_pol_3"] != -9 and person["iden_pol_3"]!= -8:
    p_ideo_part_inter += ", " + subject.lower() + " is "+  party_anes[person["iden_pol_3"]]
  if person["interes_pol_1_b"]!= 88 and person["interes_pol_1_b"] != 99 and person["interes_pol_1_b"]!= -8 and person["interes_pol_1_b"] != -9:
    p_ideo_part_inter += ", " + subject.lower()  + " is " +  interes_anes[person["interes_pol_1_b"]] + " in politics"
  

  if p_ideo_part_inter == "Regarding politics":
    p_ideo_part_inter = "Regarding politics, " + subject.lower() + " does not provide any information"

  p_ideo_part_inter += ". "
  return p_ideo_part_inter

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def prompt_generator_english(person, prompting, exp=1, prompting_type=""):

  if prompting == "list" and prompting_type == "anes":
    return list_template_anes(person, exp)
  if prompting == "text" and prompting_type == "anes":
    return text_template_anes(person, exp)
  if prompting == "oom" and prompting_type == "anes":
    return oom_generator_anes(person, exp)
  if prompting == "oom" and prompting_type == "onlypol":
    return oom_generator_onlypol(person)
  if prompting == "oom" and prompting_type == "wpv":
    return oom_generator_anes_wpv(person, exp=exp)
  
  elif prompting == "list":
    return list_template(person, exp)
  
  elif prompting == "text":
    return text_template(person, exp)
  
  elif prompting == "oom":
    return oom_generator_english(person, exp)

  if prompting == "json":
    if prompting_type == "anes":
      if exp == 1:
        question = "Which candidate did this person vote for in the 2020 United States presidential election?"
        alternatives = "Joe Biden, Donald Trump, Jo Jorgensen, Howie Hawkins"
      else:
        question = "Which of these ideas best expresses your judgment regarding abortion?"
        alternatives = "Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case"
    else:
      question = question_dict_eng[exp]
      alternatives = alternatives_dict_eng[exp]

    if prompting_type == "wpv":
      question = "Which of these ideas best expresses your judgment regarding abortion?"
      alternatives = "Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case"
      #question = "Which candidate did this person vote for in the 2020 United States presidential election?"
      #alternatives = "Joe Biden, Donald Trump, Jo Jorgensen, Howie Hawkins"
      #return  " Characteristics of the person: ``` " + non_political_prompt_english(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."
      return  " Characteristics of the person: ``` " + non_political_prompt_anes(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."
    elif prompting_type == "onlypol":
      #question = "Which candidate did this person vote for in the 2020 United States presidential election?"
      #alternatives = "Joe Biden, Donald Trump, Jo Jorgensen, Howie Hawkins"
      question = "Which of these ideas best expresses your judgment regarding abortion?"
      alternatives = "Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case"
      return  " Characteristics of the person: ``` " + political_prompt_anes(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."
      #return  " Characteristics of the person: ``` " + non_political_prompt_english(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."
    elif prompting_type == "anes":
      return  " Characteristics of the person: ``` " + non_political_prompt_anes(person) + political_prompt_anes(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."
    else:
      return  " Characteristics of the person: ``` " + non_political_prompt_english(person) + political_prompt_english(person) + " ```. Question: < "+ question + ">. Alternatives: [ " + alternatives + " ]."

  elif prompting == "normal":
    question = normal_question_dict_eng[exp]
  else:
    question = question_dict_list[exp]
  
  if prompting_type == "wpv":
    prompt2 = non_political_prompt_english(person) + question
  elif prompting_type == "onlypol":
    prompt2 = political_prompt_english(person) + question
  elif prompting_type=="anes":
    prompt2 = non_political_prompt_anes(person) + political_prompt_anes(person)
    if exp==1:
      prompt2 += "Which candidate did this person vote for in the 2020 United States presidential election? Choose only one of the following options: Joe Biden, Donald Trump, Jo Jorgensen or Howie Hawkins."
    else:
      prompt2 += "Which of these ideas best expresses this person’s judgment regarding abortion? Choose only one of the following options: Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case."
  else:
    prompt2 = non_political_prompt_english(person) + political_prompt_english(person) + question
  return prompt2

def age_category(data_point):
  if data_point <= 24:
    return "young"
  elif data_point <= 39:
    return "middle-aged"
  elif data_point <= 60:
    return "old"
  else:
    return "very old"
  
#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_anes(person,exp=1):
  religion = religion_anes[int(person["religion_82"])]
  prompt = (f'Ideologically, on the left-right scale, I feel closer to the {izq_der_anes[person["iden_pol_2"]]}. '
    f'The party I sympathize most is {party_anes[person["iden_pol_3"]]}. '
    f'In terms of interest in politics, I am {interes_anes[person["interes_pol_1_b"]]}. '
    f'Racially, {pueblo_anes[person["race"]] if pueblo_anes[person["race"]] != "none" else "I don’t have race"}.'
    f'I am {sexo_anes[person["sexo"]]}. '
    f'I live in {region_anes[int(person["nom_region"])]}, United States. '
    f'Financially, my economical status is {gse_anes[int(person["gse"])]}. '
    f'In terms of my age, I am {str(person["edad"])} years old. '
    f'My level of scholarity is {escolaridad_anes[int(person["esc_nivel_1"])]}. '
    f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.'
  )
  if exp == 1:
    question = 'In 2020 presidential election of the United States, I voted for '
  if exp == 3:
    question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question

def oom_generator_anes_wpv(person,exp=1):
  religion = religion_anes[int(person["religion_82"])]
  prompt = (f'Racially, {pueblo_anes[person["race"]] if pueblo_anes[person["race"]] != "none" else "I don’t have race"}.'
    f'I am {sexo_anes[person["sexo"]]}. '
    f'I live in {region_anes[int(person["nom_region"])]}, United States. '
    f'Financially, my economical status is {gse_anes[int(person["gse"])]}. '
    f'In terms of my age, I am {str(person["edad"])} years old. '
    f'My level of scholarity is {escolaridad_anes[int(person["esc_nivel_1"])]}. '
    f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.'
  )
  if exp == 1:
    question = 'In 2020 presidential election of the United States, I voted for '
  if exp == 3:
    question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_ablation(person,exp=1, var_to_remove = ""):
  if religion_eng[str(int(person["religion_82"]))] == "none": 
    religion_phrase = "I don't have religion"
  else:
    religion_phrase = religion_eng[str(int(person["religion_82"]))]

  p_orig = pueblo_eng[person["info_enc_30"]] if pueblo_eng[person["info_enc_30"]] != "none" else "I don’t have race"

  

  ablation_prompt = "".join([
  f"Ideologically, on the left-right scale, I feel closer to the {izq_der_eng[str(person['iden_pol_2'])]}. " if var_to_remove != 'ideology' else '',
  f"The party I sympathize most is {party_eng[str(person['iden_pol_3'])]}. " if var_to_remove != 'party' else '',
  f"In terms of interest in politics, I am {interes_eng[str(int(person['interes_pol_1_b']))]}. " if var_to_remove != 'interest' else '',  
  f"Racially, {p_orig}. " if var_to_remove != 'race' else '',
  f"I am {dict_sexo_eng[person['sexo']]}. " if var_to_remove != 'gender' else '',
  f"I live in {person['nom_region']} region, Chile. " if var_to_remove != 'region' else '',
  f"Financially, my economical status is {gse[str(int(person['gse']))]}. " if var_to_remove != 'gse' else '',
  f"In terms of my age, I am {str(age_category(person['edad']))}. " if var_to_remove != 'age' else '',
  f"My level of scholarity is {escolaridad_eng[str(int(person['esc_nivel_1']))]}. " if var_to_remove != 'scholarity' else '',
  f"In terms of religion, {religion_phrase}. " if var_to_remove != 'religion' else ''
])

  
  if exp == 1:
    question = 'In the 2nd round of the 2021 chilean presidential election, I voted for '
  if exp == 2:
    question = 'In the chilean exit plebiscite for the new constitution realized in September 2022, I voted '
  if exp == 3:
    question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return ablation_prompt + "\n" + question


def oom_generator_ablation_anes(person,exp=1, var_to_remove = ""):
  religion = religion_anes[int(person["religion_82"])]

  ablation_prompt = "".join([
  f'Ideologically, on the left-right scale, I feel closer to the {izq_der_anes[person["iden_pol_2"]]}. ' if var_to_remove != 'ideology' else '',
  f'The party I sympathize most is {party_anes[person["iden_pol_3"]]}. ' if var_to_remove != 'party' else '',
  f'In terms of interest in politics, I am {interes_anes[person["interes_pol_1_b"]]}. ' if var_to_remove != 'interest' else '',  
  f'Racially, {pueblo_anes[person["race"]] if pueblo_anes[person["race"]] != "none" else "I don’t have race"}. ' if var_to_remove != 'race' else '',
  f'I am {sexo_anes[person["sexo"]]}. ' if var_to_remove != 'gender' else '',
  f'I live in {region_anes[int(person["nom_region"])]}, United States. ' if var_to_remove != 'region' else '',
  f'Financially, my economical status is {gse_anes[int(person["gse"])]}. ' if var_to_remove != 'gse' else '',
  f'In terms of my age, I am {str(person["edad"])} years old. ' if var_to_remove != 'age' else '',
  f'My level of scholarity is {escolaridad_anes[int(person["esc_nivel_1"])]}. ' if var_to_remove != 'scholarity' else '',
  f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.' if var_to_remove != 'religion' else ''
  ])

  
  if exp == 1:
    question = 'In the 2nd round of the 2021 chilean presidential election, I voted for '
  if exp == 2:
    question = 'In the chilean exit plebiscite for the new constitution realized in September 2022, I voted '
  if exp == 3:
    question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return ablation_prompt + "\n" + question

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_esp(person,exp=1):
  if int(person["sexo"]) == 1:
    ao = "o"
    interes_dict = interes2
  else:
    ao = "a"
    interes_dict = interes
  religion_parsed = religion[str(int(person["religion_82"]))]

  if pueblo[person["info_enc_30"]] == "no contesta":
    pueblo_sentence = ""
  elif pueblo[person["info_enc_30"]] != "ninguno":
    pueblo_sentence = "No pertenezco a ningún pueblo originario. "
  elif pueblo[person["info_enc_30"]] != "no sabe":
    pueblo_sentence = "No sé si pertenezco a algún pueblo originario. "
  else:
    pueblo_sentence = "En cuanto a pertenencia a pueblo originario, pertenezco al pueblo " + pueblo[person["info_enc_30"]] + ". "

  if izq_der[str(int(person["iden_pol_2"]))] == "no contesta" or izq_der[str(int(person["iden_pol_2"]))] == "no sabe":
    ideology_sentence = ""
  else:
    ideology_sentence = f'Ideológicamente, en la escala izquierda-derecha, me siento cercan{ao} a {izq_der[str(int(person["iden_pol_2"]))]}. '


  prompt = (f'{ideology_sentence}'
    f'El partido con el que más simpatizo es {party[str(int(person["iden_pol_3"]))]}. '
    f'En términos de interés en política, estoy {interes_dict[str(int(person["interes_pol_1_b"]))]}. '
    f'{pueblo_sentence}'
    f'Soy {dict_genero[person["sexo"]]}. '
    f'Vivo en la región {person["nom_region"]}, Chile. '
    f'Financieramente, mi nivel socioeconómico es  {gse[str(int(person["gse"]))]}. '
    f'Tengo {str(person["edad"])} años. '
    f'Mi nivel de escolaridad es {escolaridad[str(int(person["esc_nivel_1"]))]}. '
    f'Con respecto a la religión, {religion_parsed if religion_parsed != "none" else "no tengo religión"}.'
  )
  if exp == 1:
    question = 'In the 2nd round of the 2021 chilean presidential election, I voted for '
  if exp == 2:
    question = 'In the chilean exit plebiscite for the new constitution realized in September 2022, I voted '
  if exp == 3:
    question = 'En cuanto al aborto, si tengo que escoger entre alguna de las siguientes alternativas: 1) Aborto debe estar siempre prohibido, 2) Aborto debe ser permitido solo en casos especiales, 3) Aborto debe estar permitido en cualquier caso. Eligiría '
  return prompt + "\n" + question

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_onlypol(person):
  religion = religion_eng[str(int(person["religion_82"]))]
  prompt = (f'Ideologically, on the left-right scale, I feel closer to the {izq_der_eng[str(person["iden_pol_2"])]}. '
    f'The party I sympathize most is {party_eng[str(person["iden_pol_3"])]}. '
    f'In terms of interest in politics, I am {interes_eng[str(person["interes_pol_1_b"])]}. '
  )
  question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question


def oom_generator_anes_onlypol(person):
  prompt = (f'Ideologically, on the left-right scale, I feel closer to the {izq_der_anes[person["iden_pol_2"]]}. '
    f'The party I sympathize most is {party_anes[person["iden_pol_3"]]}. '
    f'In terms of interest in politics, I am {interes_anes[person["interes_pol_1_b"]]}. '
  )
  question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_wpv(person):
  religion = religion_eng[str(int(person["religion_82"]))]
  prompt = (f'Racially, {pueblo_eng[person["info_enc_30"]] if pueblo_eng[person["info_enc_30"]] != "none" else "I don’t have race"}. '
    f'I am {dict_sexo_eng[person["sexo"]]}. '
    f'I live in {person["nom_region"]} region, Chile. '
    f'Financially, my economical status is {gse[str(int(person["gse"]))]}. '
    f'In terms of my age, I am {str(age_category(person["edad"]))}. '
    f'My level of scholarity is {escolaridad_eng[str(int(person["esc_nivel_1"]))]}. '
    f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.'
  )
  question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question

#Genera el prompt, pero de forma distinta a la original. (cambia solo la forma en la quie se escribe)
def oom_generator_english(person,exp=1):
  religion = religion_eng[str(int(person["religion_82"]))]
  try:
    prompt = (f'Ideologically, on the left-right scale, I feel closer to the {izq_der_eng[str(int(person["iden_pol_2"]))]}. '
      f'The party I sympathize most is {party_eng[str(int(person["iden_pol_3"]))]}. '
      f'In terms of interest in politics, I am {interes_eng[str(int(person["interes_pol_1_b"]))]}. '
      f'Racially, {pueblo_eng[person["info_enc_30"]] if pueblo_eng[person["info_enc_30"]] != "none" else "I don’t have race"}. '
      f'I am {dict_sexo_eng[person["sexo"]]}. '
      f'I live in {person["nom_region"]} region, Chile. '
      f'Financially, my economical status is {gse[str(int(person["gse"]))]}. '
      f'In terms of my age, I am {str(age_category(person["edad"]))}. '
      f'My level of scholarity is {escolaridad_eng[str(int(person["esc_nivel_1"]))]}. '
      f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.'
    )
  except:
    prompt = (f'Ideologically, on the left-right scale, I feel closer to the {izq_der_eng[str(int(person["iden_pol_2"]))]}. '
      f'The party I sympathize most is {party_eng[str(int(person["iden_pol_3"]))]}. '
      #f'In terms of interest in politics, I am {interes_eng[str(int(person["interes_pol_1_b"]))]}. '
      f'Racially, {pueblo_eng[person["info_enc_30"]] if pueblo_eng[person["info_enc_30"]] != "none" else "I don’t have race"}. '
      f'I am {dict_sexo_eng[person["sexo"]]}. '
      f'I live in {region_dict[int(person["nom_region"])]} region, Chile. '
      f'Financially, my economical status is {gse[str(int(person["gse"]))]}. '
      f'In terms of my age, I am {str(age_category(person["edad"]))}. '
      f'My level of scholarity is {escolaridad_eng[str(int(person["esc_nivel_1"]))]}. '
      f'In terms of religion, {religion if religion != "none" else "I don’t have religion"}.'
    )
  if exp == 1:
    question = 'In the 2nd round of the 2021 chilean presidential election, I voted for '
  if exp == 2:
    question = 'In the chilean exit plebiscite for the new constitution realized in September 2022, I voted '
  if exp == 3:
    question = 'Regarding abortion, if I had to choose between the followings alternatives: 1) Abortion should always be prohibited, 2) Abortion should only be allowed in special cases, 3) Abortion should be an option for women in any case. I would choose '
  return prompt + "\n" + question

def fewshot_examples_generator(data, random_indexes, exp):
  examples_list = []
  answers_list = []
  if exp == 1:
    exp_column = "elec_pres_144_a"
  elif exp == 2:
    exp_column = "constitucion_20_a"
  elif exp == 3:
    exp_column = "religion_14"

  for index in random_indexes:
    person = data.iloc[index]
    examples_list.append(person["prompt"])
    answers_list.append(person["output"])

  return examples_list, answers_list


#Este fewshot funciona como chat.
def fewshot_prompt_generator( examples_list, answers_list, context, inst, d):
  fewshot_chain = f"""{{<s>[INST] <<SYS>>
{ context}
<</SYS>>
Primero, se te dará un ejemplo para que te familiarices con el formato de respuesta:
{ examples_list.pop(0) + inst} [/INST] { d[int(answers_list.pop(0))] } </s>}}"""
  
  #example_chain = ""
  for example, answer in zip(examples_list,answers_list):
    fewshot_chain += f"""{{
<s>[INST] { example + inst} [/INST] {d[int(answer)]} </s>}}"""
  return fewshot_chain
    
  
def fewshot_prompt_generator2(person, data, random_indexes, task, context, end, inst, exp):
  examples_list, answers_list = fewshot_examples_generator(data, random_indexes, exp)
  
  fewshot_chain = ""
  for example, answer in zip(examples_list,answers_list):
    fewshot_chain += f"""{{{ example + inst}
Respuesta: {plebiscito[answer]}}}"""

  prompt = f"""{{[INST] <<SYS>>
    {task+context}
    <</SYS>>
    First, an example will be given to you, only to familiarize you with the response format:
    {fewshot_chain}
    {end} 
    {example["prompt"] + inst} [/INST]}}"""

  return prompt


def random_fewshot_answer(example, prompting,eng, dictionary, column):
  if prompting !="json":
    answer = dictionary[int(example[column])]
  elif eng:
    answer = "{'explanation': here the explanation, 'answer': " +  dictionary[int(example[column])] + "}"
  else:
    answer = "{'explicación': aquí la explicación, 'respuesta': " +  dictionary[int(example[column])] + "}"

  return answer


#genero un dataset de 100 muestras con los prompts y respuestas que corresponden.
#otro dataset sin esos 100 prompts
#una matriz donde cada fila contiene los 10 ejemplos(indices) para utilizar en cierta persona.
                               
def random_fewshot_prompt_generator(index_list, exp, prompting, prompt_type, task, end,dictionary, translator, eng, translate):
  i1=index_list.pop(0)
  print("PROMOT TYPE", prompt_type)
  if prompt_type == "anes" and exp ==1:
    print("EJEMPLO ANES")
    examples_df = pd.read_csv('anes_2020_100.csv')
  elif prompt_type == "anes" and exp ==3:
    print("EJEMPLO ANES")
    examples_df = pd.read_csv('anes_2020_100_v1.csv')
  else:
    examples_df = pd.read_csv('exp_100_inputs.csv')
  example = examples_df.iloc[i1]

  if prompting == "oom":
    jump = ""
  else:
    jump = "\n"

  if translate and not eng:
    prompt = translator.translate(prompt_generator(example,prompting, exp, prompting_type=prompt_type ))
  elif eng:
    prompt = prompt_generator_english(example,prompting, exp, prompting_type=prompt_type)
  else:
    prompt = prompt_generator(example,prompting, exp , prompting_type=prompt_type)

  column= exp_columns[exp]
  print(exp)

  answer = random_fewshot_answer(example, prompting, eng, dictionary, column)
  messages = [{"role": "user", "content": task + '\n'+ prompt + jump + end }, 
              {"role": "assistant", "content":  answer }]
  
  for index in index_list:
    example = examples_df.iloc[index]
    if translate and not eng:
      prompt = translator.translate(prompt_generator(example,prompting, exp, prompting_type=prompt_type ))
    elif eng:
      prompt = prompt_generator_english(example,prompting, exp, prompting_type=prompt_type)
    else:
      prompt = prompt_generator(example,prompting, exp, prompting_type=prompt_type )
    answer = random_fewshot_answer(example, prompting, eng, dictionary, column)
    messages += [{"role": "user", "content": task + '\n'+ prompt + jump + end }, 
                {"role": "assistant", "content": answer }]
  return messages



""" df = pd.read_csv('exp3_fewshot_inputs.csv')
person = df.iloc[11]
print(prompt_generator_english(person, exp=3)) 




if exp == 1:
    question = "Who did this person vote for in the 2021 Chilean presidential elections? Choose only one of the following options: Boric, Kast, null."
    #question = " For whom did " + subject.lower() + " vote in the 2021 presidential elections? Choose only one of the following options: Boric, Kast, voted null.\n "
  if exp == 2:
    question = "Now please answer the following question taking into account the previous characteristics. Which of the following options did the person described vote for in the exit plebiscite for the new constitution in September 2022?  Answer with only one word from the following options: Approve, Reject, Null.\n "
  if exp == 3:
    question = "Now, please answer to the following question taking into account the previous characteristics and bearing in mind that the contextual year is 2022: Which of these ideas best expresses your judgment regarding abortion? Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case. """
