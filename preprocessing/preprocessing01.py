import json
from pathlib import Path
from collections import defaultdict

'''
This script preprocesses the json verb files in order to suit our
needs:
    a) filters out verb json files with no conjugation at them (to
       a different filtered_content folder) and updates the categories
       lists (new filtered one and updated content one)
    b) sets '' as form type for invariant personal infinitive and
       gerund, to have a more uniform data set,    
    c) reorders the literals 's1' (singular first), 's2, etc. to
       '1s', etc.,
    d) sets as defective forms including "Normally defective" for
       Portuguese verbs (not such literal in Spanish data set),
    e) sets '' instead of '-' as value for defective forms for
       Portuguese verbs (Spanish ones already have ''),
    f) chooses the accentuated variant of Indicative Preterite,
       corresponding to the European Portuguese norm, for the verbs
       from the 1st conjugation,
    g) stores some lists for future analysis or use: defective verbs,
       defective forms, variant forms (beyond participles),
    h) chosses the 'tú' variant over the voseo variant for Spanish
       conjugations, due mainly to scope,
    i) adding não to imperative negative for Portuguese verbs (Spanish
       verbs already have 'no' for this tense),
    j) selecting non obsolete form when 'Obsolete:' is present
    h) a few exceptions (Portuguese case) also in the script.

Former list comprising exceptions for d), with just one variant, only
led to defective or irregular forms.

Working dir: root/preprocessing
'''

base_path_in = Path('../json/portuguese')
base_path_out = Path('../json_01/portuguese')
content_path_in = base_path_in / 'content'
content_path_out = base_path_out / 'content'
content_path_out.mkdir(parents=True, exist_ok=True)
filteredcontent_path_out = base_path_out / 'filtered_content'
filteredcontent_path_out.mkdir(parents=True, exist_ok=True)

filtered_pt = defaultdict(list)
defective_forms_pt = []
defective_verbs_pt = set()
variant_forms_pt = []
exceps_var = {
    'demos - dêmos' : 'demos',
    'desdemos - desdêmos' : 'desdemos',
    'estamos - estámos' : 'estamos',
    'havemos - hemos' : 'havemos',
    'vamos - imos' : 'vamos'
}

for file in content_path_in.rglob('*'):
    if file.is_file():
        
        rel_path = file.relative_to(content_path_in)
        file_out = content_path_out / rel_path
        filteredfile_out = filteredcontent_path_out / rel_path
        
        with open(file, 'r', encoding='utf-8') as f_in:
            data = json.load(f_in)
            
        if data.get('conjugations') is None:
            filtered_pt[file.stem[0]].append(file.stem)
            filteredfile_out.parent.mkdir(parents=True, exist_ok=True)
            with open(filteredfile_out, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=2, ensure_ascii=False)
        else:
            for v_form in data['conjugations']:
                
                if v_form.get('form', None) is None:
                    v_form['form'] = ''
                
                if v_form['form'] in ['s1', 's2', 's3', 'p1', 'p2', 'p3']:
                    v_form['form'] = v_form['form'][::-1]
                    
                if '-Normally defective' in v_form['value']:
                    v_form['value'] = ''
                    defective_verbs_pt.add(file.stem)
                    defective_forms_pt.append([file.stem, v_form['group'],
                                               v_form['form']])
                
                if (file.stem.endswith('ar') and 
                    v_form['group'] == 'indicative/preterite' and
                    v_form['form'] == '1p'):
                    if '-' in v_form['value']:
                        parts = v_form['value'].split('-')
                        for part in parts:
                            if 'á' in part:
                                v_form['value'] = part.strip()
                                break
                
                if '-' in v_form['value']:
                    if v_form['value'] == '-':
                        v_form['value'] = ''
                        if (v_form['group'] in ['imperative/affirmative',
                                                'imperative/negative']
                            and v_form['form'] == '1s'):
                            pass
                        else:
                            defective_verbs_pt.add(file.stem)
                            defective_forms_pt.append([file.stem, v_form['group'],
                                                       v_form['form']
                                                       ])
                    else:
                        variant_forms_pt.append([file.stem, v_form['group'],
                                                  v_form['form'], v_form['value']
                                                  ])
                        if v_form['value'] in exceps_var:
                            v_form['value'] = exceps_var[v_form['value']]
                
                if 'Obsolete:' in v_form['value']:
                    v_form['value'] = v_form['value'].split('Obsolete:')[0]
                
                if (v_form['group'] == 'imperative/negative' and
                    v_form['value'] != ''):
                    v_form['value'] = 'não ' + v_form['value']
                    
                                                  
            file_out.parent.mkdir(parents=True, exist_ok=True)
            with open(file_out, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=2, ensure_ascii=False)
            
