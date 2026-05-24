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


def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste, 'rb') as f:
        cab = leer_cabecera(f)

        if cab["channels"] != 2:
            raise ValueError("El fichero no es estéreo")

        data = f.read()

    muestras = struct.unpack('<' + 'h' * (len(data)//2), data)

    L = muestras[0::2]
    R = muestras[1::2]

    if canal == 0:
        mono = L
    elif canal == 1:
        mono = R
    elif canal == 2:
        mono = [(l + r)//2 for l, r in zip(L, R)]
    elif canal == 3:
        mono = [(l - r)//2 for l, r in zip(L, R)]
    else:
        raise ValueError("Canal inválido")

    packed = struct.pack('<' + 'h'*len(mono), *mono)

    with open(ficMono, 'wb') as f:
        escribir_cabecera(f, 1, cab["rate"], 16, len(packed))
        f.write(packed)
