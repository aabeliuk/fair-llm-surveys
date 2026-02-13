import os
import json
from pprint import pprint
import random

import bitsandbytes as bnb
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import aux_ablation
import dictionaries
from prompt_generator import prompt_generator, prompt_generator_english
from deep_translator import GoogleTranslator

import transformers
from datasets import load_dataset
from peft import (
  LoraConfig,
  PeftConfig,
  PeftModel,
  get_peft_model,
)
from transformers import (
  AutoConfig,
  AutoModelForSeq2SeqLM,
  AutoModelForCausalLM,
  AutoTokenizer,
  BitsAndBytesConfig,
)

os.environ["TRANSFORMERS_CACHE"] = "~/data"


bnb_config = BitsAndBytesConfig(
  load_in_4bit=True,
  bnb_4bit_use_double_quant=True,
  bnb_4bit_quant_type="nf4",
  bnb_4bit_compute_dtype=torch.float16,
)

# Definir la clase base (clase padre)
class Exp_Request:
  def __init__(self, exp, model_name, b,chat,jsonl_name, task, context, end , inst, dictionary, eng, prompt_estructure, prompt_type ,translate,ablation, finetuned, nsamples, random_fewshot, index_matrix):
    self.model_n = model_name
    if finetuned:
      self.model_name = model_name

    elif self.model_n == "mistral" and b == "v0.1":
      self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    elif self.model_n == "mistral" and b == "v0.2":
      self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    elif self.model_n == "t0":
      self.model_name = "bigscience/T0pp"
    else:
      self.model_name = "meta-llama/Llama-2-" + b + "b-chat-hf"

    print(self.model_name)
    print(jsonl_name)
    self.finetuned = False
    self.model, self.tokenizer, self.generation_config = self.get_model_params(self.model_name)
    self.mistral = False if self.model_n.find("t0") != -1 else True
    self.translate = translate
    if translate:
      self.translator = GoogleTranslator(source='es', target='en')
      self.task = self.translator.translate(task)
      self.context = self.translator.translate(context)
      self.end = self.translator.translate(end)
      self.inst = self.translator.translate(inst)
    else:
      self.task = task
      self.context = context
      self.end = end
      self.inst = inst

    self.jsonl_name = jsonl_name
    self.random_fewshot = random_fewshot
    if prompt_type == "anes":
      self.examples_df = pd.read_csv('anes_2020_660_v1.csv')
    else:
      #self.examples_df = pd.read_csv('exp_100_inputs.csv')
      self.examples_df = pd.read_csv('anes_2020_660_v1.csv')
    self.imatrix = index_matrix
    self.nsamples = nsamples
    self.dictionary = dictionary
    self.eng = eng
    self.exp = exp
    self.prompt_estructure = prompt_estructure
    self.prompt_type = prompt_type
    self.ablation = ablation
    self.var_removed = ""
    self.chat = chat
    self.data_ablation = False


  def load_model(self,model_name, charger):
    model = charger.from_pretrained(
      model_name,
      #device_map={"":0},
      device_map="auto",
      quantization_config=bnb_config,
      trust_remote_code=True,
      use_auth_token=True
    )
    model.config.use_cache = False

    return model
  
  def load_t0_model(self,model_name):
    model = AutoModelForSeq2SeqLM.from_pretrained("bigscience/T0pp")

    model = AutoModelForSeq2SeqLM.from_pretrained(
      model_name,
      #device_map={"":1},
      device_map="auto",
      quantization_config=bnb_config,
      trust_remote_code=True
    )
    model.config.use_cache = False

    return model
  
  def load_model_finetuned(self,model_name, x):
    
    # Load the model with quantization config
    model = AutoModelForCausalLM.from_pretrained(
      model_name,
      return_dict=True,
      #device_map={"":1},
      device_map = "auto",
      quantization_config=bnb_config,
      trust_remote_code=True
    )
    return model


  def get_model_params(self, model_name):
    print("comienzo a generar modeloaaaaaaaaaaaa")
    if self.finetuned:
      PEFT_MODEL = model_name
      config = PeftConfig.from_pretrained(PEFT_MODEL)
      model_name_path = config.base_model_name_or_path
      model = self.load_model_finetuned(model_name_path, AutoModelForCausalLM)
      model = PeftModel.from_pretrained(model, PEFT_MODEL)
    elif self.model_n =="t0":
      model_name_path = model_name
      model = self.load_model("bigscience/T0pp", AutoModelForSeq2SeqLM)
    else:
      model_name_path = model_name
      model =  self.load_model(model_name_path, AutoModelForCausalLM)
      model.config.use_cache = False

    print("ahora tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(model_name_path, trust_remote_code=True)
    #tokenizer.pad_token = tokenizer.eos_token

    generation_config = ""
    #tokenizer.pad_token = tokenizer.eos_token
    """ generation_config = model.generation_config
    generation_config.max_new_tokens = 500
    generation_config.temperature = 1.5
    #generation_config.do_sample = True
    generation_config.top_p = 0.7
    generation_config.num_return_sequences = 1
    generation_config.pad_token_id = tokenizer.eos_token_id
    generation_config.eos_token_id = tokenizer.eos_token_id """
    print("listo tokenizer")
    return model, tokenizer, generation_config
    

  def ablation_request(self, dataset):
    #"gender", "age", "region", "indigenous", "gse", "scholarity", "religion","ideology", "party", "interest"
    variables = ["scholarity", "religion","ideology", "party", "interest"]

    for var in variables:
      self.var_removed = var
      data_ablation = aux_ablation.ablation_df(dataset, var, self.prompt_estructure, self.eng, self.exp)
      examples_data_ablation = aux_ablation.ablation_df(self.examples_df, var, self.prompt_estructure, self.eng, self.exp)
      self.data_ablation = data_ablation
      self.examples_df = examples_data_ablation
      #print(data_ablation.iloc[0])
      #print(examples_data_ablation)

      self.answers_generator(data_ablation)


  def answers_generator(self, dataset):
    for index, example in dataset.iterrows():
      
      prompt = self.prompting(example, index)
      print("----------------------")
      print()

      self.request_generator(prompt, index)


  def request_generator(self, prompt, index):
    length = len(prompt)
    device = "cuda:1"
    if self.mistral:
      if not self.random_fewshot:
        messages = [
          {"role": "user", "content": prompt}
        ]
      else:
        messages= prompt
      
      print(messages)
      tokenized_chat = self.tokenizer.apply_chat_template(messages, tokenize=True,add_generation_prompt=True ,return_tensors="pt")
      outputs = self.model.generate(tokenized_chat, max_new_tokens=300)
      decoded = self.tokenizer.batch_decode(outputs)
      aux = decoded[0]

    else:
      print(prompt)
      encoding = self.tokenizer(prompt, return_tensors="pt").to(device)

      if self.model_n == "t0":
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs)
        aux = self.tokenizer.decode(outputs[0])
        print("aux", aux)
      else:
        with torch.inference_mode():
          outputs = self.model.generate(
            input_ids = encoding.input_ids,
            attention_mask=encoding.attention_mask,
            generation_config = self.generation_config,
          )
        aux = self.tokenizer.decode(outputs[0],skip_special_tokens=True)
    #print(aux)
    print(index)
    
    #aux = self.post_processing(aux, length)
    
    aux = aux.split("[/INST]")[-1]
    print(aux)

    if index == 0:
      respuesta = {
        'id_pregunta':index,
        'var_removed': self.var_removed,
        'prompt': prompt,
        'respuesta':aux
      }
    else:
      respuesta = {
        'id_pregunta':index,
        'var_removed': self.var_removed ,
        'respuesta':aux
      }
    
    with open(self.jsonl_name, "a") as file:
      json.dump(respuesta, file)
      file.write("\n")

  
  def prompting(self, example, index):
    print("PROMPT")
    if self.ablation:
      person_prompt = example["prompt"]
    elif not self.eng:
      person_prompt = prompt_generator(example, self.prompt_estructure,  self.exp, self.prompt_type)
    else:
      person_prompt = prompt_generator_english(example, self.prompt_estructure, self.exp, self.prompt_type )

    if self.translate:
      person_prompt = self.translator.translate(person_prompt)

    
    if self.random_fewshot:
      index_list = self.imatrix[index][0:self.nsamples] #list of random 10 indexes that indicates the examples to be used in this case
      fs_examples_prompt = self.random_fewshot_prompt_generator(index_list)
      #prompt = fs_examples_prompt + "<s>[INST]" + self.end + person_prompt + self.inst + "[/INST]"
      if self.mistral:
        prompt = fs_examples_prompt + [{"role": "user", "content": self.task + self.context + self.end + '\n'+ person_prompt + "\n" +self.inst }]
      else:
        prompt = fs_examples_prompt + f""" 
'user': {self.task}
{person_prompt} 
{self.inst}
'assistant': """
    elif not self.chat:
      prompt = f"""{{### Instruction {self.task}
      ### Input: { self.end + self.translator.translate(person_prompt)}}}"""
      
    
    else:

      if self.mistral:
        prompt = f"""{self.task + self.context + self.end}{person_prompt} 
{self.inst }"""
      else:
        #<<SYS>> <</SYS>> [INST] [/INST]
        """ prompt = {{
{self.task}
{ person_prompt + self.end }}} """

        prompt = f"""{self.task}{ person_prompt}
{self.end}"""


      
    return prompt
  
  def prompt_language(self, example):
    if self.ablation and self.translate:
      prompt = self.translator.translate(example["prompt"])
    elif self.ablation:
      prompt = example["prompt"]
    elif self.translate and not self.eng:
      prompt = self.translator.translate(prompt_generator(example, self.prompt_estructure, self.exp, self.prompt_type))
    elif self.eng:
      prompt = prompt_generator_english(example, self.prompt_estructure, self.exp, self.prompt_type )
    else:
      prompt = prompt_generator(example,  self.prompt_estructure, self.exp, self.prompt_type)
    return prompt
  
  def random_fewshot_answer(self,example, column):
    if self.prompt_estructure !="json":
      answer = self.dictionary[int(example[column])]
    elif self.eng:
      answer = "{'explanation': here the explanation, 'answer': " +  self.dictionary[int(example[column])] + "}"
    else:
      answer = "{'explicación': aquí la explicación, 'respuesta': " +  self.dictionary[int(example[column])] + "}"

    return answer
  
