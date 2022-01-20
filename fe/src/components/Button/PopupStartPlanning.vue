<!-- <template>
  <v-dialog max-width="600px" v-model="dialog">
    <v-btn flat slot="activator" class="success">Add New Planning</v-btn>
    <v-card>
      <v-card-title>
        <h2>Fill the Form</h2>
      </v-card-title>
    </v-card>
  </v-dialog>
</template> -->

<template>
  <v-row justify="center">
    <v-col align="right" class="mr-7">
      <v-dialog
        v-model="dialog"
        persistent
        max-width="800px"
        height="unset">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="cyan"
            dark
            v-bind="attrs"
            v-on="on">
            + START NEW PLANNING
          </v-btn>
        </template>
        
        <v-card>
          <v-card-title class="text-h5">
            Start a New Planning
          </v-card-title>
          <v-card-text>
            <v-form class="px-3">
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <div class="planningFor">
                    <v-text-field v-model="planningFor" label="Planning for" prepend-icon="mdi-notebook"></v-text-field>
                  </div>
                </v-col>
                <v-col ml="4" offset-md="2">
                  <div class="status">
                    <v-text-field v-model="status" label="Status" prepend-icon="mdi-clock-check"></v-text-field>
                  </div>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-menu
                    v-model="menu2"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="auto">
                    <template v-slot:activator="{ on, attrs }">
                      <div class="dueDate">
                        <v-text-field
                          v-model="date"
                          label="Due Date"
                          prepend-icon="mdi-calendar"
                          readonly
                          v-bind="attrs"
                          v-on="on">
                        </v-text-field>
                      </div>
                    </template>
                    <v-date-picker
                      v-model="date"
                      @input="menu2 = false">
                    </v-date-picker>
                  </v-menu>
                </v-col>

                <!-- Send Notification DropDown-->
                <v-col md="4" offset-md="2">
                  <div class="sendNotif">
                    <!-- <v-text-field v-model="sendNotif" label="Send Notification" prepend-icon="mdi-bell-ring"></v-text-field> -->

                    <v-menu>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          flat slot="activator"
                          color="white"
                          v-bind="attrs"
                          v-on="on">
                          <span>Send Notification</span>
                          <v-icon>mdi-chevron-down</v-icon>
                        </v-btn>
                      </template>

                      <v-list>
                        <v-list-item @click="">
                          <v-list-item-title>
                            HAHAHA
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-for="(link, index) in links" :key="index" router :to="link.route">
                          <v-list-item-title>
                            {{ link.title }}
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>

                    <!-- If Send Notification Yes -->
                    <v-expand-transition>
                      <div v-show="show">
                        <v-divider></v-divider>
                        <v-card-text>
                          I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
                        </v-card-text>
                      </div>
                    </v-expand-transition>

                    <!-- <v-switch
                      v-model="sendNotif"
                      label="Send Notification"></v-switch>
                    <v-menu top :close-on-content-click="sendNotif">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="white"
                          v-bind="attrs"
                          v-on="on">
                          Send Notification
                        </v-btn>
                      </template>

                      <v-list>
                        <v-list-item
                          v-for="(item, index) in items"
                          :key="index">
                          <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu> -->
                  </div>
                </v-col>
              </v-row>
              <!-- <v-btn flat @click="submit" class="success mx-0 mt-3">Submit</v-btn> -->
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-col md="2" offset-md="7">
              <div class="cancelBtn">
                <v-btn
                  rounded
                  outlined
                  color="blue-grey darken-2"
                  @click="dialog = false"
                  style="width:100px;">
                  Cancel
                </v-btn>
              </div>
            </v-col>
            <v-col>
              <div class="saveBtn">
                <v-btn
                  rounded
                  color="cyan"
                  dark
                  @click="submit"
                  style="width:100px;"
                  class="saveBtn--text">
                  Save
                </v-btn>
              </div>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>  
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      planningFor: '',
      status: '',
      sendNotif: '',
      date: null,
    }
  },
  data: () => ({
      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      menu2: false,
      dialog: false,

      links: [
        { title: 'Yes', route: '/' },
        { title: 'No', route: '/' },
      ],
      closeOnContentClick: true,
    }),
  methods: {
    submit() {
      console.log(this.planningFor, this.status, this.date, this.sendNotif)
    },
  },
}
</script>

<style scoped>
    .planningFor {
        width: 295px;
    }
    .status {
        width: 295px;
    }
    .dueDate {
        width: 295px;
    }
    .sendNotif {
        width: 295px;
    }

    .cancelBtn {
        width: 200px;
    }
    .saveBtn {
        width: 200px;
    }
    .saveBtn--text /deep/ label {
        color: white;
    }
</style>
