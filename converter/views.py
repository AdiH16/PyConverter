from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from .forms import UploadFileForm
from .utils import convert_file
import os

def serve_file(request, file_path):
    # Make sure to delete the file after it's been served
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
    return response

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_file = request.FILES['file']
            target_format = request.POST.get('target_format')

            # Save the uploaded file temporarily
            fs = FileSystemStorage()
            filename = fs.save(input_file.name, input_file)
            uploaded_file_path = fs.path(filename)
            
            try:
                # Call convert_file with the path to the temporary file
                output_file_path = convert_file(uploaded_file_path, '.' + target_format)

                # Don't forget to clean up the temporary file when you're done
                os.remove(uploaded_file_path)

                return serve_file(request, output_file_path)
            except Exception as e:
                os.remove(uploaded_file_path)
                return HttpResponse(f"Error: {str(e)}")

        else:
            context = {'form': form}
            return render(request, 'converter/upload_file.html', context)

    else:
        form = UploadFileForm()
        context = {'form': form}
        return render(request, 'converter/upload_file.html', context)
