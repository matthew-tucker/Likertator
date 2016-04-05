# Likertator – A Script for Creating Likert Estimation Surveys

_Author:_
Matthew A. Tucker (Language, Mind, & Brain Laboratory,
NYU Abu Dhabi)

<http://matthew-tucker.github.io>

## Overview

Likertator is a script which creates several copies of a Likert-style acceptability estimation survey according to a Latin Square random distribution of experimental stimuli that are assumed to be sentences. This script was specially designed for the experiments reported in: Tucker, Matthew A., Ali Idrissi, Jon Sprouse, and Diogo Almeida. In Preparation. "Does grammaticalized resumption repair islands? Evidence from Standard Arabic reading." In Robert Hoberman and Matthew A. Tucker (eds.) *Perspectives on Arabic Linguistics 30: Papers from the Annual Symposium on Arabic Linguistics, Stony Brook, New York, 2016*. Amsterdam \& Philadelpha: John Benjamins. As such, it is most likely to work for designs like the experiments reported there and is specifically designed to work with Arabic in UTF-8.

## Usage

The script requires some auxiliary files that it expects to find in a file labeled `inputs/` in the same folder as `likertator.py`:

1. **A configuration file** which declares some experimental parameters in a <key> <value> format. **This file must be named `config.txt`**.
2. **A LaTeX template** defining the layout for the paper surveys themselves.
3. **A list of experimental items**.
4. **A list of filler items**.
5. **A file containing the directions to the experiment** in a separate file.

Files (2-5) are all specified in `config.txt`.

The script outputs and compiles a `.tex` file in an individual folder for each list in a directory 'outputs/'. It will create this directory if it does not already exist and ovewrite its contents without warning if it does.

## The Config File

The configuration file is a list of congfiguration parameters which are specified with the syntax `<key> <value>`. All the following parameters must be specified but can come in any order:
	
1. `no_lists`: The number of separate lists to create. Currently support is limited to a number of lists equal to the number of conditions (a complete/full Latin Square).
2. `no_conds`: The number of separate conditions in the experiment. Currently, this should equal `no_lists` for guaranteed successful operation.
3. `stimuli`: A stimuli file containing the experimental items; an example is included in `bahrain-stim.txt`
4. `fillers`: A fillers file containing the filler items to interleave with the experimental items; an example is included in `bahrain-fillers.txt`
5. `directions`: A directions file containing the directions to be inserted into the final surveys; an example is included in `Bahrain-Directions.txt`
6. `filler_ratio`: the filler:item ratio. If the number of fillers and experimental items doesn't meet this ratio, an error will be produced.
7. `template`: A template LaTeX file that specifies how to lay out the survey itself; an example template is included in `template.tex`
8. `ex_name`: The name of the experiment itself, which should be somewhat opaque as it is printed in the header of each survey.

## Formatting Supplementary Files

### Stimuli

The stimuli file should contain lines that are either complete sentences for the experiment or blank. An **item** is divided into **conditions**, one per line. An item is considered complete when a blank line appears. The script itself doesn't care about the order of conditions, but obviously it is most sensible if the items contain the same conditions in the same order, for all items.

### Fillers

The fillers must appear in a separate file, one per line, that is specified in `fillers`. The script itself supports randomizing the order of presentation of both fillers and items but does not attempt to pseudoranomize fillers and items. It is therefore possible that multiple experimental items could appear in a row if there are not many fillers. The only workaround for this at present is to inspect the output files by hand and change the order of items.

### Directions

The directions page, which will appear at the beginning of each survey, should appear in the file in `directions` and can include whatever directions are needed. LaTeX commands are supported in this file.

### Template

The `template` is the most important required file as it specifies the document-level setup for each survey. It is basically a LaTeX file with two important differences: first, for Python-string-related reasons, each instance of `{` or `}` must be doubled; so `\begin{document}` becomes `\begin{{document}}`. Moreover, the location of the experimental items/fillers must be specified with `{{{items}}}` (see the example template).

## Miscellaneous Script-Wide Choices

### Formatting Items

Items are TeXified on line 137 in the function `exify_item`. This function should be edited directly to change the formatting of the items.

### Formatting Judgments

Judgments in the included script are in Arabic and range from 1-7. To change this, edit the function `write_likert_document`, specifically lines 155-6.

### Typesetting Engine

The resulting `.tex` files are typeset with `xelatex` by default as this is the author's preference. To edit this, change line 267 in `main`.

## Version History

* 1.0/5 April 2016
