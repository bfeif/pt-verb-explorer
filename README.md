# pt-verb-table-builder

Python code that scrapes and builds a table of verb conjugations and boolean verb irregularities for the Portuguese language.
An example of the exploration and analyses that can be done using this code can be found in the [demo ipython notebook about the L-shaped morphome](https://github.com/bfeif/pt-verb-table-builder/blob/master/Demo%2C%20L-shaped%20Morphome.ipynb).

## Overview

I have pre-built verb tables for both conjugations and boolean-irregularities, for the 50 highest frequency verbs in Portuguese. You can download them [here as a two sheet spreadhsheet on google drive](https://docs.google.com/spreadsheets/d/1tv1fjhV5BaeYCNVyje6sY5dxAxSMv_vy0ECVbx0eQN8/edit?usp=sharing) or as two csvs [of conjugations](https://drive.google.com/file/d/1gPWyk7b5PfkpZZesBADqrBqQTq3V0Q33/view?usp=sharing) and [of irregularities](https://drive.google.com/file/d/1Jkb61deb6Ov7qmZO-KpY9v5zIxqx_qP0/view?usp=sharing).
If you'd like to run the python code to generate the tables on your own system, proceed to **Getting Started**.

## Getting Started

These instructions will get you the project up and running on your local machine. At the moment, this project only supports Linux and Mac machines.

### Prerequisites

This project is created with Python, and uses Miniconda as a package manager. As part of the Miniconda install, Python is installed. As such, the only prerequisite is Miniconda.
- [Miniconda Installation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)

### Getting Set Up

Once the Miniconda installation is complete and this repository is cloned to your local machine, open up a terminal process, navigate to the cloned `pt-verb-table-builder` directory and run the following commands:
1. `conda env create -f environment.yml `
2. `conda activate pt-verb-table-builder `
3. ```conda env config vars set VERB_TABLE_BUILDER_HOME=`pwd` ```
4. `conda activate pt-verb-table-builder ` (yes, this has to be run twice :o)

### Creating the Verb Tables

In the `pt-verb-table-builder` directory and with the conda environment `pt-verb-table-builder` activated, execute the following command:
1. `python run.py`

The resulting verb tables will be stored as csvs in `pt-verb-table-builder/data/verb-tables/`.
If you'd like to build the verb tables using more verbs than the default top 50 verbs, then more verbs can be added to the list at `pt-verb-table-builder/data/verb-list/50_top_verbs.json`.

## Using the Verb Tables

Check out the ipython notebook [demo about the L-shaped morphome](https://github.com/bfeif/pt-verb-table-builder/blob/master/Demo%2C%20L-shaped%20Morphome.ipynb) in order to get comfortable with using the verb tables.

## Acknowledgments

* This code scrapes data from the Portuguese verb conjugation website [Conjugação do Verbos](https://www.conjugacao.com.br/).