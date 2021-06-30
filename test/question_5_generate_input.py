from random import choice, shuffle


def generate_input(number_of_reads=10, read_length=50):
    alphabet = 'ATCG'
    chromosome = ""
    seqs = []

    for read in range(number_of_reads):
        if read == 0:
            seq = ""
            for base in range(read_length):
                seq += choice(alphabet)
            chromosome += seq
        else:
            seq = chromosome[-read_length//2:]
            while len(seq) < read_length:
                seq += choice(alphabet)
            chromosome += seq[-read_length//2:]
        seqs.append(seq + '\n')
    shuffle(seqs)
    with open('example_data/generated_input.txt', 'w') as file:
        file.writelines(seqs)

    return chromosome
