import json
import pandas as pd
import numpy as np

from scipy.spatial.distance import jensenshannon
from sklearn.metrics import accuracy_score, cohen_kappa_score

def percentage_per_option(votes_column, n_options):
  """ Calculates the proportion of people for each choice, vote or opinion.

  :param votes_column: a pd.DataFrame, the original votes column or predicted votes column.
  :return: a List, containing the proportion of votes for each possible choice.
  """
  n_options = n_options + 1 # number of voting options plus the case in which the answer was not found
  total = len(votes_column)
  if total == 0:
    return [0] * n_options

  counts = votes_column.value_counts() # gets the quantity of votes for each option
  percentages_list = []

  for i in range(n_options):
    if i == n_options-1:
      i = -2
    option_count = counts.get(i+1, 0) # gets the quantity of votes for option i+1
    option_percentage = (option_count / total) * 100
    percentages_list.append(option_percentage)

  return percentages_list

def jsd_function(original_votes_column, pred_votes_column, n_options=3):
  """Calculates JSD function between original votes column and predictions column.
  
  :param original_votes_column: a pd.DataFrame, containing the original choice of each person for the survey question.
  :param pred_votes_column: a DataFrame, containing the predicted choice for each person in the survey question.
  :param n_options: an int, corresponding to the amount of possible choices for the survey question .
  
  :return: a float, the value of jensen shannon divergence between the original and predicted distributions.
  """
  P = percentage_per_option(original_votes_column, n_options)
  Q = percentage_per_option(pred_votes_column, n_options)
  jsd = jensenshannon(P, Q, base=2)
  return jsd


def harmonic_mean(jsd, acc):
  """ Calculates Harmonic mean between jsd and accuracy.
  
  :param jsd: a float, the value of jensen shannon divergence between the original and predicted distributions.
  :param acc: a float, the value of accuracy between the original and predicted distributions.
  
  :return: a float, the value of harmonic mean between both accuracy and jsd.
  """
  inverted_jsd = 1- jsd
  if inverted_jsd + acc == 0:
    return float('nan')
  h = 2*inverted_jsd*acc/(inverted_jsd+acc)
  return h


