<template>
  <v-app id="master-product">
    <v-container class="master-product__container outer-container">
      <v-row no-gutters>
        <iframe src='http://10.20.212.231/single/?appid=3e419129-d21b-41c2-b547-b9871eb73bc1&sheet=c3006dfe-4109-464f-bbbb-3b8d985c9c76&opt=currsel%2Cctxmenu' style='border:none;width:100%;height:100%;'></iframe>
        <!-- <iframe src='https://app.powerbi.com/groups/me/dashboards/eb19d692-dc81-453b-8a58-8b85f20dbe12' style='border:none;width:100%;height:100%;'></iframe> -->
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: "Dashboard",
  components: {
      
  },
  watch: {},
  data: () => ({
    
  }),
  created() {
    
  },
  computed: {
    
  },
  methods: {
    
  }
}
</script>

<style>
button {
  min-width: 2rem;
}
</style>

<style lang="scss" scoped>
#master-product {
  .master-product__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-product__input {
    padding: 10px 32px;
  }

  .master-product__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-product__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-product {
    .master-product__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-product__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
