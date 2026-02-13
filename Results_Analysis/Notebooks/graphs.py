import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import vapeplot
import matplotlib.pyplot as plt

from matplotlib.transforms import ScaledTranslation
from metrics import quantities_per_option_per_group, metrics_dataset_gen_chile


def prompting_bar(df_list, title, x_label, metric = "Accuracy"):
  """ 
  Generates a bar plot that represents the variation of selected metric across the different models and prompts.
  
  :param df_list: a list of pd.DataFrame, each dataframe corresponds to an metric_by_prompt_table, for different models.
  :param title: a string, the plot title.
  :param x_label: a string, the label for x axis in the plot.
  :param metric: a string, the metric to plot.
  """
  new_df = pd.DataFrame(columns = ["Prompting"])
  new_df["Prompting"] = df_list[0]["Prompting"]
  models_list = []
  for df in df_list:
    model_name = df.iloc[0]["Model"]
    models_list.append(model_name)
    new_df[model_name] = df[metric]

  ax = new_df.plot(kind='bar', x='Prompting', y=models_list, width=0.8, figsize=(10, 6))

  ax.set_xlabel(x_label)
  ax.set_ylabel(metric)
  ax.set_title(title)
  plt.legend(title='Model',loc='upper right', bbox_to_anchor=(1, 1))
  plt.xticks(rotation=80)
  plt.ylim(0, 1)

  plt.show()


def distribution_of_votes_per_group_graph(df, column_name, options, title):
    """ Generates a bar plot, that shows votes distribution for each sociodemographic group. 
      Can be use to visualize original distribution of votes, or the predicted one.

    :param df: a pd.DataFrame, the test dataset containing all persons.
    :param column: a string, the name of the column containing the values for the question in the survey that will be counted.
    :param options: an list of string, the  options or choices available to answer the predicted survey question.
    :param title: a string, the plot title.
    """
    quantities_df = quantities_per_option_per_group(df, column_name, options)
    # Calculates relatives percentages
    df_total = quantities_df[options].sum(axis=1)
    percentages_df = quantities_df[options].div(df_total, axis=0) * 100

    percentages_df = pd.DataFrame(percentages_df, columns=options)
    percentages_df["Group"] = ["Woman", "Man", "Young adult", "Adult", "Senior adult", "Metropolitan region", \
                                "Other region", "Indigenous people", "Non-indigenous people", \
                                "Low Education", "Medium Education", "High Education",\
                                "High Class", "Middle Class", "Low Class","Left", "Center", "Right", "No ideology", \
                                "Religious", "Atheist/agnostic"]

    vapeplot.set_palette('jazzcup')
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle')

    # Creates figures
    fig, ax = plt.subplots(figsize=(12, len(percentages_df) * 0.35))
    bar_height = 0.6  # Bar sizes

    # Axis Y bar positions
    y_positions = range(len(percentages_df))

    # Stack bars
    left_accum = [0] * len(percentages_df)
    for option in options:
      ax.barh(
        y=y_positions,
        width=percentages_df[option],
        height=bar_height,
        left=left_accum,
        label=option
      )
      left_accum = [left_accum[i] + percentages_df[option].iloc[i] for i in range(len(percentages_df))]

    # Axis Y configuration
    ax.set_yticks(y_positions)
    ax.set_yticklabels(percentages_df["Group"], fontsize=12)
    ax.set_ylim(-0.5, len(percentages_df) - 0.5)  # Ajustar el rango del eje Y para evitar espacio extra

    # Remove additional margins
    ax.margins(y=0)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    # Leyend
    ax.legend(title='Options', bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=len(options), fontsize=12)
    ax.set_title(title, ha='center', fontsize=14)

    # Add percentages values inside bars
    for bars in ax.containers:
      labels = [f'{v:.1f}' if v > 0 else '' for v in bars.datavalues]
      ax.bar_label(bars, labels=labels, label_type='center', fontsize=11)

    plt.tight_layout()
    plt.show()




