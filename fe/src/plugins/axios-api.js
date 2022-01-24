import axios from "axios";
import Config from "./Config";

const getAPI = axios.create({
  baseURL: Config.BASE_URL,
  timeout: 170000,
});

const employeeAPI = axios.create({
  baseURL: Config.EMPLOYEE_URL,
  timeout: 170000,
});
export { getAPI,employeeAPI};