lists_path_out = Path('lists')
lists_path_out.mkdir(parents=True, exist_ok=True)

path_out = lists_path_out / 'defective_forms_pt.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(defective_forms_pt, f_out, indent=2, ensure_ascii=False)

defective_verbs_pt = sorted([verb for verb in defective_verbs_pt])
path_out = lists_path_out / 'defective_verbs_pt.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(defective_verbs_pt, f_out, indent=2, ensure_ascii=False)

path_out = lists_path_out / 'variant_forms_pt.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(variant_forms_pt, f_out, indent=2, ensure_ascii=False)

for key in filtered_pt.keys():
    path_in = base_path_in / 'categories' / f'{key}.json'
    path_out = base_path_out / 'categories' / f'{key}.json'
    path_out.parent.mkdir(parents=True, exist_ok=True)
    filtered_path_out = base_path_out / 'filtered_categories' / f'{key}.json'
    filtered_path_out.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path_in, 'r', encoding='utf-8') as f_in:
        data = json.load(f_in)
    
    for verb in filtered_pt[key]:
        data.remove(verb)
    
    with open(path_out, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, indent=2, ensure_ascii=False)
    
    with open(filtered_path_out, 'w', encoding='utf-8') as f_out:
        json.dump(sorted(filtered_pt[key]), f_out, indent=2, 
                  ensure_ascii=False)


base_path_in = Path('../json/spanish')
base_path_out = Path('../json_01/spanish')
content_path_in = base_path_in / 'content'
content_path_out = base_path_out / 'content'
content_path_out.mkdir(parents=True, exist_ok=True)
filteredcontent_path_out = base_path_out / 'filtered_content'
filteredcontent_path_out.mkdir(parents=True, exist_ok=True)

filtered_es = defaultdict(list)
defective_forms_es = []
defective_verbs_es = set()
variant_forms_es = []

for file in content_path_in.rglob('*'):
    if file.is_file():
        
        rel_path = file.relative_to(content_path_in)
        file_out = content_path_out / rel_path
        filteredfile_out = filteredcontent_path_out / rel_path
        
        with open(file, 'r', encoding='utf-8') as f_in:
            data = json.load(f_in)
            
        if data.get('conjugations') is None:
            filtered_es[file.stem[0]].append(file.stem)
            filteredfile_out.parent.mkdir(parents=True, exist_ok=True)
            with open(filteredfile_out, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=2, ensure_ascii=False)
        else:
            for v_form in data['conjugations']:
                
                if v_form.get('form', None) is None:
                    v_form['form'] = ''
                
                if v_form['form'] in ['s1', 's2', 's3', 'p1', 'p2', 'p3']:
                    v_form['form'] = v_form['form'][::-1]
                    
                if '(tú)' in v_form['value']:
                    v_form['value'] = v_form['value'].split('(tú)')[0].strip()
                                    
                if '' == v_form['value']:
                    if (v_form['group'] in ['imperative/affirmative',
                                            'imperative/negative']
                        and v_form['form'] == '1s'):
                        pass
                    else:
                        defective_verbs_es.add(file.stem)
                        defective_forms_es.append([file.stem, v_form['group'],
                                                   v_form['form']
                                                   ])
                                                  
            file_out.parent.mkdir(parents=True, exist_ok=True)
            with open(file_out, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=2, ensure_ascii=False)
            
lists_path_out = Path('lists')
lists_path_out.mkdir(parents=True, exist_ok=True)

path_out = lists_path_out / 'defective_forms_es.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(defective_forms_es, f_out, indent=2, ensure_ascii=False)

defective_verbs_es = sorted([verb for verb in defective_verbs_es])
path_out = lists_path_out / 'defective_verbs_es.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(defective_verbs_es, f_out, indent=2, ensure_ascii=False)

path_out = lists_path_out / 'variant_forms_es.json'
with open(path_out, 'w', encoding='utf-8') as f_out:
    json.dump(variant_forms_es, f_out, indent=2, ensure_ascii=False)

for key in filtered_es.keys():
    path_in = base_path_in / 'categories' / f'{key}.json'
    path_out = base_path_out / 'categories' / f'{key}.json'
    path_out.parent.mkdir(parents=True, exist_ok=True)
    filtered_path_out = base_path_out / 'filtered_categories' / f'{key}.json'
    filtered_path_out.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path_in, 'r', encoding='utf-8') as f_in:
        data = json.load(f_in)
    
    for verb in filtered_es[key]:
        data.remove(verb)
    
    with open(path_out, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, indent=2, ensure_ascii=False)
    
    with open(filtered_path_out, 'w', encoding='utf-8') as f_out:
        json.dump(sorted(filtered_es[key]), f_out, indent=2, 
                  ensure_ascii=False)