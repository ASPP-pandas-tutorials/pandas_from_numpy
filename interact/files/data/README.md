---
orphan: true
---

# Datasets and licenses

## `children-per-woman-vs-human-development-index`

See [Children HDI README](children-per-woman-vs-human-development-index) for
source and citation.

## `gender_stats`

See [Gender Stats README](gender_stats) for source and citation.

## `year_2000_hdi_fert.csv`

This derives from `children-per-woman-vs-human-development-index.csv` with row
selection from data in `gender_stats.csv`.  See `./make_y2k_hdi_fert.Rmd`
notebook for the exact derivation.

## `airline_passengers.csv`

This is classic dataset from Box and Jenkins "Time Series Analysis,
Forecasting and Control" book, first published in 1970.  It's available via
base R as the [AirPassengers
dataset](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html).

The `airline_passengers.csv` itself derives directly from the R dataset, by
running the `make_airline_passengers.R` script.

## References

Box, G. E. P., Jenkins, G. M. and Reinsel, G. C. (1976) *Time Series Analysis,
Forecasting and Control. Third Edition*. Holden-Day. Series G.
