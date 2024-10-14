import base64
from io import BytesIO
import numpy as np
import os
from PIL import Image
import uuid

from django.http import HttpResponse
from pyzbar.pyzbar import decode
from .form import QRCodeForm
from django.conf import settings
from django.shortcuts import render
import cv2
import os
import qrcode
from openpyxl import Workbook, load_workbook
import sqlite3

# المسار لحفظ الصورة
IMAGE_PATH = os.path.join(os.path.dirname(os.getcwd()), r'media\image.jpg')


def login_with_qr_code(image_path):
    # قراءة الصورة من المسار
    image_path = image_path.replace('\\','/')
    img = cv2.imread(image_path)

    if img is None:
        print("can,t get imge in this path")
        return

    # استخدام QRCodeDetector لاكتشاف وقراءة الباركود
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if data:
        print("id QR Code:")
        print(data)

        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('qr_codes.db')
        c = conn.cursor()

        # التحقق من المعرف وعدد مرات الاستخدام المتبقية
        c.execute("SELECT num_uses,used FROM qr_codes where id=?", (data.replace("qr_id:", ''),))
        result = c.fetchone()
        print('result', result)

        if result:
            num_uses, used = result
            if used < num_uses:
                # السماح بالدخول وتحديث الاستخدام

                c.execute("UPDATE qr_codes SET used = used + 1 WHERE id=?", (data.replace('qr_id:', ''),))
                conn.commit()
                return ("Okay, you are allowed to enter")
            else:
                return (" Sorry, this QR code has been overused.")
        else:

            return ("ID QR code cannot be found ")
        conn.close()
    else:
        return ("The QR Code cannot be found in this image. Make sure that the code is visible and clear, then try again")


def detect_qr_codes(frame):
    # البحث عن الأكواد في الصورة
    qr_codes = decode(frame)
    return qr_codes


############################################
def scancode(request):
    image_path = None  # Initialize the image_path to None
    login_return = 'Scan Qr Code To Show The Result'
    if request.method == 'POST':
        try:
            image_data = request.POST['image_data']
            # Extract base64 data
            header, encoded = image_data.split(',', 1)
            # Decode the image data
            image_data = base64.b64decode(encoded)

            # Prepare the path for saving the image
            media_path = os.path.join(settings.MEDIA_ROOT, 'images')  # Ensure this folder exists
            os.makedirs(media_path, exist_ok=True)  # Create the folder if it doesn't exist

            # Save the image
            image_name = 'captured_image.jpg'  # You can change the filename or use a unique ID
            image_path = os.path.join(media_path, image_name)
            with open(image_path, 'wb') as f:
                f.write(image_data)

            # Prepare the path for rendering in the template

            print(image_path)
            login_return = login_with_qr_code(os.path.join(os.path.dirname(os.getcwd()), r'QrCode\media\images\captured_image.jpg'))

        except Exception as e:
            print("Error in scancode view:", e)
            return HttpResponse("An error occurred while processing your request.")

    # Render the image page with the image path if available
    return render(request, 'scan.html', {'image_path': 'media/images/captured_image.jpg', 'login_return': login_return})


# إنشاء قاعدة بيانات لتخزين معرفات QR
def create_database():
    conn = sqlite3.connect('qr_codes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS qr_codes
                 (id TEXT PRIMARY KEY, used INTEGER)''')
    conn.commit()
    conn.close()


def qrCodeGenerate(request):
    try:
        form = QRCodeForm(request.POST)

        if form.is_valid():
            # الحصول على عدد أكواد QR وعدد مرات الاستخدام
            num_qr_codes = form.cleaned_data['num_qr_codes']
            num_uses = form.cleaned_data['num_uses']

            # مسار حفظ الصور
            folder = "media"
            if not os.path.exists(folder):
                os.makedirs(folder)  # إنشاء المجلد إذا لم يكن موجودًا

            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect('qr_codes.db')
            c = conn.cursor()

            # إنشاء جدول qr_codes إذا لم يكن موجودًا
            c.execute('''CREATE TABLE IF NOT EXISTS qr_codes
                         (id TEXT PRIMARY KEY, num_uses INTEGER, used INTEGER DEFAULT 0)''')

            # مسار الصورة الخارجية التي تريد دمج الباركود معها
            background_image_path = r'media\borderimge.jpg'  # تأكد من وجود الصورة

            # إنشاء أكواد QR ودمجها مع الصورة الخارجية
            qr_image_paths = []
            for _ in range(num_qr_codes):
                qr_id = str(uuid.uuid4())  # إنشاء معرّف فريد
                qr_image_path = os.path.join(folder, f"{qr_id}_{num_uses}.png")

                # إنشاء QR Code
                qr_data = f"{qr_id}"
                qr = qrcode.make(qr_data)

                # فتح الصورة الخارجية
                background_image = Image.open(background_image_path)

                # دمج QR Code فوق الصورة الخارجية
                qr = qr.resize((500, 500))  # تغيير حجم الباركود إذا لزم الأمر
                background_image.paste(qr, (200, 550))  # تعديل الإحداثيات (50, 50) حسب الموقع الذي تريده

                # حفظ الصورة النهائية بعد الدمج
                background_image.save(qr_image_path)
                qr_image_paths.append(qr_image_path)

                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO qr_codes (id, num_uses, used) VALUES (?, ?, ?)", (qr_id, num_uses, 0))

            conn.commit()
            conn.close()

            return render(request, 'qr_success.html', {'qr_image_paths': qr_image_paths})
    except Exception as ee:
        print(ee)
        form = QRCodeForm()

    return render(request, 'create_qr_codes.html', {'form': form})


####################################################
def createqrcode(request):
    return qrCodeGenerate(request)


def display_all_qr_codes(request):
    # تحديد المسار الذي يحتوي على ملفات الـ QR
    media_dir = os.path.join(settings.MEDIA_ROOT)

    # الحصول على جميع الملفات في هذا المجلد
    qr_codes = []
    for filename in os.listdir(media_dir):
        if filename.endswith(".png"):  # يمكنك تخصيص هذه الصيغة حسب تنسيق صورك
            qr_codes.append(os.path.join(settings.MEDIA_URL, filename))

    return render(request, 'all_qr_codes.html', {'qr_codes': qr_codes})


def base(request):
    return render(request, 'base.html')
