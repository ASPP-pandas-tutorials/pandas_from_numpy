#!/usr/bin/env python3
""" Process notebooks

* Replace local kernel with Pyodide kernel in metadata.
* Filter:
    * Note and admonition markers.
    * Exercise markers.
    * Solution blocks.
* Write notebooks to output directory.
* Write JSON jupyterlite file.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import re

import jupytext

_JL_JSON_FMT = r'''\
{{
  "jupyter-lite-schema-version": 0,
  "jupyter-config-data": {{
    "contentsStorageName": "rss-{language}"
  }}
}}
'''

def proc_admonitions(nb_path):
    # Run through panflute filter
    # Filter detects notes, admonitions, drops level, adds beginning and
    # end text.
    # Filter replace exercise start and end markers with text.
    return nb


_EX_SOL_MARKER = re.compile(
    r'''
    ^\s*(?:```+|:::+|~~~+)
    \{\s*
    (?P<ex_sol>exercise|solution)-
    (?P<st_end>start|end)
    \s*\}\n
    (?P<attrs>\s*:\S+: \s* \S+\s*\n)*
    \n*
    \s*(?:```+|:::+|~~~+)$
    ''',
    flags=re.VERBOSE)


class ParseError(ValueError):
    """ Error parsing notebook
    """


def proc_ex_sol(nb, nb_path):
    state = 'outside'
    for cell in nb.cells:
        if cell['cell_type'] != 'markdown':
            continue
        src = cell['source']
        if (m := _EX_SOL_MARKER.match(src)):
            ex_sol, st_end, _ = m.groups()
            if ex_sol not in ('exercise', 'solution'):
                raise ParseError(f'Unexpected ex_sol "{st_end}"')
            if st_end not in ('start', 'end'):
                raise ParseError(f'Unexpected st_end "{st_end}"')
            if st_end == 'end':
                if state != ex_sol:
                    raise ParseError(
                        f'{ex_sol} end marker in "{state}" block: {src}')
                state = 'outside'
                cell['source'] =f'**End of {ex_sol}**'
            else:  # start
                if state != 'outside':
                    raise ParseError(
                        f'Can only start {ex_sol} from "outside" block')
                state = ex_sol
                cell['source'] = f'**Start of {ex_sol}**'
            print(f'{src} in state "{state}"')
    1/0
    return nb


def load_process_nb(nb_path, fmt='myst'):
    """ Load and process notebook

    Deal with:

    * Note and admonition markers.
    * Exercise markers.
    * Solution blocks.

    Parameters
    ----------
    nb_path : file-like
        Path to notebook
    fmt : str, optional
        Format of notebook (for Jupytext)

    Returns
    -------
    nb : dict
        Notebook as loaded and parsed.
    """
    nb_path = Path(nb_path)
    nb = jupytext.read(nb_path, fmt=fmt)
    nb2 = proc_admonitions(nb, nb_path)
    return proc_ex_sol(nb2, nb_path)


def process_dir(input_dir, output_dir, in_nb_suffix='.Rmd',
                nb_fmt='myst',
                kernel_name='python',
                kernel_dname='Python (Pyodide)',
                out_nb_suffix='.ipynb'
               ):
    output_dir.mkdir(exist_ok=True, parents=True)
    for path in input_dir.glob('*' + in_nb_suffix):
        nb = load_process_nb(path, nb_fmt)
        nb['metadata']['kernelspec'] = {
            'name': kernel_name,
            'display_name': kernel_dname}
        jupytext.write(nb, output_dir / (path.stem + out_nb_suffix))


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('input_dir',
                        help='Directory containing input notebooks')
    parser.add_argument('output_dir',
                        help='Directory to which we will output notebooks')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    out_path = Path(args.output_dir)
    process_dir(Path(args.input_dir), out_path)
    (out_path / 'jupyter-lite.json').write_text(
        _JL_JSON_FMT.format(language='python'))


if __name__ == '__main__':
    main()
