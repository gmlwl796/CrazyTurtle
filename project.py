from turtle import *
import random
import time

#글로벌변수.. class로 만들어도 될듯?
screenSize = [500, 500]

now_play = False
score = 0
round = 1
count = 0
item_state = 0
item_number = 0
item_time = 0
end_time = 0

#기본 스크린 설정
screen = Screen()
screen.setup(screenSize[0], screenSize[1])
screen.title("Crazy Turtle")
screen.bgcolor("lightyellow")

class Myturtle(Turtle): #터틀생성
    def __init__(self,screen,shape,color,width,height,speed,x,y,set):
        Turtle.__init__(self)
        self.screen = screen
        self.setheading(set)
        self.speed(0)
        self.shape(shape)
        self.color(color)
        self.penup()
        self.goto(x,y)

    def move(self): #적 쫓아다님->일단1
        global score
        if random.randint(1,5) == 3: #1~5사이에서 뽑은 수가 3이면(20%확률) => 너무 빠르면 
            ang = self.towards(t.pos()) #빨리 잡힐까봐 악당 거북이의 방향 가끔씩 바꿔 난이도 조절
            self.setheading(ang)      #악당거북이가 주인공 거북이를 바라봅니다
        speed = score + 5      #점수에 5를 더해서 속도를 올립니다
        if speed >= 10:
            speed = 9
        self.forward(speed)
    
class Item(Turtle): #아이템 생성
    def __init__(self,screen,width,height,x,y):
        Turtle.__init__(self)
        self.screen = screen
        self.shape("circle")
        self.penup()
        self.goto(x,y)

        
"""기본객체생성"""
t = Myturtle(screen,"turtle","black",1,1,0,0,0,0) #주인공
big = []
big.append(Myturtle(screen,"turtle","purple",1,1,0,0,200,0))#큰악당
small = []
small.append(Myturtle(screen,"turtle","red",1,1,9,000,-200,0)) #작은악당 생성
item = Item(screen,1,1,0,0)
item.ht();
color = ["green","cyan","blue"]
mes = Myturtle(screen,"turtle","blue",3,3,0,0,0,0) #메세지 출력용 거북이
mes.ht();mes.up() ; #hidetuttle()


def start():        #게임을 시작하는 함수
    global now_play
    
    if now_play == False:
        now_play = True
        mes.clear()
        play()

def after() :
    global round

    for i in range(0, round) : 
        if i%2==0 :
            big.append(Myturtle(screen,"turtle","purple",1,1,0,i*25,200,0))
        big.append(Myturtle(screen,"turtle","purple",1,1,0,-i*25,200,0))
            

def end(): #게임을 끝내는 함수
    global round, score
    global now_play
    
    t.hideturtle();
    for i in range (len(big)) :
        big[i].hideturtle();
    for i in range(len(small)):
        small[i].hideturtle()
    text = "Round: " + str(round) + "\nScore: " + str(score)
    message("Game Over", text)      #게임을 종료
    now_play = False; score = 0; round = 0 #변수초기화

