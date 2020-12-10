=====
Usage
=====

Collate files and save HTML2 output
--------

To use CollateX Utils in a project::

    import glob
    from datetime import datetime

    from collatex import *
    from acdh_collatex_utils.acdh_collatex_utils import *
    from acdh_collatex_utils.collatex_patch import visualize_table_vertically_with_colors

    glob_pattern = f"./acdh_collatex_utils/**/*.xml"
    files = glob.glob(
        glob_pattern,
        recursive=False
    )

    collation = Collation()
    for x in files:
      doc = CxReader(xml=x)
      wit = doc.collatex_wit
      collation.add_plain_witness(wit[0], wit[1])

    start_time = datetime.now()
    print(f"{start_time}")
    table = collate(collation)
    end_time = datetime.now()
    print(f"{end_time}")
    print(f"{end_time - start_time}")

    with open('out.html', 'w') as f:
      print(
        visualize_table_vertically_with_colors(
          table,
          collation
        ),
        file=f
      )
