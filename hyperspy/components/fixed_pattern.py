# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Hyperspy developers
#
# This file is part of  Hyperspy.
#
#  Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Hyperspy.  If not, see <http://www.gnu.org/licenses/>.

from hyperspy.component import Component
from scipy.interpolate import interp1d
from hyperspy import messages

class FixedPattern(Component):
    """Fixed pattern component with interpolation support.
    
        f(x) = A*p(x-x0)
    
    +------------+-----------+
    | Parameter  | Attribute |
    +------------+-----------+
    +------------+-----------+
    |     A      |   yscale  |
    +------------+-----------+
    |    x0      |  origin   |
    +------------+-----------+
    
    
    The fixed pattern is defined by an array which must be provided to the 
    FixedPattern constructor, e.g.:
    
    .. code-block:: ipython

        In [1]: my_fixed_pattern = components.FixedPattern(np.array([1,2,3,4,5,6,7,8]))
    
    The array must have the same spectral dimension as the data that is being
    analysed if interpolation is not used. When interpolation is not used 
    the origin parameter is always fixed and its value is zero.
    
    To enable interpolation use the :py:meth:`prepare_interpolator`
    method and set the :py:attr:`interpolate` attribute to True, e.g.:
    
    .. code-block:: ipython
    
        In [2]: # First provide the spectral axis of the fixed pattern
        In [3]: my_fixed_pattern.prepare_interpolator(
                        np.array((0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08])))
        In [4]: # Then enable interpolation
        In [5]: my_fixed_pattern.interpolate = True
    
    
    Please note that enabling the interpolation has a computation time penalty
    and therefore it must only be enabled when needed.
    
    See Also
    --------
    ScalableFixedPattern : another component which permit 
        "stretching" the fixed pattern in the spectral dimension. Eventually 
        both components will be merged.
    
    """

    def __init__( self, array):
        Component.__init__(self, ['yscale', 'origin'])
        self.name = 'Fixed pattern'
        self.array = array
        self.yscale.free = True
        self.yscale.value = 1.
        self.origin.value = 0
        self.origin.free = False
        self.isbackground = True
        self.convolved = False
        self.yscale.grad = self.grad_yscale
        self.interpolate = False
        self._interpolation_ready = False
    
    def prepare_interpolator(self, x, kind = 'linear', fill_value = 0, **kwards):
        """Prepare interpolation.
        
        Parameters
        ----------
        x : array
            The spectral axis of the fixed pattern
        kind: str or int, optional
            Specifies the kind of interpolation as a string
            ('linear','nearest', 'zero', 'slinear', 'quadratic, 'cubic')
            or as an integer specifying the order of the spline interpolator
            to use. Default is 'linear'.

        fill_value : float, optional
        If provided, then this value will be used to fill in for requested
        points outside of the data range. If not provided, then the default
        is NaN.
        
        Any extra keyword argument is passed to `scipy.interpolate.interp1d`
        
        """
        self.interp = interp1d(x, self.array, kind = kind, 
        fill_value = fill_value, bounds_error=False, **kwards)
        self._interpolation_ready = True
        
    def function(self, x):
        if self.interpolate is False:
            return self.array * self.yscale.value
        elif self._interpolation_ready is True:
            return self.interp(x - self.origin.value) * self.yscale.value
        else:
            messages.warning(
            'To use interpolation you must call prepare_interpolator first')
            
    def grad_yscale(self, x):
        return self.array
    
