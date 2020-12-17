"""Console script for acdh_collatex_utils."""
import sys
import click

from . acdh_collatex_utils import CUSTOM_XSL, CHUNK_SIZE, CxCollate


@click.command()  # pragma: no cover
@click.option('-g', '--glob-pattern', default='./fixtures/*.xml', show_default=True)  # pragma: no cover
@click.option('-o', '--output-dir', default='./tmp', show_default=True)  # pragma: no cover
@click.option('--nr/--r', default=False, show_default=True)  # pragma: no cover
def collate(glob_pattern, output_dir, nr):  # pragma: no cover
    """Console script to flatten XML/TEI files of a work."""
    out = CxCollate(glob_pattern=glob_pattern, glob_recursive=nr, output_dir=output_dir, char_limit=False).collate()
    for x in out:
        click.echo(
            click.style(
                f"finished saving: {x}\n",
                fg='green'
            )
        )

    click.echo(
        click.style(
            f"\n################################\n",
            fg='green'
        )
    )
