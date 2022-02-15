const breadcrumbs = {
    namespaced: true,
    state: {
      links: [
        {
          text: "Index",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "Index",
          },
        },
      ],
    },
    getters: {
    },
    mutations: {
      PUSH_LINK(state, newLink) {
        state.links.push(newLink);
      },
      POP_LINK(state) {
        state.links.pop();
      },
      SET_LINKS(state, links) {
        state.links = links;
      },
    },
    actions: {
    },
  };
  
  export default breadcrumbs;
  