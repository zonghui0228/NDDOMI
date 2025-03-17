# NDDOMI
a digital platform for outcome measurement instrument selection and utilization in neurodegenerative disease research


# Introduction

The selection of appropriate outcome measurement instruments (OMIs) in neurodegenerative diseases (NDDs) researches remains complex and often inconsistent. This study aims to consolidate knowledge on OMIs applied in NDD over the last two decades and to develop NDDOMI, a web-based knowledge platform for OMIs selection.

We collected clinical trials from the past two decades across six prevalent NDDs from ClinicalTrials.gov. OMIs were manually extracted, categorized, and normalized by experts. We analyzed OMI utilization patterns, corss-disease applicability, and temporal trends. Additionally, we developed NDDOMI, a knowledge resource platform, using Django, ECharts, and JavaScript. The usability of NDDOMI was assessed using the System Usability Scale (SUS) and Net Promoter Score (NPS), with evaluations from 18 clinicians and researchers

The NDDOMI platform provides an interface covering 4619 clinical trials and 2494 OMIs. On average, 4.4 instruments were utilized per trial. 15 instruments are shared across six NDDs. 76.75% of the trials employed more than one instruments, often in combination. A positive correlation was observed between the number of trials and the diversity of OMIs employed. The top 10 frequently employed instruments for each disease were identified, and their utilization has increased over time. The usability assessment demonstrated excellent user satisfaction with an average SUS score of 88.19.

# Data download

## config file
config file is a yaml file named with MESH ID. The content contains `name`, `mesh_id`, `entry_terms`. All the information can be obtained from MESH offical website.

folder: `./conf/`

take `Parkinson Disease` as an example, the config file looks like:

```yaml
name: Parkinson Disease
mesh_id: D010300
entry_terms:
  - Idiopathic Parkinson's Disease
  - Lewy Body Parkinson's Disease
  - Parkinson's Disease, Idiopathic
  - Parkinson's Disease, Lewy Body
  - Parkinson Disease, Idiopathic
  - Parkinson's Disease
  - Idiopathic Parkinson Disease
  - Lewy Body Parkinson Disease
  - Primary Parkinsonism
  - Parkinsonism, Primary
  - Paralysis Agitans
```

## download clinical trials

automatic download clinical trial registration files by run

```python
python download_clinicaltrial_file.py -mesh=D010300
```

## extract registration information
extract registration information by run

```python
python extract_clinicaltrial_data.py -mesh=D010300
```

## OMI annotation

To determine whether a trial applied any instruments, we manually annotated instrument entities within the description text of outcome measurements. The instruments annotation was performed using brat, a widely used web-based and user-friendly tool for text annotation in natural language processing research. Two annotators, the one is neurology clinician and the other is neuroscience researcher, collaborated to annotate the data.

Initially, they surveyed the definitions and literatures of the OMIs, and reviewed various expressions within clinical trials text. Then, the data was divided into two parts and labeled separately. Finally, they cross-checked each other's annotations to ensure consistency, and discussed contradictions until consensus was achieved. Based on the annotation results, we removed trials that did not applied any instruments in the outcome measurements. For instance, some outcome descriptions, such as “status of progression – changes in language processing” indicated the intention to measure language ability but did not reference any related assessment tools. Therefore, these trials were not included in our analysis.


## OMI Normalization

Generally, an instrument comprises of multiple subscales, and maybe has various versions. To address this issue, we proposed a two-level instrument name normalization pipeline aimed at transforming original instrument expressions in the text into their corresponding normalized full names. Frist, we accounted for variability in writing styles, including punctuation marks, singular and plural numbers, among others, and we standardized various instruments expressions to formal expressions. Second, we considered the diversity of versions and modules, and standardized the formal expressions to higher level instrument. For example, the terms “Alzheimer’s Disease Assessment Scale – Cognitive Subscale” and “ADAS-cog” are different expressions, but actually refer to same instrument “Alzheimer’s Disease Assessment Scale - Cognitive Subscale”. We defined it as a level 2 instrument and further mapped to the level 1 instrument “Alzheimer’s Disease Assessment Scale”. Similarly, “Neuropsychiatric Inventory-Questionnaire” and “NPI-Q” are both normalized as instrument “Neuropsychiatric Inventory”.


