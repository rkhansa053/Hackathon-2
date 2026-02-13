import React, { useState } from 'react';
import { CreateTaskData } from '@/types/task';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

interface TaskFormProps {
  onSubmit: (data: CreateTaskData) => void;
  onCancel?: () => void;
  isLoading?: boolean;
  initialData?: Partial<CreateTaskData>;
}

export function TaskForm({ onSubmit, onCancel, isLoading, initialData }: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Task title is required');
      return;
    }

    if (title.length > 200) {
      setError('Task title must be less than 200 characters');
      return;
    }

    setError('');
    onSubmit({ title: title.trim(), description: description.trim() });

    if (!initialData) {
      // Only reset the form if this is for creating a new task
      setTitle('');
      setDescription('');
    }
  };

  const isEditing = !!initialData;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Input
          id="task-title"
          name="title"
          type="text"
          required
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          error={error}
          aria-label="Task title"
        />
      </div>

      <div>
        <Input
          id="task-description"
          name="description"
          type="text"
          placeholder="Task description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          aria-label="Task description"
        />
      </div>

      <div className="flex space-x-2">
        <Button type="submit" loading={isLoading} disabled={isLoading}>
          {isEditing ? 'Update Task' : 'Add Task'}
        </Button>
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}