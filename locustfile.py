from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def sumar_numeros(self):
        payload = {"x": 10, "y": 5}
        self.client.post("/sumar", json=payload)