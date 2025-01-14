import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
from django.shortcuts import render

def generate_qr_code(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        
        if data:
            # Generate the QR Code
            qr = qrcode.make(data)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Convert QR code to base64 for displaying in HTML
            qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

            # Store QR code in session history
            qr_history = request.session.get('qr_history', [])
            qr_history.append({'data': data, 'qr_image': qr_image_base64})
            request.session['qr_history'] = qr_history

            # Create the downloadable response
            response = HttpResponse(buffer, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
            return response

    # Retrieve QR code history from session
    qr_history = request.session.get('qr_history', [])
    return render(request, 'QR.html', {'qr_history': qr_history})