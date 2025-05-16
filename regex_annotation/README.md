# Regex Baseline Annotation
The script `regex_baseline.py` generates a simple annotation of people in a dataset (their birth year and year in the image caption). For every person, it generates a file named `regex_annotation.json` that has the same structure as `annotation.json` created by manual annotation using the annotation tool.

## Requirements
`regex_baseline.py` requires Python 3.x and Numpy.

## Example usage
1) Clone this repository.
2) cd into this directory:
    ```
    cd regex_annotation
    ```
3) Run the script with an ABSOLUE PATH to the dataset directory as the only argument. It should look something like this:
    ```
    python3 regex_baseline.py <path_to_LLM-wiki-mining>/annotation_tool/example_set
    ```
4) Result: every person in the dataset should now contain `regex_annotation.json` in their direcotry. `output.txt` should also be generated.
    