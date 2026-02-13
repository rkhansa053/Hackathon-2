import React from 'react';
import { Task } from '@/types/task';
import { TaskCard } from './TaskCard';
import { EmptyState } from './EmptyState';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: string) => void;
  onUpdate: (id: string, data: Partial<Task>) => void;
  onDelete: (id: string) => void;
  isLoading?: boolean;
  emptyMessage?: string;
}

export function TaskList({
  tasks,
  onToggleComplete,
  onUpdate,
  onDelete,
  isLoading,
  emptyMessage = 'No tasks yet. Create your first task!',
}: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState message={emptyMessage} />;
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onUpdate={onUpdate}
          onDelete={onDelete}
          isLoading={isLoading}
        />
      ))}
    </div>
  );
}