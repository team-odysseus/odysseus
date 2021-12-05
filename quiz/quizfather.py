from quizmain import QuizMain

class QuizFather(object):
    def __init__(self):
        self.agents: dict = {}
        agent = QuizMain()
        self.agents.update({0: agent})
        pass

    def __call__(self):

        pass

if __name__ == '__main__':
    q = QuizFather()
