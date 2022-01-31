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
    statusMonitor: [
      { id: "2", label: "Submitted" },
      { id: "1", label: "Draft" },
      { id: "0", label: "To-Do" },
    ]
  },
};

export default statusInfo;
