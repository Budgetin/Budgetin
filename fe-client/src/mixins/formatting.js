export default {
    methods: {
      /**
       * Function to insert . in between 3 digits.
       * @param num
       * @returns {string}
       */
      numberWithDots(num) {
        if (num) {
          num = num.toString().replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '');
          return num.toString().split( /(?=(?:\d{3})+(?:\.|$))/g ).join( "," );
        }
      },
  
      /**
       * Function to format Date into: dd Month yyyy
       * ex: 01 June 2021
       * @param date
       * @returns {string}
       */
      formatDate(date) {
        if (date) {
          const newDate = new Date(date);
          const day = newDate.getDate();
          const month = newDate.toLocaleString("default", { month: "long" });
          const year = newDate.getFullYear();
          return day + " " + month + " " + year;
        }
      },
  
      /**
       * Function to format datetime into: DD/MM/YYYY - hh:mm:ss
       * ex: 01/06/2021 - 10:30:05
       * @param datetime
       * @returns {string}
       */
      formatDateTime(datetime) {
        let date = this.formatDate(datetime);
        let hour = String(parseInt(datetime.slice(11, 13)) + 7).padStart(2, "0");
        let time = hour + ":" + datetime.slice(14, 19);
        return date + " - " + time;
      },
  
      /**
       * Function to format Date into: Month yyyy
       * ex: June 2021
       * @param date
       * @returns {string}
       */
      formatMonth(date) {
        if (date) {
          const newDate = new Date(date);
          const month = newDate.toLocaleString("default", { month: "long" });
          const year = newDate.getFullYear();
          return month + " " + year;
        }
      },
      camelCaseToSentenceCase(text) {
        const result = text.replace(/([A-Z])/g, " $1");
        const finalResult = result.charAt(0).toUpperCase() + result.slice(1);
        return finalResult;
      },
    },
  };
  