import React, { useState, useEffect } from 'react';
import { Theme, presetGpnDefault } from '@consta/uikit/Theme';
import { Button } from '@consta/uikit/Button';
import { Layout, LayoutContent } from '@consta/uikit/Layout';
import { Header } from '@consta/uikit/Header';
import DataTable from './components/DataTable';
import FilterPanel from './components/FilterPanel';
import WorkForm from './components/WorkForm';
import ConfirmDialog from './components/ConfirmDialog';
import { worksApi } from './services/api';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(100);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedWork, setSelectedWork] = useState(null);
  const [workToDelete, setWorkToDelete] = useState(null);
  const [currentFilter, setCurrentFilter] = useState({ field: null, value: null });

  const fetchData = async (pageNum = 1, filter = null) => {
    setLoading(true);
    try {
      let response;
      if (filter && filter.field && filter.value) {
        response = await worksApi.getAll(pageNum, limit, filter.field, filter.value);
      } else {
        response = await worksApi.getAll(pageNum, limit);
      }
      setData(response.items || []);
      setTotal(response.total || 0);
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      alert('Не удалось загрузить данные. Проверьте подключение к серверу.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(page, currentFilter);
  }, [page]);

  const handleFilter = (field, value) => {
    const filter = { field, value };
    setCurrentFilter(filter);
    setPage(1);
    fetchData(1, filter);
  };

  const handleResetFilter = () => {
    setCurrentFilter({ field: null, value: null });
    setPage(1);
    fetchData(1, null);
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

  const handleSubmitForm = async (formData) => {
    try {
      if (selectedWork) {
        await worksApi.update(selectedWork.id, formData);
      } else {
        await worksApi.create(formData);
      }
      fetchData(page, currentFilter);
      setIsFormOpen(false);
    } catch (error) {
      console.error('Ошибка сохранения:', error);
      alert(error.response?.data?.detail || 'Произошла ошибка при сохранении');
    }
  };

  const handleConfirmDelete = async () => {
    if (workToDelete) {
      try {
        await worksApi.delete(workToDelete.id);
        fetchData(page, currentFilter);
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Произошла ошибка при удалении');
      } finally {
        setIsConfirmOpen(false);
        setWorkToDelete(null);
      }
    }
  };

  const totalPages = Math.ceil(total / limit);

  const filterFields = [
    { label: 'Номер документа', value: 'doc_number' },
    { label: 'Статус', value: 'status' },
    { label: 'Вид НД', value: 'work_type' },
    { label: 'Подразделение', value: 'department' },
    { label: 'Производитель работ', value: 'work_foreman' },
  ];

  return (
    <Theme preset={presetGpnDefault}>
      <Layout>
        <Header leftSide={<h1 style={{ margin: 0 }}>Наряд-допуски</h1>} />
        <LayoutContent>
          <div className="app-container">
            <div className="actions-bar">
              <Button label="+ Добавить запись" onClick={handleAdd} />
            </div>

            <FilterPanel
              fields={filterFields}
              onFilter={handleFilter}
              onReset={handleResetFilter}
            />

            <DataTable
              data={data}
              onEdit={handleEdit}
              onDelete={handleDelete}
              loading={loading}
            />

            {totalPages > 0 && (
              <div className="pagination">
                <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
                  ◀ Предыдущая
                </button>
                <span>Страница {page} из {totalPages}</span>
                <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>
                  Следующая ▶
                </button>
              </div>
            )}

            <WorkForm
              isOpen={isFormOpen}
              onClose={() => setIsFormOpen(false)}
              onSubmit={handleSubmitForm}
              initialData={selectedWork}
              isEditing={!!selectedWork}
            />

            <ConfirmDialog
              isOpen={isConfirmOpen}
              onClose={() => setIsConfirmOpen(false)}
              onConfirm={handleConfirmDelete}
              title="Подтверждение удаления"
              message={`Вы действительно хотите удалить запись "${workToDelete?.doc_number}"?`}
            />
          </div>
        </LayoutContent>
      </Layout>
    </Theme>
  );
}

export default App;