def get_people_in_group_chile(df, charasteristic, id):
  """ Filter people of an specific group in the dataframe.
  
  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param charasteristic: a string, the column (or characteristic) by which the people will be filtered. 
    For example: age, religion column (religion_82), etc.
  :param id: a string or int, the indicator for the group that belogs to charasteristic and is going to be filtered.

  :return: a pd.DataFrame, containing only the people that belongs to desired group."""
  # This variable will contain a bool value for each person in df, indicating if the person belong to the sociodemographic group or not
  group_index = None

  #Region sociodemographic info is classified in only 2 groups: Metropolitana region, other region.
  if charasteristic == "nom_region":
    if id == "METROPOLITANA":
      group_index = (df[charasteristic] == id)
    else:
      group_index = (df[charasteristic] == "TARAPACÁ") | (df[charasteristic] == "ANTOFAGASTA") | (df[charasteristic] == "ATACAMA") \
       | (df[charasteristic] == "COQUIMBO") | (df[charasteristic] == "VALPARAÍSO") | (df[charasteristic] == "LIBERTADOR BERNARDO OHIGGINS") \
       | (df[charasteristic] == "MAULE") | (df[charasteristic] == "BIOBÍO") | (df[charasteristic] == "ARAUCANÍA") | \
        (df[charasteristic] == "LOS LAGOS") | (df[charasteristic] == "AYSÉN") | (df[charasteristic] == "MAGALLANES") | \
         (df[charasteristic] == "LOS RÍOS") | (df[charasteristic] == "ARICA Y PARINACOTA") | (df[charasteristic] == "ÑUBLE")

  # According to age, people are classified into 3 age groups
  elif charasteristic == "age":
    if id == "young":
      group_index = (df["edad"] >= 18) & (df["edad"] <= 26)
    elif id == "adult":
      group_index = (df["edad"] >= 27) & (df["edad"] <= 59)
    elif id == "senior":
      group_index = (df["edad"] >= 60)

  # According to Indigenous people, id = 3 corresponds to people who do not know or did not answer (values 8, 9, 99, 88).
  elif charasteristic == "info_enc_58" and id == 3:
    group_index = (df[charasteristic] == 8) | (df[charasteristic] == 9) | (df[charasteristic] == 99) | (df[charasteristic] == 88)

  # Regarding political ideology, people are classified in 3 groups: left, center, right, none.
  elif charasteristic == "iden_pol_2":
    if id == "left":
      group_index = (df[charasteristic] == 1) | (df[charasteristic] == 2) | (df[charasteristic] == 3) | (df[charasteristic] == 4)
    elif id == "center":
      group_index = (df[charasteristic] == 5) | (df[charasteristic] == 6)
    elif id == "right":
      group_index = (df[charasteristic] == 7) | (df[charasteristic] == 8) | (df[charasteristic] == 9) | (df[charasteristic] == 10)
    elif id == "none":
      group_index = (df[charasteristic] == 88) | (df[charasteristic] == 99)

  # According to economic level, people are classified in 3 groups: high class, middle class and poor. Where:
  # High class:
  # 1: ABC1
  # Middle class:
  # 2: C2
  # 3: C3
  # Poor class:
  # 4: D
  # 5: E
  elif charasteristic == "gse":
      if id == "high class":
        group_index = (df["gse"] == 1)
      elif id == "middle class":
        group_index = (df["gse"] == 2) | (df["gse"] == 3)
      elif id == "poor class":
        group_index = (df["gse"] == 4) | (df["gse"] == 5)

  # Regarding education level, people are classified in 4 groups.
  elif charasteristic == "esc_nivel_1":
    if id == "low education": # No formal education, incomplete school
      group_index = (df[charasteristic] == 1) | (df[charasteristic] == 2) | (df[charasteristic] == 3) | (df[charasteristic] == 0)
    elif id == "medium education": #school, and university or institute incomplete
      group_index = (df[charasteristic] == 5) | (df[charasteristic] == 7) | (df[charasteristic] == 4)
    elif id == "high education": #university,  institute, or higher
      group_index = (df[charasteristic] == 6) | (df[charasteristic] == 8)| (df[charasteristic] == 9)| (df[charasteristic] == 10)
    elif id == "none":
      group_index = (df[charasteristic] == 99)| (df[charasteristic] == 88) | (df[charasteristic] == -9)| (df[charasteristic] == -8)

  # In terms of religion, people are classified in 3 groups: religious, atheist/agnostinc, doesn't know.
  elif charasteristic == "religion_82":
    if id == "religious":
      group_index = (df[charasteristic] == 1) | (df[charasteristic] == 2) | (df[charasteristic] == 3) | (df[charasteristic] == 4) | (df[charasteristic] == 5) | (df[charasteristic] == 6) | (df[charasteristic] == 7) | (df[charasteristic] == 8)
    if id == "atheist/agnostic":
      group_index = (df[charasteristic] == 10) | (df[charasteristic] == 11 ) | (df[charasteristic] == 9)
    if id == "doesnt know":
      group_index = (df[charasteristic] == 88) | (df[charasteristic] == 99)

  # Some sociodemografic groups are simply classified be the person chosen option for an answers,
  # so there is no need to group responses to create subgroups.
  else:
    group_index = df[charasteristic]==id

  # Finally, the people that belongs to the expected sociodemographic group are filtered
  df_group = df[group_index]
  return df_group


def _compute_group_metrics(df_group, pred_variable, pred_column_name, n_options):
  """Compute JSD, accuracy, harmonic mean, JSS, and Cohen's Kappa for a DataFrame subset."""
  jsd = jsd_function(df_group[pred_variable], df_group[pred_column_name], n_options)
  acc = accuracy_score(df_group[pred_variable], df_group[pred_column_name])
  h = harmonic_mean(jsd, acc)
  jss = 1 - jsd
  kappa = cohen_kappa_score(df_group[pred_variable], df_group[pred_column_name])
  return jsd, acc, h, jss, kappa


