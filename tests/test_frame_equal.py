from pandas.util.testing import assert_frame_equal
import glob
import os


def  test_dakota_files_correct():
    files = glob.glob("../analysis*.dat")
    dfs = []
    for file in files:
        df = pd.read_csv(file, engine="python", sep="\s+")

        filename = os.path.split(file)[-1]
        other_file = os.path.join(["data", filename])

        df_test = pd.read_csv(other_file, engine="python", sep="\s+")

        assert_frame_equal(df, df_test)
