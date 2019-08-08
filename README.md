# Wikidata Parser
- [Wikidata Parser](#wikidata-parser)
  - [Description](#description)
  - [Usage](#usage)
    - [Install required packages](#install-required-packages)
    - [Select target language pair](#select-target-language-pair)
    - [Run parser](#run-parser)
    - [Result](#result)
  - [Filters](#filters)

## Description
**Wikidata parser** extracts labels(document name) from [Wikidata dump](https://www.wikidata.org/wiki/Wikidata:Database_download) in given language pairs.

Wikidata dump is a single huge [ndjson](http://ndjson.org/) file. Each line is an json object describing an entity.

Project structure is as shown below.

```
Wikidata_Parser
├── filters
│   ├── en_pair.json
│   ├── namespaces.json
│   ├── remove_regex.json
│   ├── skip_regex.json
│   ├── target_pairs.json
│   ├── templates.json
│   └── typos.json
├── README.md
├── run_parse_wiki.py
└── wikidata.py
```

## Usage

### Install required packages

```bash
pip3 install -r requirements.txt
```

### Select target language pair

```bash
./filters/target_pairs.json
[
    ["ko", "en"],
    ["ko", "zh"],
    ["ko", "ja"],
    ["ko", "vi"],
    ["ko", "es"],
    ["ko", "fr"],
    ["ko", "de"],
    ["ko", "it"],
    ["ko", "ru"],
    ["ko", "pt"],
    ["ko", "pl"],
    ["ko", "nl"],
    ["ko", "ar"],
    ["ko", "hi"],
    ["ko", "yue"]
]
```

### Run parser

```bash
python3 run_parse_wiki.py WIKIDATA_DUMP_DIR(latest-all.json.bz2)
```

`run_parse_wiki.py` extracts the bz2 file and parses each line in parallel for each language pair. Extracting bz2 file seems to be a bottleneck. If you have enough space on your disk (about 800GB), you may want to extract it using `pbzip2` before parsing.

### Result

```bash
./corpus
├── ko-ar
│   ├── corpus.ar
│   └── corpus.ko
├── ko-de
│   ├── corpus.de
│   └── corpus.ko
├── ko-en
│   ├── corpus.en
│   └── corpus.ko
├── ko-es
│   ├── corpus.es
│   └── corpus.ko
├── ko-fr
│   ├── corpus.fr
│   └── corpus.ko
├── ko-hi
│   ├── corpus.hi
│   └── corpus.ko
├── ko-it
│   ├── corpus.it
│   └── corpus.ko
├── ko-ja
│   ├── corpus.ja
│   └── corpus.ko
├── ko-nl
│   ├── corpus.ko
│   └── corpus.nl
├── ko-pl
│   ├── corpus.ko
│   └── corpus.pl
├── ko-pt
│   ├── corpus.ko
│   └── corpus.pt
├── ko-ru
│   ├── corpus.ko
│   └── corpus.ru
├── ko-vi
│   ├── corpus.ko
│   └── corpus.vi
├── ko-yue
│   ├── corpus.ko
│   └── corpus.yue
└── ko-zh
    ├── corpus.ko
    └── corpus.zh

```

## Filters

```bash
./filters
├── namespaces.json
├── remove_regex.json
├── skip_regex.json
├── target_pairs.json
├── templates.json
└── typos.json
```

When you found error from corpora, you can update those filters and run filtering again. You can find each filter in `wikidata.py` module.
Your contributions are always welcome!
