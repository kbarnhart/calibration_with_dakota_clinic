# Calibration with Dakota

[![Build Status](https://travis-ci.com/kbarnhart/calibration_with_dakota_clinic.svg?branch=master)](https://travis-ci.com/kbarnhart/calibration_with_dakota_clinic)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kbarnhart/calibration_with_dakota_clinic/master?filepath=Clinic_Notes_and_Tutorial.ipynb)

# Under development

## About

This repository contains resources used in a clinic on using [Dakota](https://dakota.sandia.gov) for calibration taught by @kbarnhart. If you have any questions, comments, or problems, please [make an issue](https://github.com/kbarnhart/calibration_with_dakota_clinic/issues).

## Options for running the examples.

1) Use [Binder](https://mybinder.org/v2/gh/kbarnhart/calibration_with_dakota_clinic/master?filepath=Clinic_Notes_and_Tutorial.ipynb).
2) Use [Hydroshare](https://doi.org/10.4211/hs.c287d48b50064acd86b82ddc4346f810). 
3) Install the repo and Dakota yourself.

## Install instructions

Make sure you had [git](https://git-scm.com) and the [Anaconda python distribution](https://www.anaconda.com/distribution/) (recommended version 3.6 or above).

### Step 1: Get Dakota and this repository

#### Option A: Full env with conda.

This option is only available on Linux and on MacOSX. **It will not work on Windows.**

(1) Open a terminal and navigate to a folder where you want this folder copied.

Then execute the following commands to download the repository, create the specified conda environment, and build/test the `heat` module. Note that you'll have to replace `YOUR_OS_HERE` with either `osx` or `linux`.

```bash
$ git clone https://github.com/kbarnhart/calibration_with_dakota_clinic.git
$ cd calibration_with_dakota_clinic
$ conda env create -f environment_YOUR_OS_HERE.yml
$ conda activate dakota_clinic
$ make install
```

If you've never made an environment with conda before, you might need to use `source` instead of `conda` in the last command. If that command fails, conda will give you an error message that is reasonably helpful. Basically, it will instruct you to run

```bash
$ conda init <NAME OF SHELL>
```
which will make the the `conda activate dakota_clinic` command will work.

If you want to test your install, type
```bash
pytest
```
This may take ~15 minutes (you are running all of the experiments we will do in the clinic and testing that they work).

#### Option B: Dakota Binary + conda env

Step 1: [Install the Dakota binary for Windows](https://dakota.sandia.gov/download.html) and make a [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments) based on the file `environment_everything_but_dakota.yml`.

After downloading/installing the Dakota binary, open a terminal and do the following:
```bash
$ git clone https://github.com/kbarnhart/calibration_with_dakota_clinic.git
$ conda env create -f environment_everything_but_dakota.yml
$ conda activate dakota_clinic
$ make install
```

### Step 2: Open a notebook.

Assuming that the results of `pytest` don't include any failures, open Jupyter Notebooks.

```bash
$ jupyter notebook
```

Click `Clinic_Notes_and_Tutorial.ipynb`.
