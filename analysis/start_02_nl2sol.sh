#!/bin/bash
dakota -i dakota_02_nl2sol.in -o dakota_02_nl2sol.out -write_restart dakota_02_nl2sol.rst &> dakota_02_nl2sol.log
dakota_restart_util to_tabular dakota_02_nl2sol.rst dakota_02_nl2sol.dat