def ablation_graph(df_list,df_ablation, exp_column, title, metric):
  """ Creates bar plot for ablation experiment.

  :param df_list: a list of pd.DataFrame, where each element is the prediction dataframe for some prompt variation of ablation experiment.
    That is: prompt containing all variables, prompt without political variables, and prompt with political variables only.
  :param df_ablation: a pd.DataFrame, the dataframe containing the predictions for all other variations of ablation experiment, that is,
    all prompt combinations resulted by removing one person charasteristic each time.
  :param exp_column: a string, the name of the column that corresponds to the predicted survey question.

  :return: a pd.DataFrame, containing the metrics for each possible prompt in the ablation experiment.
  """
  models_list = ["All", "Without political variables", "Only political variables"]
  var_list = ["- gender", "- age","- region", "- race", "- gse", "- scholarity", "- religion", "- ideology", "- party", "- interest"]

  accs = []
  jsss = []
  hs = []
  df_final = pd.DataFrame()

  for df in df_list:
    metrics_df = metrics_dataset_gen_chile(df, exp_column)
    acc = metrics_df.iloc[-1]["Accuracy"]
    accs.append(acc)
    jss = metrics_df.iloc[-1]["JSS"]
    jsss.append(jss)
    h =  metrics_df.iloc[-1]["Harmonic Mean"]
    hs.append(h)


  for var in var_list:
    metrics_df = metrics_dataset_gen_chile(df_ablation, exp_column,"pred_" + var[2:])
    acc = metrics_df.iloc[-1]["Accuracy"]
    accs.append(acc)
    jss = metrics_df.iloc[-1]["JSS"]
    jsss.append(jss)
    h = metrics_df.iloc[-1]["Harmonic Mean"]
    hs.append(h)

  line =[]
  for i in range(len(models_list)+len(var_list)):
    line.append(hs[0])

  df_final["model"] = models_list + var_list
  df_final["acc"] = accs
  df_final["jss"] = jsss
  df_final["h"] = hs


  plt.bar(x = models_list+ var_list, height=hs)
  plt.xticks(rotation=80)
  plt.ylim(0, 1)
  plt.plot(models_list+ var_list, line, "r--")
  plt.title(title)
  plt.ylabel(metric)
  return df_final




def sociodemographic_line_plot(modelos, modelos_colores, modelos_nombres, title):
  fig, ax = plt.subplots(figsize=(12, 6))

  plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle')

  # Define range in x axis for each group
  grupos = {
    "Sexo": (0, 1),       # Índices para el grupo "Sexo"
    "Edad": (2, 4),       # Índices para el grupo "Edad"
    "Región": (5, 6),     # Índices para el grupo "Región"
    "Pueblo originario": (7, 8),     # Índices para el grupo "Región"
    "Escolaridad": (9, 11),     # Índices para el grupo "Región"
    "GSE": (12, 14), # Índices para "Ideología 1"
    "Ideología": (15, 18),
    "Religion": (19, 20),
    # "Total": (21, 21)    # Índices para "Total"
  }

  # Define background colors
  colores = {
    "Sexo": "#f0f8ff",
    "Edad": "#ffebcd",
    "Región": "#add8e6",
    "Pueblo originario": "#A49CF2",
    "Escolaridad": "#8FBC8F",
    "GSE": "#d3f8d3",
    "Ideología": "#ffe4e1",
    "Religion": "#fffacd",
    # "Total": "#ffffff"
  }

  # Add background color by group
  for grupo, (inicio, fin) in grupos.items():
    ax.axvspan(inicio - 0.5, fin + 0.5, color=colores[grupo], alpha=0.5)

  # Plot the lines by group with specific colors
  CI_LOWER = "Harmonic Mean_CI_lower"
  CI_UPPER = "Harmonic Mean_CI_upper"

  for modelo_data, modelo_nombre in zip(modelos, modelos_nombres):
    modelo_data = modelo_data[modelo_data['Group'] != "None (indigenous)"]
    modelo_data = modelo_data[modelo_data['Group'] != "None (education)"]
    modelo_data = modelo_data[modelo_data['Group'] != "No religion response"]
    has_ci = CI_LOWER in modelo_data.columns and CI_UPPER in modelo_data.columns
    for grupo, (inicio, fin) in grupos.items():
      x = list(range(inicio, fin + 1))
      y = modelo_data["Harmonic Mean"].iloc[inicio:fin + 1]
      ax.plot(x, y, '-o', label=modelo_nombre if grupo == "Sexo" else "", color=modelos_colores[modelo_nombre])
      if has_ci:
        y_lo = modelo_data[CI_LOWER].iloc[inicio:fin + 1].astype(float)
        y_hi = modelo_data[CI_UPPER].iloc[inicio:fin + 1].astype(float)
        ax.fill_between(x, y_lo, y_hi, color=modelos_colores[modelo_nombre], alpha=0.2)


  data = modelos[0][modelos[0]['Group'] != "None (indigenous)"]
  data = data[data['Group'] != "None (education)"]
  data = data[data['Group'] != "No religion response"]

  ax.set_ylim(0, 1)
  ax.set_xticks(range(len(data["Group"])))
  ax.set_xticklabels(data["Group"], rotation=80,ha='right')
  ax.legend(loc='lower right')
  ax.set_title(title)


  for label in ax.get_xticklabels():
    offset = ScaledTranslation(5/72, 0, fig.dpi_scale_trans)
    label.set_transform(label.get_transform() + offset)

  plt.tight_layout()
  plt.show()