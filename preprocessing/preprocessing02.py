import json
from pathlib import Path
from collections import defaultdict

'''
After having preprocessed and normalized the contents, this script
preprocesses the structure of the verb json files, shifting from a list
of verbal forms to a structured dictionary with tenses as main keys.

Input format:
    {
        "conjugations": [
            {
                "group": "indicative/present",
                "form": "s1",
                "value": "bailo",
                ...
            },
            ...
        ]
    }

Output format:
    {
        "PresI": {
            "1s": "bailo",
            "2s": "bailas",
            ...
        },
        "Ger": {
            "": "bailando"
        },
        ...
    }

Design notes:
    a) Portuguese tense labels are used as the unified reference system
       for both languages to simplify future cross-language mappings.
    b) Participles receive special handling: first, artificial 
       divisions are supressed; second, some Portuguese verbs present
       two participles for two uses, we unify this setting by capturing
       both uses whether the participles coincide or not.
       
Manually copying categories folder to final dataset.

Working dir: root/preprocessing
'''


dicc_pt = {
    'infinitive/impersonal'     : 'InfI',   # Infinitivo Impessoal
    'infinitive/personal'       : 'InfP',   # Infinitivo Pessoal
    'gerund'                    : 'Ger',    # Gerúndio
    'pastparticiple/masculine'  : 'Partm',  # Particípio Passado
    'pastparticiple/feminine'   : 'Partf',  # Particípio Passado
    'pastparticipleshort/masculine' : 'Partirrm', # Particípio Passado
    'pastparticipleshort/feminine'  : 'Partirrf', # Particípio Passado
    'pastparticiplelong/masculine'  : 'Partregm', # Particípio Passado
    'pastparticiplelong/feminine'   : 'Partregf', # Particípio Passado
    'indicative/present'        : 'PresI',  # Presente do Indicativo
    'indicative/imperfect'      : 'PImpI',  # Pret. Imperfeito do Indicativo
    'indicative/preterite'      : 'PPSI',   # Pret. Perfeito Simples do Ind.
    'indicative/pluperfect'     : 'PMQPSI', # Pret. Mais Que Perf. Simples Ind.
    'indicative/future'         : 'FutSI',  # Futuro de Presente Simples Ind.
    'conditional'               : 'CondS',  # Condicional Simples
                                            # Futuro do Pretérito Simp. do Ind.
    'subjunctive/present'       : 'PresC',  # Presente de Conjuntivo
    'subjunctive/imperfect'     : 'PImpC',  # Pret. Imperfeito do Conjuntivo
    'subjunctive/preterite'     : 'FutSC',  # Futuro Simples Conj.
    'imperative/affirmative'    : 'ImpA',   # Imperativo Afirmativo
    'imperative/negative'       : 'ImpN',   # Imperativo Negativo
}

dicc_es = {
    'infinitive'                : 'InfI',   # Infinitivo Impessoal
    'gerund'                    : 'Ger',    # Gerúndio
    'pastparticiple/singular'   : 'Parts',  # Particípio Passado
    'pastparticiple/plural'     : 'Partp',  # Particípio Passado
    'indicative/present'        : 'PresI',  # Presente do Indicativo
    'indicative/imperfect'      : 'PImpI',  # Pret. Imperfeito do Indicativo
    'indicative/preterite'      : 'PPSI',   # Pret. Perfeito Simples do Ind.
    'subjunctive/imperfect_ra'  : 'PMQPSI', # Pret. Mais Que Perf. Simples Ind.
    'indicative/future'         : 'FutSI',  # Futuro de Presente Simples Ind.
    'indicative/conditional'    : 'CondS',  # Condicional Simples
                                            # Futuro do Pretérito Simp. do Ind.
    'subjunctive/present'       : 'PresC',  # Presente de Conjuntivo
    'subjunctive/imperfect_se'  : 'PImpC',  # Pret. Imperfeito do Conjuntivo
    'subjunctive/future'        : 'FutSC',  # Futuro Simples Conj.
    'imperative/affirmative'    : 'ImpA',   # Imperativo Afirmativo
    'imperative/negative'       : 'ImpN',   # Imperativo Negativo
}

base_path_in = Path('../json_01/portuguese')
base_path_out = Path('../verbs/portuguese')
content_path_in = base_path_in / 'content'
content_path_out = base_path_out / 'content'
content_path_out.mkdir(parents=True, exist_ok=True)

for file in content_path_in.rglob('*'):
    if file.is_file():  
        with open(file, 'r', encoding='utf-8') as f_in:
            data = json.load(f_in)
    else:
        continue
    conj = data['conjugations']
    verb = defaultdict(dict)
    
    for v_form in conj:
        verb[dicc_pt[v_form['group']]][v_form['form']]=v_form['value']
    
    if 'Partm' in verb:
        verb['Part-ter'][''] = verb['Partm']['s']
        for num in ['s', 'p']:
            for gen in ['m', 'f']:
                verb['Part-ser'][gen + num] = verb['Part' + gen][num]
        for gen in ['m', 'f']:
            del verb['Part' + gen]
    else:
        verb['Part-ter'][''] = verb['Partregm']['s']
        for num in ['s', 'p']:
            for gen in ['m', 'f']:
                verb['Part-ser'][gen + num] = verb['Partirr' + gen][num]
        for option in ['reg','irr']:
            for gen in ['m', 'f']:
                del verb['Part' + option + gen]
        
    rel_path = file.relative_to(content_path_in)
    file_out = content_path_out / rel_path
    file_out.parent.mkdir(parents=True, exist_ok=True)
    with open(file_out, 'w', encoding='utf-8') as f_out:
        json.dump(verb, f_out, indent=2, ensure_ascii=False)


base_path_in = Path('../json_01/spanish')
base_path_out = Path('../verbs/spanish')
content_path_in = base_path_in / 'content'
content_path_out = base_path_out / 'content'
content_path_out.mkdir(parents=True, exist_ok=True)

for file in content_path_in.rglob('*'):
    if file.is_file():  
        with open(file, 'r', encoding='utf-8') as f_in:
            data = json.load(f_in)
    else:
        continue
    conj = data['conjugations']
    verb = defaultdict(dict)
    
    for v_form in conj:
        verb[dicc_es[v_form['group']]][v_form['form']]=v_form['value']
    
    verb['Part-ter'][''] = verb['Parts']['masculine']
    for num in ['s', 'p']:
        for gen in ['masculine', 'feminine']:
            verb['Part-ser'][gen[0] + num] = verb['Part' + num][gen]
        del verb['Part' + num]
    
    rel_path = file.relative_to(content_path_in)
    file_out = content_path_out / rel_path
    file_out.parent.mkdir(parents=True, exist_ok=True)
    with open(file_out, 'w', encoding='utf-8') as f_out:
        json.dump(verb, f_out, indent=2, ensure_ascii=False)
