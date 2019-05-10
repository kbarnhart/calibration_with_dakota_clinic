from pandas.util.testing import assert_frame_equal
import pandas as pd
import glob
import os
import pytest

files = glob.glob("analysis/*.dat")

@pytest.mark.parametrize("file", files)
def test_dat_equiv(file):
    df = pd.read_csv(file, engine="python", delim_whitespace=True)

    filename = os.path.split(file)[-1]
    other_file = os.path.join(*["tests", "data", filename])

    df_test = pd.read_csv(other_file, engine="python", delim_whitespace=True)

    assert_frame_equal(df.sort_values("%eval_id").reset_index(drop=True),
                       df_test.sort_values("%eval_id").reset_index(drop=True),
                       check_less_precise=2)