#genero un dataset de 100 muestras con los prompts y respuestas que corresponden.
#otro dataset sin esos 100 prompts
#una matriz donde cada fila contiene los 10 ejemplos(indices) para utilizar en cierta persona.
  def random_fewshot_prompt_generator(self, index_list):
    i1=index_list.pop(0)
    if self.ablation:
      example = self.examples_df.iloc[i1]
      prompt = self.prompt_language(example)
    else:
      example = self.examples_df.iloc[i1]
      prompt = self.prompt_language(example)

    if self.exp == 3:
      ex = "Primero, se te dará un ejemplo solo para que te familiarices con el FORMATO de respuesta, independiente de la opción elegida:\n"
    else:
      ex = "A continuación se te darán algunos ejemplos:\n"

    if self.mistral:
      column= dictionaries.exp_columns[self.exp]
      answer = self.random_fewshot_answer(example, column)
      messages = [{"role": "user", "content": self.task + self.context + self.end + '\n'+ prompt + "\n" + self.inst }, 
                  {"role": "assistant", "content": answer}]
      for index in index_list:
        if self.ablation:
          example = self.examples_df.iloc[index]
          prompt = self.prompt_language(example)
        else:
          example = self.examples_df.iloc[index]
          prompt = self.prompt_language(example)
        answer = self.random_fewshot_answer(example, column)
        messages += [{"role": "user", "content": self.task + self.context + self.end + '\n'+ prompt +'\n'+ self.inst }, 
                          {"role": "assistant", "content": answer}]
        
    else:
      column= dictionaries.exp_columns[self.exp]
      answer = self.random_fewshot_answer(example, column)
      messages = f""" 'user': {self.task}
{prompt}{self.end} 
{self.inst}
'assistant' : {answer}"""
      for index in index_list:
        if self.ablation:
          example = self.data_ablation.iloc[index]
          prompt = self.prompt_language(example)
        else:
          example = self.examples_df.iloc[index]
          prompt = self.prompt_language(example)
        answer = self.random_fewshot_answer(example, column)
        messages += f"""
'user': {self.task}
{prompt} {self.end} 
{self.inst if (self.prompt_estructure == "list" or self.prompt_estructure == "text" or self.prompt_estructure == "json") else ""}
'assistant': {answer}. """
    

    #'{ "explanation": here the explanation, "answer": ' + answer +'}'
    """ fewshot_chain = "<s>[INST] <<SYS>>\n"+ self.context + "\n" + "<</SYS>>\n" + \
      ex +person_prompt +"[/INST]\n"+ \
        self.dictionary[int(self.examples_df.iloc[i1]["religion_14"])] + "</s>"
    
    #example_chain = ""
    for index in index_list:
      example = self.examples_df.iloc[index]
      prompt = prompt_generator(example, self.exp, self.wpv, self.red )
      answer = self.examples_df.iloc[index]["religion_14"]
      fewshot_chain += "<s>[INST]" + prompt + "[/INST]" + self.dictionary[int(answer)] + "</s>" """
    return messages