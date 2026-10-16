"""
Synthetic KYC Document Generator for PoC Testing
Creates realistic mock identity cards (PAN, Aadhaar, Passport) and a Blurry document
so users can immediately test all features without uploading personal credentials.
"""

import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent / "app" / "static" / "samples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_default_font(size: int = 20):
    try:
        # Standard Windows fonts
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("segoeui.ttf", size)
        except Exception:
            return ImageFont.load_default()


def create_pan_card(filename: str = "sample_pan.png", blur: bool = False):
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color=(235, 243, 250))
    draw = ImageDraw.Draw(img)

    # Decorative header
    draw.rectangle([(0, 0), (width, 80)], fill=(24, 76, 120))
    draw.rectangle([(0, 80), (width, 86)], fill=(218, 165, 32))

    font_header = get_default_font(22)
    font_sub = get_default_font(15)
    font_label = get_default_font(14)
    font_value = get_default_font(18)
    font_pan = get_default_font(26)

    # Header Text
    draw.text((40, 15), "INCOME TAX DEPARTMENT", fill=(255, 255, 255), font=font_header)
    draw.text((40, 48), "GOVT. OF INDIA", fill=(220, 235, 250), font=font_sub)
    draw.text((480, 30), "PERMANENT ACCOUNT NUMBER CARD", fill=(255, 255, 255), font=font_sub)

    # Photo Box
    draw.rectangle([(50, 110), (200, 290)], fill=(210, 215, 225), outline=(100, 110, 130), width=2)
    draw.text((90, 190), "[ PHOTO ]", fill=(100, 110, 130), font=font_sub)

    # Signature Box
    draw.rectangle([(50, 310), (200, 370)], fill=(255, 255, 255), outline=(160, 170, 180), width=1)
    draw.text((70, 330), "V. R. Sharma", fill=(20, 20, 80), font=font_value)
    draw.text((95, 375), "Signature", fill=(120, 120, 120), font=font_label)

    # Card Fields
    x_offset = 240
    # Name
    draw.text((x_offset, 110), "Name / नाम", fill=(100, 110, 120), font=font_label)
    draw.text((x_offset, 130), "VIKRAM RAJESH SHARMA", fill=(20, 30, 50), font=font_value)

    # Father's Name
    draw.text((x_offset, 175), "Father's Name / पिता का नाम", fill=(100, 110, 120), font=font_label)
    draw.text((x_offset, 195), "RAJESH MOHAN SHARMA", fill=(20, 30, 50), font=font_value)

    # Date of Birth
    draw.text((x_offset, 240), "Date of Birth / जन्म की तारीख", fill=(100, 110, 120), font=font_label)
    draw.text((x_offset, 260), "14/07/1988", fill=(20, 30, 50), font=font_value)

    # Permanent Account Number (PAN)
    draw.rectangle([(x_offset - 10, 320), (width - 60, 390)], fill=(255, 255, 255), outline=(24, 76, 120), width=2)
    draw.text((x_offset + 10, 325), "Permanent Account Number :", fill=(80, 90, 100), font=font_label)
    draw.text((x_offset + 10, 345), "ABCDE1234F", fill=(180, 20, 20), font=font_pan)

    # Security Chip / Hologram simulation
    draw.rectangle([(width - 150, 110), (width - 70, 190)], fill=(220, 200, 120), outline=(180, 160, 80), width=2)
    draw.text((width - 140, 140), "SECURITY", fill=(140, 120, 40), font=font_label)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))

    # If blur requested, reload and apply Gaussian blur to force Laplacian < 100
    if blur:
        cv_img = cv2.imread(str(out_path))
        # Heavy blur to ensure variance drops below 100
        blurred = cv2.GaussianBlur(cv_img, (27, 27), 9.0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        var = cv2.Laplacian(gray, cv2.CV_64F).var()
        print(f"Generated Blurry PAN variance: {var:.2f} (Target < 100)")
        cv2.imwrite(str(out_path), blurred)
    else:
        cv_img = cv2.imread(str(out_path))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        var = cv2.Laplacian(gray, cv2.CV_64F).var()
        print(f"Generated Sharp PAN variance: {var:.2f} (Target >= 100)")


def generate_qr_pil_image(payload: str, size: int = 140) -> Image.Image:
    enc = cv2.QRCodeEncoder_create()
    mat = enc.encode(payload)
    resized = cv2.resize(mat, (size, size), interpolation=cv2.INTER_NEAREST)
    return Image.fromarray(resized).convert("RGB")


def create_aadhaar_card(filename: str = "sample_aadhaar.png", tampered_qr: bool = False):
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Tricolor stripe top
    draw.rectangle([(0, 0), (width, 20)], fill=(255, 153, 51))
    draw.rectangle([(0, 20), (width, 40)], fill=(255, 255, 255))
    draw.rectangle([(0, 40), (width, 60)], fill=(19, 136, 8))

    font_header = get_default_font(20)
    font_sub = get_default_font(15)
    font_label = get_default_font(15)
    font_value = get_default_font(18)
    font_aadhaar = get_default_font(30)

    # Headers
    draw.text((120, 75), "GOVERNMENT OF INDIA", fill=(20, 30, 50), font=font_header)
    draw.text((120, 102), "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", fill=(80, 90, 100), font=font_sub)

    # Photo Box
    draw.rectangle([(50, 150), (200, 330)], fill=(230, 235, 240), outline=(150, 160, 170), width=2)
    draw.text((90, 230), "[ PHOTO ]", fill=(120, 130, 140), font=font_sub)

    # Details
    x_offset = 240
    draw.text((x_offset, 160), "PRIYA ANAND VERMA", fill=(20, 30, 50), font=font_value)
    
    draw.text((x_offset, 205), "DOB: 22/11/1995", fill=(20, 30, 50), font=font_value)
    draw.text((x_offset, 245), "Gender: FEMALE", fill=(20, 30, 50), font=font_value)

    # Embed Secure Digital QR Code
    if tampered_qr:
        # Deliberate mismatch: visual card says "PRIYA ANAND VERMA", but digital QR says "SURESH KUMAR GUPTA"
        qr_payload = '<PrintLetterBarcodeData uid="991289012345" name="SURESH KUMAR GUPTA" gender="M" yob="1978" co="S/O Mohan Gupta" vtc="Jaipur" state="Rajasthan" pc="302001"/>'
    else:
        qr_payload = '<PrintLetterBarcodeData uid="541289012345" name="PRIYA ANAND VERMA" gender="F" yob="1995" co="D/O Anand Verma" vtc="Delhi" state="Delhi" pc="110016"/>'

    qr_pil = generate_qr_pil_image(qr_payload, size=140)
    img.paste(qr_pil, (width - 200, 160))
    draw.rectangle([(width - 200, 160), (width - 60, 300)], outline=(40, 40, 40), width=1)

    # Red divider line
    draw.rectangle([(40, 360), (width - 40, 364)], fill=(200, 30, 30))

    # Aadhaar Number
    draw.text((220, 385), "5412  8901  2345", fill=(180, 20, 20), font=font_aadhaar)
    
    # Bottom Tagline
    draw.rectangle([(0, 460), (width, 500)], fill=(24, 76, 120))
    draw.text((280, 470), "Mera Aadhaar, Meri Pehchan", fill=(255, 255, 255), font=font_sub)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))

    cv_img = cv2.imread(str(out_path))
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"Generated Aadhaar variance: {var:.2f}")


