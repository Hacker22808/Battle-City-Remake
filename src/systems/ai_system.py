"""
Прості вороги: випадкові повороти, уникнення стіни, прицільний вогонь якщо на одній лінії, таймери прийняття рішень.
"""
class AISystem:
    def __init__(self, physics):
        self.physics = physics

    def update(self, dt, enemies, blocks):
        for e in enemies:
            e.decide(dt)
            dx = int(e.dir.x * e.speed * dt)
            dy = int(e.dir.y * e.speed * dt)
            self.physics.move_and_collide(e, dx, dy, blocks)
