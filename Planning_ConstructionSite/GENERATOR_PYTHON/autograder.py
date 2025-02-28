import random
import sys


class ProblemGenerator:
    def __init__(self):
        self.gx = -1
        self.gy = -1
        self.gnum_types = -1
        self.gtool_vec = -1
        self.gbarrier_vec = -1
        self.gp_goal = 100
        self.gtool_number = []
        self.gbarrier_number = []

        self.gx_pos = -1
        self.gy_pos = -1
        self.gx_tool_pos = []
        self.gy_tool_pos = []
        self.gx_barrier_pos = []
        self.gy_barrier_pos = []
        self.gx_tool_goal_pos = []
        self.gy_tool_goal_pos = []
        self.gbarrier = []

    def create_random_positions(self):
        max_value = max(max(self.gtool_number, default=0), max(self.gbarrier_number, default=0))
        self.gx_tool_pos = [[0] * max_value for _ in range(self.gnum_types)]
        self.gy_tool_pos = [[0] * max_value for _ in range(self.gnum_types)]
        self.gx_barrier_pos = [[0] * max_value for _ in range(self.gnum_types)]
        self.gy_barrier_pos = [[0] * max_value for _ in range(self.gnum_types)]
        self.gx_tool_goal_pos = [[-1] * max_value for _ in range(self.gnum_types)]
        self.gy_tool_goal_pos = [[-1] * max_value for _ in range(self.gnum_types)]

        self.gbarrier = [[False] * self.gy for _ in range(self.gx)]

        for i in range(self.gnum_types):
            for j in range(self.gbarrier_number[i]):
                while True:
                    rx, ry = random.randint(0, self.gx - 1), random.randint(0, self.gy - 1)
                    if not self.gbarrier[rx][ry]:
                        self.gbarrier[rx][ry] = True
                        self.gx_barrier_pos[i][j] = rx
                        self.gy_barrier_pos[i][j] = ry
                        break

            for j in range(self.gtool_number[i]):
                self.gx_tool_pos[i][j] = random.randint(0, self.gx - 1)
                self.gy_tool_pos[i][j] = random.randint(0, self.gy - 1)

                if random.randint(0, 99) < self.gp_goal:
                    self.gx_tool_goal_pos[i][j] = random.randint(0, self.gx - 1)
                    self.gy_tool_goal_pos[i][j] = random.randint(0, self.gy - 1)

        while True:
            rx, ry = random.randint(0, self.gx - 1), random.randint(0, self.gy - 1)
            if not self.gbarrier[rx][ry]:
                self.gx_pos = rx
                self.gy_pos = ry
                break

    def process_command_line(self, argv):
        arg_map = {
            "-x": "gx",
            "-y": "gy",
            "-t": "gnum_types",
            "-p": "gp_goal",
            "-k": "gtool_vec",
            "-l": "gbarrier_vec",
        }
        for i in range(1, len(argv) - 1, 2):
            option, value = argv[i], argv[i + 1]
            if option in arg_map:
                setattr(self, arg_map[option], int(value))
            else:
                print(f"Unknown option: {option}")
                self.usage()
                sys.exit(1)

        if self.gnum_types > 0:
            self.gtool_number = self.setup_numbers(self.gtool_vec, self.gnum_types)
            self.gbarrier_number = self.setup_numbers(self.gbarrier_vec, self.gnum_types)
        else:
            self.usage()
            sys.exit(1)

    def setup_numbers(self, vec, num_types):
        numbers = []
        for _ in range(num_types):
            numbers.insert(0, vec % 10)
            vec //= 10
        return numbers

    def usage(self):
        print("Usage:")
        print("OPTIONS   DESCRIPTIONS")
        print("-x <num>    x scale (minimal 1)")
        print("-y <num>    y scale (minimal 1)")
        print("-t <num>    num different tool+barrier types (minimal 1)")
        print("-k <num>    number tools vector (decimal)")
        print("-l <num>    number barriers vector (decimal)")
        print("-p <num>    probability of any tool being mentioned in the goal (default: 100)")

    def print_problem(self):
        print(f"(define (problem construction-x{self.gx}-y{self.gy}-t{self.gnum_types}-"
              f"k{self.gtool_vec}-l{self.gbarrier_vec}-p{self.gp_goal})")
        print("(:domain construction-site)")
        print("(:objects")

        for y in range(self.gy):
            print(" ".join(f"f{x}-{y}f" for x in range(self.gx)))
        for i in range(self.gnum_types):
            print(f"type{i}")
        for i, count in enumerate(self.gtool_number):
            for j in range(count):
                print(f"tool{i}-{j}")
        print(")")

        print("(:init")
        print("(free)")
        for y in range(self.gy):
            for x in range(self.gx):
                print(f"(location f{x}-{y}f)")
        for i in range(self.gnum_types):
            print(f"(type type{i})")
            for j in range(self.gtool_number[i]):
                print(f"(tool tool{i}-{j})")
                print(f"(tool-type tool{i}-{j} type{i})")
        self.print_connections()
        self.print_open_barriers()
        self.print_tool_positions()
        print(f"(at-worker f{self.gx_pos}-{self.gy_pos}f)")
        print(")")

        print("(:goal")
        print("(and")
        self.print_tool_goal_positions()
        print(")")
        print(")")
        print(")")

    def print_connections(self):
        for y in range(self.gy):
            for x in range(self.gx - 1):
                print(f"(connected f{x}-{y}f f{x + 1}-{y}f)")
            for x in range(1, self.gx):
                print(f"(connected f{x}-{y}f f{x - 1}-{y}f)")
        for x in range(self.gx):
            for y in range(self.gy - 1):
                print(f"(connected f{x}-{y}f f{x}-{y + 1}f)")
            for y in range(1, self.gy):
                print(f"(connected f{x}-{y}f f{x}-{y - 1}f)")

    def print_open_barriers(self):
        for y in range(self.gy):
            for x in range(self.gx):
                if not self.gbarrier[x][y]:
                    print(f"(open f{x}-{y}f)")
        for i in range(self.gnum_types):
            for j in range(self.gbarrier_number[i]):
                print(f"(barrier f{self.gx_barrier_pos[i][j]}-{self.gy_barrier_pos[i][j]}f)")
                print(f"(barrier-type f{self.gx_barrier_pos[i][j]}-{self.gy_barrier_pos[i][j]}f type{i})")

    def print_tool_positions(self):
        for i in range(self.gnum_types):
            for j in range(self.gtool_number[i]):
                print(f"(at tool{i}-{j} f{self.gx_tool_pos[i][j]}-{self.gy_tool_pos[i][j]}f)")

    def print_tool_goal_positions(self):
        for i in range(self.gnum_types):
            for j in range(self.gtool_number[i]):
                if self.gx_tool_goal_pos[i][j] != -1:
                    print(f"(at tool{i}-{j} f{self.gx_tool_goal_pos[i][j]}-{self.gy_tool_goal_pos[i][j]}f)")


if __name__ == "__main__":
    generator = ProblemGenerator()
    generator.process_command_line(sys.argv)
    generator.create_random_positions()
    generator.print_problem()