def create_passport_page(filename: str = "sample_passport.png"):
    width, height = 800, 550
    img = Image.new("RGB", (width, height), color=(248, 244, 235))
    draw = ImageDraw.Draw(img)

    # Top border
    draw.rectangle([(0, 0), (width, 50)], fill=(15, 30, 60))
    
    font_header = get_default_font(20)
    font_sub = get_default_font(14)
    font_label = get_default_font(13)
    font_value = get_default_font(17)
    font_mrz = get_default_font(18)

    draw.text((40, 15), "REPUBLIC OF INDIA / भारत गणराज्य", fill=(255, 255, 255), font=font_header)
    draw.text((600, 15), "PASSPORT / पासपोर्ट", fill=(255, 255, 255), font=font_header)

    # Photo box
    draw.rectangle([(40, 80), (190, 270)], fill=(225, 220, 210), outline=(120, 110, 100), width=2)
    draw.text((80, 170), "[ PHOTO ]", fill=(110, 100, 90), font=font_sub)

    # Metadata Grid
    draw.text((220, 75), "Type / प्रकार", fill=(120, 120, 120), font=font_label)
    draw.text((220, 95), "P", fill=(20, 20, 20), font=font_value)

    draw.text((320, 75), "Country Code / कोड", fill=(120, 120, 120), font=font_label)
    draw.text((320, 95), "IND", fill=(20, 20, 20), font=font_value)

    draw.text((480, 75), "Passport No. / पासपोर्ट क्र.", fill=(120, 120, 120), font=font_label)
    draw.text((480, 95), "Z1234567", fill=(180, 20, 20), font=get_default_font(22))

    draw.text((220, 135), "Surname / उपनाम", fill=(120, 120, 120), font=font_label)
    draw.text((220, 155), "DESHMUKH", fill=(20, 20, 20), font=font_value)

    draw.text((220, 195), "Given Name(s) / दिया गया नाम", fill=(120, 120, 120), font=font_label)
    draw.text((220, 215), "ANANYA", fill=(20, 20, 20), font=font_value)

    draw.text((220, 255), "Nationality / राष्ट्रीयता", fill=(120, 120, 120), font=font_label)
    draw.text((220, 275), "INDIAN", fill=(20, 20, 20), font=font_value)

    draw.text((380, 255), "Sex / लिंग", fill=(120, 120, 120), font=font_label)
    draw.text((380, 275), "FEMALE", fill=(20, 20, 20), font=font_value)

    draw.text((500, 255), "Date of Birth / जन्म तिथि", fill=(120, 120, 120), font=font_label)
    draw.text((500, 275), "05/03/1991", fill=(20, 20, 20), font=font_value)

    # MRZ Band simulation at bottom
    draw.rectangle([(20, 420), (width - 20, 520)], fill=(240, 235, 220), outline=(180, 170, 160), width=1)
    draw.text((40, 440), "P<INDDESHMUKH<<ANANYA<<<<<<<<<<<<<<<<<<<<<<", fill=(30, 30, 30), font=font_mrz)
    draw.text((40, 475), "Z1234567<4IND9103056F3103057<<<<<<<<<<<<<<<4", fill=(30, 30, 30), font=font_mrz)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))

    cv_img = cv2.imread(str(out_path))
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"Generated Passport variance: {var:.2f}")


