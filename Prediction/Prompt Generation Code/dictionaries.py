sexo_anes = {
    1: "male",
    2: "female",
    -8: "doesn't know",
    -9: "does not answer",
    88: "doesn't know",
    99: "does not answer",
}
pueblo_anes = {
    -8: "doesn't know",
    -9: "does not answer",
    88: "doesn't know",
    99: "does not answer",
    1: "white, non-Hispanic",
    2: "black, non-Hispanic",
    3: "hispanic",
    4: "asian or Native Hawaiian/other Pacific Islander, non-Hispanic alone",
    5: "native American/Alaska Native or other race, non-Hispanic alone",
    6: "multiple races, non-Hispanic",
  }
izq_der_anes = {
    -8: "doesn't know",
    -9: "does not answer",
    88: "doesn't know",
    99: "does not answer",
    1: "extremely liberal",
    2: "liberal",
    3: "slightly liberal",
    4: "moderate; middle of the road",
    5: "slightly conservative",
    6: "conservative",
    7: "extremely conservative",
  }
party_anes = {
    -8: "doesn't know",
    -9: "does not answer",
    88: "doesn't know",
    99: "does not answer",
    1: "strong Democrat",
    2: "not very strong Democrat",
    3: "independent-Democrat",
    4: "independent",
    5: "independent-Republican",
    6: "not very strong Republican",
    7: "strong Republican",
  }
religion_anes = {
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  1: "Protestant",
  2: "Roman Catholic",
  3: "Orthodox Christian (such as Greek or Russian Orthodox)",
  4: "Latter-Day Saints (LDS)",
  5: "Jewish",
  6: "Muslim",
  7: "Buddhist",
  8: "Hindu",
  9: "Atheist",
  10: "Agnostic",
  11: "something else",
  12: "none in particular"
}

region_anes = {
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  1: "Alabama",
  2: "Alaska",
  4.: "Arizona",
  5: "Arkansas",
  6: "California",
  8: "Colorado",
  9: "Connecticut",
  10: "Delaware",
  11: "District of Columbia (Washington DC)",
  12: "Florida",
  13: "Georgia",
  15: "Hawaii",
  16: "Idaho",
  17: "Illinois", 
  18: "Indiana",
  19: "Iowa",
  20: "Kansas",
  21: "Kentucky",
  22: "Louisiana",
  23: "Maine", 
  24: "Maryland",
  25: "Massachusetts",
  26: "Michigan", 
  27: "Minnesota",
  28: "Mississippi",
  29: "Missouri",
  30: "Montana",
  31: "Nebraska",
  32: "Nevada",
  33: "New Hampshire",
  34: "New Jersey",
  35: "New Mexico",
  36: "New York",
  37: "North Carolina",
  38: "North Dakota",
  39: "Ohio",
  40: "Oklahoma",
  41: "Oregon",
  42: "Pennsylvania",
  44: "Rhode Island",
  45: "South Carolina",
  46: "South Dakota",
  47: "Tennessee",
  48: "Texas",
  49: "Utah",
  50: "Vermont",
  51: "Virginia",
  53: "Washington",
  54: "West Virginia", 
  55: "Wisconsin",
  56: "Wyoming",
  57: "Puerto Rico",
  58: "Another U.S. territory (Guam, Samoa, U.S. Virgin Islands)",
  59: "Another country",
}

zona_anes = {
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  1: "Rural area",
  2: "Small town",
  3: "Suburb",
  4: "City",
}

escolaridad_anes={
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  1: "Less than high school credential",
  2: "High school graduate - High school diploma or equivalent (e.g. GED)",
  3: "Some college but no degree",
  4: "Associate degree in college - occupational/vocational",
  5: "Associate degree in college - academic",
  6: "Bachelor's degree (e.g. BA, AB, BS)",
  7: "Master's degree (e.g. MA, MS, MEng, MEd, MSW, MBA)",
  8: "Professional school degree (e.g. MD, DDS, DVM, LLB, JD)/Doctoral degree (e.g. PHD, EDD)",
  95: "Other"
}


interes_anes = {
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  -7: "No post-election data, deleted due to incomplete interview",
  -6: "No post-election interview",
  -5: "Interview breakoff (sufficient partial IW)",
  1: "very interested",
  2: "somewhat interested",
  3: "not very interested",
  4: "not at all interested",
}

