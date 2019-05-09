# Calibration with Dakota

[![Build Status](https://travis-ci.com/kbarnhart/calibration_with_dakota_clinic.svg?branch=master)](https://travis-ci.com/kbarnhart/calibration_with_dakota_clinic)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kbarnhart/calibration_with_dakota_clinic.git/master)

# Under development

## About

This repository contains resources used in a clinic on using [Dakota]() for calibration taught by @kbarnhart. If you have any questions, comments, or problems, please [make an issue]().

## Options for running the examples.

1) Use [this Binder link](https://mybinder.org/v2/gh/kbarnhart/calibration_with_dakota_clinic.git/master).
2) Use [Hydroshare]().
3) Install the repo and Dakota yourself.

## Install instructions

Make sure you had [git](https://git-scm.com) and the [Anaconda python distribution](https://www.anaconda.com/distribution/) (recommended version 3.6 or above).

### Step 1: Get Dakota and this repository

#### Option A: Full env with conda.

This option is only available on Linux and on MacOSX. **It will not work on Windows.**

Open a terminal and execute the following commands to download the repository, create the specified conda environment, and build/test the `heat` module. Note that you'll have to replace `YOUR_OS_HERE` with either `osx` or `linux`.

```bash
$ git clone https://github.com/kbarnhart/calibration_with_dakota_clinic.git
$ conda env create -f environment_YOUR_OS_HERE.yml
$ conda activate dakota_clinic
$ cd heat/
$ make install
$ pytest
```

#### Option B: Dakota Binary + conda env

Step 1: [Install the Dakota binary for Windows](https://dakota.sandia.gov/download.html) and make a [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#managing-environments) based on the file `environment_everything_but_dakota.yml`.

After downloading/installing the Dakota binary, open a terminal and do the following:
```bash
$ git clone https://github.com/kbarnhart/calibration_with_dakota_clinic.git
$ conda env create -f environment_everything_but_dakota.yml
$ conda activate dakota_clinic
$ cd heat/
$ make install
$ pytest
```

### Step 2: Open a notebook.

Assuming that the results of `pytest` don't include any failures, go up one directory level and open jupyter notebooks.

```bash
$ cd ..
$ jupyter notebook
```

Click `Clinic Notes and Tutorial.ipynb`.
