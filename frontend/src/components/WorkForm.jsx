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
    department: '',
    work_foreman: '',
  });

  useEffect(() => {
    if (initialData && isEditing) {
      setFormData({
        doc_number: initialData.doc_number || '',
        status: initialData.status || '',
        work_type: initialData.work_type || '',
        department: initialData.department || '',
        work_foreman: initialData.work_foreman || '',
      });
    } else if (!isEditing) {
      setFormData({
        doc_number: '',
        status: '',
        work_type: '',
        department: '',
        work_foreman: '',
      });
    }
  }, [initialData, isEditing, isOpen]);

  const handleSubmit = () => {
    if (!formData.doc_number) {
      alert('Номер документа обязателен');
      return;
    }
    onSubmit(formData);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <Card verticalSpace="l" horizontalSpace="l" style={{ minWidth: '400px' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>
          {isEditing ? 'Редактировать запись' : 'Добавить запись'}
        </h2>
        
        <TextField
          label="Номер документа"
          value={formData.doc_number}
          onChange={({ value }) => setFormData({ ...formData, doc_number: value })}
          disabled={isEditing}
          required
        />
        
        <TextField
          label="Статус"
          value={formData.status}
          onChange={({ value }) => setFormData({ ...formData, status: value })}
        />
        
        <TextField
          label="Вид НД"
          value={formData.work_type}
          onChange={({ value }) => setFormData({ ...formData, work_type: value })}
        />
        
        <TextField
          label="Подразделение"
          value={formData.department}
          onChange={({ value }) => setFormData({ ...formData, department: value })}
        />
        
        <TextField
          label="Производитель работ"
          value={formData.work_foreman}
          onChange={({ value }) => setFormData({ ...formData, work_foreman: value })}
        />
        
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '20px' }}>
          <Button label="Отмена" view="ghost" onClick={onClose} />
          <Button label={isEditing ? 'Сохранить' : 'Создать'} onClick={handleSubmit} />
        </div>
      </Card>
    </Modal>
  );
};

export default WorkForm;