gse_anes = {
  -8: "doesn't know",
  -9: "does not answer",
  88: "doesn't know",
  99: "does not answer",
  1: "very poor",
  2: "very poor",
  3: "poor",
  4: "poor",
  5: "poor",
  6: "poor",
  7: "poor",
  8: "poor",
  9: "poor",
  10: "middle class",
  11: "middle class",
  12: "middle class",
  13: "middle class",
  14: "middle class",
  15: "middle class",
  16: "middle class",
  17: "middle class",
  18: "middle class",
  19: "middle class",
  20: "upper class",
  21: "upper class",
  22: "upper class",
}

voto_anes = {
  1: "Joe Biden",
  2: "Donald Trump",
  3: "Jo Jorgensen",
  4: "Howie Hawkins",
  5: "Other candidate",
}

dict_sexo = {
  1: "masculino",
  2: "femenino",
  "hombre": 1,
  "mujer": 2
}

dict_genero = {
  1: "hombre",
  2: "mujer",
  "hombre": 1,
  "mujer": 2
}

dict_sexo_eng = {
  1: "male",
  2: "female",
}

zona_eng = {
  2:"rural",
  1:"urban"
}

question_dict = {
  1: "¿Por quién votó en las elecciones presidenciales del 2021?",
  2: "¿Por cuál opción votó en el plebiscito de salida para la nueva constitución de Chile en Septiembre del 2022?",
  9 : "Ahora porfavor responde a la siguiente pregunta teniendo en cuenta los rasgos anteriores. ¿Por cuál de las siguientes opciones votó en el plebiscito constitucional de entrada realizado el 25 de octubre del 2020? Elije solo una de las siguientes opciones: Apruebo, Rechazo, Nulo. \n ",
  3: "¿Cuál es la opinión de esta persona sobre el aborto?",
  4 : "Ahora porfavor responde a la siguiente pregunta teniendo en cuenta los rasgos anteriores y considerando que el año de contexto es el 2022: La persona descrita ¿Con cuál de las siguientes frases estaría más de acuerdo con respecto a la democracia?. Recuerda responder SOLO con los números asociados a las frases como ya se te indicó, sin explicaciones ni palabras extras. \n",
  5: "Ahora porfavor responde a la siguiente pregunta teniendo en cuenta los rasgos anteriores y considerando que el año de contexto es el 2022: Independiente de su posición política, la persona descrita anteriormente ¿Aprueba o desaprueba la forma como está conduciendo Gabriel Boric el gobierno? Recuerda responder SOLO con una de las siguientes opciones, sin palabras extras, ni cambiadas, y sin números: Aprueba, Desaprueba, No aprueba ni desaprueba. \n",
  6: "Ahora porfavor responde a la siguiente pregunta teniendo en cuenta los rasgos anteriores y considerando que el año de contexto es el 2022: Para la persona ya descrita, ¿Cuál sería el problema al que debería dedicar mayor esfuerzo en solucionar el gobierno? Recuerda responder SOLO con el número asociado a la respuesta, sin ninguna palabra extra.\n",

}

normal_question_dict_eng = {
  1: "Which candidate did this person vote for in the 2nd round of the December 2021 chilean presidential election? Choose only one of the following options: Gabriel Boric, José Antonio Kast, null.",
  2: "Which of the following options did this person vote for in the chilean exit plebiscite for the new constitution in September 2022? Choose only one of the following options: Approve, Reject, null.",
  3: "Which of these ideas best expresses this person's judgment regarding abortion? Choose only one of the following options: Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case."
}

question_dict_eng = {
  #1: "Which candidate did this person vote for in the 2nd round of the December 2021 chilean presidential election? Choose only one of the following options: Gabriel Boric, José Antonio Kast, null.",
  #1: "Which candidate did this person vote for in the 2nd round of the December 2021 chilean presidential election?",
  1: "Which candidate did you vote for in the 2nd round of the December 2021 chilean presidential election?",
  2: "Which of the following options did this person vote for in the chilean exit plebiscite for the new constitution in September 2022?",
  #3: "Which of these ideas best expresses your judgment regarding abortion?"
  3: "What is this person's opinion on abortion?"
}

