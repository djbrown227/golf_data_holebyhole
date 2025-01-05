import os
from django.conf import settings
from django.shortcuts import render

def file_list(request):
    # Path to the directory where golf files are stored
    golf_files_dir = os.path.join(settings.MEDIA_ROOT, 'golf_files')

    # Check if the directory exists
    if os.path.exists(golf_files_dir):
        # List all files in the directory
        files = [{'name': file} for file in os.listdir(golf_files_dir) if file]  # Filter out empty names
    else:
        files = []  # If the directory doesn't exist, return an empty list

    print(files)  # Debug: Print the files list to check its content
    return render(request, 'index.html', {'files': files})



from django.http import FileResponse, Http404
import os
from django.conf import settings

def download_file(request, file_name):
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, 'golf_files', file_name)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and send it as a downloadable attachment
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        # Return a 404 error if the file doesn't exist
        raise Http404("File does not exist")
