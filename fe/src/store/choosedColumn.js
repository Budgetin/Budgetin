const choosedColumn = {
    namespaced: true,
    state: {
      listColumn: [
        { text: "For", value: "planning.year", width: "5rem" },
      ],
    },
    getters: {
    },
    mutations: {
      PUSH_LIST(state, newList) {
        state.listColumn.push(newList);
      },
      POP_LIST(state) {
        state.listColumn.pop();
      },
      SET_LIST(state, list) {
        state.listColumn = list;
      },
    },
    actions: {
    },
  };
  
  export default choosedColumn;
  