from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

from src.agents import Freelance, Student, College
from src.model import CollegeStudent


def university_canvas(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Student:
        if agent.tipo == 0:
          portrayal["Shape"] = "assets/black_student.png"
        elif agent.tipo == 1:
            portrayal["Shape"] = "assets/pink_student.png"
        elif agent.tipo == 2:
           portrayal["Shape"] = "assets/yellow_student.png"
        elif agent.tipo == 3:
           portrayal["Shape"] = "assets/green_student.png"
        elif agent.tipo == 4:
            portrayal["Shape"] = "assets/red_student.png"
        else:
           portrayal["Shape"] = "assets/blue_student.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is College:
        def coresDoCollege(tipo): 
            return {0: "#000", 1: "#8e24aa", 2: "#ffeb3b", 3:  "#4caf50", 4: "#ef5350"}[tipo],
   
        colors = list(map(coresDoCollege,agent.tipos)) 

        portrayal["Color"] = colors
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Freelance:
        if agent.is_available:
            portrayal["Shape"] = "assets/bitcoin.png"
            portrayal["scale"] = 0.9
            portrayal["Layer"] = 2
        else:
            portrayal["Color"] = ["#7f0000", "#b71c1c", "#f05545"]
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(university_canvas, 20, 20, 500, 500)

model_params = {
    "initial_student": UserSettableParameter(
        "slider", "Quantidade inicial de estudantes", 100, 10, 300
    ),
     "tipos_estudantes": UserSettableParameter(
        "slider", "Quantidade de tipos de estudantes", 3, 1, 5
    ),
    "initial_college": UserSettableParameter(
        "slider", "Quantidade de trabalho da faculdade", 50, 10, 300
    ),
    "college_multiply": UserSettableParameter(
        "slider",
        "Quantidade de oportunidades de trabalho em porcento",
        0.05,
        0.01,
        1.0,
        0.01,
        description="Quantidade de oportunidades de trabalho",
    ),
    "student_gain_from_wage": UserSettableParameter(
        "slider", "Valor recebido por freela", 4, 1, 10
    ),
}

server = ModularServer(
    CollegeStudent, [canvas_element,
                     ], "Universitários em busca do PJ", model_params
)
server.port = 8521
