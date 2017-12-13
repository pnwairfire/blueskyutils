import pytest

from blueskyutils import bsf2wrfchem
from bsf2finndata import BSF_FIRES, FINN_FIRES

class TestBsf2Finn(object):

    def test_convert_bsf_to_finn(self):
        finn_fire = bsf2wrfchem.convert_bsf_to_finn(BSF_FIRES[0])
        # need to use pytest.approx because expected values
        # are truncated
        for k in sorted(FINN_FIRES[0].keys()):
            assert pytest.approx(finn_fire[k], abs=1e-4) == float(FINN_FIRES[0][k])
