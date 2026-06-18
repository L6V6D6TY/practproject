import React, { useState, useEffect } from 'react';
import { Theme, presetGpnDefault } from '@consta/uikit/Theme';
import { Button } from '@consta/uikit/Button';
import { Table } from '@consta/uikit/Table';
import { SnackBar } from '@consta/uikit/SnackBar';
import FilterPanel from './components/FilterPanel';
import WorkForm from './components/WorkForm';
import ConfirmDialog from './components/ConfirmDialog';
import { worksApi } from './api/works';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedWork, setSelectedWork] = useState(null);
  const [workToDelete, setWorkToDelete] = useState(null);
  
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [currentFilter, setCurrentFilter] = useState({ field: null, value: null });
  
  const [snacks, setSnacks] = useState([]);

  const showNotification = (message, status = 'success') => {
    setSnacks(prev => [...prev, { message, status, autoClose: true, key: Date.now() }]);
  };

  const handleEdit = (work) => {
    setSelectedWork(work);
    setIsFormOpen(true);
  };

  const handleDelete = (work) => {
    setWorkToDelete(work);
    setIsConfirmOpen(true);
  };

  const fetchData = async (newPage = 1, field = null, value = null) => {
    setLoading(true);
    try {
      const params = { page: newPage, limit: 100 };
      if (field && value) {
        params.field = field;
        params.value = value;
      }
      const response = await worksApi.getAll(params);
      const items = response.data.items || [];
      
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
                fontSize: '12px'
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
                fontSize: '12px'
              }}
            >
              Удалить
            </button>
          </div>
        ),
      }));
      
      setData(itemsWithButtons);
      setTotal(response.data.total || 0);
      setTotalPages(response.data.total_pages || 0);
      setPage(newPage);
    } catch (error) {
      console.error('Ошибка:', error);
      showNotification('Ошибка загрузки данных', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(1);
  }, []);

  const handleFilter = (field, value) => {
    setCurrentFilter({ field, value });
    fetchData(1, field, value);
  };

  const handleResetFilter = () => {
    setCurrentFilter({ field: null, value: null });
    fetchData(1);
  };

  const handlePageChange = (newPage) => {
    fetchData(newPage, currentFilter.field, currentFilter.value);
  };

  const handleAdd = () => {
    setSelectedWork(null);
    setIsFormOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (workToDelete) {
      try {
        await worksApi.delete(workToDelete.id);
        fetchData(page, currentFilter.field, currentFilter.value);
        showNotification('Запись удалена');
      } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка при удалении', 'error');
      } finally {
        setIsConfirmOpen(false);
        setWorkToDelete(null);
      }
    }
  };

  const handleSubmitForm = async (formData) => {
    try {
      if (selectedWork) {
        await worksApi.update(selectedWork.id, formData);
        showNotification('Запись обновлена');
      } else {
        await worksApi.create(formData);
        showNotification('Запись добавлена');
      }
      fetchData(page, currentFilter.field, currentFilter.value);
      setIsFormOpen(false);
      setSelectedWork(null);
    } catch (error) {
      console.error('Ошибка:', error);
      showNotification(error.response?.data?.detail || 'Произошла ошибка', 'error');
    }
  };

  const columns = [
    { title: 'Номер документа', accessor: 'doc_number' },
    { title: 'Статус', accessor: 'status' },
    { title: 'Вид НД', accessor: 'work_type' },
    { title: 'Подразделение', accessor: 'department' },
    { title: 'Производитель работ', accessor: 'work_foreman' },
    { title: 'Действия', accessor: 'actions' },
  ];

  return (
    <Theme preset={presetGpnDefault}>
      <div style={{ padding: '20px' }}>
        <h1>Наряд-допуски</h1>
        <h3>Всего записей: {total}</h3>
        
        <FilterPanel onFilter={handleFilter} onReset={handleResetFilter} />
        
        <div style={{ marginBottom: '20px' }}>
          <Button label="Добавить запись" onClick={handleAdd} />
        </div>
        
        <Table columns={columns} rows={data} loading={loading} />
        
        {totalPages > 1 && (
          <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center', alignItems: 'center' }}>
            <Button 
              label="◀ Предыдущая" 
              disabled={page === 1}
              onClick={() => handlePageChange(page - 1)}
            />
            <span>Страница {page} из {totalPages}</span>
            <Button 
              label="Следующая ▶" 
              disabled={page === totalPages}
              onClick={() => handlePageChange(page + 1)}
            />
          </div>
        )}
        
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
        
        <SnackBar
          items={snacks}
          onItemClose={(item) => setSnacks(prev => prev.filter(i => i.key !== item.key))}
        />
      </div>
    </Theme>
  );
}

export default App;