import React, { useState } from 'react';
import { TextField } from '@consta/uikit/TextField';
import { Button } from '@consta/uikit/Button';
import { Select } from '@consta/uikit/Select';
import { Card } from '@consta/uikit/Card';

const FilterPanel = ({ onFilter, onReset }) => {
  const [selectedField, setSelectedField] = useState(null);
  const [filterValue, setFilterValue] = useState('');

  const fieldOptions = [
    { label: 'Номер документа', value: 'doc_number' },
    { label: 'Статус', value: 'status' },
    { label: 'Вид НД', value: 'work_type' },
    { label: 'Подразделение', value: 'department' },
    { label: 'Производитель работ', value: 'work_foreman' },
  ];

  const handleFieldChange = (item) => {
    setSelectedField(item || null);
  };

  const handleApplyFilter = () => {
    if (selectedField && filterValue && filterValue.trim() !== '') {
      onFilter(selectedField.value, filterValue);
    }
  };

  const handleReset = () => {
    setSelectedField(null);
    setFilterValue('');
    onReset();
  };

  return (
    <Card verticalSpace="m" horizontalSpace="m" style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
        <Select
          placeholder="Выберите поле"
          items={fieldOptions}
          value={selectedField}
          onChange={handleFieldChange}
          style={{ width: '200px' }}
        />
        <TextField
          placeholder="Значение для фильтрации"
          value={filterValue}
          onChange={({ value }) => setFilterValue(value || '')}
          style={{ width: '250px' }}
        />
        <Button label="Применить фильтр" onClick={handleApplyFilter} />
        <Button label="Сбросить" view="ghost" onClick={handleReset} />
      </div>
    </Card>
  );
};

export default FilterPanel;