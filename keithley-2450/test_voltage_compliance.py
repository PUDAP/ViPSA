"""Offline recording-transport regression; no VISA resource is opened."""
import unittest
from unittest.mock import Mock
from driver import Driver

class VoltageCompliance(unittest.TestCase):
    def test_output_state_readback(self):
        d=Driver.__new__(Driver)
        d.address='offline-recording-transport'
        d.smu=Mock()
        d.smu.query.return_value='0'
        self.assertEqual(d.get_output(),'0')
        d.smu.query.assert_called_once_with(':OUTP?')

    def test_voltage_source_paths_use_native_ilim_only(self):
        for name, kwargs in [
            ('set_protection', dict(function='VOLT', value=1e-4)),
            ('hold_voltage_measure_current', dict(voltage=0, current_compliance=1e-4)),
            ('source_voltage_measure_current', dict(voltages=[0]*10, current_compliance=1e-4)),
        ]:
            with self.subTest(path=name):
                d=Driver.__new__(Driver)
                transport=Mock()
                transport.query.return_value='0'
                d.smu=transport
                d._get_session=Mock(return_value=(transport,False))
                d._close_temp=Mock()
                d._read_trace_records=Mock(return_value=[])
                getattr(d,name)(**kwargs)
                commands=[c.args[0] for c in transport.write.call_args_list]
                self.assertTrue(any(c.startswith(':SOUR:VOLT:ILIM ') for c in commands))
                self.assertFalse(any(c.startswith(':SENS:CURR:PROT ') for c in commands), commands)

if __name__=='__main__': unittest.main()
