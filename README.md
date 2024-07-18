# random_scripts
These are simple repo that stores some random (hopefully useful) scripts that I made a long the way.

#### `rename_arxiv_files.py`

Renames all the arXiv pdfs in a folder to the paper's name, and optionally, includes year. 

Usage: `python rename_arxiv_files.py ~/papers_folder --include-year`. If you are afraid of messing things up, use the ` --dry-run` option that only give you the `mv` commands to execute.

#### `mobilesam_dir_single_point.py`

This script take all the images inside a folder and request a single point from the user to segment the desired object (single one per image). It's quite useful for annotating a bunch of images quickly. Is based on the awesome [MobileSAM](https://github.com/ChaoningZhang/MobileSAM).

⚠️ This script was moved to https://github.com/gustavofuhr/mobilesam_annotator since it a part of a annotation project.

#### `check_realmadrid_tickets.py`

This is a (maybe weird) script that uses Selenium to check if match tickets are available on the Real Madrid website. The main reason I created this was to receive an e-mail as soon as possible to buy the tickets fast, since they quickly sell out. It is supposed to run until a change appears in the match card (which may represent tickets going on sale), then it will send you an email notifying you ([check code line](https://github.com/gustavofuhr/random_scripts/blob/c540ad7ebb790dca36afa9b41e2e871278f15a4f/check_realmadrid_ticket.py#L72)). It also sends periodic emails (every 30 minutes) telling you that it is still checking the website, so that you can notice if the script stops running. 

The main function is `check_ticket_availability` and you can change it to the match date that you're looking for. You will also need to put your gmail address and app key ([you can make one here](https://myaccount.google.com/apppasswords)) at [the start of the script](https://github.com/gustavofuhr/random_scripts/blob/c540ad7ebb790dca36afa9b41e2e871278f15a4f/check_realmadrid_ticket.py#L15).


