import os
import zipfile


def create_osz(
    source_dir,
    output_path
):

    with zipfile.ZipFile(
        output_path,
        'w',
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, _, files in os.walk(source_dir):

            for file in files:

                full_path = os.path.join(
                    root,
                    file
                )

                arcname = os.path.relpath(
                    full_path,
                    source_dir
                )

                zipf.write(
                    full_path,
                    arcname
                )