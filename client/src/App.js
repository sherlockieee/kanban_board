import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";

import Form from "./components/Form";
import Task from "./components/Task";

function App() {
  const [allTasks, setAllTasks] = useState([]);
  const [refresh, setRefresh] = useState({});

  useEffect(() => {
    axios
      .get("/api/tasks")
      .then((res) => {
        setAllTasks(res.data);
      })
      .catch((err) => console.log(err));
  }, [refresh]);

  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  return (
    <div className="App">
      <h1>Welcome to my Kanban board</h1>
      <Form />
      <div className="columns">
        {["to-do", "doing", "done"].map((taskType) => (
          <div>
            <h3 className="header">{capitalizeFirstLetter(taskType)}</h3>
            <ul className="lists">
              {allTasks
                .filter((task) => task.type == taskType)
                .map((task) => (
                  <Task task={task} setRefresh={setRefresh} />
                ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
