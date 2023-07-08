from PIL import Image
import os
import pandas as pd
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PyPDF2 import PdfFileReader
from reportlab.pdfgen import canvas
from docx import Document
from pdf2docx import Converter
import patoolib

def convert_file(input_path, output_extension):
    input_extension = os.path.splitext(input_path)[1].lower()
    print("Input path without extension:", input_extension)
    print("Output extension:", output_extension)
    output_path = os.path.splitext(input_path)[0] + output_extension

    if input_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.ico', '.tiff', '.webp'] and output_extension in  ['.jpg', '.jpeg', '.png', '.bmp', '.ico', '.tiff', '.webp']:
        img = Image.open(input_path)
        try:
            img.save(output_path)
        except IOError:
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
                img.save(output_path)
            else:
                raise
    elif input_extension in ['.csv', '.xlsx'] and output_extension in ['.csv', '.xlsx']:
        df = pd.read_excel(input_path) if input_extension == '.xlsx' else pd.read_csv(input_path)
        df.to_excel(output_path, index=False) if output_extension == '.xlsx' else df.to_csv(output_path, index=False)
    elif input_extension in ['.mp3', '.wav', '.flac', '.ogg'] and output_extension in ['.mp3', '.wav', '.flac', '.ogg']:
        audio = AudioSegment.from_file(input_path, format=input_extension[1:])
        audio.export(output_path, format=output_extension[1:])
    elif input_extension in ['.mp4', '.avi', '.mov', '.gif'] and output_extension in ['.mp4', '.avi', '.mov', '.gif']:
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path, codec='libx264')
    elif input_extension == '.txt' and output_extension == '.pdf':
        with open(input_path, 'r') as f:
            text = f.read()
        c = canvas.Canvas(output_path)
        for i, line in enumerate(text.split('\n')):
            c.drawString(100, 800 - i * 14, line)
        c.save()
    elif input_extension == '.pdf' and output_extension == '.txt':
        pdf = PdfFileReader(input_path)
        text = '\n'.join(page.extract_text() for page in pdf.pages)
        with open(output_path, 'w') as f:
            f.write(text)
    elif input_extension == '.docx' and output_extension == '.pdf':
        from pdf2docx import convert
        convert(input_path, output_path)
    elif input_extension == '.pdf' and output_extension == '.docx':
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    elif input_extension in ['.zip', '.tar', '.rar', '.7z'] and output_extension in ['.zip', '.tar', '.rar', '.7z']:
        temp_dir = 'temp'
        patoolib.extract_archive(input_path, outdir=temp_dir)
        patoolib.create_archive(output_path, (temp_dir,))
    else:
        raise ValueError(f'Cannot convert {input_extension} to {output_extension}.') 
    
    return output_path
    