import React, { useState, useEffect } from 'react';
import { Modal } from '@consta/uikit/Modal';
import { TextField } from '@consta/uikit/TextField';
import { Button } from '@consta/uikit/Button';
import { Card } from '@consta/uikit/Card';

const WorkForm = ({ isOpen, onClose, onSubmit, initialData, isEditing }) => {
  const [formData, setFormData] = useState({
    doc_number: '',
    status: '',
    work_type: '',
    organization: '',
    department: '',
    unit: '',
    work_foreman: '',
    commission_decision: '',
    work_location: '',
    work_content: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        doc_number: initialData.doc_number || '',
        status: initialData.status || '',
        work_type: initialData.work_type || '',
        organization: initialData.organization || '',
        department: initialData.department || '',
        unit: initialData.unit || '',
        work_foreman: initialData.work_foreman || '',
        commission_decision: initialData.commission_decision || '',
        work_location: initialData.work_location || '',
        work_content: initialData.work_content || '',
      });
    } else {
      setFormData({
        doc_number: '',
        status: '',
        work_type: '',
        organization: '',
        department: '',
        unit: '',
        work_foreman: '',
        commission_decision: '',
        work_location: '',
        work_content: '',
      });
    }
  }, [initialData, isOpen]);

  const validate = () => {
    const newErrors = {};
    if (!formData.doc_number) newErrors.doc_number = 'Обязательное поле';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      onSubmit(formData);
      onClose();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <Card verticalSpace="l" horizontalSpace="l" style={{ minWidth: '600px', maxWidth: '800px' }}>
        <h2>{isEditing ? 'Редактировать запись' : 'Добавить запись'}</h2>

        <TextField
          label="Номер документа"
          value={formData.doc_number}
          onChange={({ value }) => setFormData({ ...formData, doc_number: value })}
          status={errors.doc_number ? 'error' : undefined}
          caption={errors.doc_number}
          disabled={isEditing}
          required
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Статус"
          value={formData.status}
          onChange={({ value }) => setFormData({ ...formData, status: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Вид НД"
          value={formData.work_type}
          onChange={({ value }) => setFormData({ ...formData, work_type: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Организация"
          value={formData.organization}
          onChange={({ value }) => setFormData({ ...formData, organization: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Подразделение"
          value={formData.department}
          onChange={({ value }) => setFormData({ ...formData, department: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Установка/Участок"
          value={formData.unit}
          onChange={({ value }) => setFormData({ ...formData, unit: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Производитель работ"
          value={formData.work_foreman}
          onChange={({ value }) => setFormData({ ...formData, work_foreman: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Решение комиссии"
          value={formData.commission_decision}
          onChange={({ value }) => setFormData({ ...formData, commission_decision: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Место проведения работ"
          value={formData.work_location}
          onChange={({ value }) => setFormData({ ...formData, work_location: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <TextField
          label="Содержание работ"
          value={formData.work_content}
          onChange={({ value }) => setFormData({ ...formData, work_content: value })}
          style={{ marginBottom: '16px', width: '100%' }}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '20px' }}>
          <Button label="Отмена" view="ghost" onClick={onClose} />
          <Button label={isEditing ? 'Сохранить' : 'Создать'} onClick={handleSubmit} />
        </div>
      </Card>
    </Modal>
  );
};

export default WorkForm;