from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from src.agents import Student, College, Freelance
from src.schedule import RandomActivationByType
class CollegeStudent(Model):
    # valores iniciais da aplicação
    height = 30
    width = 30
    tipos_estudantes = 5
    initial_student = 100
    initial_college = 20

    student_multiply = 0.05
    college_multiply = 0.03

    college_gain_from_wage = 20

    freela = False
    freela_job_deadline = 30
    student_gain_from_wage = 4

    description = (
        "Um simples modelo para simular a relacao entre trabalhos da faculdade e um universitario tentando ganhar dinheiro(predador-presa)."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_student=100,
        tipos_estudantes=5,
        initial_college=20,
        student_multiply=0.05,
        college_multiply=0.03,
        college_gain_from_wage=20,
        freela=True,
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
            student = Student(self.next_id(), (x, y), self, True, money, tipo=i%tipos_estudantes)
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)

        # Create college
        for i in range(self.initial_college):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            money = self.random.randrange(2 * self.college_gain_from_wage)
            tipo_alun_matric = []
          
            for tipo_estudante in range(tipos_estudantes):
                rand = self.random.randrange(2)%2
                if rand == 0 and len(tipo_alun_matric) < 3:
                    tipo_alun_matric.append(tipo_estudante)
            if len(tipo_alun_matric) == 0:
                tipo_alun_matric = [self.random.randrange(1, tipos_estudantes,) -1]
            elif len(tipo_alun_matric) < 3: 
               while len(tipo_alun_matric) < 3:
                   tipo_alun_matric.append(tipo_alun_matric[0])
            college = College(self.next_id(), (x, y), self, True, money, tipo_alun_matric)
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

                patch = Freelance(self.next_id(), (x, y),
                                  self, is_available, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
