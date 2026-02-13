'use client';

import React, { useState } from 'react';
import { Task, UpdateTaskData } from '@/types/task';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card, CardBody } from '../ui/Card';
import { formatDate } from '@/lib/utils/date-format';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onUpdate: (id: string, data: UpdateTaskData) => void;
  onDelete: (id: string) => void;
  isLoading?: boolean;
}

export function TaskCard({ task, onToggleComplete, onUpdate, onDelete, isLoading }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleSave = () => {
    if (title.trim() === '') return;

    onUpdate(task.id, { title, description });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleCancel();
    } else if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSave();
    }
  };

  return (
    <Card className="mb-4">
      <CardBody>
        {isEditing ? (
          <div className="space-y-3">
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Task title"
              autoFocus
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Task description (optional)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              rows={3}
            />
            <div className="flex space-x-2">
              <Button onClick={handleSave} disabled={isLoading}>
                Save
              </Button>
              <Button variant="outline" onClick={handleCancel} disabled={isLoading}>
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id)}
                disabled={isLoading}
                className="h-5 w-5 text-indigo-600 rounded mt-0.5"
                aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
              />
              <div className="flex-1 min-w-0">
                <h3
                  className={`text-lg font-medium truncate ${
                    task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-500 mt-1">{task.description}</p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  Created: {formatDate(task.createdAt)} | Updated: {formatDate(task.updatedAt)}
                </p>
              </div>
            </div>
            <div className="flex space-x-2 ml-4">
              <Button variant="outline" size="sm" onClick={() => setIsEditing(true)}>
                Edit
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDelete(task.id)}
                disabled={isLoading}
                className="text-red-600 hover:text-red-800"
              >
                Delete
              </Button>
            </div>
          </div>
        )}
      </CardBody>
    </Card>
  );
}