import React from 'react';
import { Table } from '@consta/uikit/Table';
import { Button } from '@consta/uikit/Button';
import { IconEdit } from '@consta/icons/IconEdit';
import { IconTrash } from '@consta/icons/IconTrash';

const DataTable = ({ data, onEdit, onDelete, loading }) => {
  const columns = [
    { title: 'ID', accessor: 'id', width: 70 },
    { title: 'Номер документа', accessor: 'doc_number', width: 140 },
    { title: 'Дата формирования', accessor: 'doc_date', width: 130 },
    { title: 'Статус', accessor: 'status', width: 120 },
    { title: 'Вид НД', accessor: 'work_type', width: 150 },
    { title: 'Организация', accessor: 'organization', width: 180 },
    { title: 'Подразделение', accessor: 'department', width: 120 },
    { title: 'Установка/Участок', accessor: 'unit', width: 150 },
    { title: 'Производитель работ', accessor: 'work_foreman', width: 200 },
    { title: 'Решение комиссии', accessor: 'commission_decision', width: 120 },
    { title: 'Кол-во загрузок', accessor: 'load_count', width: 100 },
    {
      title: 'Действия',
      accessor: 'actions',
      width: 100,
      cell: (row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button
            view="ghost"
            size="s"
            iconLeft={IconEdit}
            onClick={() => onEdit(row)}
            title="Редактировать"
          />
          <Button
            view="ghost"
            size="s"
            iconLeft={IconTrash}
            onClick={() => onDelete(row)}
            title="Удалить"
          />
        </div>
      ),
    },
  ];

  const formattedData = data.map(item => ({
    ...item,
    doc_date: item.doc_date ? new Date(item.doc_date).toLocaleDateString('ru-RU') : '-',
  }));

  return (
    <div className="data-table">
      <Table
        columns={columns}
        rows={formattedData}
        loading={loading}
        zebraStriped="odd"
        borderBetweenRows
        borderBetweenColumns
      />
    </div>
  );
};

export default DataTable;