---
orphan: true
---

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
file reads the input Myst-MD format notebooks using `jupytext` before
converting to Jupyter `.ipynb` files.

## Notes and admonitions

Stick to standard Myst-MD syntax.  Don't use extensions like using `:::` for
`<div>` blocks, although [JupyterBook allows
this](https://jupyterbook.org/en/stable/content/content-blocks.html#markdown-friendly-directives-with).
So, for example, use:

~~~
``` {note}

My note

```
~~~

instead of:

~~~
::: {note}

My note

:::
~~~

This allows the notebook post-processing script in
`_scripts/process_notebooks.py` to read these notebooks correctly.  It appears
that `jupytext.read("my_nb.Rmd", fmt="myst")` does not honor the second form.

For the same reason, do not use:

~~~
``` {admonition} A custom title

My admonition

```
~~~

as `jupytext` does not read these correctly as separate blocks.

## Exercises and solutions

We use [sphinx-exercise](https://ebp-sphinx-exercise.readthedocs.io) for the exercises and solutions.

Mark exercises and solution with [gated
markers](https://ebp-sphinx-exercise.readthedocs.io/en/latest/syntax.html#alternative-gated-syntax),
like this:

~~~
<!-- #region -->
```{exercise-start}
:label: my-exercise-label
:class: dropdown
```
<!-- #endregion -->

My exercise.

<!-- #region -->
```{exercise-end}
```
<!-- #endregion -->

<!-- #region -->
```{solution-start} my-exercise-label
:class: dropdown
```
<!-- #endregion -->

My solution.

<!-- #region -->
```{solution-end}
```
<!-- #endregion -->
~~~

The region markers are to prevent Jupytext getting confused as to whether these should be code cells.

The gated markers (of form `solution-start` and `solution-end` etc) allow you
to embed code cells in the exercise or solution, because this allows code
cells to be at the top level of the notebook, where Jupyter needs them to be.

See <
