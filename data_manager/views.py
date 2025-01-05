import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
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

import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse

def fetch_golf_data(request):
    file_name = request.GET.get('file_name')  # Get file_name from the query parameters

    if not file_name:
        return JsonResponse({'error': 'No file name provided'}, status=400)
    
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, 'golf_files', file_name)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return JsonResponse({'error': f'File "{file_name}" not found at {file_path}'}, status=404)

    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Validate required columns
        required_columns = ['Player Name', 'Overall_Cumulative_Score', 'Round', 'Hole']
        if not all(col in data.columns for col in required_columns):
            return JsonResponse({
                'error': f'Missing required columns. Expected: {required_columns}'
            }, status=400)

        # Filter data for Round 4, Hole 18
        round_4_hole_18_data = data[(data['Round'] == 4) & (data['Hole'] == 18)]

        # Check if there are any results for Round 4, Hole 18
        if round_4_hole_18_data.empty:
            return JsonResponse({'error': 'No data available for Round 4, Hole 18'}, status=404)

        # Get top 10 golfers based on their Overall_Cumulative_Score at Round 4, Hole 18
        top_golfers = round_4_hole_18_data.groupby('Player Name')['Overall_Cumulative_Score'].max().nlargest(10)

        # Prepare the response data
        golfer_scores = [{
            'name': golfer,
            'score_round_4': score
        } for golfer, score in top_golfers.items()]

        response_data = {
            'top_golfers': golfer_scores
        }

        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)
