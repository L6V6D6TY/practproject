import { render, screen } from '@testing-library/react';
import App from './App';

test('renders table with title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Наряд-допуски/i);
  expect(titleElement).toBeInTheDocument();
});

test('displays filter panel', () => {
  render(<App />);
  const filterButton = screen.getByText(/Применить фильтр/i);
  expect(filterButton).toBeInTheDocument();
});