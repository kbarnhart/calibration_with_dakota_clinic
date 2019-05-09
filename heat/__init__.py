"""Model the diffusion of heat over a 1D column."""

from ._version import get_versions
from .bmi_heat import BmiHeat
from .heat import solve_1d

__all__ = ["BmiHeat", "solve_1d"]
__version__ = get_versions()["version"]
del get_versions
