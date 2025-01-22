# Month of Code: September - Flash Card "Game"
# 作り人：　アスター (Made by: Me ♡)

import os
import pandas
import pygame
import random
import time

pygame.init()

clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
screen = pygame.display.set_mode((800, 600))

card_data = {
    "Front": [],
    "Back": [],
    "Reading": []
}
card_set = "september_jlpt5.csv"
flashcard = pygame.Rect(100, 150, 600, 300)
file_list = []

def instructions():
    """
    Superfluous. Print instructions to screen ig???
    """
    betsu_no_font = pygame.font.Font(None, 36)
    suiyoubi_o_kirai = ["Press (space) to flip card", "Press (R) for furigana", "Press (F) to unflip card", "Press (left/right arrows) to switch decks"]
    who_cares = {}

    for i in suiyoubi_o_kirai:
        who_cares[suiyoubi_o_kirai.index(i)] = betsu_no_font.render(i, True, pygame.Color("white"))
        screen.blit(who_cares[suiyoubi_o_kirai.index(i)], (10, (20 * (suiyoubi_o_kirai.index(i) + 1))))

def read_data(file_name: str):
    """Checks if the file (assumed to be on the same level as the program) exists.\n
    It will then add the data for the front and back sides of the card.\n
    Readings (i.e., furigana) are also taken, assuming the CSV has them."""
    if os.path.isfile(f"{file_name}"):
        # Translation: "All good!" :D
        print("全部いいよ！")
        file_data = pandas.read_csv(f"{file_name}")
        file_data_dict = file_data.to_dict(orient="list")

        card_data["Front"] = file_data_dict[str(list(file_data_dict.keys())[0])]
        card_data["Back"] = file_data_dict[str(list(file_data_dict.keys())[1])]
        
        # Will only apply if CSV set has (assumedly) Japanese readings, which…
        # yeah, it probably will. (笑)

        if "Reading" in file_data_dict:
            card_data["Reading"] = file_data_dict["Reading"]

    else:
        # Translation: "Bug: The file does not exist at this location. Please change the file path or create one."
        print("バグ：その所にファイルがない。ファイル道を変わってかファイルを作らせてください。")

