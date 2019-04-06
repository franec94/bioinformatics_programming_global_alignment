
import numpy as np


def show_paths(graph_matrix, graph_paths, subject_sequence, query_sequence):
    m, n = graph_matrix.shape
    val = max(graph_matrix[m-1, :])
    print("max: ", val)

    for i in range(1, n):
        item = graph_matrix[m-1, i]
        if item == val:
            print("bottom coordinates:", m-1, i)
            sol = list()
            sol.insert(0, query_sequence[m - 2])

            r, c = m-1, i
            z = m-3
            while r != 0 and c != 0:
                tmp_list = graph_paths[r, c][:]
                # print(tmp_list)

                if tmp_list[0] == 1:
                    r, c = r-1, c-1

                    if z < 0:
                        sol.insert(0, '-')
                    else:
                        sol.insert(0, query_sequence[z])

                    z -= 1
                elif tmp_list[1] == 1:
                    c = c - 1
                    sol.insert(0, '-')
                elif tmp_list[2] == 1:
                    r = r - 1
                    sol.insert(0, '-')
            # sol = (n - 1 - i) * ['-']
            sol.extend((n-1 - len(sol)) * ['-'])
            print(subject_sequence)
            print(sol)


def calculate_paths(graph_matrix, score_scheme, subject_sequence, query_sequence):
    """Calculate path for a give matrix"""
    m, n = graph_matrix.shape
    assert m == len(query_sequence) + 1
    assert n == len(subject_sequence) + 1

    gm = graph_matrix
    scsc = score_scheme

    x = np.zeros((m, n, 3))
    x[:, 0][0] = 1
    x[0, :][3] = 1
    # print(x)

    for i in range(0, m-1):
        t = query_sequence[i]

        for j in range(0, n-1):
            t2 = subject_sequence[j]
            res = scsc["match"] if t == t2 else scsc["mismatch"]

            tmp_list = [res+gm[i][j], gm[i+1][j]+scsc["gap"], gm[i][j+1]+scsc["gap"]]
            val = max(tmp_list)

            gm[i+1][j+1] = val
            x[i + 1][j + 1][:] = [int(val == i) for i in tmp_list]
            # print(x[i + 1][j + 1][:])

    # print(x)
    return x


def create_graph_matrix(_n, _m):
    """Create Graph Matrix for later computing the possible paths"""
    _graph_matrix = np.zeros((_m + 1, _n + 1), dtype=np.int)
    print("Shape matrix graph_matrix:", _graph_matrix.shape)

    _graph_matrix[0][1:] = np.arange(start=-1, stop=-_graph_matrix.shape[1], step=-1)
    _graph_matrix[1:, 0] = np.arange(start=-1, stop=-_graph_matrix.shape[0], step=-1)

    print(_graph_matrix)

    return _graph_matrix


def read_score_scheme(file_name):
    """Read file, with txt format, containing score scheme as pairs key = value"""
    _score_scheme = dict()
    with open(file_name) as f:
        rules = f.read().split("\n")
        for line in rules:
            # print(line, len(line))
            if len(line) != 0:
                key, value = line.split("=")
                _score_scheme[key.strip().lower()] = int(value.strip())

    # print(_score_scheme)
    return _score_scheme


def read_sequence_file(file_name):
    """"Read file, with txt format, containing biological sequence"""
    with open(file_name) as f:
        data_sequence = f.read()
    return list(data_sequence)


def config_work(args):
    _score_scheme = read_score_scheme(args[1])
    res = "\n ".join(['{0} : {1}'.format(k, str(v)) for k, v in _score_scheme.items()])
    print("Score Scheme\n", res)

    _subject_sequence = read_sequence_file(args[2])
    print("Subject Sequence\n", _subject_sequence)

    _query_sequence = read_sequence_file(args[3])
    print("Query String\n", _query_sequence)

    return _score_scheme, _subject_sequence, _query_sequence
