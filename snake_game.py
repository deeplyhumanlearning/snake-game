import random

import pygame


WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
FPS = 7

BACKGROUND = (20, 20, 20)
SNAKE_COLOR = (50, 200, 80)
FOOD_COLOR = (220, 60, 60)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (50, 100, 200)
BUTTON_HOVER_COLOR = (70, 130, 230)


def create_food(snake):
    while True:
        food = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE),
        )

        if food not in snake:
            return food


def draw_text(screen, font, text, position):
    rendered_text = font.render(text, True, TEXT_COLOR)
    text_rect = rendered_text.get_rect(center=position)
    screen.blit(rendered_text, text_rect)


def draw_button(screen, font, text, rect, mouse_position):
    color = (
        BUTTON_HOVER_COLOR
        if rect.collidepoint(mouse_position)
        else BUTTON_COLOR
    )

    pygame.draw.rect(screen, color, rect, border_radius=8)
    draw_text(screen, font, text, rect.center)


def draw_snake(screen, snake):
    for segment in snake:
        pygame.draw.rect(
            screen,
            SNAKE_COLOR,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
        )


def draw_food(screen, food):
    pygame.draw.rect(
        screen,
        FOOD_COLOR,
        (food[0], food[1], CELL_SIZE, CELL_SIZE),
    )


def run_game(screen, clock, font, high_score):
    snake = [
        (300, 200),
        (280, 200),
        (260, 200),
    ]

    direction = (CELL_SIZE, 0)
    food = create_food(snake)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", high_score

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)

                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)

                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)

                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        head_x, head_y = snake[0]
        direction_x, direction_y = direction

        new_head = (
            head_x + direction_x,
            head_y + direction_y,
        )

        hit_wall = (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        )

        hit_self = new_head in snake

        if hit_wall or hit_self:
            return score, high_score

        snake.insert(0, new_head)

        if new_head == food:
            score += 1

            if score > high_score:
                high_score = score

            food = create_food(snake)
        else:
            snake.pop()

        screen.fill(BACKGROUND)

        draw_snake(screen, snake)
        draw_food(screen, food)

        score_text = font.render(
            f"Score: {score}",
            True,
            TEXT_COLOR,
        )
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(
            f"High Score: {high_score}",
            True,
            TEXT_COLOR,
        )
        screen.blit(high_score_text, (10, 35))

        pygame.display.flip()
        clock.tick(FPS)


def start_screen(screen, clock, title_font, button_font, high_score):
    start_button = pygame.Rect(200, 210, 200, 50)
    quit_button = pygame.Rect(200, 280, 200, 50)

    while True:
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return "start"

                if quit_button.collidepoint(event.pos):
                    return "quit"

        screen.fill(BACKGROUND)

        draw_text(
            screen,
            title_font,
            "SNAKE GAME",
            (WIDTH // 2, 100),
        )

        draw_text(
            screen,
            button_font,
            f"High Score: {high_score}",
            (WIDTH // 2, 155),
        )

        draw_button(
            screen,
            button_font,
            "Start Game",
            start_button,
            mouse_position,
        )

        draw_button(
            screen,
            button_font,
            "Quit",
            quit_button,
            mouse_position,
        )

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(
    screen,
    clock,
    title_font,
    button_font,
    score,
    high_score,
):
    restart_button = pygame.Rect(200, 240, 200, 50)
    quit_button = pygame.Rect(200, 310, 200, 50)

    while True:
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    return "restart"

                if quit_button.collidepoint(event.pos):
                    return "quit"

        screen.fill(BACKGROUND)

        draw_text(
            screen,
            title_font,
            "GAME OVER",
            (WIDTH // 2, 90),
        )

        draw_text(
            screen,
            button_font,
            f"Score: {score}",
            (WIDTH // 2, 145),
        )

        draw_text(
            screen,
            button_font,
            f"High Score: {high_score}",
            (WIDTH // 2, 185),
        )

        draw_button(
            screen,
            button_font,
            "Restart",
            restart_button,
            mouse_position,
        )

        draw_button(
            screen,
            button_font,
            "Quit",
            quit_button,
            mouse_position,
        )

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 32)

    high_score = 0

    while True:
        action = start_screen(
            screen,
            clock,
            title_font,
            button_font,
            high_score,
        )

        if action == "quit":
            break

        score, high_score = run_game(
            screen,
            clock,
            button_font,
            high_score,
        )

        if score == "quit":
            break

        action = game_over_screen(
            screen,
            clock,
            title_font,
            button_font,
            score,
            high_score,
        )

        if action == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()