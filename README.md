# Biodiversity Hackathon: OBIS Resources

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/iobis/hackathon/HEAD)

This repository contains materials and instructions for participants of the Biodiversity Hackathon.
Here we outline the various tools, demos, and resources that can be used to access and use the biological and biogeographical data in OBIS.

- [Data access](#access-obis-data)
- [Demo Notebooks](#notebook-demos)
- [Other resources](#other-resources)


## Access OBIS data

There are several options available to download data from OBIS, some of which include:

- R package [robis](https://github.com/iobis/robis)
- Python package [pyobis](https://github.com/iobis/pyobis)
- [Full data exports](#full-data-exports)
- [OBIS homepage search](https://obis.org/) or [advanced dataset search](https://obis.org/datasets)
- [OBIS Mapper](https://mapper.obis.org/)


### robis

The [robis R package](https://github.com/iobis/robis) connects to the OBIS API from R. The package can be installed from CRAN or from GitHub (latest development version). 

```r
# install from CRAN
install.packages("robis")

# latest development version
remotes::install_github("iobis/robis")
```

You can use the package to obtain a list of datasets, a taxon checklist, or raw occurrence data by supplying e.g. a taxon name or [WoRMS AphiaID](https://www.marinespecies.org/about.php). You can also specify whether to include absence records when obtaining occurrence data.
To download this data, simply export R objects with the write.csv function. If we wanted to obtain Mollusc data from OBIS, some options would be:

```r
library(robis)

# obtain occurrence data
moll <- occurrence("Mollusca")
moll_abs <- occurrence(“Mollusca”, absence = "include") # include absence records
write.csv(moll, "mollusca-obis.csv") # save the data to csv

# obtain a list of datasets for a taxon
molldata <- dataset(scientificname = "Mollusca")

#obtain a checklist of Mollusc species in a certain area
mollcheck <- checklist(scientificname = "Mollusca", geometry = "POLYGON ((2.3 51.8, 2.3 51.6, 2.6 51.6, 2.6 51.8, 2.3 51.8))")
```

#### Filter datasets by keyword

You can use robis to obtain all datasets and then filter based on keywords in the title and/or abstract. See example below where we filter to find datasets related to seamounts. Multiple keywords can be provided by using | to separate each word, e.g. "seamount|deepsea|benthos".

```r
search_terms <- "seamount" # define your search terms

datasets <- robis::dataset() # obtain datasets from OBIS

seamount_datasets <- datasets[
  grepl(paste(search_terms, collapse = "|"), datasets$title, ignore.case = TRUE) |
  grepl(paste(search_terms, collapse = "|"), datasets$abstract, ignore.case = TRUE),]
```

## Full data exports

[links to jupyter notebook for full data export?]

A full data export of OBIS data is available for download as a Parquet file, [here](https://obis.org/data/access/). Note the following:

- These exports do not include measurement data, dropped records, or absence records
- The exported file will be a single, flattened Occurrence table
- The table includes all provided Event and Occurrence data, as well as 68 fields added by the OBIS Quality Control Pipeline, including taxonomic information obtained from WoRMS

## OBIS homepage

From the OBIS homepage, you can search for data in the search bar in the middle of the page. You can search by particular taxonomic groups, common names, dataset names, OBIS nodes, institute name, areas (e.g., Exclusive Economic Zone (EEZ)), or by the data provider’s country.
See [here](https://manual.obis.org/access.html#obis-homepage-and-dataset-pages) for more details.

## OBIS Mapper

The [OBIS Mapper](https://mapper.obis.org) lets you visualize and filter OBIS data by taxonomy, location, time, and data quality, with options to combine layers and download them as CSV. For more details, see the [OBIS manual](https://manual.obis.org/access.html#mapper).

## Notebook demos

We have prepared several JupyterHub Notebooks that can be used for reference, see: https://github.com/iobis/hackathon/tree/master/notebooks. The notebooks cover several topics including OBIS data access, data cleaning, environmental information extraction, and data visualization.

You can also access the notebooks through the Binder link.

## Other Resources

Here is a list of other OBIS-relevant resources:

- [Darwin Core term Quick Reference Guide](https://dwc.tdwg.org/terms/): provides definitions of the DwC terms in datasets obtained from OBIS
- [OBIS MapTool](https://obis.org/maptool/#): used for generating WKT strings, georeferencing, etc.
  - How to use the OBIS MapTool [YouTube tutorial](https://www.youtube.com/watch?v=XM23WEvE364&list=PLlgUwSvpCFS4TS7ZN0fhByj_3EBZ5lXbF&index=14)
- [Wellknown Text (WKT) visualization tool](https://wktmap.com/): tool to visualize WKT strings
- YouTube video tutorial on accessing data with [OBIS Mapper](https://youtu.be/9PSPEtqgjUI?si=mMzqAWUbwWDIdjss)
- YouTube video tutorial on accessing data with [robis](https://youtu.be/8Ep4fGICQWU?si=8GXfZKb871r4wHzx)
