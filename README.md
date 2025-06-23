# ASPP Pandas tutorials

This repository houses the Pandas tutorials originally written for the
Advanced Scientific Programming in Python course](https://aspp.school).

This file is for those writing or editing these pages.

The repository uses [JupyterBook](https://jupyterbook.org) to make
nice-looking HTML pages from the component `.md` text files and `.Rmd` (R
Markdown) notebooks.

## A note on processing

The pages are designed both as pages for pretty HTML output, and to be used as interactive notebooks in e.g. JupyterLite.

There is some markup that we need for the pretty HTML output that looks ugly
in a Jupyter interface such as
[JupyterLite](https://jupyterlite.readthedocs.io).  Accordingly, we
post-process the pages with a script `_scripts/process_notebooks.py` to load
the pages as text notebooks, and write out `.ipynb` files with modified markup
that looks better in a Jupyter interface.  Some of the authoring advice here
is to allow that process to work smoothly, because the `process_notebooks.py`
file reads the input Myst-MD format notebooks using
[Jupytext](https://jupytext.readthedocs.io) before converting to Jupyter
`.ipynb` files.

## Notes and admonitions

Use `:::` for
`<div>` blocks ([JupyterBook allows
this](https://jupyterbook.org/en/stable/content/content-blocks.html#markdown-friendly-directives-with)):
So, for example, prefer:

~~~
::: {note}

My note

:::
~~~

to the more standard Myst markup of:

~~~
<!-- #region -->
``` {note}

My note

```
<!-- #endregion -->
~~~

Note the `region` and `endregion` markup in the second form; this makes more
sure that Jupytext does not confuse the `{note}` with a code block.  One of
the advantages of the `:::` markup is that you don't need these `#region`
demarcations.

For the same reason, prefer the `:::` form for notes, warnings and admonitions.  For example, prefer:

~~~
::: {admonition} A custom title

My admonition

:::
~~~


## Exercises and solutions

We use [sphinx-exercise](https://ebp-sphinx-exercise.readthedocs.io) for the exercises and solutions.

Mark *all* exercises and solution with [gated
markers](https://ebp-sphinx-exercise.readthedocs.io/en/latest/syntax.html#alternative-gated-syntax),
like this:

~~~
::: {exercise-start}
:label: my-exercise-label
:class: dropdown
:::

My exercise.

::: {exercise-end}
:::

::: {solution-start} my-exercise-label
:class: dropdown
:::

My solution.

::: {solution-end}
:::
~~~

The region markers are to prevent Jupytext getting confused as to whether these should be code cells.

The gated markers (of form `solution-start` and `solution-end` etc) allow you
to embed code cells in the exercise or solution, because this allows code
cells to be at the top level of the notebook, where Jupyter needs them to be.

The gated markers also make it possible to for the `process_notebooks.py`
script to recognize exercise and solutions blocks, to parse them correctly.

## Development

Once:

```
pip install pre_commit
pre-commit install
```

Before each commit that you will push:

```
pre-commit run --all
```
