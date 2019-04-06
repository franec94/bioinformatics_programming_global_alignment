import numpy as np


class GlobalAlignment:

    def __init__(self):
        self.score_scheme = dict()
        self.query_string = list()
        self.reference_string = list()

        self.graph_matrix = None
        self.paths_matrix = None

    def __init__(self, query_string, reference_string, score_scheme):
        self.score_scheme = score_scheme
        self.query_string = query_string
        self.reference_string = reference_string

        self.graph_matrix = None
        self.paths_matrix = None

    def create_graph_matrix(self):
        m, n = len(self.query_string), len(self.reference_string)
        graph_matrix = np.zeros((m + 1, n + 1), dtype=np.int)
        print("Shape matrix graph_matrix:", graph_matrix.shape)

        graph_matrix[0][1:] = np.arange(start=-1, stop=-graph_matrix.shape[1], step=-1)
        graph_matrix[1:, 0] = np.arange(start=-1, stop=-graph_matrix.shape[0], step=-1)

        self.graph_matrix = graph_matrix

    def calculate_paths(self):

        self.create_graph_matrix()

        m, n = len(self.query_string) + 1, len(self.reference_string) + 1

        x = np.zeros((m + 1, n + 1, 3))
        x[:, 0][0] = 1
        x[0, :][3] = 1

        gm = self.graph_matrix
        qs = self.query_string
        rs = self.reference_string
        score = self.score_scheme

        val = max(gm[m - 1, :])
        print("max: ", val)

        for i in range(0, m - 1):
            t = qs[i]

            for j in range(0, n - 1):
                t2 = rs[j]
                res = score["match"] if t == t2 else score["mismatch"]

                tmp_list = [res + gm[i][j], gm[i + 1][j] + score["gap"], gm[i][j + 1] + score["gap"]]
                val = max(tmp_list)

                gm[i + 1][j + 1] = val
                x[i + 1][j + 1][:] = [int(val == i) for i in tmp_list]
                # print(x[i + 1][j + 1][:])

        # print(x)
        self.paths_matrix = x

    def show_paths(self,):

        gm = self.graph_matrix
        qs = self.query_string
        rs = self.reference_string
        pm = self.paths_matrix

        m, n = gm.shape
        val = max(gm[m-1, :])
        print("max: ", val)

        for i in range(1, n):
            item = gm[m-1, i]
            if item == val:
                print("bottom coordinates:", m-1, i)
                sol = list()
                sol.insert(0, qs[m - 2])

                r, c = m-1, i
                z = m-3
                while r != 0 and c != 0:
                    tmp_list = pm[r, c][:]
                    # print(tmp_list)

                    if tmp_list[0] == 1:
                        r, c = r-1, c-1

                        if z < 0:
                            sol.insert(0, '-')
                        else:
                            sol.insert(0, qs[z])
                        z -= 1
                    elif tmp_list[1] == 1:
                        c = c - 1
                        sol.insert(0, '-')
                    elif tmp_list[2] == 1:
                        r = r - 1
                        sol.insert(0, '-')
                # sol = (n - 1 - i) * ['-']
                sol.extend((n-1 - len(sol)) * ['-'])
                print(rs)
                print(sol)
