from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(0.5, 3.0)
    
    # Test Without Login
    def on_start(self):
        # self.client.post("/login", {
        #     "username": "test_user",
        #     "password": ""
        # })
        pass
    
    # # GET COA
    @task(1)
    def coa(self):
        self.client.get("/api/coa/")
        
    # GET Strategy
    # @task(2)
    # def strategy(self):
    #     self.client.get("/api/strategy/")

    # # GET biro
    # @task(3)
    # def biroall(self):
    #     self.client.get("/api/biro/")

    # @task(4)
    # def biro(self):
    #     self.client.get("/api/ithc/biro/")

    # @task(5)
    # def monitoring(self):
    #     self.client.get("/api/monitoring/")

    # @task(6)
    # def planning(self):
    #     self.client.get("/api/planning/")
    
    # @task(7)
    # def product(self):
    #     self.client.get("/api/product/")

    # @task(8)
    # def project(self):
    #     self.client.get("/api/project/")
    
    # @task(9)
    # def projecttyle(self):
    #     self.client.get("/api/project_type/")

    # @task(10)
    # def user(self):
    #     self.client.get("/api/user/")