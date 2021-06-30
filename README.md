# bioinformatics_HIAE

## About

Implementation of **HIAE challenge | question 5**.

## Problem Definition

Given `n` DNA strings whose size does not exceed 
1000 bases, and that from these `n` reads it is 
possible to build an entire chromosome by 
aligning pairs of reads that overlap more than 
half their size, the goal is to return the 
superstring of smallest possible dimension containing 
all strings (this is equivalent in this problem to 
being able to reconstruct a chromosome).

**Input EXAMPLE (input.txt)**:
- ATTAGACCTG
- CCTGCCGGAA
- AGACCTGCCG
- GCCGGAATAC

**Output EXAMPLE (output.txt)**: 
- ATTAGACCTGCCGGAATAC

Write a script in a language of your choice to receive an input.txt file and the output will be an output.txt file containing the superstring.

## Usage

**Warning**: This solution was coded using Python 3,

To run the script, you first need to install 
the requirements:

```python
pip install -r requirements.txt
```

Then, simple run:
```python
python main.py [input_file]
```

A file named `output.txt` will be created in the 
current directory containing the resulting
chromosome.

## Tests

To run the test suite, simple run:
```python
pytest -v .
```