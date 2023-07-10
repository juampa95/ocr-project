import os
import random
import pathlib
import subprocess

training_text_file = 'test/ocra-01.training_text'  # Texto para entrenamiento

lines = []

with open(training_text_file, 'r') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

output_directory = 'tesstrain/data/ocra-01-ground-truth'  # Directorio de salida, se crea solo si no existe.

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

count = 5000

lines = lines[:count]

line_count = 0
for line in lines:
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
    with open(line_training_text, 'w') as output_file:
        output_file.writelines([line])

    file_base_name = f'ocra-01_{line_count}'  # El nombre tiene que coincidir con el de las carpetas, sino falla. 

    subprocess.run([
        'text2image',
        '--font=OCR A Extended',
        f'--text={line_training_text}',
        f'--outputbase={output_directory}/{file_base_name}',
        '--max_pages=1',
        '--degrade_image',
        '--strip_unrenderable_words',
        '--leading=20',
        '--xsize=2300',
        '--ysize=250',
        '--char_spacing=0.5',
        '--exposure=0',
        '--unicharset_file=langdata/eng.unicharset'
        '--distort_image',
        '--invert',
        '--white_noise',
        '--smooth_noise',
        '--blur',
#        '--output_individual_glyph_images',    # Esos sirven para crear imagenes individuales
#        '--glyph_resized_size=32',             # Esos sirven para crear imagenes individuales
#        '--glyph_num_border_pixels_to_pad=2'   # Esos sirven para crear imagenes individuales
    ])

    line_count += 1
