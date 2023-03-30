class GameStage:
    def __init__(self, stage_number, enemy_count):
        self.stage_number = stage_number
        self.enemy_count = enemy_count

class StageManager:
    def __init__(self, font):
        self.current_stage = None
        self.stages = []
        self.font = font

    def add_stage(self, stage):
        self.stages.append(stage)

    def start_next_stage(self):
        if self.current_stage is None:
            self.current_stage = 0
        else:
            self.current_stage += 1
        return self.stages[self.current_stage]

    def display_stage_info(self, screen):
        stage_info_text = f"Stage {self.current_stage + 1}"
        stage_info_rendered = self.font.render(stage_info_text, True, WHITE)
        stage_info_rect = stage_info_rendered.get_rect()
        stage_info_rect.center = (game_area_width // 2, windowed_height // 2)
        screen.blit(stage_info_rendered, stage_info_rect)