class My_Card():
    def __init__(self, ref_data: dict):
        self.card_text = "変われ"
        self.font = pygame.font.Font("Japanese2.ttf", 60)
        self.ref_data = ref_data

        self.show_furigana: bool = False
        self.show_text: bool = True

        self.dev_mode = False
    
    def draw_card(self):
        kotoba = self.font.render(self.card_text, True, pygame.Color("black"))
        shikaku = kotoba.get_rect(center=flashcard.center)

        pygame.draw.rect(screen, pygame.Color("white"), flashcard)
        
        if self.show_text and (self.card_text in card_data["Front"]):
            screen.blit(kotoba, shikaku)
        
        if self.show_text and (self.card_text in card_data["Back"]):
            self.box_text(screen, self.card_text, pygame.Color("black"), flashcard, self.font)
        
        if self.show_furigana:
            if self.card_text in card_data["Front"]:
                FONT_AGAIN = pygame.font.Font("Japanese2.ttf", 25)
                reading = card_data["Reading"][card_data["Front"].index(self.card_text)]

                # Is it just me, or are they just using HTML colors…?
                KOTODAMA = FONT_AGAIN.render(reading, True, pygame.Color("black"))
                FURIGANA = KOTODAMA.get_rect(center=flashcard.center)
                FURIGANA.y -= 50

                screen.blit(KOTODAMA, FURIGANA)
    
    # ふざけるな！
    # エディト：　ふざけてしまった ٩(^ᗜ^ )و ´-
    def animate_card(self):
        self.show_text = False
        self.show_furigana = False
        if not self.dev_mode:
            flip_spd = 0.025
        else:
            flip_spd = 0.001
        
        # なぜどうしようもなら、まだ大丈夫ならない…
        for _ in range(6):
            # It kept drawing the previous rectangles what the fuck

            screen.fill(pygame.Color("navy"))
            flashcard.left += 50
            flashcard.width -= 90
            flashcard.center = (400, 300)

            time.sleep(flip_spd)
            pygame.draw.rect(screen, pygame.Color("white"), flashcard)
            pygame.display.update()
             
        flashcard.center = (400, 300)
        time.sleep(flip_spd)

        for _ in range(6):
            screen.fill(pygame.Color("navy"))
            flashcard.left -= 50
            flashcard.width += 90
            flashcard.center = (400, 300)

            time.sleep(flip_spd)
            pygame.draw.rect(screen, pygame.Color("white"), flashcard)
            pygame.display.update()
        
        self.show_text = True
        self.show_furigana = True

    def flip_card(self):
        filler = self.card_text
        print(filler)

        self.animate_card()
        if self.card_text in card_data["Front"]:
            self.font = pygame.font.Font("Japanese2.ttf", 24)
            self.card_text = card_data["Back"][card_data["Front"].index(filler)]
        
        elif self.card_text in card_data["Back"]:
            self.font = pygame.font.Font("Japanese2.ttf", 60)
        
        else:
            # 誰も知らない。
            pass

    def redraw(self):
        atarashii = random.choice(card_data["Front"])
        if atarashii == self.card_text:
            atarashii = random.choice(card_data["Front"])
        else:
            self.card_text = atarashii
            self.font = pygame.font.Font("Japanese2.ttf", 60)
            self.show_furigana = False
    
    # "Thank you, StackOverflow," we all say in unison. (credit goes to @Rabbid76 on Replit)
    def box_text(self, surface, text, color, rect, font, align=0, aa=True, bkg=None):
        lineSpacing = -2
        spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

        listOfWords = text.split(" ")
        if bkg:
            imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
            for image in imageList: image.set_colorkey(bkg)
        else:
            imageList = [font.render(word, aa, color) for word in listOfWords]

        maxLen = rect[2]
        lineLenList = [0]
        lineList = [[]]
        for image in imageList:
            width = image.get_width()
            lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
            if len(lineList[-1]) == 0 or lineLen <= maxLen:
                lineLenList[-1] += width
                lineList[-1].append(image)
            else:
                lineLenList.append(width)
                lineList.append([image])

        lineBottom = rect[1]
        lastLine = 0
        for lineLen, lineImages in zip(lineLenList, lineList):
            lineLeft = rect[0]
            if align == 1:
                lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
            elif align == 2:
                lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
            elif align == 3 and len(lineImages) > 1:
                spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
            if lineBottom + fontHeight > rect[1] + rect[3]:
                break
            lastLine += 1
            for i, image in enumerate(lineImages):
                x, y = lineLeft + i*spaceWidth, lineBottom
                surface.blit(image, (round(x), y))
                lineLeft += image.get_width() 
            lineBottom += fontHeight + lineSpacing

        if lastLine < len(lineList):
            drawWords = sum([len(lineList[i]) for i in range(lastLine)])
            remainingText = ""
            for text in listOfWords[drawWords:]: remainingText += text + " "
            return remainingText
        
        return ""

def main():
    file_list = [file for file in os.listdir() if ".csv" in file]
    file_list.reverse()
    print(file_list)

    card_set = file_list[0]

    read_data(card_set)

    demo = My_Card(card_data)
    demo.card_text = random.choice(card_data["Front"])

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
               pygame.quit()
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                if demo.card_text in card_data["Front"]:
                    demo.flip_card()
                else:
                    demo.redraw()

            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                print("ヤッホ〜")
                demo.show_furigana = True
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_d):
                print("I am literally NEO.")
                demo.dev_mode = True
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_f):
                if demo.card_text in card_data["Back"]:
                    demo.animate_card()
                    demo.font = pygame.font.Font("Japanese2.ttf", 60)
                    demo.card_text = card_data["Front"][card_data["Back"].index(demo.card_text)]
                    demo.show_furigana = False
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
                if card_set != file_list[-1]:
                    card_set = file_list[file_list.index(card_set) + 1]
                    read_data(card_set)
                    demo.redraw()
                    print("Success (R)!!")
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
                if card_set != file_list[0]:
                    card_set = file_list[file_list.index(card_set) - 1]
                    read_data(card_set)
                    demo.redraw()
                    print("Success (L)!!")
                
        screen.fill(pygame.Color("navy"))
        instructions()
        demo.draw_card()
        pygame.display.update()

if __name__ == "__main__":
    # あのプログラムはただもっと悪いアンキ。どうして使いたいですか？
    main()