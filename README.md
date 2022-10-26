# VGMU - batchTSVParser

## Usage
To use this utility, enter the following in the command line (assuming Python 3 is installed on your computer)
`python songParser`
To see the parameters you can (and must) use, enter
`python songParser --help`

**note**: *in order to use this utility, you must be on the same level as it, NOT WITHIN IT*

## Example use
1. Place your CSV and TSV files into `./sources`
2. run `python songParser sources`

Your new JSON files will be placed in the `./_new` and `./_old` directories - the former uses a slightly different system that legacy projects dislike.