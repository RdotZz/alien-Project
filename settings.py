class Settings:

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (87,250,255)
        
        #飞船速度
        self.ship_speed = 1.5

        #子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3