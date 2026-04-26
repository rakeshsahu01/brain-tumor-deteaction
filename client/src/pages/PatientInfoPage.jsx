import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

import Layout from "../Components/Layout";
import { patientApi } from "../services/api";

const Card = styled.div`
  background: ${({ theme }) => theme.card};
  border: 1px solid ${({ theme }) => theme.bgLighter};
  border-radius: 14px;
  padding: 18px;
`;

const Form = styled.form`
  display: grid;
  grid-template-columns: repeat(2, minmax(200px, 1fr));
  gap: 12px;
  @media (max-width: 760px) {
    grid-template-columns: 1fr;
  }
`;

const Field = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const Label = styled.label`
  color: ${({ theme }) => theme.textSoft};
  font-size: 14px;
`;

const Input = styled.input`
  min-height: 42px;
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.soft};
  padding: 0 10px;
`;

const Textarea = styled.textarea`
  min-height: 90px;
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.soft};
  padding: 10px;
`;

const Full = styled.div`
  grid-column: 1 / -1;
`;

const SaveButton = styled.button`
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

function PatientInfoPage() {
  const navigate = useNavigate();
  const generatedPatientId = useMemo(
    () => `PT-${new Date().toISOString().slice(0, 10).replaceAll("-", "")}-${Math.floor(1000 + Math.random() * 9000)}`,
    []
  );
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    patientId: generatedPatientId,
    fullName: "",
    age: "",
    gender: "",
    phone: "",
    email: "",
    address: "",
    doctorName: "",
    allergies: "",
    medicalHistory: "",
    symptoms: "",
    bloodGroup: "",
  });

  const setField = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const onSave = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await patientApi.create(form);
      localStorage.setItem("activePatient", JSON.stringify(res.data.patient));
      navigate("/prediction");
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to save patient information.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Card>
        <h2>Patient Information Dashboard</h2>
        <Form onSubmit={onSave}>
          <Field>
            <Label>Patient ID</Label>
            <Input value={form.patientId} readOnly />
          </Field>
          <Field>
            <Label>Full Name</Label>
            <Input value={form.fullName} onChange={(e) => setField("fullName", e.target.value)} required />
          </Field>
          <Field>
            <Label>Age</Label>
            <Input value={form.age} onChange={(e) => setField("age", e.target.value)} required />
          </Field>
          <Field>
            <Label>Gender</Label>
            <Input value={form.gender} onChange={(e) => setField("gender", e.target.value)} required />
          </Field>
          <Field>
            <Label>Phone Number</Label>
            <Input value={form.phone} onChange={(e) => setField("phone", e.target.value)} required />
          </Field>
          <Field>
            <Label>Email</Label>
            <Input type="email" value={form.email} onChange={(e) => setField("email", e.target.value)} required />
          </Field>
          <Field>
            <Label>Address</Label>
            <Input value={form.address} onChange={(e) => setField("address", e.target.value)} required />
          </Field>
          <Field>
            <Label>Doctor Name</Label>
            <Input value={form.doctorName} onChange={(e) => setField("doctorName", e.target.value)} required />
          </Field>
          <Field>
            <Label>Allergies</Label>
            <Input value={form.allergies} onChange={(e) => setField("allergies", e.target.value)} />
          </Field>
          <Field>
            <Label>Blood Group (Optional)</Label>
            <Input value={form.bloodGroup} onChange={(e) => setField("bloodGroup", e.target.value)} />
          </Field>
          <Full>
            <Field>
              <Label>Existing Diseases / Medical History</Label>
              <Textarea value={form.medicalHistory} onChange={(e) => setField("medicalHistory", e.target.value)} />
            </Field>
          </Full>
          <Full>
            <Field>
              <Label>Symptoms / Problem Description</Label>
              <Textarea value={form.symptoms} onChange={(e) => setField("symptoms", e.target.value)} required />
            </Field>
          </Full>
          <Full>
            <SaveButton type="submit" disabled={loading}>
              {loading ? "Saving..." : "Save & Continue"}
            </SaveButton>
          </Full>
        </Form>
        {error && <ErrorText>{error}</ErrorText>}
      </Card>
    </Layout>
  );
}

export default PatientInfoPage;
