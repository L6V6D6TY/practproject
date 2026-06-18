import React from 'react';
import { Modal } from '@consta/uikit/Modal';
import { Button } from '@consta/uikit/Button';
import { Card } from '@consta/uikit/Card';

const ConfirmDialog = ({ isOpen, onClose, onConfirm, title, message }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <Card verticalSpace="l" horizontalSpace="l" style={{ minWidth: '300px' }}>
        <h3 style={{ marginTop: 0 }}>{title}</h3>
        <p>{message}</p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '20px' }}>
          <Button label="Отмена" view="ghost" onClick={onClose} />
          <Button label="Подтвердить" onClick={onConfirm} />
        </div>
      </Card>
    </Modal>
  );
};

export default ConfirmDialog;