question_dict_list = {
  1: "Which candidate did this person vote for in the 2nd round of the December 2021 chilean presidential election? Gabriel Boric, José Antonio Kast, or null?",
  2: "Which of the following options did this person vote for in the chilean exit plebiscite for the new constitution in September 2022? Approve, Reject or null?",
  3: "Which of these ideas best expresses this person's judgment regarding abortion? Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case?"
}

question_dict_list_anes = {
  1: "Which candidate did this person vote for in the 2020 United States presidential election? Joe Biden, Donald Trump, Jo Jorgensen or Howie Hawkins?",
  3: "Which of these ideas best expresses this person's judgment regarding abortion? Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case?"
}

question_dict_list_esp = {
  1: "Which candidate did this person vote for in the 2nd round of the December 2021 chilean presidential election? Gabriel Boric, José Antonio Kast, or null?",
  2: "¿Cuál de las siguientes opciones votó esta persona en el plebiscito de salida para la nueva constitución de Chile en Septiembre del 2022'?¿Apruebo, Rechazo, o nulo?",
  3: "¿Cuál de estas ideas expresa de mejor el juicio de esta persona respecto del aborto? ¿Aborto debe estar siempre prohibido, aborto solo debe estar permitido en casos especiales, aborto debe ser una opción para las mujeres en cualquier caso?",
  #3: "Which of these ideas best expresses this person's judgment regarding abortion? Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case?"
}


alternatives_dict = {
  #1: " Gabriel Boric Font (left-wing), José Antonio Kast Rist(right-wing), Votó nulo.",
  1: " Gabriel Boric Font, José Antonio Kast Rist, Votó nulo.",
  2: " Rechazo, Apruebo, Votó nulo.",
  3: " Aborto debe estar siempre prohibido, aborto solo debe estar permitido en casos especiales, aborto debe ser una opción para las mujeres en cualquier caso."
}

alternatives_dict_eng = {
  #1: " Gabriel Boric Font (left-wing), José Antonio Kast Rist(right-wing), Votó nulo.",
  1: " Gabriel Boric Font, José Antonio Kast Rist, voted null.",
  2: " Approve,  Reject, voted null.",
  3: "Abortion should always be prohibited, abortion should only be allowed in special cases, abortion should be an option for women in any case."
}

region_dict = {
  1: "Tarapacá",
  2: "Antofagasta",
  3: "Atacama",
  4: "Coquimbo",
  5: "Valparaíso",
  6: "OHiggins",
  7: "Maule",
  8: "BioBio",
  9: "La Araucanía",
  10: "Los Lagos",
  11: "Aysen",
  12: "Magallanes",
  13: "Metropolitana",
  14: "Los Rios",
  15: "Arica y Parinacota",
  16: "Ñuble"

}
gse= {
  '1': 'ABC1',
  '2': 'C2',
  '3': 'C3',
  '4': 'D',
  '5': 'E',
  "abc1":1,
  "c2":2,
  "c3":3,
  "d":4,
  "e":5
}

escolaridad= {
  '0': 'Sin estudios',
  '1': 'Básica incompleta',
  '2': 'Básica completa',
  '3': 'Media incompleta',
  '4': 'Media completa',
  '5': 'Instituto técnico incompleto',
  '6': 'Instituto técnico completo',
  '7': 'Universitaria incompleta',
  '8': 'Universitaria completa',
  '9': 'Postgrado incompleto',
  '10': 'Postgrado completo',
  '88': 'No sabe',
  '99': 'No contesta'
}

escolaridad_eng= {
  '0': 'without studies',
  '1': 'middle school incomplete',
  '2': 'middle school complete',
  '3': 'high school incomplete',
  '4': 'high school complete',
  '5': 'secondary school incomplete',
  '6': 'secondary school complete',
  '7': 'university incomplete',
  '8': 'university complete',
  '9': 'postgraduate degree incomplete',
  '10': 'postgraduate degree complete',
  '88': 'No sabe',
  '99': 'No contesta'
}

