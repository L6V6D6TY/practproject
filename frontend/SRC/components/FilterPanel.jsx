import React, { useState } from 'react';
import { TextField } from '@consta/uikit/TextField';
import { Button } from '@consta/uikit/Button';
import { Card } from '@consta/uikit/Card';

const FilterPanel = ({ onFilter, onReset }) => {
  const [selectedField, setSelectedField] = useState('');
  const [filterValue, setFilterValue] = useState('');

  const fieldOptions = [
    { label: 'Номер документа', value: 'doc_number' },
    { label: 'Статус', value: 'status' },
    { label: 'Вид НД', value: 'work_type' },
    { label: 'Подразделение', value: 'department' },
    { label: 'Производитель работ', value: 'work_foreman' },
  ];

  const handleApplyFilter = () => {
    if (selectedField && filterValue && filterValue.trim() !== '') {
      onFilter(selectedField, filterValue);
    }
  };

  const handleReset = () => {
    setSelectedField('');
    setFilterValue('');
    onReset();
  };

  return (
    <Card verticalSpace="m" horizontalSpace="m" style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
        
        {/* Обычный select вместо Consta Select */}
        <select
          value={selectedField}
          onChange={(e) => setSelectedField(e.target.value)}
          style={{ 
            padding: '8px 12px', 
            fontSize: '14px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            backgroundColor: 'white',
            width: '200px',
            height: '36px'
          }}
        >
          <option value="">Выберите поле</option>
          {fieldOptions.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Значение для фильтрации"
          value={filterValue}
          onChange={(e) => setFilterValue(e.target.value)}
          style={{ 
            padding: '8px 12px', 
            fontSize: '14px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            width: '250px',
            height: '36px'
          }}
        />

        <Button label="Применить фильтр" onClick={handleApplyFilter} />
        <Button label="Сбросить" view="ghost" onClick={handleReset} />
      </div>
    </Card>
  );
};

export default FilterPanel;