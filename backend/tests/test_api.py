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
