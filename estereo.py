import struct

def leer_cabecera(f):
    riff, size, wave = struct.unpack('<4sI4s', f.read(12))

    if riff != b'RIFF' or wave != b'WAVE':
        raise ValueError("No es WAV válido")

    fmt_id, fmt_size = struct.unpack('<4sI', f.read(8))

    if fmt_id != b'fmt ':
        raise ValueError("Falta fmt")

    fmt_data = f.read(fmt_size)

    audio_format, num_channels, sample_rate, byte_rate, block_align, 
bits_per_sample = struct.unpack(
        '<HHIIHH', fmt_data[:16]
    )

    data_id, data_size = struct.unpack('<4sI', f.read(8))

    if data_id != b'data':
        raise ValueError("Falta data")

    return {
        "channels": num_channels,
        "rate": sample_rate,
        "bits": bits_per_sample,
        "size": data_size
    }
