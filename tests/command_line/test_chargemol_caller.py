from __future__ import annotations

from numpy.testing import assert_allclose
from pytest import approx

from pymatgen.command_line.chargemol_caller import ChargemolAnalysis
from pymatgen.core import Element
from pymatgen.util.testing import TEST_FILES_DIR

TEST_DIR = f"{TEST_FILES_DIR}/command_line/chargemol"


class TestChargemolAnalysis:
    def test_parse_chargemol(self):
        test_dir = f"{TEST_DIR}/spin_unpolarized"
        ca = ChargemolAnalysis(path=test_dir, run_chargemol=False)
        assert_allclose(ca.ddec_charges, [0.8432, -0.8432])
        assert ca.get_partial_charge(0) == approx(0.8432)
        assert ca.get_partial_charge(0, charge_type="cm5") == approx(0.420172)
        assert ca.get_charge_transfer(0) == approx(-0.8432)
        assert ca.get_charge_transfer(0, charge_type="cm5") == approx(-0.420172)
        assert ca.get_charge(0, nelect=1) == approx(1 - 0.8432)
        assert ca.get_charge(0, nelect=1, charge_type="cm5") == approx(1 - 0.420172)
        assert_allclose(ca.dipoles, [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        assert ca.ddec_spin_moments is None
        assert_allclose(ca.bond_order_sums, [0.53992, 0.901058])
        assert_allclose(ca.ddec_rsquared_moments, [8.261378, 34.237274])
        assert_allclose(ca.ddec_rcubed_moments, [14.496002, 88.169236])
        assert_allclose(ca.ddec_rfourth_moments, [37.648248, 277.371929])
        assert_allclose(ca.cm5_charges, [0.420172, -0.420172])
        assert ca.summary["ddec"]["partial_charges"] == ca.ddec_charges
        assert ca.summary["ddec"]["dipoles"] == ca.dipoles
        assert ca.summary["ddec"]["bond_order_sums"] == ca.bond_order_sums
        assert ca.summary["ddec"]["rsquared_moments"] == ca.ddec_rsquared_moments
        assert ca.summary["ddec"]["rcubed_moments"] == ca.ddec_rcubed_moments
        assert ca.summary["ddec"]["rfourth_moments"] == ca.ddec_rfourth_moments
        assert ca.summary["cm5"]["partial_charges"] == ca.cm5_charges
        assert ca.summary["ddec"]["bond_order_dict"] == ca.bond_order_dict
        assert ca.summary["ddec"].get("spin_moments") is None
        assert ca.natoms == [1, 1]
        assert ca.structure is not None
        assert len(ca.bond_order_dict) == 2
        assert ca.bond_order_dict[0]["bonded_to"][0] == {
            "spin_polarization": 0.0,
            "index": 1,
            "direction": (-1, -1, 0),
            "bond_order": 0.0882,
            "element": Element("Cl"),
        }
        assert ca.bond_order_dict[1]["bonded_to"][-1]["direction"] == (-1, 0, 0)
        assert ca.get_property_decorated_structure().site_properties["partial_charge_ddec6"] == ca.ddec_charges

    def test_parse_chargemol2(self):
        test_dir = f"{TEST_DIR}/spin_polarized"
        ca = ChargemolAnalysis(path=test_dir, run_chargemol=False)
        assert_allclose(ca.ddec_spin_moments, [0.201595, 0.399203, 0.399203])
        assert_allclose(
            ca.dipoles,
            [
                [-0.0, 0.0, -0.127251],
                [0.0, -0.027857, -0.010944],
                [0.0, 0.027857, -0.010944],
            ],
        )
        assert ca.summary["ddec"]["bond_order_dict"][0]["bonded_to"][0]["spin_polarization"] == approx(0.0490)
        assert ca.summary["ddec"]["spin_moments"] == ca.ddec_spin_moments
        assert ca.natoms is None
        assert ca.structure is None