def metrics_group_chile(df, charasteristic, id, pred_variable, pred_column_name, n_options, n_bootstrap=0, confidence_level=0.95, random_seed=None):
  """ Calculates accuracy, jsd, and harmonic mean for an specific sociodemografic group in the dataframe and return the result in an array.

  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param charasteristic: a string, the column (or characteristic) by which the people will be filtered.
    For example: age, religion column (religion_82), etc.
  :param id: a string or int, the indicator for the group that belogs to charasteristic and is going to be filtered.
  :param pred_variable: a string, the name of the column containing the original values for the question in the survey that is being predicted.
  :param pred_column_name: a string, the name of the column that contains the llm predictions.
  :param n_options: an int, the amount of options or choices available to answer the predicted survey question.
  :param n_bootstrap: an int, number of bootstrap iterations (0 = no bootstrapping).
  :param confidence_level: a float, confidence level for bootstrap intervals (default 0.95).
  :param random_seed: an int or None, optional seed for reproducibility.

  :return: a List, containing the metrics (jsd, acc, h, and jss) obtained for the group.
    When n_bootstrap > 0, also includes CI lower/upper bounds for each metric.
  """
  df_group = get_people_in_group_chile(df, charasteristic, id)

  if len(df_group) == 0:
    if n_bootstrap > 0:
      return [None] * 15
    return [None] * 5

  jsd, acc, h, jss, kappa = _compute_group_metrics(df_group, pred_variable, pred_column_name, n_options)

  if n_bootstrap <= 0:
    return [jsd, acc, h, jss, kappa]

  rng = np.random.default_rng(random_seed)
  boot_metrics = np.empty((n_bootstrap, 5))
  n_samples = len(df_group)

  for i in range(n_bootstrap):
    sample = df_group.sample(n=n_samples, replace=True, random_state=int(rng.integers(0, 2**31)))
    boot_metrics[i] = _compute_group_metrics(sample, pred_variable, pred_column_name, n_options)

  alpha = 1 - confidence_level
  lo = np.nanpercentile(boot_metrics, 100 * alpha / 2, axis=0)
  hi = np.nanpercentile(boot_metrics, 100 * (1 - alpha / 2), axis=0)

  return [jsd, acc, h, jss, kappa, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], lo[3], hi[3], lo[4], hi[4]]

