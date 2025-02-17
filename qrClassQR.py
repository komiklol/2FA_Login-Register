import qrcode, io, base64


class qrCodeQR:
    def __init__(self, data):
        # Initialize the qrCode class with the data to encode in the QR code
        self.data = data

    def generate_qr(self):
        # Create a QRCode object with specific configurations
        qr = qrcode.QRCode(
            version=1,  # Version of the QR code (defines size)
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
            box_size=10,  # Size of each QR code box
            border=4,  # Border size around the QR code
        )
        # Add data to the QR code
        qr.add_data(self.data)
        # Generate the QR code
        qr.make(fit=True)
        # Create the QR code image with specified colors
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to an in-memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        # Encode the image data in base64 and return it as a string
        return base64.b64encode(buffer.getvalue()).decode("utf-8")