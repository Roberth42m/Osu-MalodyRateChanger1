import subprocess


def build_atempo_chain(rate):

    filters = []

    while rate > 2.0:

        filters.append("atempo=2.0")

        rate /= 2.0

    while rate < 0.5:

        filters.append("atempo=0.5")

        rate /= 0.5

    filters.append(f"atempo={rate}")

    return ",".join(filters)


def rate_audio(
    input_audio,
    output_audio,
    rate,
    keep_pitch=True
):

    # Mantener pitch
    if keep_pitch:

        atempo_filter = build_atempo_chain(rate)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_audio,
            "-filter:a",
            atempo_filter,
            output_audio,
        ]

    # Cambiar pitch
    else:

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_audio,
            "-af",
            f"asetrate=44100*{rate},aresample=44100",
            output_audio,
        ]

    subprocess.run(
        command,
        check=True
    )