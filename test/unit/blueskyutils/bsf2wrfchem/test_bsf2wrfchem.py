import pytest

from blueskyutils import bsf2wrfchem
from bsf2finndata import BSF_FIRES, FINN_FIRES

class TestBsf2Finn(object):

    def test_convert_bsf_to_finn(self):
        finn_fire = bsf2wrfchem.convert_bsf_to_finn(BSF_FIRES[0])
        # need to use pytest.approx because expected values
        # are truncated
        for k in sorted(FINN_FIRES[0].keys()):
            expected = FINN_FIRES[0][k]
            val = finn_fire[k]
            if not hasattr(val, 'startswith'):
                val = pytest.approx(val, abs=1e-2)
            assert_msg = "{} didn't match - {} vs {}".format(k, expected, val)
            assert expected == val, assert_msg
