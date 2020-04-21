<div class="clearfix" style="padding: 0px; padding-left: 100px; display: flex; flex-wrap: nowrap; justify-content: space-evenly; align-items:center">
<a href="http://bimcv.cipf.es/"><img src="https://github.com/BIMCV-CSUSP/DiSMed/blob/master/images/logoinst.png?raw=true"</a><a href="http://ceib.san.gva.es"></a><a href="https://deephealth-project.eu/"><img src="https://github.com/BIMCV-CSUSP/DiSMed/blob/master/images/DEEPHEALTH.png" width="200px" class="center-block" style=" display: inline-block;"></a></div>
<br></br>

# DiSMed - De-identifying Spanish Medical texts

## scripts

This folder contains python code used in DiSMed. The following pipeline was implemented:

* First, radiology reports were pre-annotated with [pre_annotator.py](https://github.com/BIMCV-CSUSP/DiSMed/blob/master/scripts/pre_annotator.py). The pre-annotated output files need to be manually corrected and tags other than "NAME" and "INST" have to be incorporated.
* The manually annotated files were then randomized with [synthetic_dataset.py](https://github.com/BIMCV-CSUSP/DiSMed/blob/master/scripts/synthetic_dataset.py). This step can be skipped if you don't need to train your models with synthetic data.
* Spacy **needs to be added**
* Then, to train with [Gillaume Genthial's](https://github.com/guillaumegenthial/tf_ner) networks, the annotation was converted into IOBES tagging scheme with [iobes_tagging.py](https://github.com/BIMCV-CSUSP/DiSMed/blob/master/scripts/iobes_tagging.py).
* In case a IOBES tagged file needs to be converted into an html-like tagging scheme, [iobes_to_html.py](https://github.com/BIMCV-CSUSP/DiSMed/blob/master/scripts/iobes_to_html.py) is available.

