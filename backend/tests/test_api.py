from app.core.database import SessionLocal
from app.models.document import Document, DocumentCategory, DocumentStatus


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_deals_includes_seed_deal(client):
    response = client.get("/api/deals")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "ABC Hydraulic Systems"


def test_get_seed_deal(client):
    response = client.get("/api/deals/ABC-HYD-001")
    assert response.status_code == 200
    assert response.json()["revenue"] == "120000000.00"
    assert response.json()["deal_stage"] == "Due Diligence"


def test_seed_deal_has_no_documents(client):
    response = client.get("/api/deals/ABC-HYD-001/documents")
    assert response.status_code == 200
    assert response.json() == []


def test_document_is_scoped_to_its_deal(client):
    with SessionLocal() as db:
        db.add(
            Document(
                document_id="DOC-001",
                deal_id="ABC-HYD-001",
                file_name="financials.pdf",
                category=DocumentCategory.FINANCIAL,
                file_path="data/documents/financials.pdf",
                status=DocumentStatus.PENDING,
            )
        )
        db.commit()

    response = client.get("/api/deals/ABC-HYD-001/documents")
    assert response.status_code == 200
    assert [document["document_id"] for document in response.json()] == ["DOC-001"]


def test_upload_and_download_document(client):
    response = client.post(
        "/api/deals/ABC-HYD-001/documents",
        data={"category": "Commercial"},
        files={"file": ("Customer Analysis.pdf", b"%PDF-1.4 sample", "application/pdf")},
    )
    assert response.status_code == 201
    document = response.json()
    assert document["category"] == "Commercial"
    assert document["status"] == "Pending"
    assert document["file_size"] == len(b"%PDF-1.4 sample")

    listed = client.get("/api/deals/ABC-HYD-001/documents")
    assert [item["document_id"] for item in listed.json()] == [document["document_id"]]

    download = client.get(f"/api/documents/{document['document_id']}/download")
    assert download.status_code == 200
    assert download.content == b"%PDF-1.4 sample"
    assert download.headers["content-type"] == "application/pdf"


def test_rejects_unsupported_document_type(client):
    response = client.post(
        "/api/deals/ABC-HYD-001/documents",
        data={"category": "Legal"},
        files={"file": ("script.exe", b"not allowed", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_documents_are_isolated_between_deals(client):
    client.post(
        "/api/deals",
        json={
            "deal_id": "SECOND-001", "name": "Second Deal", "company_name": "Second Co",
            "industry": "Software", "geography": "Europe", "revenue": 1, "ebitda": 1,
            "deal_stage": "Screening",
        },
    )
    upload = client.post(
        "/api/deals/SECOND-001/documents",
        data={"category": "Financial"},
        files={"file": ("second.txt", b"second deal only", "text/plain")},
    )
    assert upload.status_code == 201
    assert client.get("/api/deals/ABC-HYD-001/documents").json() == []
