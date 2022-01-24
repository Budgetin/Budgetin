import { getAPI, employeeAPI } from "@/plugins/axios-api";
import router from "@/router";
import store from "@/store";

export default function setup() {
  const employeeKey = "BJYGaenU.YViIPguaXbmvfcPhpb6tsNKcVaawBCyi";

  // getAPI.interceptors.request.use(
  //   (config) => {
  //     const token = store.state.auth.token;
  //     if (token) {
  //       config.headers.common["Authorization"] = `Token ${token}`;
  //     }
  //     return config;
  //   },
  //   (error) => {
  //     return Promise.reject(error);
  //   }
  // );

  employeeAPI.interceptors.request.use(
    (config) => {
      if (employeeKey) {
        config.headers.common["Authorization"] = `Api-Key ${employeeKey}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // getAPI.interceptors.response.use(
  //   (response) => {
  //     if (response.status === 200 || response.status === 201) {
  //       return Promise.resolve(response);
  //     } else {
  //       return Promise.reject(response);
  //     }
  //   },
  //   (error) => {
  //     if (error.response.status) {
  //       switch (error.response.status) {
  //         case 400:
  //           break;

  //         case 401:
  //           store
  //             .dispatch("auth/logout")
  //             .then(() => router.push({ name: "Session Expired" }));

  //           break;

  //         case 403:
  //           break;

  //         case 404:
  //           break;
  //       }
  //       return Promise.reject(error);
  //     } else {
  //       return Promise.reject(error);
  //     }
  //   }
  // );
}
