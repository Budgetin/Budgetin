<template>
  <v-container style="height: 1000px">
    <v-row no-gutters justify="space-between">
      <!-- <iframe src='http://10.20.212.231/single/?appid=3e419129-d21b-41c2-b547-b9871eb73bc1&sheet=c3006dfe-4109-464f-bbbb-3b8d985c9c76&opt=currsel%2Cctxmenu' style='border:none;width:100%;height:100%;'></iframe> -->
      <iframe src="https://sense-demo.qlik.com/single/?appid=b23be62b-79d1-4761-b576-00ebc19acfb3&sheet=GZGbMWW&opt=ctxmenu,currsel" style="border:none;width:100%;height:1000px;"></iframe>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Dashboard",
  components: {},
  
  created() {
  },
  methods: {
  },
  data: () => ({
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