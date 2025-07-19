import os
import cv2  # OpenCV for QR code decoding

def decode_qr_code(image_path):
    """Decodes a QR code from an image using OpenCV (no external DLLs needed)."""
    try:
        img = cv2.imread(image_path)
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(img)
        return data if data else None
    except Exception as e:
        print(f"Error decoding QR code from {image_path}: {e}")
        return None

def reconstruct_secret(qr_code_folder="qr_codes"):
    """Decodes all QR codes in a folder and reconstructs the secret."""
    shares = []
    qr_code_files = sorted([f for f in os.listdir(qr_code_folder) if f.endswith(".png")])

    if not qr_code_files:
        print(f"No QR code images found in the '{qr_code_folder}' folder.")
        return None

    for filename in qr_code_files:
        image_path = os.path.join(qr_code_folder, filename)
        print(f"Decoding {filename}...")
        decoded_share = decode_qr_code(image_path)
        if decoded_share is not None:
            shares.append(decoded_share)
        else:
            print(f"Could not decode QR code from {filename}. Reconstruction may be incomplete.")

    if shares:
        reconstructed_secret = "".join(shares)
        return reconstructed_secret
    else:
        return None

if __name__ == "__main__":
    print("Decoding QR codes and reconstructing the secret...")
    reconstructed = reconstruct_secret()

    if reconstructed:
        print(f"\nReconstructed Secret: {reconstructed}")
    else:
        print("\nCould not reconstruct the secret.")
