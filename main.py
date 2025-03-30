import pygame #Spēles interfeisam
import random #Sākuma skaitļu ģenerēšanai
import time #Laika skaitīšanai
#####################################################################################################################################################################################################################
#Kase virsotnes vērtībām


class TreeNode:
    def __init__(self, value, parent=None): #Konstruktors, kad jauna virsotne izveidota, piem. (node = TreeNode(12, 1), kur self: node, value: 12, parent: 1)
        self.value = value #Skaitliskā vērtība
        self.parent = parent #Virsotnes pēdējais apskatītais pirmstecis
        self.children = [] #Virsotnes pēcteči
        self.bank = 0 #Bankas vērtība
        self.score = 0 #Punktu vērtība
        self.heuristic_value = float('-inf') #Heiristiskā vērtība virsotnei, ko aprēķinās heiristiskā funkcija, inicializē ar mazāko iespējamo

    #Funkcija pēcteču veidošanai
    def add_child(self, child):
        self.children.append(child) #Pievieno pēcteci masīvam

#Pilnā koka klase
class Tree:
    #Koka inicializēšana (Koks: self)
    def __init__(self):
        self.root = None
        self.node_map = {} #Grāmatnīca duplikātiem

    #Koka ģenerēšana: sākumā saknes piešķiršana un pēcteču ģenerēšanas izsaukšana (num: izvēlētais skaitlis)
    def generate_tree(self, num):
        self.root = self._create_node(num) #Izsauc funkciju _create_node ar skaitļa vērtību.
        self._generate_children(self.root) #Izsauc funkicju _generate_children ar virsotnes vērtību.

    #Virsotnes izveidošanas funkcija, izmanto vērtības value un parent, ja tāds ir.
    def _create_node(self, value, parent=None):
        node = TreeNode(value, parent) #node: virsotne. Izveido virsotni kā TreeNode klasi ievadot vērtības value un parent, ja tāds ir.
        self._calculate(node) #Izsauc iekšējo funkciju _calculate priekš virsotnes node.

        #Izveido īpašu atslēgu virsotnei. Ievieto to duplikātu grāmatnīcā, ja tāda jau nepastāv.
        key = (node.value, node.bank, node.score)

        if key in self.node_map:
            return self.node_map[key] #Ja identiska virsotne jau pastāv, atgriež virsotnes vērtību _create_node.
        else:
            self.node_map[key] = node #Ja nepastāv, atgriež jauno virsotni _create_node.
            return node

    #Ģenerē virsotnes pēctečus (ja ir dalāmi):
    def _generate_children(self, node): #node: virsotnes vērtība
        for divisor in [2, 3, 4, 5]: #Pārbauda vai virsotne ir dalāma augošā secībā
            if node.value % divisor == 0: #Ja virsotnes vērtība ir dalāma:
                child_value = node.value // divisor #Izveido jauno vērtību pēctecim
                child = self._create_node(child_value, parent=node) #Izsauc _create_node ar jauno vērtību un glabājot pirmsteci
                node.add_child(child) #Izsauc add_child ar pēcteča vērtību
                self._generate_children(child) #izsauc _generate_children ar pēcteča vērtību

    #Funkcija bankas un punktu piešķiršanai virsotnei
    def _calculate(self, node):
        if node.value % 5 == 0: #Ja vērtība dalās ar 5 (beidzās ar 0 vai 5):
            node.bank = node.parent.bank + 1 if node.parent else 0 #Pievieno bankai pirmsteča bankas vērtību + 1, ja virsotne nav sakne
        else:
            node.bank = node.parent.bank if node.parent else 0 #Pievieno bankai pirmsteča bankas vērtību, ja nedalās ar 5 un virsotne nav sakne

        if node.value % 2 == 0: #Ja vērtība dalās ar 2 (ir pāra skaitlis):
            node.score = node.parent.score - 1 if node.parent else 0 #Punkti = pirmsteča punktiem - 1, ja virsotne nav sakne
        else:
            node.score = node.parent.score + 1 if node.parent else 0 #Punkti = pirmsteča punktiem + 1, ja virsotne ir nepāra un nav sakne

    #Heiristiskā funkcija, iziet cauri visam kokam sākot ar strupceļiem attiecīgi algoritmam:
    def calculate_heuristic(self, node, ai_turn, minimax_chosen, alpha=float('-inf'), beta=float('inf')):
        global total_nodes_evaluated
        total_nodes_evaluated += 1  # Increment counter for each node evaluated
        if len(node.children) == 0: #Ja strupceļš:
            if node.score % 2 == 0: #Ja pāra skaitlis
                final_score = node.score + node.bank #Rezultāts = punkti+banka
            else:
                final_score = node.score - node.bank #Ja nepāra, rezultāts = punkti-banka
            
            if ai_turn: #Ja MI gājiens:
                node.heuristic_value = -1 if final_score % 2 == 0 else 1 #Strupceļam piešķir -1, ja rezultāts pāra skaitlis, 1, ja nepāra
            else:
                node.heuristic_value = 1 if final_score % 2 == 0 else -1 #Ja MI iet otrais, 1, ja rezultāts pāra skaitlis, -1 - ja nepāra

            return (node.heuristic_value)
        
        else:
        #MINIMAX UN ALFA-BETA ALGORITMS
            if ai_turn: #Ja MI gājiens (MAX):
                node.heuristic_value = float('-inf') #Piesķir mazāko iespējamo vērtību ar ko salīdzināt
                for child in node.children:
                    if minimax_chosen:
                        child.heuristic_value = self.calculate_heuristic(child, not ai_turn, minimax_chosen) #Rekursīvi rēķina katra pēcteča virsotnes h. vērtību
                    else:
                        child.heuristic_value = self.calculate_heuristic(child, not ai_turn, minimax_chosen, alpha, beta) #
                    node.heuristic_value = max(node.heuristic_value, child.heuristic_value)                               #Pieškir apskatāmajai virsotnei h. vērtību
                    node.heuristic_value += child.heuristic_value #Pieskaita pēcteča vērtību (HEIRISTISKĀ FUNKCIJA)
                    if not minimax_chosen: #Ja alfa-beta
                        if node.heuristic_value >= beta: #Ja virsotnes vērtība ir lielāka par mantoto beta vērtību, nogriež neapskatītos pēctečus
                            break
                        alpha = max(alpha, node.heuristic_value) #Piešķir alpha vērtību

            else: #Ja cilvēka gājiens (MIN):
                node.heuristic_value = float('inf') #Piesķir lielāko iespējamo vērtību ar ko salīdzināt
                for child in node.children:
                    if minimax_chosen:
                        child.heuristic_value = self.calculate_heuristic(child, not ai_turn, minimax_chosen) #Rekursīvi rēķina katra pēcteča virsotnes h. vērtību
                    else:
                        child.heuristic_value = self.calculate_heuristic(child, not ai_turn, minimax_chosen, alpha, beta) #
                    node.heuristic_value = min(node.heuristic_value, child.heuristic_value)                               #Pieškir apskatāmajai virsotnei h. vērtību
                    node.heuristic_value += child.heuristic_value #Pieskaita pēcteča vērtību (HEIRISTISKĀ FUNKCIJA)
                    if not minimax_chosen:     
                        if node.heuristic_value <= alpha: #Ja virsotnes vērtība ir mazāka par mantoto alfa vērtību, nogriež neapskatītos pēctečus
                            break
                        beta = min(beta, node.heuristic_value) #Piešķir beta vērtību

            return (node.heuristic_value) #Atgriež pēdējo saknes vērtību