# metrics_dataset_gen: dataframe -> dataframe
# Returns a dataframe with metrics for each sociodemografic group and total.
def metrics_dataset_gen_chile(df, pred_variable, pred_column_name="pred", n_options=3, n_bootstrap=0, confidence_level=0.95, random_seed=None):
  """ Returns a dataframe with metrics for each sociodemografic group and total.

  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param pred_variable: a string, the name of the column containing the original values for the question in the survey that is being predicted.
  :param pred_column_name: a string, the name of the column that contains the llm predictions.
  :param n_options: an int, the amount of options or choices available to answer the predicted survey question.
  :param n_bootstrap: an int, number of bootstrap iterations (0 = no bootstrapping).
  :param confidence_level: a float, confidence level for bootstrap intervals (default 0.95).
  :param random_seed: an int or None, optional seed for reproducibility.

  :return: a pd.DataFrame, containing the metrics (jsd, acc, h, and jss) obtained for each one of the predefined sociodemographic groups.
    When n_bootstrap > 0, also includes CI lower/upper columns for each metric.
  """

  group_names = ["Woman", "Man", "Young adult", "Adult", "Senior adult", "Metropolitan region", \
         "Other region", "Indigenous people", "Non-indigenous people", 'None (indigenous)', \
         "Low Education", "Medium Education", "High Education", "None (education)",\
         "High Class", "Middle Class", "Low Class","Left", "Center", "Right", "No ideology", \
         "Religious", "Atheist/agnostic", 'No religion response']

  base_columns = ["Group", "JSD", "Accuracy", "Harmonic Mean", "JSS", "Kappa"]
  ci_columns = ["JSD_CI_lower", "JSD_CI_upper", "Accuracy_CI_lower", "Accuracy_CI_upper",
                 "Harmonic Mean_CI_lower", "Harmonic Mean_CI_upper", "JSS_CI_lower", "JSS_CI_upper",
                 "Kappa_CI_lower", "Kappa_CI_upper"]

  if n_bootstrap > 0:
    columns = base_columns + ci_columns
  else:
    columns = base_columns

  metrics_df = pd.DataFrame(columns=columns)

  bootstrap_kwargs = dict(n_bootstrap=n_bootstrap, confidence_level=confidence_level, random_seed=random_seed)

  metrics_df.loc[0] = [group_names[0]] + metrics_group_chile(df, "sexo", 2, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[1] = [group_names[1]] + metrics_group_chile(df, "sexo", 1, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[2] = [group_names[2]] + metrics_group_chile(df, "age", "young", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[3] = [group_names[3]] + metrics_group_chile(df, "age", "adult", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[4] = [group_names[4]] + metrics_group_chile(df, "age", "senior", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[5] = [group_names[5]] + metrics_group_chile(df, "nom_region", "METROPOLITANA", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[6] = [group_names[6]] + metrics_group_chile(df, "nom_region", "OTHER", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[7] = [group_names[7]] + metrics_group_chile(df, "info_enc_58", 1, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[8] = [group_names[8]] + metrics_group_chile(df, "info_enc_58", 2, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[9] = [group_names[9]] + metrics_group_chile(df, "info_enc_58", 3, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[10] = [group_names[10]] + metrics_group_chile(df, "esc_nivel_1", "low education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[11] = [group_names[11]] + metrics_group_chile(df, "esc_nivel_1", "medium education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[12] = [group_names[12]] + metrics_group_chile(df, "esc_nivel_1", "high education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[13] = [group_names[13]] + metrics_group_chile(df, "esc_nivel_1", "none", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[14] = [group_names[14]] + metrics_group_chile(df, "gse", "high class", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[15] = [group_names[15]] + metrics_group_chile(df, "gse", "middle class", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[16] = [group_names[16]] + metrics_group_chile(df, "gse", "poor class", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[17] = [group_names[17]] + metrics_group_chile(df, "iden_pol_2", "left", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[18] = [group_names[18]] + metrics_group_chile(df, "iden_pol_2", "center", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[19] = [group_names[19]] + metrics_group_chile(df, "iden_pol_2", "right", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[20] = [group_names[20]] + metrics_group_chile(df, "iden_pol_2", "none", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[21] = [group_names[21]] + metrics_group_chile(df, "religion_82", "religious", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[22] = [group_names[22]] + metrics_group_chile(df, "religion_82", "atheist/agnostic", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[23] = [group_names[23]] + metrics_group_chile(df, "religion_82", "doesnt know", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  # Total row
  total_jsd, total_acc, total_h, total_jss, total_kappa = _compute_group_metrics(df, pred_variable, pred_column_name, n_options)
  total_row = [total_jsd, total_acc, total_h, total_jss, total_kappa]

  if n_bootstrap > 0:
    rng = np.random.default_rng(random_seed)
    boot_metrics = np.empty((n_bootstrap, 5))
    n_samples = len(df)
    for i in range(n_bootstrap):
      sample = df.sample(n=n_samples, replace=True, random_state=int(rng.integers(0, 2**31)))
      boot_metrics[i] = _compute_group_metrics(sample, pred_variable, pred_column_name, n_options)
    alpha = 1 - confidence_level
    lo = np.nanpercentile(boot_metrics, 100 * alpha / 2, axis=0)
    hi = np.nanpercentile(boot_metrics, 100 * (1 - alpha / 2), axis=0)
    total_row += [lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], lo[3], hi[3], lo[4], hi[4]]

  metrics_df.loc[24] = ["Total"] + total_row

  return metrics_df


def metrics_by_prompt_table(df_list, model_name, names_list=False):
  """ Receives a list of dataframes, where each of them represents the prediction metrics of the same model, but applied to different prompts
    and returns one dataframe with metrics separated by prompt.

  :param df_list: a list of pd.DataFrame, where each element is the sociodemographic groups metrics table for a prediction made with an specific prompt.
    The variable that changes between each matric table in the list, es the prompt used to make the predictions.
  :param model_name: a string, the name of the model used to predict.
  :param names_list: a list of string, containing the names that will represent each element in df_list.

  :return: a pd.DataFrame, containing the total metrics (jsd, acc, h, and jss) obtained for each one of the different prompts.
  """
  if not names_list:
    names_list = ["Text", "List", "Chain of thought", "Text with Preamble", "Completion"]
  accs_list = []
  jsd_list = []
  h_list = []

  # For each metric dataframe metrics will be calculated.
  for df in df_list:
    total_acc = df.iloc[-1]["Accuracy"]
    total_jsd = df.iloc[-1]["JSS"]
    total_h = df.iloc[-1]["Harmonic Mean"]
    accs_list.append(total_acc)
    jsd_list.append(total_jsd)
    h_list.append(total_h)

  new_df = pd.DataFrame(columns = ["Model","Prompting", "Accuracy"])
  new_df["Prompting"] = names_list
  new_df["Accuracy"]  = accs_list
  new_df["JSS"]  = jsd_list
  new_df["Harmonic Mean"]  = h_list
  new_df["Model"] = model_name

  return new_df

def quantity_per_option_in_sociodemografic_group(df, group, id, column, n_options):
  """ Calculates the count per option in a question of the survey. The count is made for an specific sociodemographic group.
  
  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param charasteristic: a string, the column (or characteristic) by which the people will be filtered. 
    For example: age, religion column (religion_82), etc.
  :param id: a string or int, the indicator for the group that belogs to charasteristic and is going to be filtered.
  :param column: a string, the name of the column containing the values for the question in the survey that will be counted.
  :param n_options: an int, the amount of options or choices available to answer the predicted survey question.
  
  :return: a List, containing the count of votes for each possible choice.
  """
  options_quantity_list = []
  df_group = get_people_in_group_chile(df, group, id)

  if len(df_group) == 0: #Si no hay datos de este grupo
    return [None] * n_options

  for i in range (0, n_options):
    try:
      option_votes = df_group[column].value_counts()[i+1]
    except:
      option_votes = 0
    options_quantity_list.append(option_votes)

  return options_quantity_list

def quantities_per_option_per_group(df, column, options):
  """ Calculates the count per option in a question of the survey. The count is made separated by each sociodemographic group.
  
  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param column: a string, the name of the column containing the values for the question in the survey that will be counted.
  :param options: an list of string, the  options or choices available to answer the predicted survey question.
  
  :return: a pd.DataFrame, containing the count of votes for each possible choice, separated by each sociodemographic group.
  """
  n_options = len(options)
  quantities_df = pd.DataFrame(columns = ["Group"]+options)

  names = ["Woman", "Man", "Young adult", "Adult", "Senior adult", "Metropolitan region", \
         "Other region", "Indigenous people", "Non-indigenous people",  \
         "Low Education", "Medium Education", "High Education",\
         "High Class", "Middle Class", "Low Class","Left", "Center", "Right", "No ideology", \
         "Religious", "Atheist/agnostic"]

  quantities_df.loc[0] = [names[0]] + quantity_per_option_in_sociodemografic_group(df, "sexo", 2, column, n_options)
  quantities_df.loc[1] = [names[1]] + quantity_per_option_in_sociodemografic_group(df, "sexo", 1, column, n_options)

  quantities_df.loc[2] = [names[2]] + quantity_per_option_in_sociodemografic_group(df, "age", "young", column, n_options)
  quantities_df.loc[3] = [names[3]] + quantity_per_option_in_sociodemografic_group(df, "age", "adult", column, n_options)
  quantities_df.loc[4] = [names[4]] + quantity_per_option_in_sociodemografic_group(df, "age", "senior", column, n_options)

  quantities_df.loc[5] = [names[5]] + quantity_per_option_in_sociodemografic_group(df, "nom_region", "METROPOLITANA", column, n_options)
  quantities_df.loc[6] = [names[6]] + quantity_per_option_in_sociodemografic_group(df, "nom_region", "OTHER", column, n_options)

  quantities_df.loc[7] = [names[7]] + quantity_per_option_in_sociodemografic_group(df, "info_enc_58", 1, column, n_options)
  quantities_df.loc[8] = [names[8]] + quantity_per_option_in_sociodemografic_group(df, "info_enc_58", 2, column, n_options)

  quantities_df.loc[9] = [names[9]] + quantity_per_option_in_sociodemografic_group(df, "esc_nivel_1", "low education", column, n_options)
  quantities_df.loc[10] = [names[10]] + quantity_per_option_in_sociodemografic_group(df, "esc_nivel_1", "medium education", column, n_options)
  quantities_df.loc[11] = [names[11]] + quantity_per_option_in_sociodemografic_group(df, "esc_nivel_1", "high education", column, n_options)

  quantities_df.loc[12] = [names[12]] + quantity_per_option_in_sociodemografic_group(df, "gse", "high class", column, n_options)
  quantities_df.loc[13] = [names[13]] + quantity_per_option_in_sociodemografic_group(df, "gse", "middle class", column, n_options)
  quantities_df.loc[15] = [names[14]] + quantity_per_option_in_sociodemografic_group(df, "gse", "poor class", column, n_options)

  quantities_df.loc[15] = [names[15]] + quantity_per_option_in_sociodemografic_group(df, "iden_pol_2", "left",column, n_options)
  quantities_df.loc[16] = [names[16]] + quantity_per_option_in_sociodemografic_group(df, "iden_pol_2", "center", column, n_options)
  quantities_df.loc[17] = [names[17]] + quantity_per_option_in_sociodemografic_group(df, "iden_pol_2", "right", column, n_options)
  quantities_df.loc[18] = [names[18]] + quantity_per_option_in_sociodemografic_group(df, "iden_pol_2", "none", column, n_options)

  quantities_df.loc[19] = [names[19]] + quantity_per_option_in_sociodemografic_group(df, "religion_82", "religious", column, n_options)
  quantities_df.loc[20] = [names[20]] + quantity_per_option_in_sociodemografic_group(df, "religion_82", "atheist/agnostic", column, n_options)

  options_quantity_list = []
  for i in range (0, n_options):
    try:
      option_votes = df[column].value_counts()[i+1]
    except:
      option_votes = 0
    options_quantity_list.append(option_votes)

  quantities_df.loc[23] = ["Total"] + options_quantity_list
  return quantities_df


def get_people_in_group_usa(df, characteristic, id):
  """Filter people of a specific group in the USA (ANES) dataframe.

  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param characteristic: a string, the column by which people will be filtered.
  :param id: a string or int, the indicator for the group to filter.
  :return: a pd.DataFrame, containing only the people that belong to the desired group.
  """
  group_index = None

  if characteristic == "sexo":
    group_index = (df[characteristic] == id)

  elif characteristic == "edad":
    if id == "young":
      group_index = (df["edad"] >= 18) & (df["edad"] <= 26)
    elif id == "adult":
      group_index = (df["edad"] >= 27) & (df["edad"] <= 59)
    elif id == "senior":
      group_index = (df["edad"] >= 60)

  elif characteristic == "zona_u_r":
    if id == "city":
      group_index = (df[characteristic] == 1) | (df[characteristic] == 2)
    elif id == "rural":
      group_index = (df[characteristic] == 3) | (df[characteristic] == 4)

  elif characteristic == "race":
    if id == "white":
      group_index = (df[characteristic] == 1)
    elif id == "non-white":
      group_index = (df[characteristic] == 2) | (df[characteristic] == 3) | (df[characteristic] == 4) | (df[characteristic] == 5) | (df[characteristic] == 6)

  elif characteristic == "esc_nivel_1":
    if id == "low education":
      group_index = (df[characteristic] == 1) | (df[characteristic] == 2)
    elif id == "medium education":
      group_index = (df[characteristic] == 2) | (df[characteristic] == 3) | (df[characteristic] == 4) | (df[characteristic] == 5)
    elif id == "high education":
      group_index = (df[characteristic] == 6) | (df[characteristic] == 7) | (df[characteristic] == 8)

  elif characteristic == "gse":
    if id == "high class":
      group_index = (df["gse"] == 20) | (df["gse"] == 21) | (df["gse"] == 22)
    elif id == "middle class":
      group_index = (df["gse"] >= 10) & (df["gse"] <= 19)
    elif id == "poor":
      group_index = (df["gse"] >= 1) & (df["gse"] <= 9)

  elif characteristic == "iden_pol_2":
    if id == "left":
      group_index = (df[characteristic] == 1) | (df[characteristic] == 2) | (df[characteristic] == 3)
    elif id == "center":
      group_index = (df[characteristic] == 4)
    elif id == "right":
      group_index = (df[characteristic] == 5) | (df[characteristic] == 6) | (df[characteristic] == 7)
    elif id == "none":
      group_index = (df[characteristic] == 88) | (df[characteristic] == 99) | (df[characteristic] == -9) | (df[characteristic] == -8)

  elif characteristic == "iden_pol_3":
    if id == "democrat":
      group_index = (df[characteristic] == 1) | (df[characteristic] == 2)
    elif id == "republican":
      group_index = (df[characteristic] == 6) | (df[characteristic] == 7)
    elif id == "other":
      group_index = (df[characteristic] == 3) | (df[characteristic] == 4) | (df[characteristic] == 5) | (df[characteristic] == 88) | (df[characteristic] == 99) | (df[characteristic] == -8) | (df[characteristic] == -9)

  elif characteristic == "religion_82":
    if id == "religious":
      group_index = (df[characteristic] == 1) | (df[characteristic] == 2) | (df[characteristic] == 3) | (df[characteristic] == 4) | (df[characteristic] == 5) | (df[characteristic] == 6) | (df[characteristic] == 7) | (df[characteristic] == 8)
    elif id == "atheist/agnostic":
      group_index = (df[characteristic] == 9) | (df[characteristic] == 10) | (df[characteristic] == 11) | (df[characteristic] == 12)
    elif id == "doesnt know":
      group_index = (df[characteristic] == 88) | (df[characteristic] == 99) | (df[characteristic] == -8) | (df[characteristic] == -9)

  else:
    group_index = df[characteristic] == id

  df_group = df[group_index]
  return df_group


def metrics_group_usa(df, characteristic, id, pred_variable, pred_column_name, n_options, n_bootstrap=0, confidence_level=0.95, random_seed=None):
  """Calculates metrics for a specific sociodemographic group in the USA dataframe.

  Same structure as metrics_group_chile but calls get_people_in_group_usa.
  """
  df_group = get_people_in_group_usa(df, characteristic, id)

  if len(df_group) == 0:
    if n_bootstrap > 0:
      return [None] * 15
    return [None] * 5

  jsd, acc, h, jss, kappa = _compute_group_metrics(df_group, pred_variable, pred_column_name, n_options)

  if n_bootstrap <= 0:
    return [jsd, acc, h, jss, kappa]

  rng = np.random.default_rng(random_seed)
  boot_metrics = np.empty((n_bootstrap, 5))
  n_samples = len(df_group)

  for i in range(n_bootstrap):
    sample = df_group.sample(n=n_samples, replace=True, random_state=int(rng.integers(0, 2**31)))
    boot_metrics[i] = _compute_group_metrics(sample, pred_variable, pred_column_name, n_options)

  alpha = 1 - confidence_level
  lo = np.nanpercentile(boot_metrics, 100 * alpha / 2, axis=0)
  hi = np.nanpercentile(boot_metrics, 100 * (1 - alpha / 2), axis=0)

  return [jsd, acc, h, jss, kappa, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], lo[3], hi[3], lo[4], hi[4]]


def metrics_dataset_gen_usa(df, pred_variable, pred_column_name="pred", n_options=3, n_bootstrap=0, confidence_level=0.95, random_seed=None):
  """Returns a dataframe with metrics for each sociodemographic group and total (USA/ANES data).

  :param df: a pd.DataFrame, the test dataset containing all persons.
  :param pred_variable: a string, the column containing the original values.
  :param pred_column_name: a string, the column containing the predictions.
  :param n_options: an int, number of options for the predicted question.
  :param n_bootstrap: an int, number of bootstrap iterations (0 = no bootstrapping).
  :param confidence_level: a float, confidence level for bootstrap intervals.
  :param random_seed: an int or None, optional seed for reproducibility.
  :return: a pd.DataFrame with metrics per sociodemographic group.
  """

  group_names = ["Woman", "Man", "Young adult", "Adult", "Senior adult", "City/Suburb",
         "Small town/Rural", "White", "Non-White",
         "Low education", "Medium education", "High education",
         "Low class", "Middle class", "High class", "Left", "Center", "Right", "No ideology",
         "Democrat", "Republican", "None party", "Religious", "Atheist/agnostic", "No religion response"]

  base_columns = ["Group", "JSD", "Accuracy", "Harmonic Mean", "JSS", "Kappa"]
  ci_columns = ["JSD_CI_lower", "JSD_CI_upper", "Accuracy_CI_lower", "Accuracy_CI_upper",
                 "Harmonic Mean_CI_lower", "Harmonic Mean_CI_upper", "JSS_CI_lower", "JSS_CI_upper",
                 "Kappa_CI_lower", "Kappa_CI_upper"]

  if n_bootstrap > 0:
    columns = base_columns + ci_columns
  else:
    columns = base_columns

  metrics_df = pd.DataFrame(columns=columns)

  bootstrap_kwargs = dict(n_bootstrap=n_bootstrap, confidence_level=confidence_level, random_seed=random_seed)

  metrics_df.loc[0] = [group_names[0]] + metrics_group_usa(df, "sexo", 2, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[1] = [group_names[1]] + metrics_group_usa(df, "sexo", 1, pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[2] = [group_names[2]] + metrics_group_usa(df, "edad", "young", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[3] = [group_names[3]] + metrics_group_usa(df, "edad", "adult", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[4] = [group_names[4]] + metrics_group_usa(df, "edad", "senior", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[5] = [group_names[5]] + metrics_group_usa(df, "zona_u_r", "city", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[6] = [group_names[6]] + metrics_group_usa(df, "zona_u_r", "rural", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[7] = [group_names[7]] + metrics_group_usa(df, "race", "white", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[8] = [group_names[8]] + metrics_group_usa(df, "race", "non-white", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[9] = [group_names[9]] + metrics_group_usa(df, "esc_nivel_1", "low education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[10] = [group_names[10]] + metrics_group_usa(df, "esc_nivel_1", "medium education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[11] = [group_names[11]] + metrics_group_usa(df, "esc_nivel_1", "high education", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[12] = [group_names[12]] + metrics_group_usa(df, "gse", "poor", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[13] = [group_names[13]] + metrics_group_usa(df, "gse", "middle class", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[14] = [group_names[14]] + metrics_group_usa(df, "gse", "high class", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[15] = [group_names[15]] + metrics_group_usa(df, "iden_pol_2", "left", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[16] = [group_names[16]] + metrics_group_usa(df, "iden_pol_2", "center", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[17] = [group_names[17]] + metrics_group_usa(df, "iden_pol_2", "right", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[18] = [group_names[18]] + metrics_group_usa(df, "iden_pol_2", "none", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[19] = [group_names[19]] + metrics_group_usa(df, "iden_pol_3", "democrat", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[20] = [group_names[20]] + metrics_group_usa(df, "iden_pol_3", "republican", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[21] = [group_names[21]] + metrics_group_usa(df, "iden_pol_3", "other", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  metrics_df.loc[22] = [group_names[22]] + metrics_group_usa(df, "religion_82", "religious", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[23] = [group_names[23]] + metrics_group_usa(df, "religion_82", "atheist/agnostic", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)
  metrics_df.loc[24] = [group_names[24]] + metrics_group_usa(df, "religion_82", "doesnt know", pred_variable, pred_column_name, n_options, **bootstrap_kwargs)

  # Total row
  total_jsd, total_acc, total_h, total_jss, total_kappa = _compute_group_metrics(df, pred_variable, pred_column_name, n_options)
  total_row = [total_jsd, total_acc, total_h, total_jss, total_kappa]

  if n_bootstrap > 0:
    rng = np.random.default_rng(random_seed)
    boot_metrics = np.empty((n_bootstrap, 5))
    n_samples = len(df)
    for i in range(n_bootstrap):
      sample = df.sample(n=n_samples, replace=True, random_state=int(rng.integers(0, 2**31)))
      boot_metrics[i] = _compute_group_metrics(sample, pred_variable, pred_column_name, n_options)
    alpha = 1 - confidence_level
    lo = np.nanpercentile(boot_metrics, 100 * alpha / 2, axis=0)
    hi = np.nanpercentile(boot_metrics, 100 * (1 - alpha / 2), axis=0)
    total_row += [lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], lo[3], hi[3], lo[4], hi[4]]

  metrics_df.loc[25] = ["Total"] + total_row

  return metrics_df