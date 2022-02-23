<template>
  <v-container>
    <v-card class="pt-5">
      <!-- <iframe src="https://sense-demo.qlik.com/single/?appid=b23be62b-79d1-4761-b576-00ebc19acfb3&sheet=GZGbMWW&opt=ctxmenu,currsel" style="border:none;width:100%;height:1000px;"></iframe> -->
        <!-- <iframe src="http://kp2misdb03/Reports/powerbi/Dashboard/GSIT/ITHC/Test?rs:embed=true" style="border:none;width:100%;height:1000px;"></iframe> -->
        <apexchart  type="area" height="350" :options="chartOptions" :series="series"></apexchart>
      <!-- </div> -->
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Dashboard",
  components: {

  },
  
  created() {
    this.setBreadcrumbs();
  },
  methods: {
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Dashboard",
          disabled: true,
        },
      ]);
    },
  },
  data: () => ({          
    series: [{
      name: 'series1',
      data: [31, 40, 28, 51, 42, 109, 100]
    }, {
      name: 'series2',
      data: [11, 32, 45, 32, 34, 52, 41]
    }],
    chartOptions: {
      chart: {
        width: '100%',
        height: 350,
        type: 'area'
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      xaxis: {
        type: 'datetime',
        categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
      },
      tooltip: {
        x: {
          format: 'dd/MM/yy HH:mm'
        },
      },
    },
  }),
};
</script>

<style lang="scss" scoped>
#master-coa {
  width: 80%;
  margin: 0px auto;

  .master-coa__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-coa__input {
    padding: 10px 32px;
  }

  .master-coa__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-coa__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .master-coa__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-coa {
    .master-coa__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-coa__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>