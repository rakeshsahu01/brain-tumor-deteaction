import { useState } from "react";
import styled from "styled-components";

const Form = styled.form`
  display: grid;
  grid-template-columns: repeat(2, minmax(180px, 1fr));
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

const TextArea = styled.textarea`
  min-height: 90px;
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.soft};
  padding: 10px;
`;

const Full = styled.div`
  grid-column: 1 / -1;
`;

const Actions = styled.div`
  display: flex;
  gap: 10px;
  grid-column: 1 / -1;
  flex-wrap: wrap;
`;

const Btn = styled.button`
  min-height: 42px;
  border: none;
  border-radius: 8px;
  padding: 0 14px;
  background: ${({ theme, $secondary }) => ($secondary ? theme.card : theme.primary)};
  color: ${({ theme }) => theme.text};
  cursor: pointer;
`;

function PatientForm({ onPredict, onViewHistory, loading }) {
  const [form, setForm] = useState({
    fullName: "",
    age: "",
    gender: "",
    phone: "",
    email: "",
    address: "",
    symptoms: "",
  });
  const [image, setImage] = useState(null);

  const onChange = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleImage = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result);
    reader.readAsDataURL(file);
  };

  const submit = (event) => {
    event.preventDefault();
    if (!image) return;
    onPredict({ patient: form, image });
  };

  return (
    <Form onSubmit={submit}>
      <Field>
        <Label>Full Name</Label>
        <Input value={form.fullName} onChange={(e) => onChange("fullName", e.target.value)} required />
      </Field>
      <Field>
        <Label>Age</Label>
        <Input value={form.age} onChange={(e) => onChange("age", e.target.value)} required />
      </Field>
      <Field>
        <Label>Gender</Label>
        <Input value={form.gender} onChange={(e) => onChange("gender", e.target.value)} required />
      </Field>
      <Field>
        <Label>Phone Number</Label>
        <Input value={form.phone} onChange={(e) => onChange("phone", e.target.value)} required />
      </Field>
      <Field>
        <Label>Email</Label>
        <Input type="email" value={form.email} onChange={(e) => onChange("email", e.target.value)} required />
      </Field>
      <Field>
        <Label>Address</Label>
        <Input value={form.address} onChange={(e) => onChange("address", e.target.value)} required />
      </Field>
      <Full>
        <Field>
          <Label>Symptoms / Description</Label>
          <TextArea value={form.symptoms} onChange={(e) => onChange("symptoms", e.target.value)} required />
        </Field>
      </Full>
      <Full>
        <Field>
          <Label>MRI Image Upload</Label>
          <Input type="file" accept="image/*" onChange={handleImage} required />
        </Field>
      </Full>
      <Actions>
        <Btn type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </Btn>
        <Btn type="button" $secondary onClick={onViewHistory}>
          View History
        </Btn>
      </Actions>
    </Form>
  );
}

export default PatientForm;
