


import time
import random, string
from locust import HttpUser, task, between

tasks = [
    "task_shape",
    "task_pos",
    "task_size",
    "task_color",
    "task_rot",
    "task_flip",
    "task_count",
    "task_inside",
    "task_contact",
    "task_pos_shape_1",
    "task_size_shape_1",
    "task_shape_color",
    "task_shape_rot_1",
    "task_shape_flip_1",
    "task_shape_count_1",
    "task_shape_inside",
    "task_shape_contact_2",
    "task_pos_flip_1",
    "task_pos_count_2",
    "task_pos_inside_3",
    "task_pos_contact",
    "task_pos_size_1",
    "task_pos_col_1",
    "task_pos_rot_1",
    "task_size_color_1",
    "task_size_rot_2",
    "task_size_flip_1",
    "task_size_count_1",
    "task_size_inside_1",
    "task_size_contact",
    "task_rot_color",
    "task_flip_color_1",
    "task_color_count_1",
    "task_color_inside_1",
    "task_color_contact",
    "task_rot_flip_1",
    "task_rot_count_1",
    "task_rot_inside_3",
    "task_rot_contact_1",
    "task_flip_count_1",
    "task_flip_inside_3",
    "task_flip_contact_1",
    "task_inside_count_1",
    "task_contact_count_1",
    "task_inside_contact",
]
all_images = []
for t in tasks:
    for i in range(20):
        for j in range(4):
            all_images.append("/static/human_exp_images/{}/{:02d}_{}.png".format(t, i, j))
# a = "https://cvrt.clps.brown.edu/static/human_exp_images/practice_img/00_0.png"

def gen_code(N):
    """Generate random completion code."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))


prolific_ids = [gen_code(20) for i in range(200)]
class QuickstartUser(HttpUser):
    wait_time = between(0.2, 3)

    @task
    def hello_world(self):
        # self.client.get("/?PROLIFIC_PID")
        # r = self.client.get("/")
        # r.text
        with self.client.get("/", catch_response=True) as response:
            if 'nginx' in response.text:
                response.failure("Wrong page nginx")
                print('err')

    # @task(1)
    @task()
    def view_items(self):
        for item_id in range(80):
            # i = random.randint(0, len(all_images)-1)
            i = 0
            im = all_images[i]
            self.client.get(im, name="/item")
            # time.sleep(0.05)

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})