religion = {
  '1': 'católica',
  '2': 'evangélica',
  '3': 'testigo de jehová',
  '4': 'judía',
  '5': 'mormona',
  '6': 'musulmana',
  '7': 'ortodoxa',
  '8': ' ninguna de las religiones comunes',
  '9': 'ninguna',
  '10': 'ateo',
  '11': 'agnóstico',
  '88': 'no sabe',
  '99': 'no contesta',
  'católica': 1,
  'evangélica': 2,
  'testigo de jehová': 3,
  'judía': 4,
  'mormona': 5,
  'musulmana': 6,
  'ortodoxa': 7,
  'ninguna de las religiones comunes': 8,
  'ninguna': 9,
  'ateo': 10,
  'agnóstico': 11
}

religion_eng = {
  '1': 'catholic',
  '2': 'evangelic',
  '3': "jehovah's witness",
  '4': 'jude',
  '5': 'mormon',
  '6': 'muslim',
  '7': 'orthodox',
  '8': 'none of the common religions',
  '9': 'none',
  '10': 'atheist',
  '11': 'agnostic',
  '88': "doesn't know",
  '99': "does not answer"
}

izq_der = { #iden_pol_2
  '1': 'extrema izquierda',
  '2': 'izquierda',
  '3': 'izquierda',
  '4': 'izquierda',
  '5': 'centro',
  '6': 'centro',
  '7': 'derecha',
  '8': 'derecha',
  '9': 'derecha',
  '10': 'extrema derecha',
  '88': 'no sabe',
  '99': 'no contesta',
  "extrema izquierda" : 1,
  "izquierda" : 2,
  "centro": 3,
  "derecha" : 4,
  "extrema derecha": 5
}

izq_der_eng = { #iden_pol_2
  '1': 'extreme left',
  '2': 'left',
  '3': 'left',
  '4': 'left',
  '5': 'center-left',
  '6': 'center-right',
  '7': 'right',
  '8': 'right',
  '9': 'right',
  '10': 'extreme right',
  '88': "doesn't know",
  '99': "does not answer"
}
pueblo_eng = { #iden_pol_2
  0: "none",
  1: "Alacalufe",
  2: "Atacameño",
  3: "Aimara",
  4: "Colla" ,
  5: "Mapuche",
  6: "Quechua" ,
  7: "Rapa nui" ,
  8: "Yamana" ,
  9: "Diaguita" ,
  10: "Chango" ,
  11: "other" ,
  12: "none" ,
  88: "none" ,
  888: "doesn't know" ,
  999: "does not answer",
}

pueblo = { #iden_pol_2
  0: "ninguno",
  1: "Alacalufe",
  2: "Atacameño",
  3: "Aimara",
  4: "Colla" ,
  5: "Mapuche",
  6: "Quechua" ,
  7: "Rapa nui" ,
  8: "Yamana" ,
  9: "Diaguita" ,
  10: "Chango" ,
  11: "Otro" ,
  12: "ninguno" ,
  88: "ninguno" ,
  888: "no sabe" ,
  999: "no contesta",
}
party = {
  "1" : "Democracia Cristiana (DC)",
  "2" : "Evolución Política (EVOP)",
  "3" :  "Partido Comunista (PC)",
  "4" : "Partido Humanista (o AHV)",
  "5" : "Partido Por la Democracia (PPD)",
  "6" : "Partido Progresista",
  "7" : "Partido Radical Socialdemócrata (PRS)",
  "8" : "Partido Regionalista Independiente (PRI)",
  "9" : "Partido Socialista (PS)",
  "10" : "Renovación Nacional (RN)",
  "11" : "Revolución Democrática (RD)",
  "12" : "Unión de Centro Progresista",
  "13" : "Unión Demócrata Independiente (UDI)",
  "14" : "Otros",
  "15" : "ninguno",
  "16" : "Convergencia Social (CS)",
  "17" : "Partido de la Gente (PDG)",
  "18" : "Partido Republicano",
  "19" : "Comunes",
  "20" : "Partido Liberal",
  "21" : "Partido Ecologista Verde (PEV)",
  "88" : "no sabe",
  "99" : "no contesta"
}

