# import os
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime
# from dotenv import load_dotenv

# # Load secrets from .env
# load_dotenv()

# SPREADSHEET_NAME = os.getenv("GOOGLE_SPREADSHEET_NAME")
# WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME")
# CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# GOOGLE_SPREADSHEET_URL  = os.getenv("GOOGLE_SPREADSHEET_URL")


# def get_sheet():
#     gc = gspread.service_account(CREDENTIALS_FILE)
#     sh = gc.open_by_url(GOOGLE_SPREADSHEET_URL)
#     worksheet = sh.worksheet(WORKSHEET_NAME)
#     return worksheet

# def fetch_first_unprocessed_row():
#     sheet = get_sheet()
#     rows = sheet.get_all_values()
#     for row in rows[1:]:
#         if len(row) < 4 or row[3].strip().lower() not in {"downloaded", "skipped"}:
#             return row
#     return None

# def update_links_in_sheet(video_name, instagram_link=None, youtube_link=None):
#     sheet = get_sheet()
#     rows = sheet.get_all_values()

#     for i, row in enumerate(rows[1:], start=2):  # skip header
#         if len(row) >= 2 and row[1] == video_name:
#             if instagram_link:
#                 sheet.update_cell(i, 5, instagram_link)  # F
#                 print(f"[✅] Instagram link added to row {i -1}")
#             if youtube_link:
#                 sheet.update_cell(i, 6, youtube_link)   # G
#                 print(f"[✅] YouTube link added to row {i - 1}")
#             return

#     print(f"[⚠️] Video '{video_name}' not found in the sheet.")

# def get_logged_videos():
#     sheet = get_sheet()
#     rows = sheet.get_all_values()
#     return {row[1] for row in rows[1:] if len(row) >= 2}

# def append_row(video_name, status="pending"):
#     """Appends a new row to the sheet with status and timestamp."""
#     sheet = get_sheet()
#     timestamp = datetime.now().isoformat()
#     existing = sheet.get_all_values()
#     next_id = len(existing)  # crude row count (header assumed to be present)

#     sheet.append_row([str(next_id), video_name, status, timestamp])
#     print(f"[➕] Appended row: {video_name} → {status}")


# # ==============================
# # Video Reminder Functions
# # ==============================
# def get_reminder_date(row_key="Video Reminder"):
#     """
#     Fetch last reminder date from Google Sheet for given row_key.
#     Returns ISO string or None if not set.
#     """
#     sheet = get_sheet()
#     rows = sheet.get_all_values()

#     for row in rows[1:]:
#         if len(row) >= 1 and row[0] == row_key:
#             # Column G = index 6
#             if len(row) > 6 and row[6]:
#                 return row[6]
#             else:
#                 return None
#     return None


# def update_reminder_date(row_key="Video Reminder", iso_timestamp=None):
#     """
#     Update the reminder column (G) in Google Sheet for given row_key.
#     Appends new row if row_key does not exist.
#     """
#     sheet = get_sheet()
#     rows = sheet.get_all_values()

#     row_index = None
#     for i, row in enumerate(rows[1:], start=2):
#         if len(row) >= 1 and row[0] == row_key:
#             row_index = i
#             break

#     if row_index is not None:
#         sheet.update_cell(row_index, 7, iso_timestamp)  # Column G = 7
#         print(f"[✅] Updated reminder date for '{row_key}' to {iso_timestamp}")
#     else:
#         # Append new row if row_key not found
#         sheet.append_row([row_key, "", "", "", "", "", iso_timestamp])
#         print(f"[➕] Appended reminder row '{row_key}' with date {iso_timestamp}")

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

SPREADSHEET_NAME = os.getenv("GOOGLE_SPREADSHEET_NAME")
WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME")
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_SPREADSHEET_URL  = os.getenv("GOOGLE_SPREADSHEET_URL")

def get_sheet():
    gc = gspread.service_account(CREDENTIALS_FILE)
    sh = gc.open_by_url(GOOGLE_SPREADSHEET_URL)
    worksheet = sh.worksheet(WORKSHEET_NAME)
    return worksheet

def fetch_first_unprocessed_row():
    sheet = get_sheet()
    rows = sheet.get_all_values()
    for row in rows[1:]:
        if len(row) < 4 or row[3].strip().lower() not in {"downloaded", "skipped"}:
            return row
    return None

# def update_links_in_sheet(video_name, instagram_link=None, youtube_link=None):
#     sheet = get_sheet()
#     rows = sheet.get_all_values()

#     for i, row in enumerate(rows[1:], start=2):  # skip header
#         if len(row) >= 2 and row[1] == video_name:
#             if instagram_link:
#                 sheet.update_cell(i, 5, instagram_link)  # F
#                 print(f"[✅] Instagram link added to row {i -1}")
#             if youtube_link:
#                 sheet.update_cell(i, 6, youtube_link)   # G
#                 print(f"[✅] YouTube link added to row {i - 1}")
#             return

#     print(f"[⚠️] Video '{video_name}' not found in the sheet.")
def update_links_in_sheet(video_name, instagram_link=None, youtube_link=None):
    sheet = get_sheet()
    rows = sheet.get_all_values()

    last_match_row = None

    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 2 and row[1] == video_name:
            last_match_row = i  # keep updating

    if not last_match_row:
        print(f"[⚠️] Video '{video_name}' not found in the sheet.")
        return

    if instagram_link is not None:
        sheet.update_cell(last_match_row, 5, instagram_link)

    if youtube_link is not None:
        sheet.update_cell(last_match_row, 6, youtube_link)

    print(f"[✅] Links updated at row {last_match_row}")


def get_logged_videos():
    sheet = get_sheet()
    rows = sheet.get_all_values()
    return {row[1] for row in rows[1:] if len(row) >= 2}

def append_row(video_name, status="pending"):
    """Appends a new row to the sheet with status and timestamp."""
    sheet = get_sheet()
    timestamp = datetime.now().isoformat()
    existing = sheet.get_all_values()
    next_id = len(existing)  # crude row count (header assumed to be present)

    sheet.append_row([str(next_id), video_name, status, timestamp])
    print(f"[➕] Appended row: {video_name} → {status}")

# ==============================
# Video Reminder Functions
# ==============================
def get_reminder_date(row_key="Video Reminder"):
    """
    Fetch last reminder date from Google Sheet for given row_key.
    Returns ISO string or None if not set.
    """
    sheet = get_sheet()
    rows = sheet.get_all_values()

    for row in rows[1:]:
        if len(row) >= 1 and row[0] == row_key:
            # Column G = index 6
            if len(row) > 6 and row[6]:
                return row[6]
            else:
                return None
    return None


def update_reminder_date(row_key="Video Reminder", iso_timestamp=None):
    """
    Update the reminder column (G) in Google Sheet for given row_key.
    Appends new row if row_key does not exist.
    """
    sheet = get_sheet()
    rows = sheet.get_all_values()

    row_index = None
    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 1 and row[0] == row_key:
            row_index = i
            break

    if row_index is not None:
        sheet.update_cell(row_index, 7, iso_timestamp)  # Column G = 7
        print(f"[✅] Updated reminder date for '{row_key}' to {iso_timestamp}")
    else:
        # Append new row if row_key not found
        sheet.append_row([row_key, "", "", "", "", "", iso_timestamp])
        print(f"[➕] Appended reminder row '{row_key}' with date {iso_timestamp}")