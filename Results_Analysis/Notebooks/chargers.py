import json
import pandas as pd
import re


def answer_finder(raw_answer, d, prompt_type, language, is_t0=False):
  """ Receives an  llm response and search the predicted vote or option.

  :param raw_answer: a string, containing the llm response.
  :param d: a dictionary, containing each option number with it possibles answers in words.
  :param prompt_type: a string, containing the prompt design used in this prediction.
  :param language: a string, 'eng' or 'esp', whether the language used in the predicion was english or spanish.

  :return: an int, the code of the prediction vote or option.
  """
  answer = str(raw_answer).replace("[", "").replace("]", "").replace("\n", " ").replace("'", '"').replace(".", "").replace('"',"").replace('<',"").replace('>',"").replace("`","")

  if prompt_type == None:
    selected_option = answer

  elif prompt_type == 'cot':
    

    if language == 'eng':
      raw_selected_option = re.search(r"answer\s*:\s*([^,}]+)", answer)
      
    elif language == 'esp':
      raw_selected_option = re.search(r"respuesta\s*:\s*([^,}]+)", answer)

    if is_t0:
      raw_selected_option = re.search(r'pad\s*([^,}]+)', answer)

    if raw_selected_option:
      selected_option = raw_selected_option.group(1).lower().strip().replace("!", "").replace("¡", "").replace(".", "").replace(",", "").replace('}',"")
    else:
      return -1
  
  if selected_option in d.keys():
    return d[selected_option]
  else:
    for key in d.keys():
      if key in selected_option:
        return d[key]
    
    for key in d.keys():
      if key in answer.lower():
        return d[key]
    return -1


def data_charger(df_inputs, model_answers, d, prompt_type=None, language='eng', remove = False, is_t0 = False):
  """ Receives a dataframe or jsonl containing all predictions for each person in test dataset.
    Returns the dataframe with each person info, with a new column column pred containing the 
    number that represents the predicted vote or option.

  ::param df_inputs: a pd.DataFrame, each row corrsponds to a person in test dataset, and contains it sociodemographic info. 
  :param model_answers: a pd.DataFrame or jsonl, all raw predictions (in text format) for each person in test dataset.
  :param d: a dictionary, containing each option number with it possibles answers in words.
  :param prompt_type: a string, containing the prompt design used in this prediction.
  :param language: a string, 'eng' or 'esp', whether the language used in the predicion was english or spanish.
  :param remove: a List, containing all the columns that will be removed from the returned dataframe (repeated columns in general).
  
  :return: a pd.DataFrame, with each person info and predicted vote or option.
  """
  df_inputs = pd.read_csv(df_inputs)
  if remove:
    df_inputs = df_inputs.drop(df_inputs.index[[remove]])

  outputs = []
  if isinstance(model_answers, pd.DataFrame):
    for index, row in model_answers.iterrows():
      raw_answer = row["pred"]
      answer = answer_finder(raw_answer, d, prompt_type, language, is_t0)
      outputs.append(answer)
  else:
    with open(model_answers, 'r') as file:
      for line in file:
        json_object = json.loads(line)
        raw_answer = json_object["respuesta"]
        answer = answer_finder(raw_answer, d, prompt_type, language, is_t0)
        outputs.append(answer)

  df_inputs["pred"] = outputs
  return df_inputs

def ablation_charger(df_inputs, jsonl_name, d, remove):
  """ Receives a jsonl containing the predictions for each person in test dataset for all prompt variations of ablation experiment.
    Returns the dataframe with each person info, with a new column column pred containing the 
    number that represents the predicted vote or option.

  :param df_inputs: a pd.DataFrame, each row corrsponds to a person in test dataset, and contains it sociodemographic info. 
  :param jsonl_name: a string, all raw predictions (in text format) for each person in test dataset.
  :param d: a dictionary, containing each option number with it possibles answers in words.
  :param remove: a List, containing all the columns that will be removed from the returned dataframe (repeated columns in general).
  
  :return: a pd.DataFrame, with each person info and predicted vote or option.
  """
  df_inputs = pd.read_csv(df_inputs)
  if remove:
    df_inputs = df_inputs.drop(df_inputs.index[[remove]])

  with open(jsonl_name, 'r') as f:
    var = "gender"  # first variable dropped from prompt
    outputs = []  # list of outputs when var is not in prompt
    for line in f:
      line = json.loads(line)

      # If var_removed is different, then save the info for the previous dropped var, and update some values
      if line["var_removed"] != var:
        df_inputs["pred_"+var] = outputs  # save info for the previous dropped var
        outputs = []  # reset outputs for the new removed var
        var = line["var_removed"]  # update removed var value

      # Search the selected option in the answer.
      raw_answer = line["respuesta"]
      answer = answer_finder(raw_answer, d, 'cot', 'eng')
      outputs.append(answer)

  df_inputs["pred_"+var] = outputs
  return df_inputs