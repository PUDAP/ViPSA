"""Offline edge glue tests using the real SDK; never connect to VISA/NATS."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
STAGED = HERE.parent.parent / 'dciv-campaign-adapted' / 'staged_driver'
sys.path.insert(0, str(HERE))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

local_guard = load('guarded_2450', HERE / 'guarded_2450.py')
edge = load('edge_2450_driver', HERE / 'driver.py')
fixture = load('frozen_protocol_fixture', STAGED / 'test_guarded_2450.py')
# Frozen fixture calls this ProtocolInstrument; it is an offline fake VISA.
OfflineFakeVISA = fixture.ProtocolInstrument

class EdgeAPITest(unittest.TestCase):
    def driver(self):
        # Frozen make_driver() reloads its module under this name. Restore the
        # release copy before exercising edge glue, which imports lazily.
        sys.modules['guarded_2450'] = local_guard
        d = edge.Driver.__new__(edge.Driver)
        d.smu = OfflineFakeVISA()
        return d

    def test_lazy_metadata_reuses_session_without_io_or_reset(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(edge.pyvisa, 'ResourceManager', side_effect=AssertionError('no VISA open')):
            d = self.driver()
            self.assertFalse(d.get_acquisition_capabilities()['physical_qualified'])
            self.assertEqual(d.get_exposure_guard_state()['state'], 'UNPREPARED')
            guard = d._get_guarded_2450()
            self.assertIs(guard, d._get_guarded_2450())
            self.assertIs(guard.session, d.smu)
            self.assertIsNone(guard.qualification)
            self.assertEqual(d.smu.writes, [])

    def test_external_qualification_loaded_once_relative_path_sanitized(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'qualification.json'
            q = fixture.TransactionTest.make_driver().qualification
            q['secret'] = 'DO-NOT-EXPOSE'
            q['scope_reference'] = 'offline-bench-scope'
            path.write_text(json.dumps(q))
            before = path.read_bytes()
            cwd = os.getcwd()
            try:
                os.chdir(temp)
                with patch.dict(os.environ, {'VIPSA_GUARD_QUALIFICATION_FILE': 'qualification.json'}, clear=True):
                    d = self.driver()
                    caps = d.get_acquisition_capabilities()
                    os.chdir(HERE)
                    self.assertTrue(caps['qualification_configured'])
                    self.assertEqual(caps['qualification_scope_reference'], 'offline-bench-scope')
                    self.assertEqual(caps['qualification_file_reference'], str(path))
                    self.assertNotIn('DO-NOT-EXPOSE', str(caps))
                    self.assertFalse(caps['physical_qualified'])
                    self.assertEqual(d._get_guarded_2450().qualification, q)
                    self.assertEqual(path.read_bytes(), before)
                    self.assertEqual(d.smu.writes, [])
            finally:
                os.chdir(cwd)

    def qualified(self, q=None):
        import json
        import tempfile
        from contextlib import contextmanager
        @contextmanager
        def context():
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / 'qualification.json'
                path.write_text(json.dumps(q if q is not None else fixture.TransactionTest.make_driver().qualification))
                with patch.dict(os.environ, {'VIPSA_GUARD_QUALIFICATION_FILE': str(path)}, clear=True):
                    yield self.driver()
        return context()

    def test_prepare_execute_preserves_intent_digest_and_cannot_replay(self):
        with self.qualified() as d:
            params = fixture.TransactionTest.params(branch_ids=['forming'], device_id='DUT-A', remaining_device_j=5)
            plan = d.prepare_guarded_acquisition([8], [.0001], **params)
            self.assertNotIn(':INIT', d.smu.writes)
            self.assertNotIn(':OUTP ON', d.smu.writes)
            offset = len(d.smu.writes)
            self.assertTrue(d.get_exposure_guard_state()['configuration_verified'])
            self.assertEqual(d.get_terminals(), 'REAR')
            self.assertTrue(all(c.endswith('?') for c in d.smu.writes[offset:]))
            with self.assertRaisesRegex(RuntimeError, 'exact'):
                d.execute_guarded_acquisition('wrong')
            result = d.execute_guarded_acquisition(plan['plan_id'])
            self.assertTrue(result['complete'])
            self.assertEqual(result['plan_digest'], plan['plan_digest'])
            self.assertEqual(result['rows'][0]['V_cmd (V)'], 8)
            self.assertEqual(result['rows'][0]['compliance_a'], .0001)
            self.assertEqual(result['rows'][0]['branch_id'], 'forming')
            self.assertEqual(result['device_id'], 'DUT-A')
            self.assertNotIn('result', result)
            self.assertFalse(result['capabilities']['physical_qualified'])
            with self.assertRaisesRegex(RuntimeError, 'exact'):
                d.execute_guarded_acquisition(plan['plan_id'])
            self.assertEqual(d.smu.writes.count(':INIT'), 1)
            self.assertEqual(d.abort_guarded_acquisition()['state'], 'ABORTED')

    def test_deployment_integrity_uses_target_root_hashes_and_null_unknown(self):
        import hashlib
        import subprocess
        with self.qualified() as d:
            d.get_acquisition_capabilities()
            path = d._guard_qualification_path
            original = path.read_bytes()
            cwd = os.getcwd()
            try:
                os.chdir('/')
                result = d.get_protection_deployment_state()
                expected = subprocess.run(['git', '-C', str(HERE.parent), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True, timeout=2).stdout.strip()
                self.assertEqual(result['git_commit'], expected)
                self.assertFalse(result['scope_qualified'])
                self.assertEqual(result['code_sha256']['driver.py'], hashlib.sha256((HERE / 'driver.py').read_bytes()).hexdigest())
                self.assertEqual(result['code_sha256']['guarded_2450.py'], hashlib.sha256((HERE / 'guarded_2450.py').read_bytes()).hexdigest())
                self.assertEqual(result['configuration_sha256'], {'guard_qualification': hashlib.sha256(original).hexdigest()})
                self.assertEqual(path.read_bytes(), original)
                self.assertEqual(d.smu.writes, [])
                self.assertNotIn('result', result)
                with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('git', 2)):
                    self.assertIsNone(d.get_protection_deployment_state()['git_commit'])
            finally:
                os.chdir(cwd)

    def test_missing_phase_bounds_are_capability_block_before_io(self):
        q = fixture.TransactionTest.make_driver().qualification
        q.pop('measurement_max_s')
        with self.qualified(q) as d:
            with self.assertRaisesRegex(RuntimeError, 'measurement_max_s'):
                d.prepare_guarded_acquisition([8], .0001, **fixture.TransactionTest.params())
            self.assertEqual(d.smu.writes, [])

    def test_real_sdk_catalog_explicit_typed_schema_and_normalization(self):
        import inspect
        from puda.command import build_command_catalog
        from puda.edge_runner import _normalize_handler_result
        with patch.dict(os.environ, {}, clear=True):
            d = self.driver()
            text, catalog = build_command_catalog(d)
            names = {item['name'] for item in catalog}
            required = {'prepare_guarded_acquisition', 'execute_guarded_acquisition',
                        'get_exposure_guard_state', 'get_acquisition_capabilities',
                        'get_terminals', 'abort_guarded_acquisition', 'get_protection_deployment_state'}
            self.assertTrue(required <= names)
            for name in required:
                signature = inspect.signature(getattr(edge.Driver, name))
                for key, param in signature.parameters.items():
                    self.assertNotIn(param.kind, (param.VAR_KEYWORD, param.VAR_POSITIONAL))
                    if key != 'self':
                        self.assertIsNot(param.annotation, inspect.Parameter.empty)
            import guarded_2450
            frozen_signature = inspect.signature(guarded_2450.Guarded2450.prepare_guarded_acquisition)
            wrapper_signature = inspect.signature(edge.Driver.prepare_guarded_acquisition)
            self.assertEqual(list(wrapper_signature.parameters), list(frozen_signature.parameters))
            for key, param in frozen_signature.parameters.items():
                self.assertEqual(wrapper_signature.parameters[key].default, param.default)
                self.assertEqual(wrapper_signature.parameters[key].kind, param.kind)
            caps = d.get_acquisition_capabilities()
            self.assertIs(_normalize_handler_result(caps), caps)
            self.assertNotIn('result', caps)
            self.assertNotIn('guarded_source_voltage_measure_current', names)
            self.assertEqual(d.smu.writes, [])

    def test_existing_constructor_and_methods_preserved(self):
        import ast
        import subprocess
        original = subprocess.run(['git', '-C', str(HERE.parent), 'show', '62b2a91b440894e0b638501688adaf0767a85890:keithley-2450/driver.py'], check=True, capture_output=True, text=True, timeout=2).stdout
        old_tree = ast.parse(original)
        new_tree = ast.parse((HERE / 'driver.py').read_text())
        old_class = next(n for n in old_tree.body if isinstance(n, ast.ClassDef))
        new_class = next(n for n in new_tree.body if isinstance(n, ast.ClassDef))
        new_methods = {n.name: n for n in new_class.body if isinstance(n, ast.FunctionDef)}
        for method in old_class.body:
            if isinstance(method, ast.FunctionDef):
                self.assertEqual(ast.dump(method), ast.dump(new_methods[method.name]), method.name)
        fake = OfflineFakeVISA()
        rm = unittest.mock.Mock()
        rm.list_resources.return_value = ['OFFLINE-ONLY']
        rm.open_resource.return_value = fake
        with patch.object(edge.pyvisa, 'ResourceManager', return_value=rm), patch.dict(os.environ, {}, clear=True):
            d = edge.Driver()
            initial = list(fake.writes)
            d.get_acquisition_capabilities()
            d.get_exposure_guard_state()
            d.get_protection_deployment_state()
            self.assertEqual(fake.writes, initial)
            rm.open_resource.assert_called_once()
            self.assertEqual(d.get_output(), '0')
            self.assertEqual(fake.writes[-1], ':OUTP?')

    def test_frozen_module_byte_identical_and_local_guard_used(self):
        self.assertEqual((HERE / 'guarded_2450.py').read_bytes(), (STAGED / 'guarded_2450.py').read_bytes())
        with patch.dict(os.environ, {}, clear=True):
            guard = self.driver()._get_guarded_2450()
            self.assertIs(type(guard), local_guard.Guarded2450)
            self.assertEqual(Path(sys.modules['guarded_2450'].__file__).resolve(), HERE / 'guarded_2450.py')

    def test_unqualified_defaults_block_preparation_without_output_or_proof(self):
        with patch.dict(os.environ, {}, clear=True):
            d = self.driver()
            with self.assertRaisesRegex(RuntimeError, 'Missing qualification'):
                d.prepare_guarded_acquisition([8], .0001, **fixture.TransactionTest.params())
            self.assertIsNone(d._get_guarded_2450().qualification)
            self.assertEqual(d.smu.writes, [])
            self.assertFalse(d.get_protection_deployment_state()['scope_qualified'])
            self.assertEqual(d.get_protection_deployment_state()['configuration_sha256'], {'guard_qualification': None})
            with self.assertRaises(TypeError):
                d.prepare_guarded_acquisition([8], .0001, physical_qualified=True, **fixture.TransactionTest.params())

    def test_external_phase_scope_is_not_filled_from_other_phase(self):
        q = fixture.TransactionTest.make_driver().qualification
        q['envelopes'] = {'read': {'voltage_bound_v': .11}}
        with self.qualified(q) as d:
            with self.assertRaisesRegex(RuntimeError, 'category qualification envelope: forming'):
                d.prepare_guarded_acquisition([8], .0001, **fixture.TransactionTest.params())
            self.assertEqual(d.smu.writes, [])

    def test_physical_claim_never_becomes_verified_proof(self):
        q = fixture.TransactionTest.make_driver().qualification
        q.update(kind='physical', scope_reference='real-scope-ref-only', evidence={'secret': 'not-published'})
        with self.qualified(q) as d:
            caps = d.get_acquisition_capabilities()
            self.assertTrue(caps['qualification_claim_supplied'])
            self.assertFalse(caps['physical_qualified'])
            self.assertFalse(caps['qualification_evidence_verified'])
            self.assertNotIn('not-published', str(caps))
            self.assertEqual(caps['qualification_scope_reference'], 'real-scope-ref-only')
            with self.assertRaisesRegex(RuntimeError, 'Missing qualification bounds'):
                d.prepare_guarded_acquisition([8], .0001, **fixture.TransactionTest.params())
            self.assertEqual(d.smu.writes, [])

    def test_unreadable_external_qualification_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'invalid.json'
            for content in ('not-json', '[]'):
                path.write_text(content)
                with patch.dict(os.environ, {'VIPSA_GUARD_QUALIFICATION_FILE': str(path)}, clear=True):
                    d = self.driver()
                    with self.assertRaisesRegex(RuntimeError, 'qualification unavailable or invalid'):
                        d.get_acquisition_capabilities()
                    self.assertEqual(d.smu.writes, [])
                    self.assertEqual(path.read_text(), content)

if __name__ == '__main__':
    unittest.main()
