from nose.tools import (
    assert_true,
    assert_equal,
    assert_not_equal,
    raises)
import numpy as np

from hyperspy.signal import Signal
from hyperspy import utils

class Test_Utils_Stack():
    def setUp(self):
        s = Signal(np.ones((3, 2, 5)))
        s.axes_manager[0].name = "x"
        s.axes_manager[1].name = "y"
        s.axes_manager[2].name = "E"
        s.axes_manager[2].scale = 0.5    
        s.metadata.title = 'test'    
        self.signal = s
        
        
    def test_stack_default(self):
        s = self.signal
        s1 = s.deepcopy()+1
        s2 = s.deepcopy()*4
        result_signal = utils.stack([s,s1,s2])
        result_list = result_signal.split()
        assert_true(len(result_list) == 3)
        assert_true((result_list[0].data == result_signal[::,::,0].data).all())
        
    def test_stack_of_stack(self):
        s = self.signal
        s1 = utils.stack([s]*2)
        s2 = utils.stack([s1]*3)
        s3 = s2.split()[0]
        s4 = s3.split()[0]
        assert_true((s4.data == s.data).all())
        assert_true((hasattr(s4.original_metadata,'stack_elements')is False))
        assert_true((s4.metadata.title=='test'))

        
    def test_stack_not_default(self):
        s = self.signal
        s1 = s.deepcopy()+1
        s2 = s.deepcopy()*4
        result_signal = utils.stack([s,s1,s2],axis=1)
        result_list = result_signal.split()
        assert_true(len(result_list) == 3)
        assert_true((result_list[0].data == result_signal[::,0].data).all())
        


