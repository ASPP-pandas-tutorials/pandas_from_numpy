""" Test notebook parsing
"""

import sys
from pathlib import Path

import jupytext

import pytest

HERE = Path(__file__).parent
THERE = HERE.parent
EG1_NB_PATH = HERE / 'eg.Rmd'
EG2_NB_PATH = HERE / 'eg2.Rmd'

sys.path.append(str(THERE))

import process_notebooks as pn


def nb2rmd(nb, fmt='myst', ext='.Rmd'):
    return jupytext.writes(nb, fmt)


@pytest.mark.parametrize('nb_path', (EG1_NB_PATH, EG2_NB_PATH))
def test_process_nbs(nb_path):
    out_nb = pn.load_process_nb(nb_path)
    out_txt = nb2rmd(out_nb)
    out_lines = out_txt.splitlines()
    assert out_lines.count('**Start of exercise**') == 1
    assert out_lines.count('**End of exercise**') == 1
    assert out_lines.count('**See page for solution**') == 1
    # A bit of solution text, should not be there.
    assert 'You probably spotted that' not in out_txt


def test_admonition_finding():
    nb_text = EG2_NB_PATH.read_text()
    assert pn.get_admonition_lines(nb_text) == [(24, 34), (126, 130)]
