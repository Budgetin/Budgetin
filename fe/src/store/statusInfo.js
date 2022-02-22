const statusInfo = {
  namespaced: true,
  state: {
    statusRole: [
      { id: "2", label: "Admin" },
      { id: "1", label: "User" },
    ],
    statusInfoMaster: [
      { id: 1, label: "Active" },
      { id: 0, label: "Inactive" },
    ],
    statusInfoPlanning: [
      { id: 1, label: "Active" },
      { id: 0, label: "Inactive" },
    ],
    statusNotification: [
      { id: 1, label: "Yes" },
      { id: 0, label: "No" },
    ],
    statusTechNonTech: [
      { id: 1, label: "Tech" },
      { id: 0, label: "Non-Tech" },
    ],
    statusCAPEXOPEX: [
      { id: 1, label: "CAPEX" },
      { id: 2, label: "OPEX" },
    ],
    statusIsBudget: [
      { id: true, label: "Active" },
      { id: false, label: "Inactive" },
    ],
  },
};

export default statusInfo;
