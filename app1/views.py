from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64

def generate_qr(request):
    qr_code_image = None
    if request.method == "POST":
        qr_data = request.POST.get('qr_data')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'generate_qr.html', {'qr_code_image': qr_code_image, 'qr_data': qr_data if request.method == "POST" else None})
