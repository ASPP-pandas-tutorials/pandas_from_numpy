""" Test notebook parsing
"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
THERE = HERE.parent
EG_NB_PATH = HERE / 'eg2.Rmd'

sys.path.append(str(THERE))

import process_notebooks as pn


def test_process():
    out_nb = pn.load_process_nb(EG_NB_PATH)
    cells = out_nb['cells']
    assert len(cells) == 16
