# Notebooks

Here we present some notebooks covering several topics as OBIS data access, data cleaning, environmental information extraction, and data visualization.

# R
## Environmental Data For Occurrences
[environmental_data_for_occurrences.qmd](R/environmental_data_for_occurrences.qmd)
![Environmental Data For Occurrences](screenshots/environmental_data_for_occurrences.png)




# Python



------

Note for developers:

There is a GitHub actions configured for this repository. It will render any .ipynb or .qmd files added to either the Python or R folders, get a screenshot of the document and add it to this README. Code cells are **not** executed.

Avoid editing this README file, as the script might start adding duplicated entries here.

For Quarto (.qmd) files, there are two important requirements:

1. Don't add any inline R code (like `r data_vector[1]`), otherwise the code will fail.
2. Add the option of embedding resources on the Quarto header:

``` {bash}
title: "any title"
format: 
  html:
    embed-resources: true
```

_Created by the OBIS secretariat_