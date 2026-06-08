import React, { useState, useEffect } from 'react';
import { Theme, presetGpnDefault } from '@consta/uikit/Theme';
import { Button } from '@consta/uikit/Button';
import { Table } from '@consta/uikit/Table';
import FilterPanel from './components/FilterPanel';
import WorkForm from './components/WorkForm';
import ConfirmDialog from './components/ConfirmDialog';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedWork, setSelectedWork] = useState(null);
  const [workToDelete, setWorkToDelete] = useState(null);

  const fetchData = async (field = null, value = null) => {
    setLoading(true);
    try {
      let url = 'http://localhost:8000/api/works';
      if (field && value) {
        url = `http://localhost:8000/api/works?field=${field}&value=${encodeURIComponent(value)}`;
      }
      const response = await axios.get(url);
      const items = response.data.items || [];

      // ============================================================
      // ГЛАВНОЕ ИЗМЕНЕНИЕ: добавляем кнопки в каждую строку вручную
      // ============================================================
      const itemsWithButtons = items.map((item) => ({
        ...item,
        actions: (
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => handleEdit(item)}
              style={{
                cursor: 'pointer',
                padding: '4px 8px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              Редактировать
            </button>
            <button
              onClick={() => handleDelete(item)}
              style={{
                cursor: 'pointer',
                padding: '4px 8px',
                backgroundColor: '#f44336',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              Удалить
            </button>
          </div>
        ),
      }));
      // ============================================================

      setData(itemsWithButtons);
    } catch (error) {
      console.error('Ошибка:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFilter = (field, value) => {
    fetchData(field, value);
  };

  const handleResetFilter = () => {
    fetchData();
  };

  const handleAdd = () => {
    setSelectedWork(null);
    setIsFormOpen(true);
  };

  const handleEdit = (work) => {
    setSelectedWork(work);
    setIsFormOpen(true);
  };

  const handleDelete = (work) => {
    setWorkToDelete(work);
    setIsConfirmOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (workToDelete) {
      try {
        await axios.delete(`http://localhost:8000/api/works/${workToDelete.id}`);
        fetchData();
        alert('Запись удалена');
      } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении');
      } finally {
        setIsConfirmOpen(false);
        setWorkToDelete(null);
      }
    }
  };

  const handleSubmitForm = async (formData) => {
    try {
      if (selectedWork) {
        await axios.put(`http://localhost:8000/api/works/${selectedWork.id}`, formData);
        alert('Запись обновлена');
      } else {
        await axios.post('http://localhost:8000/api/works', formData);
        alert('Запись добавлена');
      }
      fetchData();
      setIsFormOpen(false);
      setSelectedWork(null);
    } catch (error) {
      console.error('Ошибка:', error);
      alert(error.response?.data?.detail || 'Произошла ошибка');
    }
  };

  // ============================================================
  // КОЛОНКИ: теперь просто выводим поле 'actions', где уже лежат кнопки
  // ============================================================
  const columns = [
    { title: 'Номер документа', accessor: 'doc_number' },
    { title: 'Статус', accessor: 'status' },
    { title: 'Вид НД', accessor: 'work_type' },
    { title: 'Подразделение', accessor: 'department' },
    { title: 'Производитель работ', accessor: 'work_foreman' },
    { title: 'Действия', accessor: 'actions' },  // <-- просто выводим готовые кнопки
  ];
  // ============================================================

  return (
    <Theme preset={presetGpnDefault}>
      <div style={{ padding: '20px' }}>
        <h1>Наряд-допуски</h1>
        <h3>Всего записей: {data.length}</h3>
        
        <FilterPanel onFilter={handleFilter} onReset={handleResetFilter} />
        
        <div style={{ marginBottom: '20px' }}>
          <Button label="Добавить запись" onClick={handleAdd} />
        </div>
        
        <Table columns={columns} rows={data} loading={loading} />
        
        <WorkForm
          isOpen={isFormOpen}
          onClose={() => {
            setIsFormOpen(false);
            setSelectedWork(null);
          }}
          onSubmit={handleSubmitForm}
          initialData={selectedWork}
          isEditing={!!selectedWork}
        />
        
        <ConfirmDialog
          isOpen={isConfirmOpen}
          onClose={() => setIsConfirmOpen(false)}
          onConfirm={handleConfirmDelete}
          title="Подтверждение удаления"
          message={`Удалить запись "${workToDelete?.doc_number}"?`}
        />
      </div>
    </Theme>
  );
}

export default App;