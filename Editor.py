# Импортирование библеотеки pygame
import pygame, sys
# Импортирование классов, функций с других файлов
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor: # создание основного классе
    def __init__(self):
        pygame.init() # Инициализация

        pygame.display.set_caption("Editor") # Название окна
        self.screen = pygame.display.set_mode((640, 480)) # Создание дисплея игры
        self.display = pygame.Surface((320, 240)) # Основной дисплей благодаря которого мы увеличиваем картинку в двое.

        self.clock = pygame.time.Clock() # Clock позволяет иметь фиксированный фпс для более точной работы физики

        self.movement = [False, False, False, False]

        # Выгрузка спрайтов
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background': load_image('background.png'),
        }

        self.tilemap = Tilemap(self, tile_size=16) # Карта (лвл)
        self.tilemap.load('map.json')

        self.scroll = [0, 0] # камера

        self.tile_list = list(self.assets) # Даст лист с выгруженными ассетами
        self.tile_group = 0
        self.tile_variant = 0
        self.click = False
        self.r_click = False

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) # Прозрачность выбранной фигуры



            self.display.blit(current_tile_img, (5, 5))

            # Обязательный цикл для работы экрана и закрытия экрана
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Проверка нажатий клавиш клавиатуры
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Нажатие ЛКМ
                        self.click = True
                    if event.button == 3: # Нажатие ПКМ
                        self.r_click = True
                    if event.button == 4:
                        self.tile_group = (self.tile_group - 1) % len(self.assets[self.tile_list[self.tile_group]]) # Смена тайлов на колёсико мыши. % len позволяет сделать цикл чтобы не уйти за пределы вариантов
                    if event.button == 5:
                        self.tile_group = (self.tile_group + 1) % len(self.assets[self.tile_list[self.tile_group]])
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Увеличение экрана без потерь
            pygame.display.update()
            self.clock.tick(60)

Editor().run()