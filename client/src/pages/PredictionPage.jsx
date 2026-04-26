import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

import Layout from "../Components/Layout";
import PredictionResult from "../Components/PredictionResult";
import { predictionApi, reportApi } from "../services/api";

const Card = styled.div`
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 14px;
  padding: 18px;
`;

const Summary = styled.div`
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 14px;
`;

const Row = styled.p`
  margin: 6px 0;
  color: ${({ theme }) => theme.text};
`;

const Input = styled.input`
  min-height: 42px;
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.soft};
  padding: 0 10px;
  width: 100%;
  box-sizing: border-box;
`;

const PredictButton = styled.button`
  margin-top: 12px;
  min-height: 42px;
  border: none;
  border-radius: 8px;
  padding: 0 14px;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  font-weight: 600;
  cursor: pointer;
`;

const ErrorText = styled.p`
  color: #ff7a7a;
  font-size: 14px;
`;

function PredictionPage() {
  const navigate = useNavigate();
  const [activePatient, setActivePatient] = useState(null);
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [latestRecord, setLatestRecord] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem("activePatient");
    if (!stored) {
      navigate("/patient-info");
      return;
    }
    setActivePatient(JSON.parse(stored));
  }, [navigate]);

  const handleImage = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result);
    reader.readAsDataURL(file);
  };

  const predict = async () => {
    if (!activePatient?.id) {
      setError("Please save patient details first.");
      return;
    }
    if (!image) {
      setError("Please upload an MRI image.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await predictionApi.predict({ patientId: activePatient.id, image });
      setLatestRecord(res.data.record);
    } catch (err) {
      setError(err?.response?.data?.message || err?.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const onDownloadReport = () => {
    if (!latestRecord?.id) return;
    reportApi
      .download(latestRecord.id)
      .then((res) => {
        const blobUrl = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
        const link = document.createElement("a");
        link.href = blobUrl;
        link.download = `brain_tumor_report_${latestRecord.id}.pdf`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(blobUrl);
      })
      .catch((err) => {
        setError(err?.response?.data?.message || "Failed to download report.");
      });
  };

  return (
    <Layout>
      <Card>
        <h2>Prediction Dashboard</h2>
        {activePatient && (
          <Summary>
            <Row>
              <strong>Patient ID:</strong> {activePatient.patientId}
            </Row>
            <Row>
              <strong>Name:</strong> {activePatient.fullName}
            </Row>
            <Row>
              <strong>Doctor:</strong> {activePatient.doctorName}
            </Row>
            <Row>
              <strong>Symptoms:</strong> {activePatient.symptoms}
            </Row>
          </Summary>
        )}
        <Input type="file" accept="image/*" onChange={handleImage} />
        <PredictButton type="button" onClick={predict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </PredictButton>
        {error && <ErrorText>{error}</ErrorText>}
      </Card>
      <PredictionResult record={latestRecord} onDownloadReport={onDownloadReport} />
    </Layout>
  );
}

export default PredictionPage;
