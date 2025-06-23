def get_clean_mat_mort_names(mm_name_series):

    # Copy the `country_name` Series
    clean_mat_mort_names_solution = mm_name_series.copy()

    # A dictionary of values. The `.keys()` are the original strings, the `.values()`
    # are the replacement strings
    replace_dict = {" ": "_",
                    "(": "",
                    ")": "",
                    ",": "",
                    ".": "",
                    "-": "_"}

    # Loop through the keys and values
    for to_replace, replace in zip(replace_dict.keys(), 
                                replace_dict.values()):
        
        # Make the replacements
        clean_mat_mort_names_solution = clean_mat_mort_names_solution.str.replace(to_replace, replace)

    # Remove capitalization
    clean_mat_mort_names_solution = clean_mat_mort_names_solution.str.lower()

    # Show the `.unique()` array.
    return clean_mat_mort_names_solution.unique()