party_eng = {
  "1" : "Democracia Cristiana (DC)",
  "2" : "Evolución Política (EVOP)",
  "3" :  "Partido Comunista (PC)",
  "4" : "Partido Humanista (o AHV)",
  "5" : "Partido Por la Democracia (PPD)",
  "6" : "Partido Progresista",
  "7" : "Partido Radical Socialdemócrata (PRS)",
  "8" : "Partido Regionalista Independiente (PRI)",
  "9" : "Partido Socialista (PS)",
  "10" : "Renovación Nacional (RN)",
  "11" : "Revolución Democrática (RD)",
  "12" : "Unión de Centro Progresista",
  "13" : "Unión Demócrata Independiente (UDI)",
  "14" : "Others",
  "15" : "None",
  "16" : "Convergencia Social (CS)",
  "17" : "Partido de la Gente (PDG)",
  "18" : "Partido Republicano",
  "19" : "Comunes",
  "20" : "Partido Liberal",
  "21" : "Partido Ecologista Verde (PEV)",
  '88': "doesn't know",
  '99': "does not answer"
}

interes = {
  "1" : "muy interesada",
  "2" : "bastante interesada",
  "3" : "algo interesada",
  "4" : "no muy interesada",
  "5" : "nada interesada",
  "8" : "no sabe (no leer)",
  "9" : "no contesta (no leer)"
}

interes2 = {
  "1" : "muy interesado",
  "2" : "bastante interesado",
  "3" : "algo interesado",
  "4" : "no muy interesado",
  "5" : "nada interesado",
  "8" : "no sabe (no leer)",
  "9" : "no contesta (no leer)"
}

interes_eng = {
  "1" : "very interested",
  "2" : "quite interested",
  "3" : "somewhat interested",
  "4" : "not very interested",
  "5" : "not at all interested",
  "8" : "no sabe (no leer)",
  "9" : "no contesta (no leer)"
}

voto ={
  "Boric" : 1,
  "Kast" : 2,
  "Nulo" : 3,
  "Blanco":3,
  "gabriel boric":1, #Las respuestas del chat varían mucho con respecto al completion, se obligó a que fueran en minuscula
  "gabriel":1,
  "jose antonio kast":2,
  "josé antonio kast":2,
  "jose antonio":2,
  "josé antonio":2,
  "boric" : 1,
  "kast" : 2,
  "nulo" : 3,
  "blanco":3,
  1:"Boric",
  2:"Kast",
  3:"Nulo"
}

voto_eng = {
  1:"Gabriel Boric Font",
  2:"José Antonio Kast Rist",
  3:"Voted null"
}

""" voto_eng = {
  1:"Boric",
  2:"Kast",
  3:"Null"
} """

plebiscito = {
  "apruebo" : 1,
  "rechazo" : 2,
  "nulo": 3,
  "blanco":3,
  1:"Apruebo",
  2:"Rechazo",
  3:"Nulo"
}

plebiscito_eng = {
  1:"Approve",
  2:"Reject",
  3:"Voted null"
}


aborto = {
  "aborto debe estar siempre prohibido." : 1,
  "aborto solo debe estar permitido en casos especiales." : 2,
  "aborto debe estar solo permitido en casos especiales." : 2,
  "aborto debe estar permitido solo en casos especiales." : 2,
  "aborto debe estar permitido en casos especiales.":2,
  "aborto debe solo estar permitido en casos especiales.":2,
  "aborto solo debe solo estar permitido en casos especiales.":2,
  "aborto debe ser una opción para las mujeres en cualquier caso.":3,
  "aborto debe estar siempre permitido":3,
  1: "Aborto debe estar siempre prohibido.",
  2: "Aborto solo debe estar permitido en casos especiales.",
  3: "Aborto debe ser una opción para las mujeres en cualquier caso.",
  "abortion should always be prohibited.": 1,
  "abortion should only be allowed in special cases." : 2,
  "abortion should be an option for women in any case." : 3
}

aborto_eng = {
  1:"Abortion should always be prohibited.",
  2:"Abortion should only be allowed in special cases.",
  3:"Abortion should be an option for women in any case."
}

democracia = {
  "1": "La democracia es preferible a cualquier otra forma de gobierno",
  "2": "En algunas circunstancias, un régimen autoritario puede ser preferible.",
  "3": "A la gente como uno, le da lo mismo un régimen democrático que uno autoritario."
}

aprobacion = {
  "aprueba" : 1,
  "desaprueba" : 2,
  "no aprueba ni desaprueba": 3,
}

