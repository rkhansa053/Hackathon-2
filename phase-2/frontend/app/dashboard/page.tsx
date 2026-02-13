'use client';

import React, { useState, useEffect } from 'react';
import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { tasksApi } from '@/lib/api/tasks';
import { TaskForm } from '@/components/tasks/TaskForm';
import { TaskList } from '@/components/tasks/TaskList';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/LoadingSpinner';
import AuthGuard from '@/lib/auth/auth-guard';
import Navbar from '@/components/navigation/Navbar';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await tasksApi.getAll();

      if (response.success) {
        setTasks(response.tasks || []);
      } else {
        setError(response.error || 'Failed to fetch tasks');
      }
    } catch (err) {
      setError('An error occurred while fetching tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (data: CreateTaskData) => {
    try {
      const response = await tasksApi.create(data);

      if (response.success && response.task) {
        setTasks([response.task, ...tasks]);
        setShowForm(false);
      } else {
        setError(response.error || 'Failed to create task');
      }
    } catch (err) {
      setError('An error occurred while creating task');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (id: string, data: UpdateTaskData) => {
    try {
      const response = await tasksApi.update(id, data);

      if (response.success && response.task) {
        setTasks(tasks.map(task => task.id === id ? response.task! : task));
      } else {
        setError(response.error || 'Failed to update task');
      }
    } catch (err) {
      setError('An error occurred while updating task');
      console.error('Error updating task:', err);
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      const response = await tasksApi.toggleComplete(id);

      if (response.success && response.task) {
        setTasks(tasks.map(task =>
          task.id === id ? response.task! : task
        ));
      } else {
        setError(response.error || 'Failed to toggle task completion');
      }
    } catch (err) {
      setError('An error occurred while toggling task completion');
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      const response = await tasksApi.delete(id);

      if (response.success) {
        setTasks(tasks.filter(task => task.id !== id));
      } else {
        setError(response.error || 'Failed to delete task');
      }
    } catch (err) {
      setError('An error occurred while deleting task');
      console.error('Error deleting task:', err);
    }
  };

  if (loading && tasks.length === 0) {
    return (
      <AuthGuard requireAuth redirectTo="/signin">
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <div className="container mx-auto py-8">
            <div className="flex justify-center items-center h-64">
              <Spinner />
            </div>
          </div>
        </div>
      </AuthGuard>
    );
  }

  return (
    <AuthGuard requireAuth redirectTo="/signin">
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <main className="container mx-auto py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>

              <Button onClick={() => setShowForm(!showForm)}>
                {showForm ? 'Cancel' : '+ Add Task'}
              </Button>
            </div>

            {error && (
              <div className="mb-4 rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            {showForm && (
              <div className="mb-8 p-6 bg-white rounded-lg shadow">
                <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
                <TaskForm
                  onSubmit={handleCreateTask}
                  onCancel={() => setShowForm(false)}
                  isLoading={loading}
                />
              </div>
            )}

            {loading && tasks.length > 0 ? (
              <div className="flex justify-center py-4">
                <Spinner />
              </div>
            ) : (
              <div>
                <TaskList
                  tasks={tasks}
                  onToggleComplete={handleToggleComplete}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                  isLoading={loading}
                />
              </div>
            )}
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}