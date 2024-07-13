# random_scripts
These are simple repo that stores some random (hopefully useful) scripts that I made a long the way.

#### `rename_arxiv_files.py`

Renames all the arXiv pdfs in a folder to the paper's name, and optionally, includes year. 

Usage: `python rename_arxiv_files.py ~/papers_folder --include-year`. If you are afraid of messing things up, use the ` --dry-run` option that only give you the `mv` commands to execute.

#### `mobilesam_dir_single_point.py`

This script take all the images inside a folder and request a single point from the user to segment the desired object (single one per image). It's quite useful for annotating a bunch of images quickly. Is based on the awesome [MobileSAM](https://github.com/ChaoningZhang/MobileSAM).

⚠️ This script was moved to https://github.com/gustavofuhr/mobilesam_annotator since it a part of a annotation project.




