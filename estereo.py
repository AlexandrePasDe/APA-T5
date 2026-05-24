import struct

def leer_cabecera(f):
    riff, size, wave = struct.unpack('<4sI4s', f.read(12))
ø
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


def leer_muestras_estereo(f, data_size):
    data = f.read(data_size)
    muestras = struct.unpack('<' + 'h' * (data_size // 2), data)

    # separar canales
    izquierda = muestras[0::2]
    derecha = muestras[1::2]

    return izquierda, derecha


