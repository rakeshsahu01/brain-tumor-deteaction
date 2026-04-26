import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { useState } from "react";

import Layout from "../Components/Layout";
import PatientForm from "../Components/PatientForm";
import PredictionResult from "../Components/PredictionResult";
import { predictionApi, reportApi } from "../services/api";

const Card = styled.div`
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 14px;
  padding: 18px;
`;

function DashboardPage() {
  const navigate = useNavigate();
  const [latestRecord, setLatestRecord] = useState(null);
  const [loading, setLoading] = useState(false);

  const onPredict = async (payload) => {
    setLoading(true);
    try {
      const res = await predictionApi.predict(payload);
      setLatestRecord(res.data.record);
    } catch (error) {
      alert(error?.response?.data?.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const onDownloadReport = () => {
    if (!latestRecord?.id) {
      alert("Please run prediction first");
      return;
    }
    window.open(reportApi.downloadUrl(latestRecord.id), "_blank");
  };

  return (
    <Layout>
      <Card>
        <h2>Patient Dashboard</h2>
        <PatientForm
          onPredict={onPredict}
          onViewHistory={() => navigate("/history")}
          loading={loading}
        />
      </Card>
      <PredictionResult record={latestRecord} onDownloadReport={onDownloadReport} />
    </Layout>
  );
}

export default DashboardPage;
