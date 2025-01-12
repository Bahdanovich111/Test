import pygame
import sys
import random


# Инициализация Pygame
pygame.init()

# Основные параметры игры
WIDTH, HEIGHT = 800, 600
BG_COLOR = (135, 206, 250)  # Голубой цвет экрана
FPS = 60

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SuperGame")
clock = pygame.time.Clock()

# Звуки
jump_sound = pygame.mixer.Sound('jump.wav')
enemy_sound = pygame.mixer.Sound('coin.wav')




# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создаем поверхность для танка
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Полупрозрачный фон
        self.turret = pygame.Surface((10, 30))  # Создаем ствол танка
        self.turret.fill((0, 0, 0))  # Ствол будет черным
        self.image.fill((34, 139, 34))  # Зеленый цвет корпуса танка
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 50))
        self.velocity_y = 0
        self.is_jumping = False

    def update(self, keys):
        # Движение влево-вправо
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Проверка на границы окна по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


        self.image.blit(self.turret, (20, 0))  #  Ствол в верхней части танка


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 215, 0))  #  Цвет для врага
        self.rect = self.image.get_rect(center=(x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))  # Черный цвет пули
        self.rect = self.image.get_rect(center=start_pos)
        self.velocity_y = -10  # Скорость пули вверх по оси Y

    def update(self):
        # Движение пули вверх
        self.rect.y += self.velocity_y

        # Удаление пули, если она выходит за верхнюю границу экрана
        if self.rect.bottom < 0:
            self.kill()



class Game:
    def __init__(self):
        self.player = Player()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.running = True
        self.win = False  # Флаг победы
        self.generate_enemy()

    def clear_enemies(self):           #удаление всех врагов
        self.coins.empty()  # Очистка группы врагов
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                self.all_sprites.remove(sprite)  # Удаление врагов из all_sprites

    def generate_enemy(self):   # Случайная генерация врагов
        for _ in range(5):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 200)
            enemy = Enemy(x, y)
            self.coins.add(enemy)
            self.all_sprites.add(enemy)

    def fire_bullet(self):
        # Создание пули, которая летит строго вверх от текущей позиции танка
        bullet = Bullet(self.player.rect.center)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        jump_sound.play()  # Воспроизведение звука выстрела

    def check_collisions(self):
        # Проверка столкновений пуль с монетами
        for bullet in self.bullets:
            hit_enemy = pygame.sprite.spritecollide(bullet, self.coins, True)
            if hit_enemy:
                bullet.kill()
                enemy_sound.play()  # Воспроизведение звука попадания
                self.score += len(hit_enemy)

        # Устанавливаем флаг победы, если достигли 5 очков
        if self.score >= 5:
            self.win = True

    def reset_game(self):
        # Сброс параметров игры
        self.player.rect.midbottom = (100, HEIGHT - 50)
        self.score = 0
        self.coins.empty()
        self.bullets.empty()
        self.clear_enemies()
        self.generate_enemy()
        self.win = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:     #если нажали R
                        self.reset_game()  # Сброс игры
                    if event.key == pygame.K_SPACE and not self.win:
                        self.fire_bullet()  # Стрельба строго вверх при нажатии пробела

            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.bullets.update()

            # Проверка столкновений только если игра не окончена
            if not self.win:
                self.check_collisions()

            # Отрисовка игрового экрана
            screen.fill(BG_COLOR)
            self.all_sprites.draw(screen)

            # Отображение счёта
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Отображение сообщения о победе
            if self.win:
                win_text = font.render("You Win! Press R to Restart", True, (0, 0, 0))
                screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))

            pygame.display.flip()
            clock.tick(FPS)



# Запуск игры
game = Game()
game.run()
pygame.quit()
sys.exit()
#dfffffffffffffffffffffffffffff