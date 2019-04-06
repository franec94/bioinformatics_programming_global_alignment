#!/usr/bin/env python3

# import numpy as np
import graph_matrix as gm
import os
import sys


def run_problem_as_gm(args):

    # subject_sequence = list() query_sequence = list() score_scheme = dict()

    # score_scheme, subject_sequence, query_sequence = gm.config_work(sys.argv)
    score_scheme, subject_sequence, query_sequence = gm.config_work(args)

    n, m = len(subject_sequence), len(query_sequence)
    graph_matrix = gm.create_graph_matrix(n, m)

    graph_paths = gm.calculate_paths(graph_matrix, score_scheme, subject_sequence, query_sequence)
    print(graph_matrix)

    gm.show_paths(graph_matrix, graph_paths, subject_sequence, query_sequence)


def run_problem_oo_approach(args):

    from GlobalAlignment import GlobalAlignment

    score_scheme, reference_sequence, query_sequence = gm.config_work(args)
    ga = GlobalAlignment(query_sequence, reference_sequence, score_scheme)

    ga.calculate_paths()
    ga.show_paths()

    pass


if __name__ == "__main__":
    """Entry point of script written for work-out purposes"""
    print('=== Python Script: Graph Matrix Alignment Calculation ===')

    if len(sys.argv) != 4:
        print("\nUsage:", os.path.basename(sys.argv[0]), "score-scheme subject-string query-string")
        sys.exit(-1)

    # run_problem_as_gm(sys.argv)

    run_problem_oo_approach(sys.argv)


