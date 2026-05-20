import os

from reamber.osu.OsuMap import OsuMap


def rate_maps(
    osu_files,
    rate,
    new_audio_filename
):

    for osu_path in osu_files:

        osu_map = OsuMap.read_file(osu_path)

        # BPM original
        original_bpm = osu_map.bpms[0].bpm

        # BPM nuevo
        new_bpm = original_bpm * rate

        # Ratear mapa
        osu_map = osu_map.rate(rate)

        # Actualizar audio
        osu_map.audio_file_name = new_audio_filename

        # Cambiar nombre de dificultad
        osu_map.version = (
            f"{osu_map.version} "
        f"[{rate:.2f}x | {new_bpm:.1f} BPM]"
        )

        # Nuevo nombre
        file_name = os.path.basename(osu_path)

        file_name_no_ext = os.path.splitext(
            file_name
        )[0]

        new_name = (
            f"{file_name_no_ext}_{rate:.2f}x.osu"
        )

        new_path = os.path.join(
            os.path.dirname(osu_path),
            new_name,
        )

        # Guardar nuevo mapa
        osu_map.write_file(new_path)

        # Eliminar viejo
        os.remove(osu_path)