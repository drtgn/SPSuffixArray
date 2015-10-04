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
        for i in range(len(seq_array)):
            self.seqs[i] = seq_array[i]
        for seq_id in self.seqs:
            seq = self.seqs[seq_id]
            for i in range(0, len(seq)-self.mmem+1, 1):
                kmer = seq[i:i+self.mmem]
                self.karray.append((kmer, seq_id, i))
        self.karray = sorted(self.karray)

    def match(self):
        '''
        Forms a kmer match dictionary. This dictionary stores kmers which match with how many times they match. This
        info will be used in the next step to start from the highest matching kmers to start forming shared nodes.

        To do: I should put kmers which appear multiple times (match) into a separate array. This should speed up the
        process of filtering later on. Filtering will be needed to remove kmers which are already extended.
        :return:
        '''
        for i in range(0, len(self.karray)-1, 1):
            current_item = self.karray[i]
            next_item = self.karray[i+1]
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

if __name__ == '__main__':
    ar = KArray(['I hardly ever find lice but she has tons of nits & they just wont come',
                 "loosen them. my heart breaks for her when weekend after weekend she has to go ever",
                 ' ever'], 5)
    for item in ar.karray:
        print item

    ar.match()
    print ar.matches