percepcion = {
  1: "Pensiones",
  2: "Corrupción",
  3: "Delincuencia, asaltos y robos",
  4: "Derechos humanos",
  5: "Educación",
  6: "Empleo",
  7: "Pobreza",
  8: "Protección del medio ambiente",
  9: "Drogas",
  10: "Salud",
  11: "Sueldos",
  12: "Transporte público",
  13: "Vivienda",
  14: "Inmigración",
  16: "Desigualdad",
  17: "Alzas de precios, inflación",
  26: "Violencia",
  27: "La Constitución"
}

zona = {
  2:"rural",
  1:"urbana"
}

exp_question_dict = {
  "sexo": "¿Cuál es su sexo? Responde SOLO con una de las siguientes opciones, sin palabras extras: hombre o mujer.",
  "region" : "¿En qué región vive?",
  "urbana-rural" : "¿Vive en una zona urbana o rural?",
  "gse" : "¿A qué grupo socioeconómico pertenece? Responde SOLO con una de las siguientes opciones, sin palabras extras: ABC1, C2, C3, D, E.",
  "indígena": "¿Pertenece usted a algún pueblo originario? Sí o no",
  "pueblo originario" : "¿A cuál de los siguientes pueblos originarios o indígenas pertenece ud? Alacalufe, Atacameño, Aimara, Colla, Mapuche, Quechua, Rapa nui, Yamana, Diaguita, Chango, Otro,Ninguno",
  "religion" : "¿Podría Ud. decirme a la religión o iglesia a la que pertenece o se siente más cercano? Responde SOLO con una de las siguientes opciones, sin palabras extras: Católica, Evangélica, Testigo de Jehová, Judía, Mormona, Musulmana, Ortodoxa, Otra religión o credo, Ninguna, Ateo, Agnóstico",
  "izq-der": "Los conceptos de izquierda y derecha son útiles para resumir de una manera muy simplificada lo que piensa la gente en muchos temas. Elija cuál de las siguientes opciones se identifica más. Responde SOLO con una de las siguientes opciones, sin explicaciones ni palabras extras: extrema izquierda, izquierda, centro, derecha, extrema derecha. ",
  "partido": "Ahora, de los siguientes partidos políticos, ¿Con cuál de ellos se identifica más o simpatiza más Ud.?Democracia Cristiana (DC), Evolución Política (EVOP),Partido Comunista (PC), Partido Humanista (o AHV), Partido Por la Democracia (PPD), Partido Progresista, Partido Radical Socialdemócrata (PRS), Partido Regionalista Independiente (PRI), Partido Socialista (PS), Renovación Nacional (RN), Revolución Democrática (RD), Unión de Centro Progresista, Unión Demócrata Independiente (UDI), Otros, Ninguno, Convergencia Social (CS), Partido de la Gente (PDG), Partido Republicano, Comunes, Partido Liberal, Partido Ecologista Verde (PEV)",
  "interes": "¿Cuán interesado está Ud. en la política? ¿Muy interesado, Bastante interesado, Algo interesado, No muy interesado, Nada interesado?",
  "elec_pres": "¿Por quién votó en las elecciones presidenciales del 2021?"
}

exp_columns = {
  1: "elec_pres_144_a",
  2: "constitucion_20_a",
  3: "religion_14"
}

columns_dict_esp = {
  "edad" : "edad",
  "sexo": "sexo",
  "nom_region": "region de residencia",
  "region": "region de residencia",
  "zona_u_r": "tipo de zona",
  "gse": "nivel socioeconómico",
  "esc_nivel_1": "nivel de escolaridad",
  "info_enc_30": "pertenece a un pueblo originario?",
  "info_enc_58": "pueblo originario",
  "religion_82": "religión",
  "iden_pol_2" : "ideología política",
  "iden_pol_3": "partido político"
}

columns_dict_eng = {
  "edad" : "age",
  "sexo": "gender",
  "nom_region": "region of residence",
  "region": "region of residence",
  "zona_u_r": "type of zone",
  "gse": "socioeconomic status",
  "esc_nivel_1": "scholarity level",
  "info_enc_30": "belongs to an indigenous community?",
  "info_enc_58": "indigenous community",
  "religion_82": "religion",
  "iden_pol_2" : "political ideology",
  "iden_pol_3": "political party"
}

def age_group(edad):
  if edad < 30:
    return "Joven"
  elif edad < 40:
    return "Adulto Joven"
  elif edad < 60:
    return "Adulto"
  else:
    return "Adulto Mayor"
  