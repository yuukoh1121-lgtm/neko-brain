import pygame
import sys
import random

# 1. 初期設定
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("アハ体験！ねこちゃん脳トレ")

clock = pygame.time.Clock()

# 2. 画像の読み込み
try:
    img_start = pygame.image.load("inuneko_s.png").convert()
    img_start = pygame.transform.scale(img_start, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    img_end = pygame.image.load("inuneko_e.png").convert()
    img_end = pygame.transform.scale(img_end, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("エラー: 画像ファイルが見つかりません！")
    sys.exit()

# 3. フォントの準備
try:
    font = pygame.font.SysFont("hg丸ｺﾞｼｯｸmpro", 85, bold=True)
    hint_font = pygame.font.SysFont("hg丸ｺﾞｼｯｸmpro", 24)
    gauge_font = pygame.font.SysFont("hg丸ｺﾞｼｯｸmpro", 18, bold=True)
    countdown_font = pygame.font.SysFont("hg丸ｺﾞｼｯｸmpro", 150, bold=True) # カウントダウン用の特大フォント
except:
    font = pygame.font.SysFont("notosanscjkjp", 85, bold=True)
    hint_font = pygame.font.SysFont("notosanscjkjp", 24)
    gauge_font = pygame.font.SysFont("notosanscjkjp", 18, bold=True)
    countdown_font = pygame.font.SysFont("notosanscjkjp", 150, bold=True)

# 4. ゲームの状態を管理する変数
alpha = 0
change_speed = 0.15 
is_correct = False

# 🎥 【新機能】カウントダウン用のタイマー（60フレーム = 1秒）
# 5秒から始めて、0になったらゲームスタート！
countdown_frame = 10 * 60 

# 🌸 赤丸のついた右下の紫陽花エリアのみに設定
flower_rect = pygame.Rect(400, 500, 180, 100) 

# 紙吹雪（クラッカー）用のデータ
particles = []

def spawn_cracker():
    """正解した瞬間にカラフルな紙吹雪を放つ"""
    colors = [
        (255, 50, 50), (50, 255, 50), (50, 100, 255),
        (255, 215, 0), (255, 105, 180), (0, 255, 255)
    ]
    for _ in range(120):
        particles.append({
            "x": 300,
            "y": 400,
            "vx": random.uniform(-8, 8),
            "vy": random.uniform(-12, -3),
            "color": random.choice(colors),
            "size": random.randint(5, 12)
        })

def draw_bold_text(text, x, y, main_color, edge_color, thickness=3, target_font=font):
    """文字をさらに太く見せるための重ね書き（引数でフォントを選べるように拡張）"""
    text_surface = target_font.render(text, True, main_color)
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                edge_surface = target_font.render(text, True, edge_color)
                screen.blit(edge_surface, (x + dx, y + dy))
    screen.blit(text_surface, (x, y))

# 5. メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # カウントダウンが終わっている（ゲームが始まっている）時だけクリックを受け付ける
            if not is_correct and countdown_frame <= 0:
                if flower_rect.collidepoint(mouse_pos):
                    is_correct = True
                    spawn_cracker()

    # --- 画面の描き込み処理 ---
    screen.blit(img_start, (0, 0))

    # カウントダウンが終わったらアハ体験（変化）を開始
    if countdown_frame <= 0 and not is_correct:
        if alpha < 255:
            alpha += change_speed
            if alpha > 255:
                alpha = 255
    
    img_end.set_alpha(int(alpha))
    screen.blit(img_end, (0, 0))

    # 📊 上部の変化ゲージ（進捗バー）の描画
    pygame.draw.rect(screen, (0, 0, 0, 150), (0, 0, SCREEN_WIDTH, 45))
    start_text = gauge_font.render("Start", True, (255, 255, 255))
    end_text = gauge_font.render("End", True, (255, 255, 255))
    screen.blit(start_text, (15, 12))
    screen.blit(end_text, (545, 12))
    
    gauge_x, gauge_y = 75, 15
    gauge_width, gauge_height = 450, 15
    pygame.draw.rect(screen, (255, 255, 255), (gauge_x, gauge_y, gauge_width, gauge_height), 2)
    
    current_progress = int(gauge_width * (alpha / 255.0))
    if current_progress > 0:
        pygame.draw.rect(screen, (50, 220, 50), (gauge_x + 2, gauge_y + 2, current_progress - 4, gauge_height - 4))

    # 🎬 【新機能】カウントダウン画面の描画処理
    if countdown_frame > 0:
        countdown_frame -= 1
        # 画面全体に薄暗いフィルターをかける
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120)) # 黒の半透明
        screen.blit(overlay, (0, 0))
        
        # 残り秒数の計算
        seconds = (countdown_frame // 60) + 1
        
        # 文字の表示（中央寄せの計算含む）
        if countdown_frame < 30: # 最後の0.5秒だけ「スタート！」にする
            draw_bold_text("START!", 50, 320, (255, 215, 0), (0, 0, 0), thickness=6, target_font=font)
        else:
            draw_bold_text(str(seconds), 250, 300, (255, 255, 255), (0, 0, 0), thickness=6, target_font=countdown_font)

    # 紙吹雪のアニメーション
    if is_correct:
        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.2
            p["vx"] *= 0.98
            if p["y"] > SCREEN_HEIGHT:
                particles.remove(p)
                continue
            pygame.draw.rect(screen, p["color"], (int(p["x"]), int(p["y"]), p["size"], p["size"]))

    # 📢 「大正解！」と下部ヒントテキストの制御
    if is_correct:
        draw_bold_text("大正解！", 130, 70, (255, 0, 0), (255, 255, 255), thickness=4)
    elif countdown_frame <= 0: # カウントダウンが終わってからヒントを表示
        if alpha < 45:
            hint_text = "どこが変わるかな？"
        elif alpha < 220:
            hint_text = "変わりだしたよ！"
        else:
            hint_text = "どこが変わったかわかった？"
            
        hint_surface = hint_font.render(hint_text, True, (255, 255, 255))
        screen.blit(hint_surface, (20, 750))

    pygame.display.update()
    clock.tick(60)