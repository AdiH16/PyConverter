from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    CHOICES = (('png', 'PNG'), ('jpg', 'JPEG'), ('pdf', 'PDF'), ('bmp', 'BMP'), ('ico', 'ICO'), ('tiff', 'TIFF'), ('webp', 'WEBP'),
                ('csv', 'CSV'), ('xlsx', 'XLSX'), 
                ('mp3', 'MP3'), ('wav', 'WAV'), ('flac', 'FLAC'), ('ogg', 'OGG'), 
                ('mp4', 'MP4'), ('avi', 'AVI'), ('mov', 'MOV'), ('gif', 'GIF'),
                ('pdf', 'PDF'), ('docx', 'DOCX'), ('txt', 'TXT'),
                ('zip', 'ZIP'), ('tar', 'TAR'), ('rar', 'RAR'), ('7z', '7Z'))
    target_format  = forms.ChoiceField(choices=CHOICES)