import pcbnew
import os




# mm

trace_width = 0.5
spacing = 0.25
edge_margin = 0.5

via_diameter = 1.0
via_drill = 0.5

output_folder = r"C:\Users\bobwo\Documents\KiCad\magnetorquer_boards"

board_specs = [
    ("MTQ_10x20", 100.0, 200.0, 51),
    ("MTQ_10x30", 100.0, 300.0, 31),
    ("MTQ_10x20", 100.0, 200.0, 24),
]

def point(x,y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))

def add_track(board, x1, y1, x2, y2, layer):
    track = pcbnew.PCB_TRACK(board)

    track.SetStart(point(x1,y1))
    track.SetEnd(point(x2,y2))
    track.SetWidth(pcbnew.FromMM(trace_width))
    track.SetLayer(layer)

    board.Add(track)

def add_via(board, x, y):
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(point(x,y))
    via.SetWidth(pcbnew.FromMM(via_diameter))
    via.SetDrill(pcbnew.FromMM(via_drill))
    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)

    board.Add(via)

def add_outline(board, board_width, board_height):
    corners = [(0.0,0.0), (board_width, 0.0), (board_width, board_height), (0.0, board_height), (0.0,0.0)]

    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[i+1]

        edge = pcbnew.PCB_SHAPE(board)
        edge.SetShape(pcbnew.S_SEGMENT)
        edge.SetStart(point(x1,y1))
        edge.SetEnd(point(x2,y2))
        edge.SetLayer(pcbnew.Edge_Cuts)
        edge.SetWidth(pcbnew.FromMM(0.05))

        board.Add(edge)

def make_spiral(board, board_width, board_height, turns):
    pitch = trace_width + spacing

    left = edge_margin + trace_width / 2
    right = board_width - edge_margin - trace_width / 2

    top = edge_margin + trace_width / 2
    bottom = board_height - edge_margin - trace_width / 2

    terminal_1_x = 2.5
    terminal_1_y = top

    add_track(board, terminal_1_x, terminal_1_y, left, top, pcbnew.F_Cu)

    x = left
    y = top

    for turn in range(turns):
        add_track(board, x, y, right, top, pcbnew.F_Cu)

        x = right
        y = top

        add_track(board, x, y, right, bottom, pcbnew.F_Cu)

        x = right
        y = bottom

        add_track(board, x, y, left, bottom, pcbnew.F_Cu)

        x = left
        y = bottom
        new_top = top + pitch

        add_track(board, x, y, left, new_top, pcbnew.F_Cu)

        x = left
        y = new_top
        new_left = left + pitch
        
        add_track(board, x, y, new_left, new_top, pcbnew.F_Cu)

        x = new_left
        y = new_top

        left = left + pitch
        right = right - pitch
        top = top + pitch
        bottom = bottom - pitch

    add_via(board, x, y)

    terminal_2_x = 2.5
    terminal_2_y = terminal_1_y + 2.0

    add_via(board, terminal_2_x, terminal_2_y)

    add_track(board, x, y, terminal_2_x, terminal_2_y, pcbnew.B_Cu)




def generate_board(name, board_width, board_height, turns):
    board = pcbnew.GetBoard()

    add_outline(board, board_width, board_height)
    make_spiral(board, board_width, board_height, turns)

    file_name = os.path.join(output_folder, name + ".kicad_pcb")
    pcbnew.SaveBoard(file_name, board)
    print(name, " created with ", turns, " turns")


os.makedirs(output_folder, exist_ok = True)

# for spec in board_specs:
#     name = spec[0]
#     width = spec[1]
#     height = spec[2]
#     turns = spec[3]

#     generate_board(name, width, height, turns)

def generate_board(board_width, board_height, turns):

    board = pcbnew.GetBoard()

    if board is None:
        print("No board is currently open.")
        return

    add_outline(board, board_width, board_height)

    make_spiral(board, board_width, board_height, turns)

    pcbnew.Refresh()

generate_board(
    100.0,
    200.0,
    24
)