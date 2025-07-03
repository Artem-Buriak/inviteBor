import qrcode
from PIL import Image
import argparse

def generate_qr_code(link, filename):
    """
    Generates a QR code from a given link and saves it as a PNG file.

    Args:
        link (str): The URL or text to encode in the QR code.
        filename (str): The desired filename for the output PNG image.
    """
    if not filename.lower().endswith(".png"):
        filename += ".png"

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"Successfully generated QR code and saved it as '{filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to run the QR code generator program.
    """
    parser = argparse.ArgumentParser(description="Generate a QR code from a link.")
    parser.add_argument("link", help="The link to generate the QR code for.")
    parser.add_argument("filename", help="The desired filename for the QR code (e.g., 'my_qr_code').")

    args = parser.parse_args()

    generate_qr_code(args.link, args.filename)

if __name__ == "__main__":
    main()
