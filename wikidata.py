import os
import json
import re

with open('./filters/namespaces.json', 'r') as f:
    namespaces = json.load(f)
with open('./filters/typos.json', 'r') as f:
    typos = json.load(f)
with open('./filters/remove_regex.json', 'r') as f:
    remove_regexes = json.load(f)
with open('./filters/skip_regex.json', 'r') as f:
    skip_regexes = json.load(f)
with open('./filters/templates.json', 'r') as f:
    templates = json.load(f)

def correct_typo(label, lang):
    if lang in typos:
        if label in typos[lang]:
            print("typo found: {}".format(label))
            return typos[lang][label]

    return label

def remove_namespace(label, lang):
    # Check english namespace as default.
    ns = list(namespaces['en'])

    # Concat language specific label.
    if lang != 'en' and lang in namespaces:
        ns += namespaces[lang]

    if label.split(':')[0] in ns:
        try:
            ns, label = label.split(':', 1)
        except:
            pass

    return label.strip()
    
def remove_regex(label, lang):
    if lang in remove_regexes:
        for regex in remove_regexes[lang]:
            label = re.sub(regex, '', label)

    return label.strip()

def remove_doubleparentheses(label):
    label = re.sub(r"\(\(([^()]*)\)\)", r"\1", label)    

    return label.strip()

def remove_parenthesis_area(label):
    inner_parentheses = re.compile(r' ?\([^()]+\)')
    while inner_parentheses.search(label):
        label =re.sub(r" ?\([^()]+\)", "", label)

    return label.strip()

def skip_regex(label, lang):
    if lang in skip_regexes:
        for regex in skip_regexes[lang]:
            if re.match(regex, label):
                return True

    return False

def parse(lang_pair, q):
    # Make directory if not exist
    lang_pair_dir = './corpus/'+'-'.join(lang_pair)
    if not os.path.exists(lang_pair_dir):
        os.makedirs(lang_pair_dir)
        print("make dir: {}".format(lang_pair_dir))

    corpus = [ open(lang_pair_dir+'/corpus.'+lang, 'w') for lang in lang_pair ]

    while True:
        line = q.get()
        try:
            labels = json.loads(line)['labels']
        except:
            if line == '[':
                # print("first line: {}".format(line))
                continue
            else:
                print("Not a valid json object: {}".format(line))
                break


        if not all(lang in labels for lang in lang_pair):
            continue

        label_pair = [ labels[lang]['value'] for lang in lang_pair ]
        label_pair = [ correct_typo(label, lang) for label, lang in zip(label_pair, lang_pair) ]
        label_pair = [ remove_namespace(label, lang) for label, lang in zip(label_pair, lang_pair) ]
        label_pair = [ remove_regex(label, lang) for label, lang in zip(label_pair, lang_pair) ]
        label_pair = [ remove_doubleparentheses(label) for label in label_pair ]
        label_pair = [ remove_parenthesis_area(label) for label in label_pair ]

        skip = [ skip_regex(label, lang) for label, lang in zip(label_pair, lang_pair) ]

        if True in skip:
            continue

        if label_pair[0] == label_pair[1]:
            continue

        for c, l in zip(corpus, label_pair):
            c.write(l+'\n') 

    for c in corpus:
        c.close() 
