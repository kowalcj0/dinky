from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    @task
    def bgnd(self):
        self.client.get("/v0/dinky/bgnd")
        

class WebsiteUser(HttpLocust):
    host = "http://127.0.0.1:8000"
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