def create_aadhaar_letter(filename: str = "sample_aadhaar_letter.png"):
    """
    Generates a full-page A4 UIDAI Aadhaar Letter Scan (tall aspect ratio ~1.44)
    with top letterhead, recipient address block (To \n <Citizen Name>),
    middle instructions/helpline, and the bottom 40% cutout identity card.
    """
    width, height = 800, 1150
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 1. Top Letterhead Header
    draw.rectangle([(0, 0), (width, 16)], fill=(255, 153, 51))
    draw.rectangle([(0, 16), (width, 32)], fill=(255, 255, 255))
    draw.rectangle([(0, 32), (width, 48)], fill=(19, 136, 8))

    font_title = get_default_font(21)
    font_sub = get_default_font(14)
    font_body = get_default_font(15)
    font_label = get_default_font(13)
    font_bold = get_default_font(17)
    font_card_num = get_default_font(26)
    font_micro = get_default_font(14)

    draw.text((60, 65), "GOVERNMENT OF INDIA", fill=(20, 30, 50), font=font_title)
    draw.text((60, 95), "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", fill=(70, 80, 95), font=font_sub)

    # Enrollment & Issue metadata (tests non-DOB date exclusion on letterhead)
    draw.rectangle([(width - 320, 65), (width - 40, 130)], fill=(245, 248, 252), outline=(200, 215, 230), width=1)
    draw.text((width - 305, 75), "Enrollment No: 1234/56789/01234", fill=(50, 60, 75), font=font_label)
    draw.text((width - 305, 100), "Issue Date: 12/03/2023", fill=(50, 60, 75), font=font_label)

    # Divider line
    draw.rectangle([(40, 145), (width - 40, 147)], fill=(220, 225, 230))

    # 2. Recipient Address Block (Citizen Name directly under "To")
    draw.text((60, 165), "To", fill=(40, 50, 60), font=font_bold)
    draw.text((60, 195), "RAHUL KUMAR VERMA", fill=(10, 20, 40), font=font_bold)
    draw.text((60, 225), "S/O Ramesh Kumar Verma", fill=(60, 70, 80), font=font_body)
    draw.text((60, 250), "124 Green Park Colony, Sector 14", fill=(60, 70, 80), font=font_body)
    draw.text((60, 275), "New Delhi - 110016", fill=(60, 70, 80), font=font_body)
    draw.text((60, 300), "Mobile: 98XXXXXX10", fill=(60, 70, 80), font=font_body)

    # QR Code / Barcode Simulation in middle
    draw.rectangle([(width - 230, 175), (width - 60, 310)], fill=(245, 245, 245), outline=(150, 150, 150), width=1)
    draw.text((width - 195, 235), "[ UIDAI QR ]", fill=(90, 90, 90), font=font_sub)

    # Middle Information & Helplines
    draw.rectangle([(40, 345), (width - 40, 470)], fill=(250, 252, 255), outline=(210, 225, 240), width=1)
    draw.text((60, 360), "Your Aadhaar Number is your identity throughout India.", fill=(24, 76, 120), font=font_bold)
    draw.text((60, 390), "• It helps you avail various government welfare services and subsidies seamlessly.", fill=(70, 80, 90), font=font_sub)
    draw.text((60, 415), "• Keep your mobile number & email updated in Aadhaar for online verifications.", fill=(70, 80, 90), font=font_sub)
    draw.text((60, 440), "Help Line: 1947 | Email: help@uidai.gov.in | Website: www.uidai.gov.in", fill=(24, 76, 120), font=font_sub)

    # 3. Cutout Scissor Line
    scissor_y = 520
    draw.line([(40, scissor_y), (width - 40, scissor_y)], fill=(180, 180, 180), width=1)
    draw.text((260, scissor_y - 10), "✂  Fold or Cut Here / यहाँ से काटें  ✂", fill=(130, 130, 130), font=font_label)

    # 4. BOTTOM 40% IDENTITY CARD CUTOUT REGION (y = 580 to 1100)
    card_y_start = 580
    card_y_end = 1080
    card_x_start = 50
    card_x_end = width - 50

    # Card outer border
    draw.rectangle([(card_x_start, card_y_start), (card_x_end, card_y_end)], fill=(255, 255, 255), outline=(180, 190, 205), width=2)

    # Card header tricolor band
    draw.rectangle([(card_x_start, card_y_start), (card_x_end, card_y_start + 12)], fill=(255, 153, 51))
    draw.rectangle([(card_x_start, card_y_start + 12), (card_x_end, card_y_start + 24)], fill=(255, 255, 255))
    draw.rectangle([(card_x_start, card_y_start + 24), (card_x_end, card_y_start + 36)], fill=(19, 136, 8))

    # Card Government Header
    draw.text((card_x_start + 30, card_y_start + 45), "GOVERNMENT OF INDIA / भारत सरकार", fill=(20, 30, 50), font=font_bold)
    draw.text((card_x_start + 30, card_y_start + 70), "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", fill=(80, 90, 100), font=font_sub)

    # Citizen Photo Box
    photo_top = card_y_start + 105
    draw.rectangle([(card_x_start + 30, photo_top), (card_x_start + 175, photo_top + 170)], fill=(235, 240, 245), outline=(160, 170, 180), width=2)
    draw.text((card_x_start + 70, photo_top + 75), "[ PHOTO ]", fill=(120, 130, 140), font=font_sub)

    # Citizen Details in Micro-Font
    cx = card_x_start + 200
    draw.text((cx, photo_top + 10), "RAHUL KUMAR VERMA", fill=(10, 20, 40), font=font_bold)
    draw.text((cx, photo_top + 50), "DOB: 15/08/1990", fill=(20, 30, 50), font=font_micro)
    draw.text((cx, photo_top + 85), "Gender: MALE", fill=(20, 30, 50), font=font_micro)

    # Embed Secure Digital QR Code on Aadhaar Letter Card
    letter_qr_payload = '<PrintLetterBarcodeData uid="541289012345" name="RAHUL KUMAR VERMA" gender="M" yob="1990" co="S/O Ramesh Kumar Verma" vtc="New Delhi" state="Delhi" pc="110016"/>'
    letter_qr_pil = generate_qr_pil_image(letter_qr_payload, size=140)
    img.paste(letter_qr_pil, (card_x_end - 170, photo_top + 10))
    draw.rectangle([(card_x_end - 170, photo_top + 10), (card_x_end - 30, photo_top + 150)], outline=(60, 60, 60), width=1)

    # Red divider bar
    bar_y = card_y_start + 320
    draw.rectangle([(card_x_start + 20, bar_y), (card_x_end - 20, bar_y + 4)], fill=(200, 30, 30))

    # Bold Aadhaar Number
    draw.text((card_x_start + 180, bar_y + 25), "5412  8901  2345", fill=(180, 20, 20), font=font_card_num)

    # Bottom Tagline Ribbon
    ribbon_y = card_y_end - 40
    draw.rectangle([(card_x_start, ribbon_y), (card_x_end, card_y_end)], fill=(24, 76, 120))
    draw.text((card_x_start + 200, ribbon_y + 10), "Mera Aadhaar, Meri Pehchan", fill=(255, 255, 255), font=font_sub)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))

    cv_img = cv2.imread(str(out_path))
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"Generated Aadhaar Letter variance: {var:.2f} (Dimensions: {width}x{height})")


