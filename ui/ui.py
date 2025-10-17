import pygame

# ========================
# FONT HỖ TRỢ
# ========================
def _ensure_font(font_path="font/MonsterFriendBack.otf", size=24):
    try:
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.Font(None, size)


# ========================
# THANH MÁU NGƯỜI CHƠI
# ========================
def draw_health_bar(surface, x, y, current_hp, max_hp, font=None):
    font = _ensure_font(size=22) if font is None else font
    bar_width, bar_height = 250, 20

    current_hp = max(0, min(current_hp, max_hp))
    ratio = current_hp / max_hp if max_hp > 0 else 0

    # Nền đen
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height))

    # Thanh vàng
    pygame.draw.rect(surface, (255, 255, 0), (x, y, bar_width * ratio, bar_height))

    # Viền trắng
    pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    # Chữ HP
    hp_text = font.render("HP", True, (255, 255, 255))
    surface.blit(hp_text, (x - 50, y - 2))

    # Số máu ở bên phải
    val_text = font.render(f"{int(current_hp)}/{int(max_hp)}", True, (255, 255, 255))
    surface.blit(val_text, (x + bar_width + 10, y - 2))


# ========================
# THANH MÁU + TÊN BOSS
# ========================
def draw_boss_info(surface, boss, screen_width=1000, y=50, width=300, height=22):
    if not boss:
        return

    # FONT: MonsterFriend (Undertale)
    name_font = _ensure_font(size=30)
    bar_font = _ensure_font(size=22)

    # Lấy thông tin boss
    name = getattr(boss, "name", "???").upper()
    level = getattr(boss, "level", "?")
    hp = getattr(boss, "hp", 0)
    max_hp = getattr(boss, "max_hp", 1)

    ratio = max(0, min(1, hp / max_hp))
    x = (screen_width - width) // 2  # canh giữa

    # --- Dòng chữ tên boss + level ---
    # --- Dòng chữ tên boss ---
    name_text = str(getattr(boss, "name", "???")).upper()

# Tạo surface chữ và căn giữa
    label_surf = name_font.render(name_text, True, (255, 255, 255))
    label_rect = label_surf.get_rect(center=(screen_width // 2, y - 25))

# Dịch nhẹ lên hoặc xuống tùy thẩm mỹ (ở đây dịch lên 5px)
    label_rect.y -= 5

    surface.blit(label_surf, label_rect)


    # --- Thanh máu boss ---
    #pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height))  # nền đen
    #pygame.draw.rect(surface, (255, 255, 0), (x, y, width * ratio, height))  # thanh vàng
    #pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)  # viền trắng

    # --- Hiển thị giá trị HP ---
    #hp_surf = bar_font.render(f"{int(hp)}/{int(max_hp)}", True, (255, 255, 255))
    #hp_rect = hp_surf.get_rect(midleft=(x + width + 15, y + height // 2))
    #surface.blit(hp_surf, hp_rect)
