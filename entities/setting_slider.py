import pygame

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: float, max: float) -> None:
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max

        self.min_center = self.slider_left_pos + 10 // 2
        self.max_center = self.slider_right_pos - 10 // 2

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, 10, self.size[1])

        self.initial_val = self.min_center + (self.max_center - self.min_center) * initial_val
        self.button_rect.centerx = self.initial_val

    def move_slider_mouse(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

        if self.button_rect.centerx < self.min_center:
            self.button_rect.centerx  = self.min_center
        if self.button_rect.centerx > self.max_center:
            self.button_rect.centerx = self.max_center

    def move_slider_button(self, button):
        if button == 'right':
            self.button_rect.centerx += self.size[0] / 100
        elif button == 'left':
            self.button_rect.centerx -= self.size[0] / 100

        if self.button_rect.centerx < self.min_center:
            self.button_rect.centerx = self.min_center
        if self.button_rect.centerx > self.max_center:
            self.button_rect.centerx = self.max_center

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "darkgray", self.container_rect)
        pygame.draw.rect(screen, "red", self.button_rect)

    def get_value(self):
        val_range = self.max_center  - self.min_center
        button_val = self.button_rect.centerx - self.min_center

        return (button_val / val_range) * (self.max - self.min) + self.min