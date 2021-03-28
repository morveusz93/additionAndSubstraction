import pygame
from random import randint, choice


class WindowGame():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nauka matematyki")
        # basic variables 
        self.run = True
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # fonts:
        self.main_font = pygame.font.SysFont('georgia', 30)
        self.big_main_font = pygame.font.SysFont('georgia', 60)
        # colors:
        self.bg_color = (35,35,35)
        self.yellow = (230,230,40)
        self.green = (13,180,13)
        self.red = (181,13,27)
        # answer:
        self.answer = ''
        # images:
        self.img_good = pygame.image.load('images/good_answer.png')
        self.img_wrong = pygame.image.load('images/wrong_answer.png')
        self.img_think = pygame.image.load('images/thinking.png')
        self.img_status = 'think'
        self.enter_pressed = False


    def EventsTaker(self):
        for event in pygame.event.get():
            # close window
            if event.type == pygame.QUIT:
                self.run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                    break
                # if pressed key is number
                if event.unicode.isnumeric():
                    self.answer += event.unicode
                # if pressed key is backspace
                elif event.key == pygame.K_BACKSPACE:
                    # delete whole sign with spaces
                    if self.answer.endswith(' - ') or self.answer.endswith(' + '):
                        self.answer = self.answer[:-3]
                    else:
                        # delete the number
                        self.answer = self.answer[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # pressed enter
                    self.enter_pressed = True
                elif event.unicode == '-':
                    # sign Minus, if there is already sign plus, change it
                    # if there is already sign minus - do nothing
                    if self.answer.endswith(" - "):
                        continue
                    elif self.answer.endswith(' + '):
                        self.answer = self.answer[:-3] + ' - '
                    else:
                        self.answer += ' - '
                elif event.unicode == '+':
                    #sign plus, if there already is sign minus - change it
                    # if tehre is already sign plus - do nothing
                    if self.answer.endswith(" + "):
                        continue
                    elif self.answer.endswith(' - '):
                        self.answer = self.answer[:-3] + ' + '
                    else:
                        self.answer += ' + '
                

    # create input box at 1/3 of height, 1/2 of width
    # draw the answer there
    def DisplayInput(self):
        self.input_block = self.main_font.render(self.answer, True, self.yellow)
        self.input_rect = self.input_block.get_rect()
        self.input_rect.center = ((self.screen.get_rect().width//2), (self.screen.get_rect().height - self.input_rect.height)//3)
        self.screen.blit(self.input_block, self.input_rect)

    # create box with task at the center top of screen
    # draw there the task 
    def DisplayTask(self, task):
        task_block = self.big_main_font.render(str(task), True, self.yellow)
        task_rect = task_block.get_rect()
        task_rect.midtop = self.screen.get_rect().midtop
        self.screen.blit(task_block, task_rect)


    def DisplayImages(self, image):
        image_pos= (self.WIDTH//2 - 200, self.HEIGHT * 2//3 -50)
        if image == 'think':
            self.screen.blit(self.img_think, image_pos)
        elif image == 'good':
            self.screen.blit(self.img_good, image_pos)
        elif image == 'wrong':
            self.screen.blit(self.img_wrong, image_pos)


    def DisplayStats(self, corrects, wrongs):
        corrcets_str = f"Correct answers: {corrects}" 
        wrongs_str = f"Wrong answers: {wrongs}"
        corrects_block = self.main_font.render(corrcets_str, True, self.green)
        wrongs_block = self.main_font.render(wrongs_str, True, self.red)
        corrects_rect = corrects_block.get_rect()
        wrongs_rect = wrongs_block.get_rect()
        wrongs_rect.topleft = (self.WIDTH - 30 - wrongs_rect.width, self.HEIGHT - 20 - wrongs_rect.height)
        corrects_rect.topleft = (wrongs_rect.x, wrongs_rect.y -40)
        self.screen.blit(wrongs_block, wrongs_rect)
        self.screen.blit(corrects_block, corrects_rect)

class MathsCalc():
    def __init__(self):
        self.task = ''

    def rollTheTask(self):
        self.task_type = choice(('add', 'sub'))
        if self.task_type == "add":
            return f"{randint(11, 80)} + {randint(11,80)} ="
        else:
            a = randint(21,199)
            b = randint(21, 160)
            while b > a:
                b = randint(21, 160)
            return f"{a} - {b} ="


    def CheckAnswer(self, answer):
        # take a list with numbers and signs
        task_parts = self.task.split(" ")
        answer_parts = answer.split(" ")
        if answer_parts[-1] == '':
            return False
        # if we are adding
        if self.task_type == 'add':
            task_sum = int(task_parts[0]) + int(task_parts[2])
            if int(answer_parts[-1]) == task_sum:
                return True
            elif int(answer_parts[-1]) + int(answer_parts[-3]) == task_sum:
                return 'ok'
            else:
                return False
        # if we are subs
        else:
            task_diff = int(task_parts[0]) - int(task_parts[2])
            if int(answer_parts[-1]) == task_diff:
                return True
            elif int(answer_parts[-3]) - int(answer_parts[-1]) == task_diff:
                return 'ok'
            else:
                return False


class Game():
    def __init__(self):
        # create the window when the new game is created
        self.new_window = WindowGame()
        self.calc = MathsCalc()
        self.clock = pygame.time.Clock()
        self.corrects = 0
        self.wrongs = 0
        self.img = 'think'

    def DrawAll(self, img, task):
            # print the task:
            self.new_window.DisplayTask(task)
            # print the answer:
            self.new_window.DisplayInput()
            # print image:
            self.new_window.DisplayImages(img)
            # print stats:
            self.new_window.DisplayStats(self.corrects, self.wrongs)


    def run_game(self):
        while self.new_window.run:
            # fill the screen with bg color
            self.new_window.screen.fill(self.new_window.bg_color)
            # catch all events:
            self.new_window.EventsTaker()
            # check enter is pressed, if True: check answer
            if self.new_window.enter_pressed:
                check = self.calc.CheckAnswer(self.new_window.answer)
                # correct parts, not result
                if check == 'ok':
                    self.DrawAll('good', self.calc.task)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    self.new_window.answer += ' = '
                # correct result
                elif check is True:
                    self.calc.task = ''
                    self.DrawAll('good', self.calc.task)
                    pygame.display.flip()
                    self.corrects +=1
                    pygame.time.wait(1000)
                    self.new_window.answer = ''
                    
                # wrong result:
                elif check is False:
                    self.DrawAll('wrong', self.calc.task)
                    pygame.display.flip()
                    self.wrongs +=1
                    pygame.time.wait(1000)
                    self.new_window.answer = ''
                self.DrawAll(self.img, self.calc.task)
                pygame.display.flip()
                self.new_window.enter_pressed = False
            # draw:
            if self.calc.task == '':
                self.calc.task = self.calc.rollTheTask()
            self.DrawAll(self.img, self.calc.task)

            # screen refresh
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    new_game = Game()
    new_game.run_game()