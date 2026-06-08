import React, { useState, useEffect } from 'react';
import { Theme, presetGpnDefault } from '@consta/uikit/Theme';
import { Button } from '@consta/uikit/Button';
import { Table } from '@consta/uikit/Table';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000/api/works')
      .then(response => {
        // Данные приходят в поле items
        const items = response.data.items || [];
        console.log('Получено записей:', items.length);
        setData(items);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка:', error);
        setLoading(false);
      });
  }, []);

  const columns = [
    { title: 'Номер документа', accessor: 'doc_number' },
    { title: 'Статус', accessor: 'status' },
    { title: 'Вид НД', accessor: 'work_type' },
    { title: 'Подразделение', accessor: 'department' },
    { title: 'Производитель работ', accessor: 'work_foreman' },
  ];

  return (
    <Theme preset={presetGpnDefault}>
      <div style={{ padding: '20px' }}>
        <h1>Наряд-допуски</h1>
        <h3>Всего записей: {data.length}</h3>
        <Button label="Добавить запись" />
        <div style={{ marginTop: '20px' }}>
          <Table columns={columns} rows={data} loading={loading} />
        </div>
      </div>
    </Theme>
  );
}

export default App;