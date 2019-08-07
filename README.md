# Wikipedia Document Label Pairs

## Original Data Source
Wikidata json dump, 2019.07 

## Description
These pairs are labels of documents from `Wikipedia dump`.

## Data
This repository contains 15 pairs of Wikipedia document labels.
```
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
Each directory under corpus has a pair of headword and `*.same` file contains headwords that are exactly same in both side.
Size of each corpus are as shown below.
```
  407480 corpus/ko-fr/
  323223 corpus/ko-nl/
  382006 corpus/ko-zh/
  594268 corpus/ko-en/
  341473 corpus/ko-ar/
  344804 corpus/ko-de/
   58947 corpus/ko-yue/
  374379 corpus/ko-es/
  323916 corpus/ko-it/
  248175 corpus/ko-pl/
  408519 corpus/ko-ja/
  306574 corpus/ko-pt/
   60357 corpus/ko-hi/
  196992 corpus/ko-vi/
  362166 corpus/ko-ru/
```
## Jupyter Notebook
You can refer to the jupyter notebook to look into data processing procedures.

## Postprocess
* Heading namespaces (e.g. Category: , Help: ) are removed.
* Parenthesis areas are removed. 
* Redundant suffixes depend on language are removed. (e.g. /설명문서)
* Removed parentheses recursively.
* Removed Wikipedia symbols.
* Manually corrected typos in original data.

If you have new things to remove, you can edit files in `./filters` and re-run post-processing script in the Jupyter Notebook.
