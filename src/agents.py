from mesa import Agent

class Freelance(Agent):

    def __init__(self, unique_id, pos, model, is_available, countdown):
        super().__init__(unique_id, model)
        self.is_available = is_available
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.is_available:
            if self.countdown <= 0:
                self.is_available = True
                self.countdown = self.model.freela_job_deadline
            else:
                self.countdown -= 1


class Student(Agent):
    money = None

    def __init__(self, unique_id, pos, model, moore, money=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.money = money

    def step(self):
        self.random_move()
        paid_bills = True

        if self.model.freela:
            self.money -= 1

            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            freelance = [obj for obj in this_cell if isinstance(obj, Freelance)][0]
            if freelance.is_available:
                self.money += self.model.student_gain_from_wage
                freelance.is_available = False

            if self.money < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                paid_bills = False

        if paid_bills and self.random.random() < self.model.student_start_work:
            if self.model.freela:
                self.money /= 2
            freshman = Student(
                self.model.next_id(), self.pos, self.model, self.moore, self.money
            )
            self.model.grid.place_agent(freshman, self.pos)
            self.model.schedule.add(freshman)


class College(Agent):

    money = None

    def __init__(self, unique_id, pos, model, moore, money=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.money = money

    def step(self):
        self.random_move()
        self.money -= 1

        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        student = [obj for obj in this_cell if isinstance(obj, Student)]
        if len(student) > 0:
            student_to_eat = self.random.choice(student)
            self.money += self.model.college_gain_from_wage

            self.model.grid._remove_agent(self.pos, student_to_eat)
            self.model.schedule.remove(student_to_eat)

        if self.money < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.college_start_work:
                self.money /= 2
                cub = College(
                    self.model.next_id(), self.pos, self.model, self.moore, self.money
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
