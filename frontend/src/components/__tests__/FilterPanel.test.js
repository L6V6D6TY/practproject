import { render, screen, fireEvent } from '@testing-library/react';
import FilterPanel from '../FilterPanel';

test('renders filter panel with buttons', () => {
  const mockOnFilter = jest.fn();
  const mockOnReset = jest.fn();
  
  render(<FilterPanel onFilter={mockOnFilter} onReset={mockOnReset} />);
  
  expect(screen.getByText(/Применить фильтр/i)).toBeInTheDocument();
  expect(screen.getByText(/Сбросить/i)).toBeInTheDocument();
});

test('calls onReset when reset button is clicked', () => {
  const mockOnFilter = jest.fn();
  const mockOnReset = jest.fn();
  
  render(<FilterPanel onFilter={mockOnFilter} onReset={mockOnReset} />);
  
  const resetButton = screen.getByText(/Сбросить/i);
  fireEvent.click(resetButton);
  
  expect(mockOnReset).toHaveBeenCalled();
});