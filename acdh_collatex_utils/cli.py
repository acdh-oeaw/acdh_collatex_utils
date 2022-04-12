"""Console script for acdh_collatex_utils."""
import click

from . acdh_collatex_utils import CxCollate


@click.command()  # pragma: no cover
@click.option('-g', '--glob-pattern', default='./fixtures/*.xml', show_default=True)  # pragma: no cover
@click.option('--nr/--r', default=False, show_default=True)  # pragma: no cover
def collate(glob_pattern, nr):  # pragma: no cover
    """Console script to flatten XML/TEI files of a work."""
    new_glob_pattern = f"{glob_pattern}"
    print(new_glob_pattern)
    output_dir = new_glob_pattern.replace("*.xml", 'collated')

    out = CxCollate(
        glob_pattern=new_glob_pattern,
        glob_recursive=nr,
        output_dir=output_dir,
        char_limit=False
    ).collate()
    for x in out:
        click.echo(
            click.style(
                f"finished saving: {x}\n",
                fg='green'
            )
        )

    click.echo(
        click.style(
            "\n################################\n",
            fg='green'
        )
    )