def create_marksheet(filename: str = "sample_10th_marksheet.png"):
    width, height = 900, 1150
    img = Image.new("RGB", (width, height), color=(253, 253, 250))
    draw = ImageDraw.Draw(img)

    # Header border & banner
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(30, 60, 114), width=3)
    draw.rectangle([(30, 30), (width - 30, 140)], fill=(30, 60, 114))

    font_title = get_default_font(24)
    font_sub = get_default_font(15)
    font_bold = get_default_font(16)
    font_regular = get_default_font(14)
    font_table_hdr = get_default_font(14)

    draw.text((150, 45), "CENTRAL BOARD OF SECONDARY EDUCATION", fill=(255, 255, 255), font=font_title)
    draw.text((220, 85), "SECONDARY SCHOOL EXAMINATION (CLASS X) 2023", fill=(220, 235, 255), font=font_sub)
    draw.text((290, 110), "MARKS STATEMENT & PERFORMANCE CERTIFICATE", fill=(255, 215, 0), font=font_sub)

    # Candidate Profile Box
    box_y = 160
    draw.rectangle([(50, box_y), (width - 50, box_y + 160)], fill=(245, 248, 252), outline=(180, 200, 220), width=1)
    
    draw.text((70, box_y + 15), "Candidate / Student Name:", fill=(80, 90, 100), font=font_regular)
    draw.text((270, box_y + 15), "ROHAN ANAND GUPTA", fill=(10, 25, 50), font=font_bold)

    draw.text((70, box_y + 45), "Roll Number:", fill=(80, 90, 100), font=font_regular)
    draw.text((270, box_y + 45), "26184920", fill=(10, 25, 50), font=font_bold)

    draw.text((500, box_y + 45), "Passing Year:", fill=(80, 90, 100), font=font_regular)
    draw.text((620, box_y + 45), "2023", fill=(10, 25, 50), font=font_bold)

    draw.text((70, box_y + 75), "School / Institution:", fill=(80, 90, 100), font=font_regular)
    draw.text((270, box_y + 75), "DELHI PUBLIC SCHOOL, R.K. PURAM, NEW DELHI", fill=(10, 25, 50), font=font_bold)

    draw.text((70, box_y + 105), "Mother's Name:", fill=(80, 90, 100), font=font_regular)
    draw.text((270, box_y + 105), "SUNITA GUPTA", fill=(10, 25, 50), font=font_bold)

    draw.text((500, box_y + 105), "Father's Name:", fill=(80, 90, 100), font=font_regular)
    draw.text((620, box_y + 105), "ANAND PRAKASH GUPTA", fill=(10, 25, 50), font=font_bold)

    # Marks Table Header
    tbl_y = 350
    draw.rectangle([(50, tbl_y), (width - 50, tbl_y + 40)], fill=(41, 128, 185))
    draw.text((70, tbl_y + 10), "SUB CODE", fill=(255, 255, 255), font=font_table_hdr)
    draw.text((180, tbl_y + 10), "SUBJECT NAME", fill=(255, 255, 255), font=font_table_hdr)
    draw.text((450, tbl_y + 10), "THEORY (80)", fill=(255, 255, 255), font=font_table_hdr)
    draw.text((580, tbl_y + 10), "PRACTICAL (20)", fill=(255, 255, 255), font=font_table_hdr)
    draw.text((720, tbl_y + 10), "TOTAL (100)", fill=(255, 255, 255), font=font_table_hdr)
    draw.text((820, tbl_y + 10), "GRADE", fill=(255, 255, 255), font=font_table_hdr)

    subjects = [
        ("184", "ENGLISH LNG & LIT", "71", "18", "089", "A1"),
        ("085", "HINDI COURSE-B", "68", "19", "087", "A2"),
        ("041", "MATHEMATICS STANDARD", "76", "20", "096", "A1"),
        ("086", "SCIENCE - THEORY", "72", "19", "091", "A1"),
        ("087", "SOCIAL SCIENCE", "70", "19", "089", "A1"),
        ("165", "COMPUTER APPLICATIONS", "48", "49", "097", "A1"),
    ]

    row_y = tbl_y + 40
    for idx, (code, name, th, pr, tot, gr) in enumerate(subjects):
        bg = (248, 250, 252) if idx % 2 == 0 else (255, 255, 255)
        draw.rectangle([(50, row_y), (width - 50, row_y + 45)], fill=bg, outline=(220, 225, 230), width=1)
        draw.text((70, row_y + 12), code, fill=(50, 50, 50), font=font_regular)
        draw.text((180, row_y + 12), name, fill=(20, 30, 40), font=font_bold)
        draw.text((470, row_y + 12), th, fill=(50, 50, 50), font=font_regular)
        draw.text((610, row_y + 12), pr, fill=(50, 50, 50), font=font_regular)
        draw.text((735, row_y + 12), tot, fill=(10, 25, 50), font=font_bold)
        draw.text((835, row_y + 12), gr, fill=(20, 100, 20), font=font_bold)
        row_y += 45

    # Summary Row
    draw.rectangle([(50, row_y), (width - 50, row_y + 60)], fill=(235, 243, 250), outline=(30, 60, 114), width=2)
    draw.text((70, row_y + 20), "OVERALL RESULT: PASS", fill=(20, 120, 40), font=font_bold)
    draw.text((320, row_y + 20), "AGGREGATE: 452 / 500 (90.4%)", fill=(30, 60, 114), font=font_bold)
    draw.text((650, row_y + 20), "OVERALL GRADE: A1", fill=(30, 60, 114), font=font_bold)

    # Signatures & Seals
    sig_y = row_y + 140
    draw.text((100, sig_y), "Controller of Examinations", fill=(80, 90, 100), font=font_regular)
    draw.text((600, sig_y), "Principal, Delhi Public School", fill=(80, 90, 100), font=font_regular)
    draw.text((380, sig_y + 50), "Date of Issue: 22/05/2023", fill=(100, 100, 100), font=font_regular)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))
    print(f"Generated Marksheet sample: {out_path}")


