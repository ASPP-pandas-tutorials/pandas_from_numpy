""" Test notebook parsing
"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
THERE = HERE.parent
EG1_NB_PATH = HERE / 'eg.Rmd'
EG2_NB_PATH = HERE / 'eg2.Rmd'

sys.path.append(str(THERE))

import process_notebooks as pn


def test_process_eg1():
    out_nb = pn.load_process_nb(EG1_NB_PATH)
    cells = out_nb['cells']
    assert len(cells) == 16
    assert '**Start of exercise**' in cells[-6]['source'].splitlines()
    assert '**End of exercise**' in cells[-4]['source'].splitlines()
    assert '**See page for solution**' in cells[-3]['source'].splitlines()


def test_process_eg2():
    out_nb = pn.load_process_nb(EG2_NB_PATH)
    cells = out_nb['cells']
    assert len(cells) == 10
    ex_cell_lines = cells[-3]['source'].splitlines()
    assert '**Start of exercise**' in ex_cell_lines
    assert '**End of exercise**' in ex_cell_lines
    assert '**See page for solution**' in cells[-2]['source'].splitlines()


def test_admonition_finding():
    nb_text = EG2_NB_PATH.read_text()
    assert pn.get_admonition_lines(nb_text) == [(24, 34), (126, 130)]
