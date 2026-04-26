import { useEffect, useState } from "react";
import styled from "styled-components";

import Layout from "../Components/Layout";
import { historyApi, reportApi } from "../services/api";

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background: ${({ theme }) => theme.card};
  border-radius: 12px;
  overflow: hidden;
  th,
  td {
    border-bottom: 1px solid ${({ theme }) => theme.bgLighter};
    padding: 10px;
    text-align: left;
    font-size: 14px;
  }
`;

const Thumb = styled.img`
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 8px;
`;

function HistoryPage() {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await historyApi.list();
        setRecords(res.data.records || []);
      } catch (error) {
        setRecords([]);
        setError(error?.response?.data?.message || "Failed to fetch history.");
      }
    };
    load();
  }, []);

  const downloadReport = async (recordId) => {
    setError("");
    try {
      const res = await reportApi.download(recordId);
      const blobUrl = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = `brain_tumor_report_${recordId}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(blobUrl);
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to download report.");
    }
  };

  return (
    <Layout>
      <h2>Prediction History</h2>
      {error && <p>{error}</p>}
      <Table>
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>MRI</th>
            <th>Prediction</th>
            <th>Confidence</th>
            <th>Date & Time</th>
            <th>Report</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record) => (
            <tr key={record.id}>
              <td>{record.patient?.fullName}</td>
              <td>
                <Thumb src={`data:image/png;base64,${record.images?.uploaded}`} alt="MRI thumbnail" />
              </td>
              <td>{record.prediction?.predictedClass}</td>
              <td>{record.prediction?.confidence}%</td>
              <td>{new Date(record.createdAt).toLocaleString()}</td>
              <td>
                <button type="button" onClick={() => downloadReport(record.id)}>
                  Download Report
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Layout>
  );
}

export default HistoryPage;
