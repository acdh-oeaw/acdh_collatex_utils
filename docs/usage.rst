=====
Usage
=====

Collate files and save HTML2 output
--------

To use CollateX Utils in a project::

    from acdh_collatex_utils.acdh_collatex_utils import CxCollate

    out = CxCollate(output_dir='./fixtures').collate()

Command line
--------

Collate Documents via command line::

    $ collate -g "/home/csae8092/Desktop/hansifreud/**/*iii-die-*.xml" -o '/home/csae8092/Desktop/collate/out
