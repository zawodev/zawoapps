import curses

def parse_logs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_alpha = None
    iteration = None
    backbone_mask = []
    genotypes = []
    in_backbone_section = False

    for line in lines:
        line = line.strip()

        # match iteration
        if line.startswith("iteration:"):
            # extract the iteration ID only
            iteration = line.split()[0]
            in_backbone_section = False
        elif line.startswith("--- Current alpha:"):
            # extract current alpha and create a new group if necessary
            current_alpha = float(line.split(":")[1].strip())
            if current_alpha not in data:
                data[current_alpha] = []
        elif line.startswith("Backbone mask:"):
            # start collecting mask and genotypes
            backbone_mask = []
            genotypes = []
            in_backbone_section = True
        elif in_backbone_section:
            # collect backbone mask or genotypes
            if len(backbone_mask) == 0:
                backbone_mask.append(line)
            elif len(genotypes) < 256:
                genotypes.append(line)
            else:
                # once we have collected all genotypes, save the data
                data[current_alpha].append({
                    "iteration": iteration,
                    "backbone_mask": backbone_mask[0],
                    "genotypes": genotypes.copy()
                })
                backbone_mask = []
                genotypes = []
                in_backbone_section = False

    return data


def display_data(stdscr, data):
    current_alpha_idx = 0
    alpha_keys = sorted(data.keys())
    max_alpha_idx = len(alpha_keys) - 1

    iteration_idx = 0

    while True:
        stdscr.clear()
        alpha = alpha_keys[current_alpha_idx]
        iteration_data = data[alpha][iteration_idx]
        max_iterations = len(data[alpha])

        stdscr.addstr(0, 0, f"Current alpha: {alpha:.5f} (Group {current_alpha_idx + 1}/{len(alpha_keys)})")
        stdscr.addstr(1, 0, f"Iteration: {iteration_data['iteration']} (State {iteration_idx + 1}/{max_iterations})")
        stdscr.addstr(3, 0, "Backbone mask:")
        stdscr.addstr(4, 0, iteration_data['backbone_mask'])

        stdscr.addstr(6, 0, "Genotypes:")
        for i, genotype in enumerate(iteration_data['genotypes'][:10]):  # show first 10 for simplicity
            stdscr.addstr(8 + i, 0, genotype)

        stdscr.addstr(20, 0, "Navigation:")
        stdscr.addstr(21, 0, "[Left/Right] Change alpha | [Up/Down] Change iteration | [Q] Quit")

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key == curses.KEY_RIGHT and current_alpha_idx < max_alpha_idx:
            current_alpha_idx += 1
            iteration_idx = 0
        elif key == curses.KEY_LEFT and current_alpha_idx > 0:
            current_alpha_idx -= 1
            iteration_idx = 0
        elif key == curses.KEY_UP and iteration_idx < len(data[alpha_keys[current_alpha_idx]]) - 1:
            iteration_idx += 1
        elif key == curses.KEY_DOWN and iteration_idx > 0:
            iteration_idx -= 1


def main(file_path):
    data = parse_logs(file_path)
    curses.wrapper(display_data, data)

if __name__ == "__main__":
    file_path = "_moAlikTest_021.txt"
    main(file_path)
