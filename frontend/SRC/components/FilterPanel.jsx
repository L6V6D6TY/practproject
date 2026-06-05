import React, { useState } from 'react';
import { TextField } from '@consta/uikit/TextField';
import { Button } from '@consta/uikit/Button';
import { Select } from '@consta/uikit/Select';
import { Card } from '@consta/uikit/Card';

const FilterPanel = ({ fields, onFilter, onReset }) => {
  const [selectedField, setSelectedField] = useState(null);
  const [filterValue, setFilterValue] = useState('');

  const fieldOptions = fields.map(field => ({
    label: field.label,
    value: field.value,
  }));

  const handleApplyFilter = () => {
    if (selectedField && filterValue) {
      onFilter(selectedField.value, filterValue);
    }
  };

  const handleReset = () => {
    setSelectedField(null);
    setFilterValue('');
    onReset();
  };

  return (
    <Card className="filter-panel" verticalSpace="m" horizontalSpace="m">
      <div className="filter-controls">
        <Select
          placeholder="Выберите поле"
          items={fieldOptions}
          value={selectedField}
          onChange={({ value }) => setSelectedField(value)}
          style={{ width: '200px' }}
        />
        <TextField
          placeholder="Значение для фильтрации"
          value={filterValue}
          onChange={({ value }) => setFilterValue(value)}
          style={{ width: '250px' }}
        />
        <Button label="Применить фильтр" onClick={handleApplyFilter} />
        <Button label="Сбросить" view="ghost" onClick={handleReset} />
      </div>
    </Card>
  );
};

export default FilterPanel;