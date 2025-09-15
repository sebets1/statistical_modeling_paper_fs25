# Modeling Linguistic Relatedness: A Comparison of UPGMA and Neighbor Joining on WALS Features in European Languages

This repository was made as part of the final project for the university course *Statistical Modeling of Language Dynamics*
Please refer to the paper for more details.

## Overview of the Scripts

###inspect_wals.py

The script loads linguistic data from the WALS dataset and transforms it into a language–feature matrix. It exports the languages, features, values, and the matrix as CSV files for further use. Additionally, some small pre-analyses are made.

###create_matrix.py

The script builds pairwise language distance matrices from a language–feature matrix, using Hamming distance. Allows to filter by language families or specific languages, apply thresholds for feature coverage and build matrices on specific linguistic features. Saves the resulting distance matrix to a text file.


###clustering_algorithms.py

The script reads a language distance matrix from a text file and constructs phylogenetic trees using the UPGMA and Neighbor-Joining algorithms, outputting the trees in Newick format. It can optionally plot the trees and save them as PDF files for visualization.