#####################################################################################################################################################################################################################

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Division Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (255, 215, 0)  # Gold color for highlighted buttons
HOVER_COLOR = (255, 235, 150)    # Lighter gold for hover
DISABLED_COLOR = (100, 100, 100) # Grey color for disabled buttons
RULES_BG_COLOR = (70, 70, 70)    # Darker background for rules window

# Fonts
FONT = pygame.font.SysFont("Arial Black", 24)
SMALL_FONT = pygame.font.SysFont("Arial Black", 16)
RULES_FONT = pygame.font.SysFont("Arial Black", 20)

# Game state
starting_numbers = [random.randint(30000, 50000) for i in range(5)]
num = None
ai_turn = None
minimax_chosen = None
game_screen = False
game_over = False
divisor = None
history = []
current_bank = 0
current_score = 0
tree = None
show_rules = False  # Track if rules window is open

ai_total_time = 0    # Total time spent by AI on all moves
ai_moves_count = 0   # Number of moves made by AI
last_ai_time = 0     # Time taken for the last AI move

total_nodes_evaluated = 0  # Total nodes evaluated by AI during the game

# Rules text
rules_text = [
    "Spēles noteikumi:",
    "",
    "•Spēlētāji veic gājienus pēc kārtas, dalot skaitli ar 2, 3, 4 vai 5.",
    "•Dalīšana ir iespējama tikai tad, ja rezultāts ir vesels skaitlis.",
    "•Ja rezultāts ir pāra skaitlis, no punktu skaita atņem 1;",
    "  ja nepāra – pieskaita 1.",
    "•Ja dalīšanas rezultāts beidzas ar 0 vai 5, bankai",
    "  tiek pieskaitīts 1 punkts.",
    "•Spēle beidzas, kad skaitli vairs nevar dalīt tā,",
    "  lai iegūtu veselu skaitli.",
    "•Ja galējais punktu skaits ir pāra skaitlis, bankas punkti tiek",
    "  pieskaitīti gala rezultātam; ja nepāra – atņemti.",
    "•Ja gala skaitlis ir nepāra, uzvar spēlētājs, kurš gāja pirmais;",
    "  ja pāra – uzvar spēlētājs, kurš gāja otrais."
]

