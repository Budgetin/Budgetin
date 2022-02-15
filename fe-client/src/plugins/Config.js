const BASE_URL_QA = "http://127.0.0.1:8000/";
const BASE_URL_UTT = "http://127.0.0.1:8000/";
const BASE_URL_PROD = "http://127.0.0.1:8000/";

let BASE_URL = null;

if (process.env.API_ENV === "production" || process.env.API_ENV === "PROD") {
  BASE_URL = BASE_URL_PROD;
} else if (
  process.env.API_ENV === "stagging" ||
  process.env.API_ENV === "UTT"
) {
  BASE_URL = BASE_URL_UTT;
} else if (
  process.env.API_ENV === "development" ||
  process.env.API_ENV === "DEVELOPMENT" ||
  process.env.API_ENV === "QA"
) {
  BASE_URL = BASE_URL_QA;
} else {
  BASE_URL = BASE_URL_QA;
}

const Config = {
  BASE_URL: BASE_URL,
};

export default Config;
