from locust import HttpUser, task, between



class HelloWorldUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")
        # self.client.get("/world")

    @task
    def test_register_with_good_data(self):
        form_data = {'username': 'Kevin', 'password': 'AZERTY05'}
        self.client.post('/register', data=form_data)

    @task
    def test_register_existing_username(self):
        form_data = {'username': 'Kevin', 'password': 'AZERTY05'}
        self.client.post('/register', data=form_data)

    @task
    def test_login_page(self):
        form_data = {'username': 'Kevin', 'password': 'AZERTY05'}
        self.client.post('/login', data=form_data)

    
