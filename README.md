

![Portfolio Screenshot](https://media-hosting.imagekit.io/f9e1ec05d7c54aa6/Screenshot%20(330).png?Expires=1841413121&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Rp2fjQtUwXabnoOmkYfxuUqm~rCL4BkOHg9eWl5XkC9pq0Q0Cg2aOYrJq3PV3PBvRgReqoRGIUxoLnbLTsjzXfSw5Dl4~4J7U3Ubq67wZ1c7PYtj6YkfLKgYTX08EYUFhxEqAlX-0FVnxAE~OaJ2IQnUjD11dyW0mQymNGiBbHBGLak8vsa0TXdHC6CPt49UGhGaxmLCMvWXXRbLwvNnN4Msy0sETetf3KbsEw85WXVjTIQ9BPqp5FkToayo9cgTrROw8uJE6U5FK5plNXF3Yg9EfSEgL6tUBLK0ecaz8xWOM6kbl5dydRfBk8b9Yr4FxvtuOZnxo0wYs7sXB8~KHg__)



# QR Code Generation and Database Integration Project

## Project Description
This project aims to create a system for generating unique QR codes and linking them to a MySQL database, allowing each QR code to be scanned a limited number of times before becoming invalid. It is ideal for event invitations, entry passes, or any use case where controlled access is required.

## Features
- **Unique QR Code Generation** for each invitation or entry pass.
- **Usage Limit Control** for each QR code.
- **Real-time Scan Verification** with automatic database updates.
- **Admin Dashboard** to view and download all QR codes.
- **MySQL Database Integration** for secure data storage.
- **Responsive Design** for mobile and desktop devices.

## Requirements
- Python 3.12
- Django
- MySQL
- qrcode
- pillow
- OpenCV (for scanning operations)

## Getting Started
1. **Install Requirements**:
    ```bash
    pip install django mysqlclient qrcode pillow opencv-python
    ```

2. **Database Setup**:
    - Create a MySQL database named `qr_codes`.
    - Add a table named `qr_codes` to store the QR code data.

3. **Run the Django Server**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

4. **Create QR Codes**:
    - Add new QR codes via the admin panel or the custom control panel included in the project.

5. **Scan and Verify QR Codes**:
    - When a QR code is scanned, the system will verify the usage count and update the database.

## Contributing
Contributions are welcome! Feel free to open pull requests or report issues on GitHub.

## License
This project is licensed under the MIT License.