# Button class with hover effect
class Button:
    def __init__(self, text, x, y, width, height, category=False, color=WHITE, border_color=BLACK):
        self.text = str(text)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.category = category 
        self.highlighted = False
        self.disabled = False
        self.hovered = False

    def draw(self, screen):
        # Determine button color based on state
        if self.disabled:
            current_color = DISABLED_COLOR
        elif self.highlighted:
            current_color = HIGHLIGHT_COLOR
        elif self.hovered:
            current_color = HOVER_COLOR
        else:
            current_color = self.color
        
        pygame.draw.rect(screen, self.border_color, self.rect.inflate(4, 4))  # Border
        pygame.draw.rect(screen, current_color, self.rect)  # Fill
        label = FONT.render(self.text, True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def toggle_selection(self, all_buttons):
        """Ensure only one button in the same category is highlighted."""
        for button in all_buttons:
            if button.category == self.category:
                button.highlighted = False  # Deselect all in the same category
        self.highlighted = True  # Highlight the clicked button

# Create buttons
num_buttons = []
x = 0
for num in starting_numbers:
    num_buttons.append(Button(num, 20 + x, 100, 200, 50, "number"))
    x += 210

algo_buttons = [
    Button("Minimax", 330, 250, 200, 50, "algorithm"),
    Button("Alpha-Beta", 550, 250, 200, 50, "algorithm")
]

seq_buttons = [
    Button("Player", 330, 400, 200, 50, "sequence"),
    Button("AI", 550, 400, 200, 50, "sequence")
]

div_buttons = []
x = 0
for divisor in [2, 3, 4, 5]:
    div_buttons.append(Button(divisor, 365+x, 250, 50, 50))
    x += 100

start_button = Button("START", 440, 620, 200, 50, "start")
restart_button = Button("RESTART", 440, 500, 200, 50)
restart_button.disabled = True
rules_button = Button("?", WIDTH-60, 20, 40, 40)  # Moved to top-right

# Text elements
text_boxes = [
    FONT.render("Pick a number:", True, WHITE),
    FONT.render("Pick the algorithm:", True, WHITE),
    FONT.render("Pick who goes first:", True, WHITE),
    FONT.render("Current number:", True, WHITE),
    FONT.render("Pick divisor:", True, WHITE),
    FONT.render("Bank:", True, WHITE),
    FONT.render("Score:", True, WHITE),
    FONT.render("Game History:", True, WHITE)
]

def update_divisors(num):
    """Update which divisor buttons are enabled based on current number"""
    for button in div_buttons:
        divisor = int(button.text)
        button.disabled = (num % divisor != 0)

def is_divisible(num):
    """Check if number is divisible by any of the divisors (2,3,4,5)"""
    return any(num % d == 0 for d in [2, 3, 4, 5])

def check_game_over():
    """Check if the game has ended (no valid moves left)"""
    return not is_divisible(num)

def reset_game():
    """Reset all game state variables and generate new numbers"""
    global num, ai_turn, minimax_chosen, game_screen, game_over, history, current_bank, current_score, tree, starting_numbers, show_rules
    global ai_total_time, ai_moves_count, last_ai_time
    global total_nodes_evaluated
    # Generate new random numbers
    starting_numbers = [random.randint(30000, 50000) for i in range(5)]
    
    # Update number buttons with new values
    for i, button in enumerate(num_buttons):
        button.text = str(starting_numbers[i])
        button.highlighted = False
    
    # Reset other game state
    num = None
    ai_turn = None
    minimax_chosen = None
    game_screen = False
    game_over = False
    history = []
    current_bank = 0
    current_score = 0
    tree = None
    show_rules = False
    ai_total_time = 0
    ai_moves_count = 0
    last_ai_time = 0
    total_nodes_evaluated = 0

    # Reset button states
    for button in algo_buttons + seq_buttons:
        button.highlighted = False
    for button in div_buttons:
        button.disabled = False
    
    restart_button.disabled = True

def print_ai_stats():
    print("\nAI Performance Statistics:")
    print(f"Total moves: {ai_moves_count}")
    print(f"Total time: {ai_total_time:.20f} seconds")
    print(f"Total nodes evaluated: {total_nodes_evaluated}")
    if ai_moves_count > 0:
        print(f"Average time per move: {ai_total_time/ai_moves_count:.20f} seconds")
        
def ai_move():
    """Perform AI move based on current game tree"""
    global num, ai_turn, current_bank, current_score, game_over, tree
    global ai_total_time, ai_moves_count, last_ai_time
    # First check if game is already over
    if check_game_over():
        game_over = True
        history.append(f"Final score: {current_score}")
        restart_button.disabled = False
        print_ai_stats()
    start_time=time.perf_counter()

    if tree.root and tree.root.children:
        # Find the child with highest heuristic value
        best_child = max(tree.root.children, key=lambda child: child.heuristic_value)
        
        # Calculate the divisor used
        divisor = num // best_child.value
        
        # Update game state from the node's values
        num = best_child.value
        current_bank = best_child.bank
        current_score = best_child.score
        tree.root = best_child
        
        end_time = time.perf_counter()
        last_ai_time = end_time - start_time
        ai_total_time += last_ai_time
        ai_moves_count += 1

        # Print move info to console
        print(f"\nAI move #{ai_moves_count}:")
        print(f"  Calculation time: {last_ai_time:.20f} seconds")
        print(f"  Move: {tree.root.parent.value}/{divisor} = {num}")
        print(f"  Score change: {current_score-tree.root.parent.score:+d}")
        print(f"  Bank change: {current_bank-tree.root.parent.bank:+d}")

        # Format history entry
        history.append(f"AI: {tree.root.parent.value}/{divisor} = {num} (p:{current_score-tree.root.parent.score:+d}, b:{current_bank-tree.root.parent.bank:+d})")
        update_divisors(num)
        
        # Check if game ended
        game_over = check_game_over()
        if game_over:
            history.append(f"Final score: {current_score}")
            restart_button.disabled = False
            # Print final stats
            print("\nFinal AI Performance Statistics:")
            print(f"Total moves: {ai_moves_count}")
            print(f"Total time: {ai_total_time:.20f} seconds")
            print(f"Total nodes evaluated: {total_nodes_evaluated}")
            if ai_moves_count > 0:
                print(f"Average time per move: {ai_total_time/ai_moves_count:.20f} seconds")

        ai_turn = False  # Switch to player turn
    else:
        # No valid moves left
        game_over = True
        winner = "AI" if current_score % 2 == 0 else "Player"
        history.append(f"Final score: {current_score}")
        restart_button.disabled = False
        print("\nFinal AI Performance Statistics:")
        print(f"Total moves: {ai_moves_count}")
        print(f"Total time: {ai_total_time:.20f} seconds")
        if ai_moves_count > 0:
            print(f"Average time per move: {ai_total_time/ai_moves_count:.20f} seconds")

def draw_rules_window():
    """Draw the rules window overlay"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw rules window
    rules_rect = pygame.Rect(150, 100, WIDTH-300, HEIGHT-200)
    pygame.draw.rect(screen, RULES_BG_COLOR, rules_rect)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rules_rect, 3)
    
    # Draw rules text with centered title and bullet points
    y_offset = 120
    for i, line in enumerate(rules_text):
        if line:  # Skip empty lines
            text = RULES_FONT.render(line, True, WHITE)
            if i == 0:  # Center only the title
                screen.blit(text, text.get_rect(center=(WIDTH//2, 150)))
            else:
                screen.blit(text, (170, y_offset))  # Left-align bullet points
        y_offset += 30 if i != 0 else 40  # Extra space after title
    
    # Draw close button with hover effect
    mouse_pos = pygame.mouse.get_pos()
    close_button = Button("Close", WIDTH//2-100, HEIGHT-120, 200, 50)
    close_button.hovered = close_button.rect.collidepoint(mouse_pos)
    close_button.draw(screen)
    
    return close_button

# Main game loop
run = True
while run:
    screen.fill(BACKGROUND_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    # Update button hover states
    all_buttons = num_buttons + algo_buttons + seq_buttons + div_buttons + [start_button, restart_button, rules_button]
    for button in all_buttons:
        button.hovered = button.rect.collidepoint(mouse_pos) and not button.disabled

    if not game_screen and not show_rules:
        # Draw selection screen UI
        screen.blit(text_boxes[0], text_boxes[0].get_rect(center=(540, 80)))
        screen.blit(text_boxes[1], text_boxes[1].get_rect(center=(540, 230)))
        screen.blit(text_boxes[2], text_boxes[2].get_rect(center=(540, 380)))

        for button in num_buttons + algo_buttons + seq_buttons:
            button.draw(screen)
        start_button.draw(screen)
        rules_button.draw(screen)

    elif game_screen and not show_rules:
        # Draw game UI
        screen.blit(text_boxes[3], text_boxes[3].get_rect(center=(540, 50)))
        current_num_text = FONT.render(f"{num}", True, WHITE)
        screen.blit(current_num_text, current_num_text.get_rect(center=(540, 80)))
        
        # Display bank and score
        screen.blit(text_boxes[5], (50, 120))
        bank_text = FONT.render(f"{current_bank}", True, WHITE)
        screen.blit(bank_text, (150, 120))
        
        screen.blit(text_boxes[6], (50, 150))
        score_text = FONT.render(f"{current_score}", True, WHITE)
        screen.blit(score_text, (150, 150))
        
        # Display game history (moved slightly left)
        screen.blit(text_boxes[7], (730, 120))  # Adjusted from 750 to 730
        for i, entry in enumerate(history[-10:]):  # Show last 10 entries
            history_text = SMALL_FONT.render(entry, True, WHITE)
            screen.blit(history_text, (730, 150 + i * 25))
        
        if not game_over:
            if not ai_turn:
                screen.blit(text_boxes[4], text_boxes[4].get_rect(center=(540, 230)))
                for button in div_buttons:
                    button.draw(screen)
        
        restart_button.draw(screen)
        rules_button.draw(screen)
        
        # Display game over message if applicable
        if game_over:
            winner = "AI" if current_score % 2 == 0 else "Player"
            game_over_text1 = FONT.render("Game Over!", True, HIGHLIGHT_COLOR)
            game_over_text2 = FONT.render(f"{winner} wins!", True, HIGHLIGHT_COLOR)
            screen.blit(game_over_text1, game_over_text1.get_rect(center=(540, 300)))
            screen.blit(game_over_text2, game_over_text2.get_rect(center=(540, 340)))

    # Draw rules window if active
    if show_rules:
        close_button = draw_rules_window()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            if show_rules:
                # Check if close button was clicked
                if close_button.rect.collidepoint(mouse_pos):
                    show_rules = False
                continue
            
            if not game_screen:
                # Rules button
                if rules_button.rect.collidepoint(mouse_pos):
                    show_rules = True
                
                # Number selection
                for button in num_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.toggle_selection(num_buttons)
                        num = int(button.text)
                
                # Algorithm selection
                for button in algo_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.toggle_selection(algo_buttons)
                        minimax_chosen = button.text == "Minimax"
                
                # Sequence selection
                for button in seq_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.toggle_selection(seq_buttons)
                        ai_turn = button.text == "AI"
                
                # Start Game
                if start_button.rect.collidepoint(mouse_pos) and num is not None and minimax_chosen is not None and ai_turn is not None:
                    game_screen = True
                    history.append(f"Starting number: {num}")
                    
                    # Initialize game tree with current values
                    tree_start_time = time.perf_counter()
                    tree = Tree()
                    tree.generate_tree(num)
                    tree.calculate_heuristic(tree.root, ai_turn, minimax_chosen)
                    tree_end_time = time.perf_counter()
                    tree_elapsed_time = (tree_end_time - tree_start_time) * 1000
                    print(f"\nTree generation time: {tree_elapsed_time:.20f} ms")
                    
                    # Set initial bank and score from root node
                    current_bank = tree.root.bank
                    current_score = tree.root.score
                    
                    update_divisors(num)
                    
                    # Check if starting number is already game over
                    if check_game_over():
                        game_over = True
                        winner = "AI" if current_score % 2 == 0 else "Player"
                        history.append(f"Final score: {current_score}")
                        restart_button.disabled = False
                    # AI goes first if selected
                    elif ai_turn:
                        ai_move()
            
            elif game_screen:
                # Rules button
                if rules_button.rect.collidepoint(mouse_pos):
                    show_rules = True
                
                # Restart button
                if restart_button.rect.collidepoint(mouse_pos) and not restart_button.disabled:
                    reset_game()
                
                # Player move
                elif not game_over and not ai_turn:
                    for button in div_buttons:
                        if button.rect.collidepoint(mouse_pos) and not button.disabled:
                            divisor = int(button.text)
                            new_num = num // divisor
                            
                            # Find the corresponding child node
                            for child in tree.root.children:
                                if child.value == new_num:
                                    # Store previous values for calculation
                                    prev_score = current_score
                                    prev_bank = current_bank
                                    
                                    tree.root = child
                                    num = new_num
                                    current_bank = child.bank
                                    current_score = child.score
                                    
                                    # Format history entry
                                    history.append(f"Player: {tree.root.parent.value}/{divisor} = {num} (p:{current_score-prev_score:+d}, b:{current_bank-prev_bank:+d})")
                                    update_divisors(num)
                                    
                                    # Check if game ended
                                    game_over = check_game_over()
                                    if game_over:
                                        history.append(f"Final score: {current_score}")
                                        restart_button.disabled = False
                                        print_ai_stats()

                                    ai_turn = True  # Switch to AI turn
                                    break
    
    # AI move if it's their turn
    if game_screen and not game_over and ai_turn and not show_rules:
        ai_move()
    
    pygame.display.update()

pygame.quit()