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


def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq, 'rb') as f1, open(ficDer, 'rb') as f2:
        cab1 = leer_cabecera(f1)
        cab2 = leer_cabecera(f2)

        if cab1["channels"] != 1 or cab2["channels"] != 1:
            raise ValueError("Ambos deben ser mono")

        if cab1["rate"] != cab2["rate"]:
            raise ValueError("Frecuencias no coinciden")

        data1 = f1.read()
        data2 = f2.read()

    L = struct.unpack('<' + 'h'*(len(data1)//2), data1)
    R = struct.unpack('<' + 'h'*(len(data2)//2), data2)

    stereo = [val for pair in zip(L, R) for val in pair]

    packed = struct.pack('<' + 'h'*len(stereo), *stereo)

    with open(ficEste, 'wb') as f:
        escribir_cabecera(f, 2, cab1["rate"], 16, len(packed))
        f.write(packed)
