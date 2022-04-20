from locust import HttpUser, task

class MatrixMultiplication(HttpUser):
    '''
    This is a locust user class that will perform matrix multiplication load testing
    '''
    @task
    def matrix(self):
        A = open('../input/A8.txt', 'r').read()
        B = open('../input/B8.txt', 'r').read()
        files={"A": A, "B": B}
        self.client.post("/matrix", files=files, data={"deadline": 0.03})
