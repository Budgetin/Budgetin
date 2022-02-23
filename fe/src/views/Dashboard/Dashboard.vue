<template>
  <v-container>
    <v-card class="pt-5">
      <div class="row sparkboxes my-4">
        <div class="col-md-3">
          <div class="box box1 ml-5">
            <h1>2022</h1>
            <h2>Year</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box2">
            <h1>1.213.123.123</h1>
            <h2>Budget Planning</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box3">
            <h1>1.213.123.123</h1>
            <h2>Budget Realisasi</h2>
          </div>
        </div>
        <div class="col-md-3">
          <div class="box box4 mr-5">
            <h1>1.213.123.123</h1>
            <h2>Forecast</h2>
          </div>
        </div>
      </div>
      <!-- <iframe src="https://sense-demo.qlik.com/single/?appid=b23be62b-79d1-4761-b576-00ebc19acfb3&sheet=GZGbMWW&opt=ctxmenu,currsel" style="border:none;width:100%;height:1000px;"></iframe> -->
      <!-- <iframe src="http://kp2misdb03/Reports/powerbi/Dashboard/GSIT/ITHC/DashboarDomisili?rs:embed=true" style="border:none;width:100%;height:1000px;"></iframe> -->
      <apexchart type="bar" height="350" :options="chartOptions" :series="series"></apexchart>
      <!-- </div> -->
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Dashboard",
  components: {},

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
    series: [
      {
        name: "Planning",
        data: [44,  57,  61,  63,  66],
      },
      {
        name: "Realization",
        data: [76,  101,  87,  91,  94],
      },
    ],
    chartOptions: {
      chart: {
        type: "bar",
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "55%",
          endingShape: "rounded",
        },
      },
      colors:['#31e3e6', '#fea197'],
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
        categories: [
          "APT",
          "IIO",
          "DMO",
          "GAQ",
          "DIS",
        ],
      },
      yaxis: {
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
            return "$ " + val + " thousands";
          },
        },
      },
    },
  }),
};
</script>

<style scoped>
::v-deep h2,
h2,
h4 {
  display: flex;
  justify-content: center;
  font-weight: 600;
  color: white;
}
</style>

<style>
h1,
h2,
h2,
h4 {
  display: flex;
  justify-content: center;
  font-weight: 600;
  color: white;
}
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
