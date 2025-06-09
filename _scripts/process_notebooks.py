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


_EX_SOL_MARKER = re.compile(
    r'''
    (?P<newlines>\n*)
    \s*(```+|:::+|~~~+)\s*
    \{\s*
    (?P<ex_sol>exercise|solution)-
    (?P<st_end>start|end)
    \s*\}
    \s*
    (?P<suffix>\S+)?\s*
    \n
    (?P<attrs>\s*:\S+: \s* \S+\s*\n)*
    \n*
    \s*(\2)\s*
    \n
    ''',
    flags=re.VERBOSE)


_SOL_MARKED = re.compile(
    r'''
    \n?
    <!--\sstart-solution\s-->\n
    .*?
    <!--\send-solution\s-->\n?
    ''',
    flags=re.VERBOSE | re.MULTILINE | re.DOTALL)


def _replace_markers(m):
    st_end = m['st_end']
    if m['ex_sol'] == 'exercise':
        return (f"{m['newlines']}**{st_end.capitalize()} "
                f"of exercise**\n\n")
    return f'\n<!-- {st_end}-solution -->\n'


def process_notes(nb_text):
    return nb_text


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
    nb_text = nb_path.read_text()
    nbt1 = _EX_SOL_MARKER.sub(_replace_markers, nb_text)
    nbt2 = _SOL_MARKED.sub('\n**See page for solution**\n\n', nbt1)
    nbt3 = process_notes(nbt2)
    return jupytext.reads(nbt3,
                          fmt={'format_name': 'myst',
                               'extension': nb_path.suffix})


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
