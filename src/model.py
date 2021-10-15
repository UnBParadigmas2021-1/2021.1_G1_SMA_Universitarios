from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import Student, College, Freelance
from schedule import RandomActivationByType


class CollegeStudent(Model):
    """
    College-Student baseado no modelo de predacao
    """

    height = 20
    width = 20

    initial_student = 100
    initial_college = 20

    student_multiply = 0.05
    college_multiply = 0.03

    college_gain = 20

    freela = False
    freela_job_deadline = 30
    student_gain_from_wage = 4

    verbose = False  # Print-monitoring

    description = (
        "Um simples modelo para simular a relacao entre trabalhos da faculdade e um universitario tentando ganhar dinheiro(predador-presa)."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_student=100,
        initial_college=20,
        student_multiply=0.05,
        college_multiply=0.03,
        college_gain_from_wage=20,
        freela=False,
        freela_job_deadline=30,
        student_gain_from_wage=4,
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_student = initial_student
        self.initial_college = initial_college
        self.student_multiply = student_multiply
        self.college_multiply = college_multiply
        self.college_gain_from_wage = college_gain_from_wage
        self.freela = freela
        self.freela_job_deadline = freela_job_deadline
        self.student_gain_from_wage = student_gain_from_wage

        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "College jobs": lambda m: m.schedule.get_type_count(College),
                "Student": lambda m: m.schedule.get_type_count(Student),
            }
        )

        # Create student:
        for i in range(self.initial_student):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            money = self.random.randrange(2 * self.student_gain_from_wage)
            student = Student(self.next_id(), (x, y), self, True, money)
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)

        # Create college
        for i in range(self.initial_college):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            money = self.random.randrange(2 * self.college_gain_from_wage)
            college = College(self.next_id(), (x, y), self, True, money)
            self.grid.place_agent(college, (x, y))
            self.schedule.add(college)

        # Create freela patches
        if self.freela:
            for agent, x, y in self.grid.coord_iter():

                is_available = self.random.choice([True, False])

                if is_available:
                    countdown = self.freela_job_deadline
                else:
                    countdown = self.random.randrange(self.freela_job_deadline)

                patch = Freelance(self.next_id(), (x, y), self, is_available, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(College),
                    self.schedule.get_type_count(Student),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number college: ", self.schedule.get_type_count(College))
            print("Initial number student: ", self.schedule.get_type_count(Student))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number college: ", self.schedule.get_type_count(College))
            print("Final number student: ", self.schedule.get_type_count(Student))