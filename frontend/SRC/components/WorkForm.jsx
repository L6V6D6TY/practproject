import React, { useState, useEffect } from 'react';
import { Modal } from '@consta/uikit/Modal';
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
    if (initialData) {
      setFormData({
        doc_number: initialData.doc_number || '',
        status: initialData.status || '',
        work_type: initialData.work_type || '',
        department: initialData.department || '',
        work_foreman: initialData.work_foreman || '',
      });
    } else {
      setFormData({
        doc_number: '',
        status: '',
        work_type: '',
        department: '',
        work_foreman: '',
      });
    }
  }, [initialData, isOpen]);

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = () => {
    if (!formData.doc_number) {
      alert('Номер документа обязателен');
      return;
    }
    onSubmit(formData);
    onClose();
  };

  const inputStyle = {
    width: '100%',
    padding: '8px 12px',
    fontSize: '14px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    marginBottom: '16px',
    boxSizing: 'border-box'
  };

  const labelStyle = {
    display: 'block',
    marginBottom: '4px',
    fontWeight: '500',
    fontSize: '14px'
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <Card verticalSpace="l" horizontalSpace="l" style={{ minWidth: '400px' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>
          {isEditing ? 'Редактировать запись' : 'Добавить запись'}
        </h2>
        
        <div>
          <label style={labelStyle}>Номер документа *</label>
          <input
            type="text"
            value={formData.doc_number}
            onChange={(e) => handleChange('doc_number', e.target.value)}
            disabled={isEditing}
            style={inputStyle}
          />
        </div>
        
        <div>
          <label style={labelStyle}>Статус</label>
          <input
            type="text"
            value={formData.status}
            onChange={(e) => handleChange('status', e.target.value)}
            style={inputStyle}
          />
        </div>
        
        <div>
          <label style={labelStyle}>Вид НД</label>
          <input
            type="text"
            value={formData.work_type}
            onChange={(e) => handleChange('work_type', e.target.value)}
            style={inputStyle}
          />
        </div>
        
        <div>
          <label style={labelStyle}>Подразделение</label>
          <input
            type="text"
            value={formData.department}
            onChange={(e) => handleChange('department', e.target.value)}
            style={inputStyle}
          />
        </div>
        
        <div>
          <label style={labelStyle}>Производитель работ</label>
          <input
            type="text"
            value={formData.work_foreman}
            onChange={(e) => handleChange('work_foreman', e.target.value)}
            style={inputStyle}
          />
        </div>
        
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '20px' }}>
          <Button label="Отмена" view="ghost" onClick={onClose} />
          <Button label={isEditing ? 'Сохранить' : 'Создать'} onClick={handleSubmit} />
        </div>
      </Card>
    </Modal>
  );
};

export default WorkForm;