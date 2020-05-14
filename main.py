import os
import time
from pynput import keyboard
import random

class Game:

    def __init__(self, width, height):
        self.field_width = width
        self.field_height = height

        self.snake = Snake(int(self.field_width / 2), int(self.field_height / 2))

        self.fruit_x = random.randint(1, self.field_width - 2)
        self.fruit_y = random.randint(1, self.field_height - 2)

        self.score = 0

        self.isGameOver = False

        #self.fruitIsOnHead = False
        
        self.startListner()

    def onPress(self, key):
        try:
            k=key.char
        except:
            k=key.name
        if k in ['w', 'a', 's', 'd']:
            if k == 'w' and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            if k == 'a' and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            if k == 's' and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            if k == 'd' and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

    def startListner(self):
        self.listener = keyboard.Listener(self.onPress)
        self.listener.start() 
    
    def clearScreen(self):
        os.system("clear")    

    def drawField(self):
        self.clearScreen()
        for y in range(0, self.field_height):
            for x in range(0, self.field_width):
                if y == 0 or y == self.field_height-1 or x == 0 or x == self.field_width-1:
                    print("#", end = "")
                elif y == self.snake.getHeadPos()[1] and x == self.snake.getHeadPos()[0]: # THIS MIGHT BE BAD SYNTAX BUT WE WILL SEE
                    print("O", end = "")
                elif self.snake.isPartOfTail(x, y):
                    print("o", end = "")
                #TODO : check if tail element here 
                elif y == self.fruit_y and x == self.fruit_x:
                    print("@", end = "")
                else:
                    print(" ", end = "")
            print()
        print("SCORE:", self.score)

    def randomFruit(self):
        self.fruit_x = random.randint(1, self.field_width - 2)
        self.fruit_y = random.randint(1, self.field_height - 2)      
    
    def isFruitOnHead(self):
        return self.fruit_x == self.snake.getHeadPos()[0] and self.fruit_y == self.snake.getHeadPos()[1]

    def isHeadInWall(self):
        return  self.snake.getHeadPos()[0] == 0 or self.snake.getHeadPos()[0]  == self.field_width - 1 or self.snake.getHeadPos()[1] == 0 or self.snake.getHeadPos()[1] == self.field_height - 1

    def isHeadOnTail(self):
        return self.snake.isPartOfTail( self.snake.getHeadPos()[0], self.snake.getHeadPos()[1])
    
    def update(self):
        self.snake.move()

        if self.isFruitOnHead():
            self.snake.addTail()
            self.score += 10
            self.randomFruit()
        
        if self.isHeadInWall() or self.isHeadOnTail(): 
            self.isGameOver = True

    def playGame(self):
        while not self.isGameOver:
            self.drawField()
            time.sleep(0.1)
            self.update()
        if self.isHeadOnTail():
            self.drawField()
        print("GAME OVER")

class SnakeElement:
    def __init__(self, element_x, element_y, isHead, number):
        self.element_x = element_x
        self.element_y = element_y

        self.isHead = isHead

        self.number = number
    
class Snake:
    def __init__(self, startx, starty):
        self.direction = 'NONE'

        self.snake_elements_list = []
        self.snake_elements_list.append(SnakeElement(startx, starty, True, 1))


    def getHeadPos(self):
        for snake_element in self.snake_elements_list:
            if snake_element.isHead:
                return [snake_element.element_x, snake_element.element_y]

    def move(self):
        if len( self.snake_elements_list ) == 1: # THIS IS HOW TO MOVE IF ONLY HEAD 
            if self.direction == 'UP':
                self.snake_elements_list[0].element_y -= 1
            if self.direction == 'DOWN':
                self.snake_elements_list[0].element_y += 1
            if self.direction == 'LEFT':
                self.snake_elements_list[0].element_x -= 1
            if self.direction == 'RIGHT':
                self.snake_elements_list[0].element_x += 1
        else:
            previous_head_index = -1
            for i in range(0, len(self.snake_elements_list)):
                if self.snake_elements_list[i].isHead == True:
                    previous_head_index = i

            for snake_element in self.snake_elements_list:
                if snake_element.number == len(self.snake_elements_list):
                    self.previous_tail_end = [ snake_element.element_x, snake_element.element_y ] 

            for snake_element in self.snake_elements_list:
                if snake_element.number == len(self.snake_elements_list):
                    if self.direction == 'UP':
                        snake_element.element_x = self.getHeadPos()[0]
                        snake_element.element_y = self.getHeadPos()[1] - 1
                    if self.direction == 'DOWN':
                        snake_element.element_x = self.getHeadPos()[0]
                        snake_element.element_y = self.getHeadPos()[1] + 1
                    if self.direction == 'LEFT':
                        snake_element.element_x = self.getHeadPos()[0] - 1
                        snake_element.element_y = self.getHeadPos()[1]
                    if self.direction == 'RIGHT':
                        snake_element.element_x = self.getHeadPos()[0] + 1
                        snake_element.element_y = self.getHeadPos()[1] 
                    snake_element.isHead = True
                    self.snake_elements_list[previous_head_index].isHead = False
                    
            for element in self.snake_elements_list:
                if element.isHead :
                    element.number = 1
                else:
                    element.number += 1


    def addTail(self):
        if len( self.snake_elements_list ) == 1: # THIS IS HOW TO ADD TAIL IF ONLY HEAD 
            if self.direction == 'UP':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x, self.snake_elements_list[0].element_y + 1, False, 2))
            if self.direction == 'DOWN':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x, self.snake_elements_list[0].element_y - 1, False, 2))
            if self.direction == 'LEFT':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x + 1, self.snake_elements_list[0].element_y, False, 2))
            if self.direction == 'RIGHT':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x - 1, self.snake_elements_list[0].element_y, False, 2))
        else:
            self.snake_elements_list.append( SnakeElement( self.previous_tail_end[0], self.previous_tail_end[1], False, len(self.snake_elements_list)+1))

    def isPartOfTail(self, x, y):
        for snake_element in self.snake_elements_list:
            if snake_element.element_x == x and snake_element.element_y == y and snake_element.isHead == False:
                return True
        return False


def main():
    game = Game(51, 21)
    game.playGame()

if __name__ == "__main__":
    main()
