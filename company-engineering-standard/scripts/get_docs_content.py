import os
import re
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/presentations.readonly",
]


GOOGLE_DOC_MIME = "application/vnd.google-apps.document"
GOOGLE_SHEET_MIME = "application/vnd.google-apps.spreadsheet"
GOOGLE_SLIDE_MIME = "application/vnd.google-apps.presentation"


def get_credentials() -> Credentials:
    """
    Authenticate with Google OAuth.
    First run opens browser login and creates token.json.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "Missing credentials.json. Download OAuth client credentials "
                    "from Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    return creds


def extract_google_file_id(url_or_id: str) -> str:
    """
    Supports:
    - Raw file ID
    - Google Docs URL
    - Google Sheets URL
    - Google Slides URL
    - Google Drive file URL
    """
    patterns = [
        r"/document/d/([a-zA-Z0-9_-]+)",
        r"/spreadsheets/d/([a-zA-Z0-9_-]+)",
        r"/presentation/d/([a-zA-Z0-9_-]+)",
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    return url_or_id.strip()


def get_drive_file_metadata(drive_service: Any, file_id: str) -> Dict[str, Any]:
    return (
        drive_service.files()
        .get(
            fileId=file_id,
            fields="id,name,mimeType,webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )


def read_google_doc(docs_service: Any, document_id: str) -> str:
    doc = docs_service.documents().get(documentId=document_id).execute()

    parts: List[str] = []

    def read_structural_elements(elements: List[Dict[str, Any]]) -> None:
        for element in elements:
            if "paragraph" in element:
                paragraph = element["paragraph"]
                for item in paragraph.get("elements", []):
                    text_run = item.get("textRun")
                    if text_run:
                        parts.append(text_run.get("content", ""))

            elif "table" in element:
                table = element["table"]
                for row in table.get("tableRows", []):
                    row_values = []
                    for cell in row.get("tableCells", []):
                        cell_parts_before = len(parts)
                        read_structural_elements(cell.get("content", []))
                        cell_text = "".join(parts[cell_parts_before:]).strip()
                        del parts[cell_parts_before:]
                        row_values.append(cell_text)
                    parts.append(" | ".join(row_values) + "\n")

            elif "tableOfContents" in element:
                toc = element["tableOfContents"]
                read_structural_elements(toc.get("content", []))

    body = doc.get("body", {})
    read_structural_elements(body.get("content", []))

    return "".join(parts).strip()


def read_google_sheet(sheets_service: Any, spreadsheet_id: str) -> Dict[str, List[List[str]]]:
    spreadsheet = (
        sheets_service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id)
        .execute()
    )

    result: Dict[str, List[List[str]]] = {}

    for sheet in spreadsheet.get("sheets", []):
        title = sheet["properties"]["title"]

        values_response = (
            sheets_service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=title,
            )
            .execute()
        )

        result[title] = values_response.get("values", [])

    return result


def read_google_slides(slides_service: Any, presentation_id: str) -> str:
    presentation = (
        slides_service.presentations()
        .get(presentationId=presentation_id)
        .execute()
    )

    output: List[str] = []
    slides = presentation.get("slides", [])

    for index, slide in enumerate(slides, start=1):
        output.append(f"\n--- Slide {index} ---\n")

        for element in slide.get("pageElements", []):
            shape = element.get("shape")
            if not shape:
                continue

            text = shape.get("text")
            if not text:
                continue

            for text_element in text.get("textElements", []):
                text_run = text_element.get("textRun")
                if text_run:
                    output.append(text_run.get("content", ""))

    return "".join(output).strip()


def read_any_google_file(url_or_id: str) -> Dict[str, Any]:
    """
    Main function:
    Pass any Google Docs / Sheets / Slides URL or file ID.
    Returns file metadata and extracted content.
    """
    file_id = extract_google_file_id(url_or_id)
    creds = get_credentials()

    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)
    slides_service = build("slides", "v1", credentials=creds)

    metadata = get_drive_file_metadata(drive_service, file_id)
    mime_type = metadata["mimeType"]

    if mime_type == GOOGLE_DOC_MIME:
        content = read_google_doc(docs_service, file_id)
        file_type = "google_doc"

    elif mime_type == GOOGLE_SHEET_MIME:
        content = read_google_sheet(sheets_service, file_id)
        file_type = "google_sheet"

    elif mime_type == GOOGLE_SLIDE_MIME:
        content = read_google_slides(slides_service, file_id)
        file_type = "google_slide"

    else:
        raise ValueError(
            f"Unsupported file type: {mime_type}. "
            "This script currently supports Google Docs, Sheets, and Slides only."
        )

    return {
        "file_id": file_id,
        "name": metadata.get("name"),
        "type": file_type,
        "mime_type": mime_type,
        "url": metadata.get("webViewLink"),
        "content": content,
    }


if __name__ == "__main__":
    url = input("Paste Google Docs / Sheets / Slides URL or file ID: ").strip()

    data = read_any_google_file(url)

    print("\n==============================")
    print(f"Name: {data['name']}")
    print(f"Type: {data['type']}")
    print(f"URL: {data['url']}")
    print("==============================\n")

    if data["type"] == "google_sheet":
        for sheet_name, rows in data["content"].items():
            print(f"\n--- Sheet: {sheet_name} ---")
            for row in rows:
                print("\t".join(row))
    else:
        print(data["content"])