def create_resume(filename: str = "sample_resume.png"):
    width, height = 900, 1200
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Top Header Banner
    draw.rectangle([(0, 0), (width, 160)], fill=(37, 51, 65))

    font_name = get_default_font(28)
    font_role = get_default_font(18)
    font_contact = get_default_font(13)
    font_section = get_default_font(17)
    font_bold = get_default_font(15)
    font_text = get_default_font(13)

    draw.text((50, 30), "PRIYA S. SHARMA", fill=(255, 255, 255), font=font_name)
    draw.text((50, 75), "Senior Full-Stack Software Engineer", fill=(110, 207, 246), font=font_role)
    draw.text((50, 115), "Email: priya.sharma@techmail.com  |  Phone: +91 98765 43210  |  Bengaluru, India  |  LinkedIn: linkedin.com/in/priyasharma", fill=(220, 230, 240), font=font_contact)

    # Section 1: Professional Summary
    sy = 190
    draw.text((50, sy), "PROFESSIONAL SUMMARY", fill=(37, 51, 65), font=font_section)
    draw.line([(50, sy + 25), (width - 50, sy + 25)], fill=(37, 51, 65), width=2)
    draw.text((50, sy + 35), "Accomplished software engineer with 5+ years of experience building resilient cloud-native web applications,", fill=(50, 60, 70), font=font_text)
    draw.text((50, sy + 55), "FastAPI microservices, and reactive React dashboards. Specialized in OCR pipelines and document automation.", fill=(50, 60, 70), font=font_text)

    # Section 2: Technical Skills
    sy = 300
    draw.text((50, sy), "TECHNICAL SKILLS", fill=(37, 51, 65), font=font_section)
    draw.line([(50, sy + 25), (width - 50, sy + 25)], fill=(37, 51, 65), width=2)
    draw.text((50, sy + 35), "Languages & Frameworks: Python, FastAPI, TypeScript, React.js, Node.js, Next.js, Django", fill=(40, 50, 60), font=font_text)
    draw.text((50, sy + 60), "Data & AI: Gemini Vision API, OpenCV, EasyOCR, PostgreSQL, Redis, Elasticsearch", fill=(40, 50, 60), font=font_text)
    draw.text((50, sy + 85), "DevOps & Cloud: Docker, Kubernetes, AWS (S3, Lambda, EC2), CI/CD GitHub Actions", fill=(40, 50, 60), font=font_text)

    # Section 3: Professional Experience
    sy = 440
    draw.text((50, sy), "PROFESSIONAL EXPERIENCE", fill=(37, 51, 65), font=font_section)
    draw.line([(50, sy + 25), (width - 50, sy + 25)], fill=(37, 51, 65), width=2)

    # Job 1
    draw.text((50, sy + 38), "TechCorp Solutions Pvt Ltd  —  Senior Full-Stack Engineer", fill=(20, 30, 40), font=font_bold)
    draw.text((650, sy + 38), "July 2022 – Present | Bengaluru", fill=(100, 110, 120), font=font_text)
    draw.text((70, sy + 65), "• Architected high-throughput KYC verification microservice processing 200,000+ IDs monthly.", fill=(50, 60, 70), font=font_text)
    draw.text((70, sy + 88), "• Integrated Gemini Vision and OpenCV quality evaluation reducing manual verification time by 82%.", fill=(50, 60, 70), font=font_text)
    draw.text((70, sy + 111), "• Mentored 6 junior engineers and spearheaded automated unit and edge-case testing.", fill=(50, 60, 70), font=font_text)

    # Job 2
    draw.text((50, sy + 150), "InnovateSoft Technologies  —  Software Development Engineer", fill=(20, 30, 40), font=font_bold)
    draw.text((650, sy + 150), "June 2019 – June 2022 | Pune", fill=(100, 110, 120), font=font_text)
    draw.text((70, sy + 175), "• Built scalable REST APIs with Python/FastAPI serving over 1M daily active users.", fill=(50, 60, 70), font=font_text)
    draw.text((70, sy + 198), "• Enhanced database query performance in PostgreSQL, decreasing P99 latency from 450ms to 65ms.", fill=(50, 60, 70), font=font_text)

    # Section 4: Education
    sy = 710
    draw.text((50, sy), "EDUCATION", fill=(37, 51, 65), font=font_section)
    draw.line([(50, sy + 25), (width - 50, sy + 25)], fill=(37, 51, 65), width=2)
    draw.text((50, sy + 40), "Bachelor of Technology (B.Tech) in Computer Science & Engineering", fill=(20, 30, 40), font=font_bold)
    draw.text((50, sy + 65), "National Institute of Technology (NIT), Surathkal", fill=(80, 90, 100), font=font_text)
    draw.text((650, sy + 65), "Passing Year: 2019  |  CGPA: 8.8 / 10.0", fill=(20, 120, 40), font=font_bold)

    # Section 5: Certifications
    sy = 830
    draw.text((50, sy), "CERTIFICATIONS", fill=(37, 51, 65), font=font_section)
    draw.line([(50, sy + 25), (width - 50, sy + 25)], fill=(37, 51, 65), width=2)
    draw.text((50, sy + 40), "• AWS Certified Solutions Architect – Associate (2023)", fill=(50, 60, 70), font=font_text)
    draw.text((50, sy + 65), "• DeepLearning.AI Prompt Engineering for Developers (2024)", fill=(50, 60, 70), font=font_text)

    out_path = OUTPUT_DIR / filename
    img.save(str(out_path))
    print(f"Generated Resume sample: {out_path}")


def generate_all_samples():
    print("Generating KYC and Universal Document test samples...")
    create_pan_card("sample_pan.png", blur=False)
    create_pan_card("sample_blurry_pan.png", blur=True)
    create_aadhaar_card("sample_aadhaar.png", tampered_qr=False)
    create_aadhaar_card("sample_tampered_aadhaar.png", tampered_qr=True)
    create_aadhaar_letter("sample_aadhaar_letter.png")
    create_passport_page("sample_passport.png")
    create_marksheet("sample_10th_marksheet.png")
    create_resume("sample_resume.png")
    print(f"All sample documents generated into: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_samples()

