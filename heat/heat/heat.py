"""The 1D heat model."""

import numpy as np
import yaml


def solve_1d(temp, spacing, k=2e3, kappa=1e-6, Qm=0.05, time_step=1.0):
    """Solve the 1D Heat Equation in a column.

    Parameters
    ----------
    temp : ndarray
        Temperature.
    spacing : array_like
        Grid spacing in the row and column directions.
    k : float, optional
        Thermal conductivity. Default is 2e3.
    kappa : float, optional
        Thermal diffusivity. Default is 1e-6.
    Qm : float, optional
        Heat flux. Default is 0.05.
    time_step : float (optional)
        Time step.

    Returns
    -------
    result : ndarray
        The temperatures after time *time_step*.

    Examples
    --------
    >>> import numpy as np
    >>> from heat import solve_1d
    >>> spacing = [100]
    >>> dTdz = 0.01
    >>> temp = dTdz * np.arange(0, 1000, spacing[0])
    >>> temp
    array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> for i in range(10*365):
    ...     temp = solve_1d(temp, spacing, time_step=24*60*60)
    >>> temp

    """
    Q = np.zeros_like(temp)
    dTdz = np.diff(temp) / spacing[0]

    Q[:-1] = - k * dTdz
    Q[-1] = - Qm
    dTdt = (-kappa/k) * np.diff(Q)/spacing[0]

    temp[1:] += dTdt * time_step

    return temp


class Heat(object):

    """Solve the Heat equation on a grid.

    Examples
    --------
    >>> heat = Heat()
    >>> heat.time
    0.0
    >>> heat.time_step
    250000.0
    >>> heat.advance_in_time()
    >>> heat.time
    250000.0

    >>> heat = Heat(shape=(5,))
    >>> heat.temperature = np.zeros_like(heat.temperature)
    >>> heat.temperature[2] = 1.
    >>> heat.advance_in_time()

    >>> heat = Heat(kappa=.5)
    >>> heat.time_step
    0.5
    >>> heat = Heat(kappa=.5, spacing=(2.,))
    >>> heat.time_step
    2.0
    """

    def __init__(
        self,
        shape=(110,),
        spacing=(1.0,),
        origin=(0.0,),
        kappa=1e-6,
        k=2e3,
        Qm=0.05,

    ):
        """Create a new heat model.

        Paramters
        ---------
        shape : array_like, optional
            The shape of the solution grid as (*rows*, *columns*).
        spacing : array_like, optional
            Spacing of grid rows and columns.
        origin : array_like, optional
            Coordinates of lower left corner of grid.
        k : float, optional
            Thermal conductivity. Default is 2e3.
        kappa : float, optional
            Thermal diffusivity. Default is 1e-6.
        Qm : float, optional
            Heat flux. Default is 0.05.
        """
        self._shape = shape
        self._spacing = spacing
        self._origin = origin
        self._time = 0.0
        self._kappa = kappa
        self._k = k
        self._Qm = Qm
        self._time_step = min(spacing) ** 2 / (4.0 * self._kappa)
        self._temperature = np.random.random(self._shape)

    @property
    def time(self):
        """Current model time."""
        return self._time

    @property
    def temperature(self):
        """Temperature of the plate."""
        return self._temperature

    @temperature.setter
    def temperature(self, new_temp):
        """Set the temperature of the plate.

        Parameters
        ----------
        new_temp : array_like
            The new temperatures.
        """
        self._temperature[:] = new_temp

    @property
    def time_step(self):
        """Model time step."""
        return self._time_step

    @time_step.setter
    def time_step(self, time_step):
        """Set model time step."""
        self._time_step = time_step

    @property
    def spacing(self):
        """Shape of the model grid."""
        return self._spacing

    @property
    def origin(self):
        """Origin coordinates of the model grid."""
        return self._origin

    @classmethod
    def from_file_like(cls, file_like):
        """Create a Heat object from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        Heat
            A new instance of a Heat object.
        """
        config = yaml.safe_load(file_like)
        return cls(**config)

    def advance_in_time(self):
        """Calculate new temperatures for the next time step."""
        self._temperature[:] = solve_1d(
            self._temperature,
            self._spacing,
            time_step=self._time_step,
            k=self._k, kappa=self._kappa, Qm=self._Qm,
        )
        self._time += self._time_step
