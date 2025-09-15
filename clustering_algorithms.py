import pandas as pd
import numpy as np
from biotite.sequence.phylo import upgma
from biotite.sequence.phylo import neighbor_joining
import biotite.sequence.phylo as phylo
import matplotlib.pyplot as plt
import biotite.sequence.graphics as graphics
from biotite.sequence.phylo import Tree as BiotiteTree
from ete3 import Tree


def prep_matrix(matrix_file):
    df = pd.read_csv(matrix_file, sep="\t")
    langs = df.iloc[:, 0].tolist()
    matrix = df.iloc[:, 1:].to_numpy()  # drop language names
    return langs, matrix


def run_algorithm(matrix_file, mode="upgma", plot=False):
    """
    Read distance matrix from text file and apply UPGMA and neighbor-joining algorithms.
    Newick string of trees is printed to terminal with optional plotting of trees.
    """
    languages, distances = prep_matrix(matrix_file)
    if mode == "upgma":
        print("\nUPGMA:\n")
        tree = upgma(distances)
        newick_str = tree.to_newick(labels=languages, include_distance=True)
        ete_tree = Tree(newick_str)

    if mode == "neighbor_joining":
        print("\nNeighbor Joining:\n")
        tree = neighbor_joining(distances)
        newick_str = tree.to_newick(labels=languages, include_distance=True)
        ete_tree = Tree(newick_str)
        ete_tree.set_outgroup(ete_tree.get_midpoint_outgroup()) # midpoint rooting

        # Root with a specific taxon (say "German")
        # ete_tree.set_outgroup("German")

    print(ete_tree.write(format=1))

    if plot:
        # quick plotting
        tree = BiotiteTree.from_newick(ete_tree.write(format=1), labels=languages)
        fig, ax = plt.subplots(figsize=(6.0, 6.0), constrained_layout=True)
        graphics.plot_dendrogram(ax, tree, labels=languages, orientation="top")
        graphic_file = f"trees/tests_pdf/{input_matrix[:-4].split("/")[1]}_{mode}.pdf"
        plt.savefig(graphic_file, dpi=300, bbox_inches="tight")
        plt.close()


if __name__ == "__main__":

    input_matrix = "matrices/Indo_European_Ger.txt"

    run_algorithm(input_matrix)
    run_algorithm(input_matrix, mode="neighbor_joining", plot=True)

    # feats = ["phonology", "morphology", "syntax"]
    # langs = ["Rom", "Slav", "Ger"]
    # for f in feats:
    #     for l in langs:
    #         input_matrix = f"matrices/{l}_{f}.txt"
    #         print(f"\n{50*"-"}\nProcessing file {input_matrix}\n{50*"-"}")
    #         run_algorithm(input_matrix)
    #         run_algorithm(input_matrix, mode="neighbor_joining")

