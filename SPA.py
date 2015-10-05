__author__ = 'SteamPowered'


class KArray:
    def __init__(self, seq_array, kmer_len):
        '''
        The first step of the algorithm is to construct the kmer array which also stores the sequence id and index in
        the sequence. This array is sorted.
        :param seq_array: array of sequences. str array
        :param kmer_len: kmer length
        :return:
        '''
        self.seqs = {}
        self.karray = []
        self.matches = {}
        self.mmem = kmer_len
        self.graph = {}
        self.node_id = 0
        for i in range(len(seq_array)):
            self.seqs[i] = seq_array[i]
        for seq_id in self.seqs:
            seq = self.seqs[seq_id]
            for i in range(0, len(seq) - self.mmem + 1, 1):
                kmer = seq[i:i + self.mmem]
                self.karray.append((kmer, seq_id, i))
        self.karray = sorted(self.karray)

    def node_caster(self, value=1):
        '''
        increase/decrease node id
        :param value: in/decrement value, int
        :return:
        '''
        self.node_id += value

    def match(self):
        '''
        Forms a kmer match dictionary. This dictionary stores kmers which match with how many times they match. This
        info will be used in the next step to start from the highest matching kmers to start forming shared nodes.

        To do: I should put kmers which appear multiple times (match) into a separate array. This should speed up the
        process of filtering later on. Filtering will be needed to remove kmers which are already extended.
        :return:
        '''
        for i in range(0, len(self.karray) - 1, 1):
            current_item = self.karray[i]
            next_item = self.karray[i + 1]
            currentk = current_item[0]
            nextk = next_item[0]
            if currentk == nextk:
                try:
                    self.matches[currentk][0] += 1
                    self.matches[currentk][1].append(next_item)
                except KeyError:
                    self.matches[currentk] = [2, []]
                    self.matches[currentk][1].append(next_item)
                    self.matches[currentk][1].append(current_item)
        self.matches = sorted(self.matches.values(), reverse=True)
        match_list = [[]]
        for matches in self.matches:
            for match in matches[1]:
                match_list[-1].append(match)
            match_list.append([])
        self.matches = match_list

    def extend_matches(self):
        '''
        Algo:
        1. Extends matches, starting from most matched ones. --> done
        2. Adds the extended match as a node into the graph object. --> done
        3. Filters out the overlapping ones.
        4. Repeats the process until the matches are empty
        :return:
        '''
        while len(self.matches) != 1:
            matches = self.matches[0]
            letters = ["*"]
            m = ''
            i = 0
            while len(set(letters)) == 1:  # Walk forward while all share the same letter/nucleotide
                m += letters[0]
                letters = []
                for match in matches:
                    try:
                        letters.append(self.seqs[match[1]][match[2] + i])
                    except IndexError:
                        letters = [1, 2]
                        break
                i += 1
            m = m[1:]
            before_m = ''
            letters = [""]
            i = 1
            while len(set(letters)) == 1:  # Walk back while all share the same letter/nucleotide
                before_m = letters[0] + before_m
                letters = []
                for match in matches:
                    idx = match[2] - i
                    if idx > -1:
                        letters.append(self.seqs[match[1]][idx])
                    else:
                        letters = [1, 2]
                        break
                i += 1
            length = len(m) + len(before_m)
            self.graph[self.node_id] = {'to': [],
                                        'contains': [(x[1], x[2] - len(before_m), x[2] + len(m) - self.mmem) for x
                                                     in matches],
                                        'length': length, 'mem': before_m+m}
            self.matches = self.matches[1:]
            # From here on in this loop should take care of the filtering.
            # Should be made into a multi process..
            element = self.graph[self.node_id]['contains'][0]
            to_del = []
            for num in range(len(self.matches)):
                for match in self.matches[num]:
                    if match[1] == element[0] and element[1] <= match[2] <= element[2]:
                        to_del.append(num)
            for del_idx in sorted(to_del, reverse=True):
                del self.matches[del_idx]
            self.node_caster()

    def build_graph(self):
        '''
        No idea !!!
        :return:
        '''
        return 0

if __name__ == '__main__':
    ar = KArray(['TTCCTCAAAAACTTTTTGTTACGACCAGCATCATCTTCAGTTTCTACACTCTTCTAATTCGACCTTTCGT'
                 'TTTAAACGACTCCTCCAATTAACATGCCTTACGCTCCTGGTGACGCTGGAAAGGGTGCTGGTCTCTTCAA'
                 'GACCCGCTGTTCTCAATGCCACACCCTCGGCCAGGGTGAGCCTCACAAAGTTGGCCCTAACCTTCACGGT'
                 'CTTTTCGGCCGCAAGACTGGTCAAGCCGAAAACTACTCATACACGGCCGCCAACGTCAACAAGGGTATCA'
                 'CCTGGGACGAGACCACTCTCTTTGAGTACCTCGAGAATCCCAAGAAGTACATCCCTGGAACGAAAATGGC'
                 'CTTCGCAGGTTTGAAGAAGGAAAAAGACAGGAATGACCTCATCACCCACCTCAAGGAGGCTACTGCTTAA'
                 'AACGCTTTCCCCATTATCCCTATGAAGGACATGAGGATAGGTTGAAGACTTTACACGCTATATCCATAAT'
                 'ACCAACTTAATATTTTATTGGCTTCCCGCCAGTCTTGTTTATGTCTTCTAGATTACATAGATGGTGTTAC'
                 'GTGTAGCGCTTATGACGAGTGAGGTAGTTCCCTCTCTCCACAACCCCCACTCCGTGAATAGATGTTGATG'
                 'TTTCGTT'],
                5)

    ar.match()
    ar.extend_matches()
    for node in ar.graph:
        print ar.graph[node]
    print len(ar.graph)
