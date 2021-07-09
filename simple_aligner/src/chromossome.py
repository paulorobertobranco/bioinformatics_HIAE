from typing import List

from Bio.Align import PairwiseAligner

from .utils import logger


class Chromosome:
    """
    Chromosome class.
    This class align multiple read sequences and merge them into an chromosome sequence.
    """

    def __init__(self):
        """
        Class initializer.
        """
        self._aligner = PairwiseAligner()
        self._aligner.mode = 'local'
        self._aligner.mismatch = -1000
        self._aligner.internal_gap_score = -1000
        self._aligner.internal_open_gap_score = -1000
        self._aligner.internal_extend_gap_score = -1000

    @logger
    def reconstruct(self, reads: List[str]) -> str:
        """
        Align and merge a list of read sequences.
        :param reads: list of reads
        :return: chromosome
        """
        _reads = reads.copy()
        _reads = sorted(_reads, key=len)
        while len(_reads) != 1:

            seq_a = _reads[0]
            query_reads = _reads.copy()
            query_reads.remove(seq_a)

            best_score = 0
            best_alignment = []
            best_query = ""

            for seq_b in query_reads:
                alignments = self._aligner.align(seq_a, seq_b)
                alignments = sorted(alignments, key=lambda x: x.score, reverse=True)

                if alignments:
                    no_gap_alignment = alignments[0]
                    if best_score < no_gap_alignment.score:
                        if len(no_gap_alignment.aligned[0]) != 1:
                            continue

                        if len(seq_b) // 2 > no_gap_alignment.score and seq_b in reads:
                            continue

                        alignment_seq_a = no_gap_alignment.aligned[0][0]
                        alignment_seq_b = no_gap_alignment.aligned[1][0]

                        if alignment_seq_b[0] == 0 and alignment_seq_a[1] == len(seq_a):
                            best_alignment = seq_a[:alignment_seq_a[0]] + seq_b
                            best_score = no_gap_alignment.score
                            best_query = seq_b

                        elif alignment_seq_a[0] == 0 and alignment_seq_b[1] == len(seq_b):
                            best_alignment = seq_b[:alignment_seq_b[0]] + seq_a
                            best_score = no_gap_alignment.score
                            best_query = seq_b

            if best_alignment:
                query_reads.remove(best_query)
                _reads = query_reads + [best_alignment]
            else:
                raise Exception(f"Read {seq_a} didn't align with no one of the other reads.")

        return _reads.pop() if _reads else ""
