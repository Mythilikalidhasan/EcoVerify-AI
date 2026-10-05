import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import re
import os
from datetime import datetime


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EcoVerify AI",
    page_icon="♻️",
    layout="wide"
)


# =========================================================
# 2. TESSERACT CONFIGURATION
# =========================================================

# Tesseract is installed on your computer at this location.
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================================================
# 3. DATABASE FILE
# =========================================================

DATABASE_FILE = "certificate_records.csv"


# =========================================================
# 4. CREATE DATABASE IF IT DOES NOT EXIST
# =========================================================

def create_database():

    if not os.path.exists(DATABASE_FILE):

        columns = [
            "certificate_no",
            "company",
            "recycler",
            "quantity",
            "collection_date",
            "recycling_date"
        ]

        df = pd.DataFrame(columns=columns)

        df.to_csv(
            DATABASE_FILE,
            index=False
        )


# =========================================================
# 5. OCR IMAGE PROCESSING
# =========================================================

def preprocess_image(image):

    # Convert PIL image to NumPy array
    image_array = np.array(image)

    # Convert RGB image to grayscale
    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    # Remove noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Make text clearer
    _, threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return threshold


# =========================================================
# 6. OCR FUNCTION
# =========================================================

def extract_text(image):

    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed_image
    )

    return text


# =========================================================
# 7. EXTRACT CERTIFICATE NUMBER
# =========================================================

