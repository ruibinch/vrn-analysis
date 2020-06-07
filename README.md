# SG VRN analysis

Singapore has a phenomenon where the licence plate of a car is not treated as just another number - instead, they are coveted items that are actively bidded for and transacted, sometimes for obscenely high prices.

There are some especially prized number plates - these are typically 1- or 2-digit numbers due to their rarity or repeating digits of the same number, e.g. 777, 888, 999, 8888.

This set me thinking - **which number is the most desirable/valuable**?

In this project, I collect a list of car models possessing selected number plates and subsequently attempt to explore which plate number has the highest value and whether there is a strong correlation between value and desirability.

## Components

This project comprises of 2 components:

### ETL pipeline

**PySpark** is used for the ETL pipeline.

**Google Sheets** is used for both the data source and destination, with interactions being made through the Google Sheets API.

A detailed writeup of the pipeline can be found in the "ETL pipeline" notebook in the `/notebooks` folder and is directly accessible [here](https://nbviewer.jupyter.org/github/ruibinch/vrn-analysis/blob/master/notebooks/ETL%20pipeline.ipynb).

### Data analysis

A **Jupyter notebook** is used to perform the data analysis, with the aid of the standard suite of tools - **pandas** for data manipulation and **seaborn** for data visualisation.

The data is analysed based on the following series of questions:

- Which plate number has the highest value?
- What is the distribution of car prices for each plate number?
- Which letter series has the highest value?
- Which are the most expensive car models?
- Which are the most expensive car brands?
- What is the distribution of car prices for each brand?
- Which are the most popular car brands?
- Which are the most popular car models?

This analysis can be found in the "SG VRN analysis" notebook in the `/notebooks` folder and is directly accessible [here](https://nbviewer.jupyter.org/github/ruibinch/vrn-analysis/blob/master/notebooks/SG%20VRN%20analysis.ipynb).

## Folder Structure

The folder structure is based on the [PySpark Example Project](https://github.com/AlexIoannides/pyspark-example-project) repository.

| Folder | Purpose |
| --- | --- |
| `configs` | Configuration files/variables |
| `helpers` | Helpers for the ETL pipeline |
| `jobs` | Details of the ETL job; each phase is seperated into its own file |
| `notebooks` | Jupyter notebooks for understanding |
| `scripts` | General scripts for purposes outside of the ETL pipeline |
| `tests` | Test cases for the pipeline |
| `utils` | Utility files used in the pipeline or for data analysis |
