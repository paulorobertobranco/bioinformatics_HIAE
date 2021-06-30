import os
from pathlib import Path

from pytest import mark, fixture, raises

from main import Chromosome, load_reads, save_result
from test.question_5_generate_input import generate_input


@fixture(scope='module')
def chromosome():
    chrm = Chromosome()
    return chrm


@fixture(scope='function')
def random_input_10_reads():
    yield generate_input()
    os.remove('example_data/generated_input.txt')


@fixture(scope='function')
def random_input_20_reads():
    yield generate_input(20)
    os.remove('example_data/generated_input.txt')


@fixture(scope='function')
def random_input_50_reads():
    yield generate_input(50)
    os.remove('example_data/generated_input.txt')


def test_load_reads():
    assert len(load_reads('example_data/input.txt')) == 4


def test_load_reads_file_not_found_exception():
    with raises(FileNotFoundError):
        load_reads('example_data/input.tt')


def test_load_reads_file_not_found_exception():
    with raises(FileNotFoundError):
        load_reads('example_data/input.tt')


def test_load_reads_file_read_longer_exception():
    with raises(Exception):
        load_reads('example_data/input_longer.txt')


@mark.parametrize(
    'expected',
    [
        'ATTAGACCTG',
        'CCTGCCGGAA',
        'AGACCTGCCG',
        'GCCGGAATAC'
    ]
)
def test_check_default_reads(expected):
    str_reads = list(map(lambda x: str(x), load_reads('example_data/input.txt')))
    assert expected in str_reads


def test_random_input_10_reads(chromosome, random_input_10_reads):
    reads = load_reads('example_data/generated_input.txt')
    reconstructed = chromosome.reconstruct(reads)
    assert random_input_10_reads == reconstructed


def test_random_input_20_reads(chromosome, random_input_20_reads):
    reads = load_reads('example_data/generated_input.txt')
    reconstructed = chromosome.reconstruct(reads)
    assert random_input_20_reads == reconstructed


def test_random_input_50_reads(chromosome, random_input_50_reads):
    reads = load_reads('example_data/generated_input.txt')
    reconstructed = chromosome.reconstruct(reads)
    assert random_input_50_reads == reconstructed


def test_write_output(chromosome, random_input_10_reads):
    reads = load_reads('example_data/generated_input.txt')
    reconstructed = chromosome.reconstruct(reads)
    output = Path('test_output.txt')
    save_result(reconstructed, output)
    assert output.is_file()
    os.remove(output)


