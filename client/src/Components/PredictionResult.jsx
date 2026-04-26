import styled from "styled-components";

const Card = styled.div`
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 12px;
  padding: 16px;
  margin-top: 16px;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, minmax(180px, 1fr));
  gap: 12px;
  @media (max-width: 760px) {
    grid-template-columns: 1fr;
  }
`;

const Img = styled.img`
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 8px;
`;

const ActionRow = styled.div`
  margin-top: 14px;
`;

const DownloadBtn = styled.button`
  min-height: 40px;
  border: none;
  border-radius: 8px;
  padding: 0 14px;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  font-weight: 600;
  cursor: pointer;
`;

function PredictionResult({ record, onDownloadReport }) {
  if (!record) return null;
  const { prediction, images } = record;
  return (
    <Card>
      <h3>Prediction Result</h3>
      <p>
        Predicted Class: <strong>{prediction?.predictedClass}</strong> | Confidence:{" "}
        <strong>{prediction?.confidence}%</strong>
      </p>
      <Grid>
        <div>
          <p>Original MRI</p>
          <Img src={`data:image/png;base64,${images?.original}`} alt="Original MRI" />
        </div>
        <div>
          <p>Grad-CAM Heatmap</p>
          <Img src={`data:image/png;base64,${images?.heatmap}`} alt="Heatmap" />
        </div>
        <div>
          <p>Overlay</p>
          <Img src={`data:image/png;base64,${images?.overlay}`} alt="Overlay" />
        </div>
      </Grid>
      <ActionRow>
        <DownloadBtn onClick={onDownloadReport}>Download Report</DownloadBtn>
      </ActionRow>
    </Card>
  );
}

export default PredictionResult;
