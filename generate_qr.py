import qrcode
import os

def split_secret(secret, num_shares):
    """Splits the secret into a specified number of shares."""
    share_length = len(secret) // num_shares
    remainder = len(secret) % num_shares
    shares = []
    start = 0
    for i in range(num_shares):
        length = share_length + (1 if i < remainder else 0)
        shares.append(secret[start : start + length])
        start += length
    return shares

def generate_qr_codes(shares, base_filename="share"):
    """Generates QR codes for each share and saves them as PNG images."""
    if not os.path.exists("qr_codes"):
        os.makedirs("qr_codes")
    for i, share in enumerate(shares):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(share)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = os.path.join("qr_codes", f"{base_filename}_{i+1}.png")
        img.save(filename)
        print(f"QR code saved to: {filename}")

if __name__ == "__main__":
    secret = input("Enter your secret message: ")
    num_shares = int(input("Enter the number of shares to create: "))

    shares = split_secret(secret, num_shares)
    generate_qr_codes(shares)

    print("\nQR code generation complete. You can find the QR code images in the 'qr_codes' folder.")