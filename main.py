import random


class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.level = 1
        self.attack_power = attack_power
        self.xp = 0

    def defend(self, damage):
        self.hp -= damage

    def attack(self, target):
        damage = self.attack_power
        target.defend(damage)

    def status(self):
        print(f"{self.name}, HP:{self.hp}, LVL:{self.level}, ATK:{self.attack_power}, XP:{self.xp}")

    def level_up(self):
        self.level += 1
        self.hp += 15
        self.attack_power += 5
        self.xp = 0

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} отримує {amount} XP (всього: {self.xp})")
        if self.xp >= self.level * 100:
            self.level_up()

    def is_alive(self):
        return self.hp > 0

    def class_name(self):
        return "Курсант"


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=130, attack_power=28)
        self.block = 5

    def defend(self, damage):
        actual = max(1, damage - self.block)
        self.hp = max(0, self.hp - actual)
        print(f"{self.name} блокує {self.block} шкоди! -{actual} HP")

    def level_up(self):
        super().level_up()
        self.block += 5

    def class_name(self):
        return "Воїн"


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, hp=80, attack_power=42)
        self.crit_chance = 0.35

    def attack(self, target):
        if random.random() < self.crit_chance:
            damage = self.attack_power * 2
            target.hp = max(0, target.hp - damage)
            print(f"КРИТИЧНИЙ УДАР! -{damage} HP!")
            return damage
        else:
            super().attack(target)

    def class_name(self):
        return "Маг"


class Scout(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack_power=34)
        self.dodge_chance = 0.35

    def defend(self, damage):
        if random.random() < self.dodge_chance:
            print(f"{self.name} ухиляється від удару!")
        else:
            super().defend(damage)

    def class_name(self):
        return "Розвідник"


class Arena:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.round_count = 0

    def fight(self):
        print(f"{'═' * 50}")
        print(
            f"БІЙ: {self.fighter1.name} ({self.fighter1.class_name()}) vs {self.fighter2.name} ({self.fighter2.class_name()})")
        print(f"{'═' * 50}")

        while self.fighter1.is_alive() and self.fighter2.is_alive():
            self.round_count += 1
            print(f"── Раунд {self.round_count} ──")

            self.fighter1.attack(self.fighter2)
            if not self.fighter2.is_alive():
                break

            self.fighter2.attack(self.fighter1)

            self.fighter1.status()
            self.fighter2.status()

        return self.show_result()

    def show_result(self):
        print(f"{'═' * 50}")
        winner = self.fighter1 if self.fighter1.is_alive() else self.fighter2
        loser = self.fighter2 if self.fighter1.is_alive() else self.fighter1
        print(f"ПЕРЕМОЖЕЦЬ: {winner.name} за {self.round_count} раундів!")
        print(f"{loser.name} переможений.")
        print(f"{'═' * 50}\n")
        winner.gain_xp(80)
        winner.hp += 20
        print(f"{winner.name} відновлює 20 HP після бою → {winner.hp} HP")
        return winner


class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.members = []

    def add_member(self, character):
        self.members.append(character)

    def total_power(self):
        return sum(m.attack_power for m in self.members)

    def find_strongest(self):
        return max(self.members, key=lambda m: m.attack_power + m.hp)

    def show_roster(self):
        print(f"\nКоманда «{self.team_name}» ({len(self.members)} бійців):")
        for m in self.members:
            m.status()
        strongest = self.find_strongest()
        print(f"Найсильніший: {strongest.name} ({strongest.class_name()})")
        print(f"Загальна сила: {self.total_power()}")


def run_tournament(fighters):
    print(f"\n{'═' * 50}")
    print("NEXUS TRIALS — ТУРНІР ПОЧИНАЄТЬСЯ")
    print(f"{'═' * 50}")

    pool = fighters[:]
    random.shuffle(pool)

    while len(pool) > 1:
        f1 = pool.pop(0)
        f2 = pool.pop(0)
        arena = Arena(f1, f2)
        winner = arena.fight()
        pool.append(winner)

    champion = pool[0]
    print(f"\nЧЕМПІОН: {champion.name} ({champion.class_name()}) — Рівень {champion.level}!")
    return champion


CLASS_list = {
    "1": ("Воїн", Warrior),
    "2": ("Маг", Mage),
    "3": ("Розвідник", Scout),
}


def choose_class(name):
    print("\nОбери клас:")
    print("  [1] Воїн      — HP:130 | ATK:28 | Блок:5")
    print("  [2] Маг       — HP:80  | ATK:42 | Крит 35%")
    print("  [3] Розвідник — HP:100 | ATK:34 | Ухил 35%")
    while True:
        choice = input("Твій вибір (1/2/3): ").strip()
        if choice in CLASS_list:
            label, cls = CLASS_list[choice]
            fighter = cls(name)
            print(f"{name} — {label} готовий до бою!")
            return fighter
        print("Введи 1, 2 або 3.")


def main():
    print("═" * 50)
    print("NEXUS TRIALS — STEPus Academy Battle System")
    print("═" * 50)

    name = input("Введи ім'я свого персонажа: ").strip() or "Курсант"
    player = choose_class(name)

    ai_fighters = [
        Warrior("NEXUS-Guard"), Mage("Shadow-Sync"), Scout("Phantom-X"),
        Scout("Glitch-Runner"), Mage("Arc-Weaver"), Warrior("Iron-Shell"),
    ]
    opponents = random.sample(ai_fighters, 2)
    fighters = [player] + opponents

    team = Team("NEXUS Trials")
    for f in fighters:
        team.add_member(f)
    team.show_roster()

    input("\nНатисни Enter щоб почати турнір...")
    run_tournament(fighters)

    print("\nСеанс завершено. NEXUS-CORE стабілізовано.\n")
