from bson import ObjectId
from flask import Response, jsonify
from flask_jwt_extended import get_jwt_identity

from backend.models.db import history_collection
from backend.utils.pdf_utils import build_report_pdf


def download_report(record_id):
    email = get_jwt_identity()
    try:
        record = history_collection.find_one({"_id": ObjectId(record_id), "userEmail": email})
    except Exception:
        record = None
    if not record:
        return jsonify({"message": "Report record not found"}), 404

    pdf_file = build_report_pdf(record)
    return Response(
        pdf_file.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=brain_tumor_report_{record_id}.pdf"},
    )