def play():
    global now_play
    global count #꼼수 0.1초마다 1번 실행하니까 30초면 300번..
    global score #점수
    global round #라운드
    global item_state
    global item_number
    global item_time
    global end_time

    if(t.position()[0] >= screenSize[0]/2-10) :
        t.setheading(180)
    if(t.position()[0] <= -(screenSize[0]/2-10)) :
        t.setheading(0)
    if(t.position()[1] >= screenSize[1]/2-10) :
        t.setheading(270)
    if(t.position()[1] <= -(screenSize[1]/2-10)) :
        t.setheading(90)    
    t.forward(10)
    end_time = time.time()
    count += 1
    #10초마다 악당 하나씩 증가
    if (count % 100) == 0 : #30초마다 한번씩은 300으로 수정
        small.append(Myturtle(screen,"turtle","red",1,1,8,random.randint(-230,230),random.randint(-230,230),0)) #작은악당 생성    
    
    for i in range(len(small)):
        small[i].move()
        if not(small[i]==None) :
            if t.distance(small[i]) < 12:
                end()
    for i in range(len(big)) :
        if t.distance(big[i]) < 12:
            end()
   
    if (count % 50) == 0 and item_state == 0: #5초마다 하나생성
        number = random.randint(1,3)
        if number == 1:
            item.color(color[0])
            item_number = 0
        elif number == 2:
            item.color(color[1])
            item_number = 1
        elif number == 3:
            item.color(color[2])
            item_number = 2
        item_x = random.randint(-230,230)
        item_y = random.randint(-230,230)
        item.goto(item_x,item_y)
        item.showturtle()
        item_state = 1 #아이템 맵에 존재함

    if t.distance(item) < 12 and item_state == 1:
        score += 2 #점수 1점 증가
        item.ht() #먹으면 눈에 안보이게
        item_state = 2 #아이템적용으로 변경
        if item_number == 0 : #1번 아이템 먹으면
            t.turtlesize(2,2)   
            item_time = time.time()
        elif item_number == 1 or item_number == 2:
            #아이템2번 먹으면 순간이동~~
            rand_x = random.randint(-230,230)
            rand_y = random.randint(-230,230)
            t_x = t.xcor(); t_y = t.ycor()
            if t_x >= 150:
                rand_x = random.randint(-250,50)
            elif t_x <= -150:
                rand_x = random.randint(-70,250)
            if t_y >= 150:
                rand_y = random.randint(-250,50)
            elif t_y <= -150:    
                rand_y = random.randint(-50,250)
            item_state = 0 #아이템 상태 0으로 바꿈
            t.goto(t.xcor()+rand_x, t.ycor()+rand_y)
        
    if item_number == 0 and item_state == 2 :#슈퍼거북이
        if(float(end_time) - float(item_time)) > 7:
            #효과 7초넘으면 원래대로 돌아가기
            t.turtlesize(1,1)
            item_state = 0
            t.fd(11)
            t.color("black")
        else:
            t.color("navy")
            t.fd(20) #7초간 슈퍼거북이 빠르게 전진~~~
            t.color("magenta")
 
                     
    if now_play:                 #게임이 플레이 중이면
        screen.ontimer(play, 100)    #0.1초 후 play함수를 실행(계임 계속)
"""    
def round_clear():
    global round,score,now_play

    if round_state == "lose" : 
        text = "Lose\n" + "Round " + str(round) + "\nScore: " + str(score)
        message("Clear", text)      #게임을 종료
        now_play = False; score = 0;
"""

def attack() :
    global now_play
    global score #점수
    global round #라운드
    ang = t.heading()
    ball = Myturtle(screen,"circle","gray",1,1,0, t.position()[0], t.position()[1], ang)
    ball.penup()
    while ball.position()[0]<250 and ball.position()[0]>-250 and ball.position()[1]<250 and ball.position()[1]>-250 :
        ball.forward(10)
        for i in range(len(big)) :
            if big[i].position()[0]-12 < ball.position()[0] and big[i].position()[0]+12 > ball.position()[0] and big[i].position()[1]-12 < ball.position()[1] and big[i].position()[1]+12 > ball.position()[1]:
                big[i].hideturtle()
                del(big[i])
                ball.goto(500,500)
                score += 100
                if len(big)==0 :
                    round +=1
                    after()
                    print(round)
                break
        for i in range(len(small)):
            if small[i].position()[0]-20 < ball.position()[0] and small[i].position()[0]+20 > ball.position()[0] and small[i].position()[1]-20 < ball.position()[1] and small[i].position()[1]+20 > ball.position()[1]:
                small[i].hideturtle()
                del(small[i])
                score += 1
                break


#키보드 설정
def turn_right():
    t.setheading(0)
def turn_left():  
    t.setheading(180)
def turn_up():   
    t.setheading(90)
def turn_down(): 
    t.setheading(270)

def message(m1,m2): #메세지 출력
    mes.clear()
    mes.goto(0,100);
    mes.write(m1,False,"center",("",20))
    mes.goto(0,-100);
    mes.write(m2,False,"center",("",15))
    mes.home()


screen.onkeypress(turn_up,"Up")      
screen.onkeypress(turn_down,"Down")
screen.onkeypress(turn_left,"Left")  
screen.onkeypress(turn_right,"Right")
screen.onkeypress(start,"space")
screen.onkeypress(attack, "a")
screen.listen()  # 그래픽 창이 키보드 입력 받도록 함
message("Turtle Run","[Space]")
