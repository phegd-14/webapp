import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ name: '', date: '', status: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/tasks')
      .then((response) => response.json())
      .then((data) => setTasks(data.tasks))
      .catch((err) => setError('Failed to fetch tasks'));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTask({ ...newTask, [name]: value });
  };

  const addTask = () => {
    fetch('http://127.0.0.1:8000/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTask),
    })
      .then((response) => response.json())
      .then((data) => {
        setTasks([...tasks, data.task]);
        setNewTask({ name: '', date: '', status: '' });
      })
      .catch((err) => setError('Failed to add task'));
  };

  const deleteTask = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
      method: 'DELETE',
    })
      .then(() => {
        setTasks(tasks.filter((task) => task.id !== taskId));
      })
      .catch((err) => setError('Failed to delete task'));
  };

  return (
    <div className="App">
      <h1>Task Manager</h1>
      {error && <p className="error">{error}</p>}
      <div className="task-form">
        <input
          type="text"
          name="name"
          placeholder="Task Name"
          value={newTask.name}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="date"
          placeholder="Task Date"
          value={newTask.date}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="status"
          placeholder="Task Status"
          value={newTask.status}
          onChange={handleInputChange}
        />
        <button onClick={addTask}>Add Task</button>
      </div>
      <div className="task-list">
        {tasks.map((task) => (
          <div key={task.id} className="task-item">
            <p>
              <strong>{task.name}</strong> - {task.date} - {task.status}
            </p>
            <button onClick={() => deleteTask(task.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
