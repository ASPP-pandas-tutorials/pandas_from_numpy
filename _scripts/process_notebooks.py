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

import docutils.core as duc
import docutils.nodes as dun
from docutils.utils import Reporter
from myst_parser.docutils_ import Parser

_END_DIV_RE = re.compile(r'^\s*(:::+|```+|~~~+)\s*$')
import jupytext

_JL_JSON_FMT = r'''\
{{
  "jupyter-lite-schema-version": 0,
  "jupyter-config-data": {{
    "contentsStorageName": "rss-{language}"
  }}
}}
'''

_DIV_RE = r'\s*(:::+|```+|~~~+)\s*'


_ADM_HEADER = re.compile(
    rf'''
    ^{_DIV_RE}
    \{{\s*(?P<ad_type>\S+)\s*\}}\s*
    (?P<ad_title>.*)\s*$
    ''', flags=re.VERBOSE)


_EX_SOL_MARKER = re.compile(
    rf'''
    (?P<newlines>\n*)
    {_DIV_RE}
    \{{\s*
    (?P<ex_sol>exercise|solution)-
    (?P<st_end>start|end)
    \s*\}}
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


_END_DIV_RE = re.compile(rf'^{_DIV_RE}$')


# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-extensions
MYST_EXTENSIONS = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]


def _replace_markers(m):
    st_end = m['st_end']
    if m['ex_sol'] == 'exercise':
        return (f"{m['newlines']}**{st_end.capitalize()} "
                f"of exercise**\n\n")
    return f'\n<!-- {st_end}-solution -->\n'


def get_admonition_lines(nb_text):
    parser = Parser()
    doc = duc.publish_doctree(
        source=nb_text,
        settings_overrides={
            "myst_enable_extensions": MYST_EXTENSIONS,
            'report_level': Reporter.ERROR_LEVEL,
        },
        parser=parser)
    lines = nb_text.splitlines()
    n_lines = len(lines)
    admonition_lines = []
    for admonition in doc.findall(dun.Admonition):
        start_line = admonition.line - 1
        following = list(admonition.findall(include_self=False,
                                            descend=False,
                                            ascend=True))
        last_line = following[0].line - 2 if following else n_lines - 1
        for end_line in range(last_line, start_line + 1, -1):
            if _END_DIV_RE.match(lines[end_line]):
                break
        else:
            raise ValueError('Could not find end div')
        admonition_lines.append((start_line, end_line))
    return admonition_lines


_ADM_HEADER = re.compile(
    r'''
    ^\s*(:::+|```+|~~~+)\s*
    \{\s*(?P<ad_type>\S+)\s*\}\s*
    (?P<ad_title>.*)\s*$
    ''', flags=re.VERBOSE)


def process_notes(nb_text):
    lines = nb_text.splitlines()
    for first, last in get_admonition_lines(nb_text):
        m = _ADM_HEADER.match(lines[first])
        if not m:
            raise ValueError(f"Cannot get match from {lines[first]}")
        ad_type, ad_title = m['ad_type'], m['ad_title']
        suffix = '' if ad_title is None else f': {ad_title}'
        lines[first] = f"**Start of {ad_type}{suffix}**"
        lines[last] = f"**End of {ad_type}**"
    return '\n'.join(lines)


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