def extract_certificate_number(text):

    patterns = [
        r"Certificate\s*(?:No|Number|ID)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        r"Cert(?:ificate)?\s*[:\-]?\s*([A-Za-z0-9\-]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return ""


# =========================================================
# 8. EXTRACT COMPANY NAME
# =========================================================

def extract_company(text):

    pattern = (
        r"Company\s*(?:Name)?\s*[:\-]?\s*(.+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        value = match.group(1).strip()

        return value.split("\n")[0].strip()

    return ""


# =========================================================
# 9. EXTRACT RECYCLER NAME
# =========================================================

def extract_recycler(text):

    pattern = (
        r"Recycler\s*(?:Name)?\s*[:\-]?\s*(.+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        value = match.group(1).strip()

        return value.split("\n")[0].strip()

    return ""


# =========================================================
# 10. EXTRACT QUANTITY
# =========================================================

def extract_quantity(text):

    patterns = [
        r"Quantity\s*[:\-]?\s*([\d,.]+\s*(?:kg|kgs|kilogram|kilograms|g|ton|tons))",
        r"Quantity\s*[:\-]?\s*([\d,.]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return ""


# =========================================================
# 11. EXTRACT COLLECTION DATE
# =========================================================

def extract_collection_date(text):

    pattern = (
        r"Collection\s*Date\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


# =========================================================
# 12. EXTRACT RECYCLING DATE
# =========================================================

def extract_recycling_date(text):

    pattern = (
        r"Recycling\s*Date\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


# =========================================================
# 13. EXTRACT ALL INFORMATION
# =========================================================

def extract_information(text):

    data = {

        "certificate_no":
            extract_certificate_number(text),

        "company":
            extract_company(text),

        "recycler":
            extract_recycler(text),

        "quantity":
            extract_quantity(text),

        "collection_date":
            extract_collection_date(text),

        "recycling_date":
            extract_recycling_date(text)
    }

    return data


# =========================================================
# 14. CHECK REQUIRED FIELDS
# =========================================================

def check_missing_fields(data):

    field_names = {

        "certificate_no":
            "Certificate Number",

        "company":
            "Company",

        "recycler":
            "Recycler",

        "quantity":
            "Quantity",

        "collection_date":
            "Collection Date",

        "recycling_date":
            "Recycling Date"
    }

    missing_fields = []

    for key, name in field_names.items():

        if not data[key]:

            missing_fields.append(name)

    return missing_fields


# =========================================================
# 15. CHECK DATES
# =========================================================

def check_dates(data):

    issues = []

    collection_date = data["collection_date"]
    recycling_date = data["recycling_date"]

    if not collection_date or not recycling_date:

        return issues

    try:

        collection = datetime.strptime(
            collection_date.replace("-", "/"),
            "%d/%m/%Y"
        )

        recycling = datetime.strptime(
            recycling_date.replace("-", "/"),
            "%d/%m/%Y"
        )

        if recycling < collection:

            issues.append(
                "Recycling date occurs before collection date."
            )

    except ValueError:

        # Try 2-digit year
        try:

            collection = datetime.strptime(
                collection_date.replace("-", "/"),
                "%d/%m/%y"
            )

            recycling = datetime.strptime(
                recycling_date.replace("-", "/"),
                "%d/%m/%y"
            )

            if recycling < collection:

                issues.append(
                    "Recycling date occurs before collection date."
                )

        except ValueError:

            issues.append(
                "Date format could not be validated."
            )

    return issues


# =========================================================
# 16. CHECK QUANTITY
# =========================================================

def check_quantity(quantity):

    issues = []

    if not quantity:
        return issues

    match = re.search(
        r"([\d,.]+)",
        quantity
    )

    if not match:

        issues.append(
            "Quantity could not be interpreted."
        )

        return issues

    try:

        number = float(
            match.group(1).replace(",", "")
        )

        if number <= 0:

            issues.append(
                "Quantity must be greater than zero."
            )

    except ValueError:

        issues.append(
            "Quantity is not valid."
        )

    return issues


# =========================================================
# 17. CHECK DUPLICATE CERTIFICATE
# =========================================================

def check_duplicate(certificate_no):

    if not certificate_no:

        return False

    create_database()

    df = pd.read_csv(
        DATABASE_FILE
    )

    if df.empty:

        return False

    existing = df["certificate_no"].astype(str)

    return certificate_no.lower() in (
        existing.str.lower().values
    )


# =========================================================
# 18. SAVE CERTIFICATE
# =========================================================

def save_certificate(data):

    create_database()

    df = pd.read_csv(
        DATABASE_FILE
    )

    new_row = pd.DataFrame([data])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(
        DATABASE_FILE,
        index=False
    )


# =========================================================
# 19. APPLICATION UI
# =========================================================

st.title("♻️ EcoVerify AI")

st.subheader(
    "E-Waste Certificate Verification Assistant"
)

st.write(
    "Upload an e-waste recycling certificate. "
    "EcoVerify AI uses OCR and automated validation "
    "to identify missing information, inconsistencies, "
    "and duplicate certificate records."
)

st.divider()


# =========================================================
# 20. IMAGE UPLOAD
# =========================================================

st.header("📤 Upload E-Waste Certificate")

uploaded_file = st.file_uploader(
    "Choose a certificate image",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)


# =========================================================
# 21. DISPLAY UPLOADED IMAGE
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    )

    st.subheader(
        "Certificate Preview"
    )

    st.image(
        image,
        caption="Uploaded E-Waste Certificate",
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # 22. VERIFY BUTTON
    # =====================================================

    if st.button(
        "🔍 Verify Certificate",
        type="primary"
    ):

        with st.spinner(
            "Reading certificate..."
        ):

            # OCR
            extracted_text = extract_text(
                image
            )

            # Extract fields
            data = extract_information(
                extracted_text
            )

            # Validation
            missing_fields = check_missing_fields(
                data
            )

            date_issues = check_dates(
                data
            )

            quantity_issues = check_quantity(
                data["quantity"]
            )

            duplicate = check_duplicate(
                data["certificate_no"]
            )

        # =================================================
        # 23. DISPLAY EXTRACTED INFORMATION
        # =================================================

        st.header(
            "📋 Extracted Certificate Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Certificate Number:**",
                data["certificate_no"]
                if data["certificate_no"]
                else "Not detected"
            )

            st.write(
                "**Company:**",
                data["company"]
                if data["company"]
                else "Not detected"
            )

            st.write(
                "**Recycler:**",
                data["recycler"]
                if data["recycler"]
                else "Not detected"
            )

        with col2:

            st.write(
                "**Quantity:**",
                data["quantity"]
                if data["quantity"]
                else "Not detected"
            )

            st.write(
                "**Collection Date:**",
                data["collection_date"]
                if data["collection_date"]
                else "Not detected"
            )

            st.write(
                "**Recycling Date:**",
                data["recycling_date"]
                if data["recycling_date"]
                else "Not detected"
            )

        st.divider()

        # =================================================
        # 24. DISPLAY OCR TEXT
        # =================================================

        with st.expander(
            "🔎 View OCR Extracted Text"
        ):

            st.text(
                extracted_text
            )

        # =================================================
        # 25. CREATE ISSUE LIST
        # =================================================

        issues = []

        for field in missing_fields:

            issues.append(
                f"{field} is missing."
            )

        issues.extend(
            date_issues
        )

        issues.extend(
            quantity_issues
        )

        if duplicate:

            issues.append(
                "Duplicate certificate number detected."
            )

        # =================================================
        # 26. FINAL RESULT
        # =================================================

        st.header(
            "📊 Verification Result"
        )

        if len(issues) == 0:

            st.success(
                "🟢 LOW RISK — No obvious inconsistencies detected."
            )

            st.write(
                "✓ All required fields detected"
            )

            st.write(
                "✓ Dates are consistent"
            )

            st.write(
                "✓ Quantity is valid"
            )

            st.write(
                "✓ No duplicate certificate detected"
            )

            st.info(
                "Recommendation: No obvious inconsistencies "
                "were detected. External verification is "
                "still recommended."
            )

        else:

            st.warning(
                "⚠️ REVIEW REQUIRED"
            )

            st.write(
                "The following issues were detected:"
            )

            for issue in issues:

                st.error(
                    f"❌ {issue}"
                )

            st.info(
                "Recommendation: Verify the certificate "
                "with the issuing organization."
            )

        # =================================================
        # 27. SAVE RECORD
        # =================================================

        if data["certificate_no"]:

            if not duplicate:

                save_certificate(
                    data
                )

                st.success(
                    "Certificate record saved."
                )

            else:

                st.warning(
                    "Certificate was not saved because "
                    "the certificate number already exists."
                )


# =========================================================
# 28. DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "EcoVerify AI performs preliminary document validation. "
    "It does not prove that a certificate is authentic or "
    "legally valid. External verification is recommended."
)