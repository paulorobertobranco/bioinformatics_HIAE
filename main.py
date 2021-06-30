import sys
from pathlib import Path
from typing import List, Any

import plac
from Bio.Align import PairwiseAligner


def logger(f: callable) -> Any:
    """
    Log decorator.
    Prints the task message and its status.
    :param f: function to be decorated
    :return: wrapper function
    """
    def wrapper(*args, message: str = ''):
        """"
        Inner wrapper function.
        :param message: message to be displayed
        :return: the result of the decorated function
        """
        try:
            if message:
                print(f'=> {message} .... ', end='', flush=True)
            r = f(*args)
            if message:
                print('ok')
            return r
        except Exception as e:
            print('err')
            raise e
    return wrapper


@logger
def load_reads(input_file: Path) -> List[str]:
    """
    Load reads from input file.
    :param input_file: input reads file
    :return: list of reads
    """
    input_file = Path(input_file)
    with open(input_file, 'r') as file:
        reads = list(map(lambda x: x.strip(), file.readlines()))
        if list(filter(lambda x: len(x) > 1000, reads)):
            raise Exception('Input file contains one or more reads longer than 1000 bases.')
    return reads


@logger
def save_result(reconstructed: str, output_file: Path) -> None:
    """
    Write the output file containing the chromosome string.
    :param reconstructed: chromosome
    :param output_file: output file name
    """
    if output_file:
        if reconstructed:
            with open(output_file, 'w') as file:
                file.write(reconstructed)


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

        reads = sorted(reads, key=len)
        while len(reads) != 1:

            seq_a = reads[0]
            query_reads = reads.copy()
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
                reads = query_reads + [best_alignment]
            else:
                raise Exception(f"Read {seq_a} didn't align with no one of the other reads {query_reads}.")

        return reads.pop() if reads else ""


@plac.opt('output_file', "Path to the output file", type=Path)
@plac.pos('input_file', "Path to the reads file", type=Path)
@plac.flg('v')
def main(input_file: Path, output_file: Path = 'output.txt', v: bool = False):

    try:
        reads = load_reads(
            input_file,
            message=f'Reading input file \'{input_file}\'' if v else ''
        )

        chromosome = Chromosome()
        reconstructed = chromosome.reconstruct(
            reads,
            message=f'Reconstructing chromosome based on {len(reads)} reads' if v else ''
        )

        if output_file:
            save_result(
                reconstructed,
                output_file,
                message=f'Writing output file \'{output_file}\'' if v else ''
            )

    except Exception as e:
        print(f' | {e}')
        sys.exit()


if __name__ == '__main__':
    plac.call(main)
