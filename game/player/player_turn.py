# player_turn.py (Phiên bản hoàn thiện)
import pygame


class PlayerTurnManager:
    def __init__(self, screen, player, boss):
        self.screen = screen
        self.player = player
        self.boss = boss
        self.font = pygame.font.Font("font/MonsterFriendBack.otf", 16)
        self.info_font = pygame.font.Font("font/MonsterFriendBack.otf", 16)

        self.turn_state = 'SELECTING_ACTION'
        self.is_turn_active = False

        # --- Tải Assets cho UI (giữ nguyên của bạn) ---
        self.fight_img = pygame.image.load('graphics/icon/spr_fightbt_0.png').convert_alpha()
        self.act_img = pygame.image.load('graphics/icon/spr_talkbt_0.png').convert_alpha()
        self.item_img = pygame.image.load('graphics/icon/spr_itembt_0.png').convert_alpha()
        self.mercy_img = pygame.image.load('graphics/icon/spr_sparebt_0.png').convert_alpha()

        self.fight_img_2 = pygame.image.load('graphics/icon/spr_fightbt_1.png').convert_alpha()
        self.act_img_2 = pygame.image.load('graphics/icon/spr_talkbt_1.png').convert_alpha()
        self.item_img_2 = pygame.image.load('graphics/icon/spr_itembt_1.png').convert_alpha()
        self.mercy_img_2 = pygame.image.load('graphics/icon/spr_sparebt_1.png').convert_alpha()

        self.selector_img = pygame.image.load('graphics/sprites/player/heart.png').convert_alpha()
        self.fight_target_img = pygame.image.load('graphics/UI/attack/spr_dumbtarget_0.png').convert_alpha()
        self.fight_bar_img = pygame.image.load('graphics/UI/attack/spr_targetchoice_1.png').convert_alpha()
        self.fight_bar_img_2 = pygame.image.load('graphics/UI/attack/spr_targetchoice_0.png').convert_alpha()

        # Bạn cần tạo file ảnh này, ví dụ một vệt chém màu trắng/vàng
        self.attack_slash_img = [pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_0.png').convert_alpha(),
                                 pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_1.png').convert_alpha(),
                                 pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_2.png').convert_alpha(),
                                 pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_3.png').convert_alpha(),
                                 pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_4.png').convert_alpha(),
                                 pygame.image.load('graphics/UI/weapon/knife/spr_slice_o_5.png').convert_alpha()]

        self.buttons = [self.fight_img, self.act_img, self.item_img, self.mercy_img]
        self.button_positions = []
        self.current_selection = 0

        self.attack_hit_snd = pygame.mixer.Sound('sound/sans_battle/undertale-sound-effect-attack-hit.mp3')
        self.heal_item_snd = pygame.mixer.Sound('sound/sans_battle/snd_heal_c.wav')
        self.select_snd = pygame.mixer.Sound('sound/sans_battle/snd_select.wav')
        self.slash_snd = pygame.mixer.Sound('sound/sans_battle/snd_laz.wav')

        # --- Trạng thái cho các animation và menu con ---
        # FIGHT
        self.fight_bar_pos_x = 0
        self.fight_bar_speed = 500
        self.is_bar_moving = False
        self.show_slash_timer = 0  # Timer cho animation đánh trúng

        # ACT
        self.act_options = ["Check", "Talk"]
        self.act_selection = 0
        self.act_info_text = ""

        # ITEM
        self.item_selection = (0, 0)  # (hàng, cột)
        self.item_grid_cols = 2

        # MERCY
        self.mercy_options = ["Sand"]
        self.mercy_selection = 0
        self.mercy_info_text = ""

        # slash animation
        self.slash_frame_index = 0
        self.slash_animation_speed = 20

        self.bar_blink_timer = 0    # Timer cho hiệu ứng nhấp nháy
        self.final_bar_pos_x = 0
        self.slash_position = None

        self.end_turn_delay = 1.0

    def start_turn(self):
        self.is_turn_active = True
        self.turn_state = 'SELECTING_ACTION'
        self.current_selection = 0
        self.act_info_text = ""
        self.mercy_info_text = ""
        self.player.rect.center = (500, 385)  # Điều chỉnh lại vị trí cho đẹp hơn
        self.player.set_gravity(False)
        self.boss.end_dodge()  # Đảm bảo boss về vị trí cũ nếu lượt trước bị miss

    def end_turn(self):
        self.boss.end_dodge()
        self.is_turn_active = False
        return False

    def handle_input(self, event):
        if not self.is_turn_active or event.type != pygame.KEYDOWN:
            return

        if self.turn_state == 'SELECTING_ACTION':
            if event.key == pygame.K_LEFT:
                self.current_selection = (self.current_selection - 1) % 4
                self.select_snd.play()
            elif event.key == pygame.K_RIGHT:
                self.current_selection = (self.current_selection + 1) % 4
                self.select_snd.play()
            elif event.key == pygame.K_RETURN:
                self.select_snd.play()
                if self.current_selection == 0:
                    self.turn_state = 'FIGHTING'; self.start_fight_minigame()
                elif self.current_selection == 1:
                    self.turn_state = 'ACTING'; self.act_selection = 0
                elif self.current_selection == 2:
                    self.turn_state = 'ITEM_MENU'; self.item_selection = (0, 0)
                elif self.current_selection == 3:
                    self.turn_state = 'MERCY_MENU'

        elif self.turn_state == 'FIGHTING':
            # Nếu thanh đang chạy và người dùng nhấn ENTER
            if self.is_bar_moving and event.key == pygame.K_RETURN:
                self.select_snd.play()
                self.stop_fight_bar()
            # Nếu người dùng nhấn ESC để quay lại
            elif event.key == pygame.K_ESCAPE:
                self.select_snd.play()
                self.turn_state = 'SELECTING_ACTION'
                self.is_bar_moving = False # Dừng thanh chạy ngay lập tức

        # <<< SỬA ĐỔI Ở ĐÂY >>>
        elif self.turn_state == 'ACTING':
            if event.key == pygame.K_UP:
                self.act_selection = (self.act_selection - 1) % len(self.act_options)
                self.select_snd.play()
            elif event.key == pygame.K_DOWN:
                self.act_selection = (self.act_selection + 1) % len(self.act_options)
                self.select_snd.play()
            elif event.key == pygame.K_RETURN:
                self.select_snd.play()
                if self.act_selection == 0:
                    self.act_info_text = "* SAND - The easiest enemy."
                elif self.act_selection == 1:
                    self.act_info_text = "* You talk to Sans. He doesn't seem to be listening."
            # Thêm K_ESCAPE vào điều kiện quay lại
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                self.select_snd.play()
                self.turn_state = 'SELECTING_ACTION'; self.act_info_text = ""

        # <<< SỬA ĐỔI Ở ĐÂY >>>
        elif self.turn_state == 'ITEM_MENU':
            item_count = len(self.player.inventory)
            # Không cần kiểm tra item_count ở đây nữa để có thể thoát ra dù không có item

            if event.key == pygame.K_UP:
                self.select_snd.play()
                if item_count > 0:
                    rows = (item_count + self.item_grid_cols - 1) // self.item_grid_cols
                    row, col = self.item_selection
                    row = (row - 1 + rows) % rows
                    self.item_selection = (row, col)
            elif event.key == pygame.K_DOWN:
                 self.select_snd.play()
                 if item_count > 0:
                    rows = (item_count + self.item_grid_cols - 1) // self.item_grid_cols
                    row, col = self.item_selection
                    row = (row + 1) % rows
                    self.item_selection = (row, col)
            elif event.key == pygame.K_LEFT:
                 self.select_snd.play()
                 if item_count > 0:
                    row, col = self.item_selection
                    col = (col - 1 + self.item_grid_cols) % self.item_grid_cols
                    self.item_selection = (row, col)
            elif event.key == pygame.K_RIGHT:
                 self.select_snd.play()
                 if item_count > 0:
                    row, col = self.item_selection
                    col = (col + 1 + self.item_grid_cols) % self.item_grid_cols
                    self.item_selection = (row, col)
            elif event.key == pygame.K_RETURN:
                self.select_snd.play()
                if item_count > 0:
                    index = self.item_selection[0] * self.item_grid_cols + self.item_selection[1]
                    item_keys = list(self.player.inventory.keys())
                    if index < len(item_keys):
                        item_name = item_keys[index]
                        if self.player.use_item(item_name):
                            self.heal_item_snd.play()
                            self.turn_state = 'ACTION_COMPLETE'  # Chuyển sang trạng thái chờ
            # Thêm K_ESCAPE vào điều kiện quay lại
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                self.select_snd.play()
                self.turn_state = 'SELECTING_ACTION'

        # <<< THÊM MỚI Ở ĐÂY >>>
        elif self.turn_state == 'MERCY_MENU':
            if event.key == pygame.K_UP:
                self.mercy_selection = (self.mercy_selection - 1) % len(self.mercy_options)
                self.select_snd.play()
            elif event.key == pygame.K_DOWN:
                self.mercy_selection = (self.mercy_selection + 1) % len(self.mercy_options)
                self.select_snd.play()
            elif event.key == pygame.K_RETURN:
                self.select_snd.play()
                if self.mercy_selection == 0:  # Chọn Sans
                    self.mercy_info_text = "* You spared Sand. He appreciates it."
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                self.select_snd.play()
                self.turn_state = 'SELECTING_ACTION'
                self.mercy_info_text = ""

    def draw_wrapped_text(self, surface, text, font, color, rect):
        words = text.split(' ')
        lines = []
        current_line = ""
        line_height = font.get_linesize()

        line_spacing_multiplier = 1.4

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < rect.width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            # Nhân line_height với hệ số nhân
            y_pos = rect.y + i * (line_height * line_spacing_multiplier)
            surface.blit(text_surface, (rect.x, y_pos))

    def update(self, dt):
        if not self.is_turn_active: return True

        if self.show_slash_timer > 0:
            self.show_slash_timer -= dt
            self.slash_frame_index += self.slash_animation_speed * dt

            if self.show_slash_timer <= 0:
                self.slash_frame_index = 0
                # Nếu boss đang ở vị trí né, ra lệnh cho boss quay về
                if self.boss.current_dodge_offset != 0:
                    self.boss.end_dodge()
                return self.end_turn()  # Kết thúc lượt
            return True

        # Logic cho các trạng thái khác (giữ nguyên)
        elif self.turn_state == 'BAR_BLINKING':
            self.bar_blink_timer -= dt
            if self.bar_blink_timer <= 0:
                self.calculate_fight_result()
                self.turn_state = 'FIGHTING'

        if self.turn_state == 'FIGHTING' and self.is_bar_moving:
            self.fight_bar_pos_x += self.fight_bar_speed * dt
            if self.fight_bar_pos_x > self.boss.box_rect.width:
                self.stop_fight_bar(miss=True)

        if (self.turn_state == 'ACTING' and self.act_info_text) or \
                (self.turn_state == 'MERCY_MENU' and self.mercy_info_text) or \
                self.turn_state == 'ACTION_COMPLETE':
            if not hasattr(self, 'end_turn_delay'): self.end_turn_delay = 1.0
            self.end_turn_delay -= dt
            if self.end_turn_delay <= 0:
                del self.end_turn_delay
                return self.end_turn()

        return True

    def start_fight_minigame(self):
        self.fight_bar_pos_x = 0 # Thanh sẽ bắt đầu từ bên trái box
        self.is_bar_moving = True

    def stop_fight_bar(self, miss=False):
        self.is_bar_moving = False
        self.final_bar_pos_x = self.fight_bar_pos_x # Lưu lại vị trí dừng

        # Nếu đánh trượt do chạy ra ngoài, xử lý như cũ
        if miss:
            self.slash_position = self.boss.body_rect.center
            self.boss.dodge()
            self.slash_snd.play()
            self.show_slash_timer = 0.6
            return

        # Nếu không, chuyển sang trạng thái nhấp nháy
        self.turn_state = 'BAR_BLINKING'
        self.bar_blink_timer = 0.4


    def calculate_fight_result(self):
        center_target = self.boss.box_rect.centerx
        bar_center = self.final_bar_pos_x + self.fight_bar_img.get_width() / 2
        distance = abs(bar_center - center_target)
        max_distance = self.boss.box_rect.width / 2

        # chém
        self.slash_frame_index = 0
        self.slash_position = self.boss.body_rect.center
        self.slash_snd.play()

        if distance < max_distance:
            self.attack_hit_snd.play()
            damage = int(20 * (1 - (distance / max_distance)))
            self.boss.take_damage(damage)
            print(f"HIT! Damage: {damage}, Boss HP: {self.boss.hp}")
            self.show_slash_timer = 0.4
        else:
            self.boss.dodge()  # Boss chỉ di chuyển SAU KHI ta đã lưu vị trí
            self.show_slash_timer = 0.6

    def draw(self, box_rect):
        if not self.is_turn_active: return

        spacing = 160
        start_x = box_rect.centerx - (3 * spacing) / 2
        self.button_positions.clear()
        for i, button_img in enumerate(self.buttons):
            image_to_draw = button_img
            if i == self.current_selection:
                if i == 0:
                    image_to_draw = self.fight_img_2
                elif i == 1:
                    image_to_draw = self.act_img_2
                elif i == 2:
                    image_to_draw = self.item_img_2
                elif i == 3:
                    image_to_draw = self.mercy_img_2

            pos = (start_x + i * spacing, box_rect.bottom + 70)
            self.button_positions.append(pos)
            button_rect = image_to_draw.get_rect(center=pos)
            self.screen.blit(image_to_draw, button_rect)

            # <<< PHẦN THÊM MỚI BẮT ĐẦU TỪ ĐÂY >>>
            # Nếu là mục đang được chọn, vẽ thêm trái tim bên trái
            if i == self.current_selection:
                # Lấy vị trí bên trái của nút làm tham chiếu
                # Đặt điểm giữa-phải (midright) của trái tim cách lề trái của nút 10px
                selector_rect = self.selector_img.get_rect(midright=(button_rect.left - 10, button_rect.centery))
                self.screen.blit(self.selector_img, selector_rect)

        if self.turn_state == 'SELECTING_ACTION':
            text = "* You feel like you're going to have a bad time"
            text_rect = box_rect.inflate(-40, -40)
            self.draw_wrapped_text(self.screen, text, self.info_font, 'white', text_rect)

        elif self.turn_state == 'FIGHTING' or self.turn_state == 'BAR_BLINKING':
            scaled_target_img = pygame.transform.scale(self.fight_target_img, (box_rect.width, box_rect.height))
            self.screen.blit(scaled_target_img, box_rect.topleft)
            # thanh tấn công
            bar_y_pos = box_rect.centery
            if self.is_bar_moving:
                #thanh chạy
                current_bar_pos_x = box_rect.left + self.fight_bar_pos_x
                bar_rect = self.fight_bar_img.get_rect(midleft=(current_bar_pos_x, bar_y_pos))
                self.screen.blit(self.fight_bar_img, bar_rect)
            elif self.turn_state == 'BAR_BLINKING':
                #thanh nhấp nháy
                final_bar_pos_x_abs = box_rect.left + self.final_bar_pos_x
                if (pygame.time.get_ticks() // 80) % 2 == 0:
                    image_to_draw = self.fight_bar_img
                else:
                    image_to_draw = self.fight_bar_img_2
                bar_rect = image_to_draw.get_rect(midleft=(final_bar_pos_x_abs, bar_y_pos))
                self.screen.blit(image_to_draw, bar_rect)

            #  chém
            if self.show_slash_timer > 0:
                current_frame = int(self.slash_frame_index)
                # Thêm điều kiện `and self.slash_position` để đảm bảo vị trí đã được set
                if current_frame < len(self.attack_slash_img) and self.slash_position:
                    image = self.attack_slash_img[current_frame]
                    # Sử dụng vị trí đã lưu thay vì vị trí hiện tại của boss
                    rect = image.get_rect(center=self.slash_position)
                    self.screen.blit(image, rect)

        elif self.turn_state == 'ACTING':
            self.draw_act_menu(box_rect)
        elif self.turn_state == 'ITEM_MENU':
            self.draw_item_menu(box_rect)
        elif self.turn_state == 'MERCY_MENU':
            self.draw_mercy_menu(box_rect)

    def draw_act_menu(self, box_rect):
        if self.act_info_text:
            text_rect = box_rect.inflate(-40, -40)
            self.draw_wrapped_text(self.screen, self.act_info_text, self.info_font, 'white', text_rect)
        else:
            for i, option in enumerate(self.act_options):
                color = 'yellow' if i == self.act_selection else 'white'
                text_surf = self.font.render(f"* {option}", True, color)

                vertical_spacing = 40
                y_pos = box_rect.top + 30 + (i * vertical_spacing)

                self.screen.blit(text_surf, (box_rect.left + 50, y_pos))

    def draw_item_menu(self, box_rect):
        item_keys = list(self.player.inventory.keys())
        for i, name in enumerate(item_keys):
            row = i // self.item_grid_cols
            col = i % self.item_grid_cols

            is_selected = (row, col) == self.item_selection
            color = 'yellow' if is_selected else 'white'

            text = f'* {name} ({self.player.inventory[name]["quantity"]})'
            item_surf = self.info_font.render(text, True, color)

            left_margin = 30
            x_pos = box_rect.left + left_margin + (col * box_rect.width / 2)
            y_pos = box_rect.top + 40 + (row * 35)  # Giữ nguyên khoảng cách dọc

            self.screen.blit(item_surf, (x_pos, y_pos))

    def draw_mercy_menu(self, box_rect):
        if self.mercy_info_text:
            text_rect = box_rect.inflate(-40, -40)
            self.draw_wrapped_text(self.screen, self.mercy_info_text, self.info_font, 'white', text_rect)
        else:
            for i, option in enumerate(self.mercy_options):
                color = 'yellow' if i == self.mercy_selection else 'white'
                # Thêm icon trái tim vào trước lựa chọn
                if i == self.mercy_selection:
                    selector_rect = self.selector_img.get_rect(
                        midright=(box_rect.left + 40, box_rect.top + 40 + (i * 40)))
                    self.screen.blit(self.selector_img, selector_rect)

                text_surf = self.font.render(f"* {option}", True, color)
                vertical_spacing = 40
                y_pos = box_rect.top + 30 + (i * vertical_spacing)
                self.screen.blit(text_surf, (box_rect.left + 50, y_pos))