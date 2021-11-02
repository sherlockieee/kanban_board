import axios from "axios";
import React, { useState } from "react";
import "./Task.css";

function Task({ task, setRefresh }) {
  const handleDelete = (e) => {
    axios.delete(`/api/tasks/${task.id}`).then((res) => {
      console.log(res);
      setRefresh({});
    });
  };

  const handleChangeType = (e) => {
    const new_task = { ...task, type: e.target.value };
    axios.put(`/api/tasks/${task.id}`, new_task).then((res) => {
      console.log(res);
      setRefresh({});
    });
  };
  return (
    <li className="taskCard">
      <h4 className="taskName">{task.name}</h4>
      <p className="taskDescription">
        {task.description ? task.description : "No description available"}
      </p>

      <button className="changeTypeButton">
        <label htmlFor="type">Change task type:</label>
        <select
          name="task_type"
          id="type"
          className=""
          value={task.type}
          required
          onChange={handleChangeType}
        >
          <option value="to-do">To-do</option>
          <option value="doing">Doing</option>
          <option value="done">Done</option>
        </select>
      </button>
      <button className="deleteButton" onClick={handleDelete}>
        Delete
      </button>
    </li>
  );
}

export default Task;
