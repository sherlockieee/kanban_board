import React, { useState } from "react";
import axios from "axios";

function Form() {
  const [taskName, setTaskName] = useState("");
  const [taskDescription, setTaskDescription] = useState("");
  const [taskType, setTaskType] = useState("to-do");

  const handleSubmit = (e) => {
    const task = {
      name: taskName,
      description: taskDescription,
      type: taskType,
    };

    axios
      .post("/api/tasks", { task })
      .then((res) => {
        console.log(res);
        setTaskName("");
        setTaskDescription("");
        setTaskType("to-do");
      })
      .catch((err) => console.log(err));
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2 className="header">Add a new task</h2>
      <ul>
        <li>
          <label htmlFor="name">Task name:</label>
          <input
            type="text"
            id="name"
            name="task_name"
            className="input"
            value={taskName}
            onChange={(e) => setTaskName(e.target.value)}
            required
          />
        </li>
        <li>
          <label htmlFor="description">Task description:</label>
          <textarea
            id="description"
            name="task_description"
            className="input"
            value={taskDescription}
            onChange={(e) => setTaskDescription(e.target.value)}
          ></textarea>
        </li>
        <li>
          <label htmlFor="type">Task type:</label>
          <select
            name="task_type"
            id="type"
            className=""
            value={taskType}
            required
            onChange={(e) => setTaskType(e.target.value)}
          >
            <option value="to-do">To-do</option>
            <option value="doing">Doing</option>
            <option value="done">Done</option>
          </select>
        </li>
        <li>
          <button type="submit" className="submit-button">
            Submit
          </button>
        </li>
      </ul>
    </form>
  );
}

export default Form;
