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

        self.scroll = [0, 0] # камера

        # Исключаем background из списка тайлов
        self.tile_list = [key for key in self.assets if key != "background"]
        self.tile_group = 0
        self.tile_variant = 0
        self.click = False
        self.r_click = False
        self.shift = False

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) # Прозрачность выбранной фигуры от 0 до 255

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # Это нужно, чтобы получить правильные координаты мышки поскольку я использую мудрёную систему увеличения всего экрана
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.click:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.r_click:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

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
                    if self.shift:
                        if event.button == 4:  # Прокрутка вверх (смена варианта)
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:  # Прокрутка вниз (смена варианта)
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:  # Прокрутка вверх (смена группы)
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0  # Сброс варианта при смене группы
                        if event.button == 5:  # Прокрутка вниз (смена группы)
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0  # Сброс варианта при смене группы
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.r_click = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Увеличение экрана без потерь
            pygame.display.update()
            self.clock.tick(60)

Editor().run()
