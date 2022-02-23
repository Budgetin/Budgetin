<template>
  <v-app id="dashboard">
  <v-container class="dashboard__container outer-container">
      <v-subheader class="dashboard__header">Overview {{year}}
      </v-subheader>
      <div class="row sparkboxes my-4">
        <div class="col-md-3">
          <div class="box box1 ml-5">
            <h1>{{year}}</h1>
            <h2>Year</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box2">
            <h1>{{numberWithDots(totalPlanning)}}</h1>
            <h2>Budget Planning</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box3">
            <h1>PEER NICH !!</h1>
            <h2>Budget Realisasi</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box4 mr-5">
            <h1>PEER NICH !!</h1>
            <h2>Forecast</h2>
          </div>
        </div>
      </div>
      <!-- <iframe src="https://sense-demo.qlik.com/single/?appid=b23be62b-79d1-4761-b576-00ebc19acfb3&sheet=GZGbMWW&opt=ctxmenu,currsel" style="border:none;width:100%;height:1000px;"></iframe> -->
      <!-- <iframe src="http://kp2misdb03/Reports/powerbi/Dashboard/GSIT/ITHC/DashboarDomisili?rs:embed=true" style="border:none;width:100%;height:1000px;"></iframe> -->
      <apexchart
        ref="refreshChart"
        type="bar"
        :options="chartOptions"
        :series="series"
      ></apexchart>
      <v-btn @click="setValue">Pencet aku mas</v-btn>
  </v-container>
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import formatting from "@/mixins/formatting";
export default {
  name: "Dashboard",
  components: {},
  mixins: [formatting],
  created() {
    this.setBreadcrumbs();
    this.setValue();
  },
  computed: {
    ...mapState("dashboard", [
      "loadingGetBudgetRealizationEveryGroup",
      "dataGroup",
      "dataBudgetEveryGroup",
    ]),
  },
  methods: {
    ...mapActions("dashboard", ["getBudgetRealizationEveryGroup"]),
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Dashboard",
          disabled: true,
        },
      ]);
    },

    setValue() {
      this.getBudgetRealizationEveryGroup().then(() => {
        this.chartOptions = {
          ...this.chartOptions,
          ...{
            xaxis: {
              categories: this.dataGroup,
            },
          },
        };
        this.$refs.refreshChart.updateSeries([
          {
            data: this.dataBudgetEveryGroup,
          },
        ]);
        for (let index = 0; index < this.dataBudgetEveryGroup.length; index++) {
          this.totalPlanning = this.totalPlanning + this.dataBudgetEveryGroup[index];
        }
      });
    },
  },
  data: () => ({
    year : new Date().getFullYear(),
    totalPlanning : 0, 
    series: [
      {
        name: "Planning",
        data: [],
      },
      {
        name: "Realization",
        data: [],
      },
    ],
    chartOptions: {
      chart: {
        type: "bar",
        height: 500,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "55%",
          endingShape: "rounded",
        },
      },
      colors: ["#31e3e6", "#fea197"],
      // colors:['#6adaf0', '#ff89a8'],
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ["transparent"],
      },
      xaxis: {
        categories: [],
      },
      yaxis: {
        labels: {
          formatter: function (val) {
            return val
              .toString()
              .split(/(?=(?:\d{3})+(?:\.|$))/g)
              .join(",");
          },
        },
        title: {
          text: "",
        },
      },
      fill: {
        opacity: 1,
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val
              .toString()
              .split(/(?=(?:\d{3})+(?:\.|$))/g)
              .join(",");
          },
        },
      },
    },
  }),
};
</script>

<style scoped>
::v-deep h1,
h2 {
  display: flex;
  justify-content: center;
  font-weight: 600;
  color: white;
}
</style>

<style>
.box {
  background-color: #2b2d3e;
  padding: 25px 20px;
}

.sparkboxes .box {
  padding-top: 10px;
  padding-bottom: 10px;
  text-shadow: 0 1px 1px 1px #666;
  box-shadow: 0px 1px 15px 1px rgba(69, 65, 78, 0.08);
  border-radius: 5px;
}

.sparkboxes .box1 {
  /* background-color: #0396ff; */
  background-image: linear-gradient(135deg, #abdcff 10%, #0396ff 100%);
}

.sparkboxes .box2 {
  /* background-color: #1B4332; */
  background-image: linear-gradient(135deg, #2afadf 10%, #4c83ff 100%);
}

.sparkboxes .box3 {
  /* background-color: #fd6585; */
  background-image: linear-gradient(135deg, #ffd3a5 10%, #fd6585 100%);
}

.sparkboxes .box4 {
  /* background-color: #744EC2; */
  background-image: linear-gradient(135deg, #ee9ae5 10%, #5961f9 100%);
}
</style>

<style lang="scss" scoped>
#dashboard {
  .dashboard__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .dashboard__input {
    padding: 10px 32px;
  }

  .dashboard__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .dashboard__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}
</style>