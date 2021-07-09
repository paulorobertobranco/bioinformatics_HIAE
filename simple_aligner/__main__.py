import sys
from pathlib import Path

import plac

from src.chromossome import Chromosome
from src.utils import load_reads, save_result


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
        if v:
            print(f' | {e}')
        sys.exit()


if __name__ == '__main__':
    plac.call(main)
