from typing import Any, List
from pathlib import Path


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
            if message:
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