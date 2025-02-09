# Импортирование библеотеки pygame
import pygame, sys
# Импортирование классов, функций с других файлов
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game: # создание основного классе
    def __init__(self):
        pygame.init() # Инициализация

        pygame.display.set_caption("Platformer") # Название окна
        self.screen = pygame.display.set_mode((640, 480)) # Создание дисплея игры
        self.display = pygame.Surface((320, 240)) # Основной дисплей благодаря которого мы увеличиваем картинку в двое.

        self.clock = pygame.time.Clock() # Clock позволяет иметь фиксированный фпс для более точной работы физики

        self.movement = [False, False]

        # Выгрузка спрайтов
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16) # Облака

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15)) # Игрок

        self.tilemap = Tilemap(self, tile_size=16) # Карта (лвл)
        self.tilemap.load('map.json')

        self.scroll = [0, 0] # камера

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 25 # Применяем "физику" камеры. Значение в конце функции означает "плавность движения камеры"
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 25 # Чем дальше игрок от камеры, тем интенсивнее она следует за игроком
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update() # Облака
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)


           # print(self.tilemap.physics_rects_around(self.player.pos)) # Отображение коллизий в терминале

            # Вызов функций движения и рендер игрока
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            # Обязательный цикл для работы экрана и закрытия экрана
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Проверка нажатий клавиш клавиатуры
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Увеличение экрана без потерь
            pygame.display.update()
            self.clock.tick(60)

Game().run()