import matplotlib.pyplot as plt 

RHO_COPPER = 1.68e-8



def coil_geometry(board_width, board_height, turns, trace_width, spacing, edge_margin):
    pitch = trace_width + spacing

    
    outer_width = board_width - 2*edge_margin - trace_width
    outer_height = board_height - 2*edge_margin - trace_width

    inner_width = outer_width - 2 * (turns - 1) * pitch
    inner_height = outer_height - 2 * (turns - 1) * pitch

    if inner_width <= 0 or inner_height < 0:
        return None

    total_length = 2 * turns * (outer_width + outer_height) - 4 * pitch * turns * (turns - 1)

    area_sum = turns * outer_width * outer_height - pitch * (outer_width + outer_height) * turns * (turns - 1) + (2/3) * pitch**2 * turns * (turns - 1) * (2 * turns - 1)

    return total_length, area_sum

def simulate_coil(board_width, board_height, turns, trace_width, spacing, copper_thickness, edge_margin, drive_voltage, current_limit, magnetic_field, layers=1):
    geometry = coil_geometry(board_width, board_height, turns, trace_width, spacing, edge_margin)
    if geometry is None:
        return None

    length_per_layer, area_sum_per_layer = geometry

    total_length = layers * length_per_layer
    total_area = layers * area_sum_per_layer

    copper_area = trace_width * copper_thickness
    resistance = RHO_COPPER * total_length / copper_area

    current = min(current_limit, drive_voltage / resistance)
    power = current**2 * resistance
    magnetic_moment = current * total_area
    max_torque = magnetic_moment * magnetic_field
    current_density = current / copper_area

    return {
        "turns": turns,
        "length": total_length,
        "resistance": resistance,
        "current": current,
        "power": power,
        "magnetic_moment": magnetic_moment,
        "max_torque": max_torque,
        "current_density": current_density
    }


def find_max_turns(board_width, board_height, trace_width, spacing, edge_margin):
    pitch = trace_width + spacing
    outer_width = board_width - 2*edge_margin - trace_width
    outer_height = board_height - 2*edge_margin - trace_width

    smaller_dimension = min(outer_width, outer_height)

    max_turns = int(smaller_dimension // (2*pitch)) + 1

    return max_turns



faces = {
    "10x20": (.10, .20),
    "10x30": (.10, .30),
    "20x30": (.20, .30)
}

#test values
trace_width = 0.5e-3
spacing = 0.25e-3
copper_thickness = 35e-6
edge_margin = 5e-3
drive_voltage = 5.0
current_limit = 0.25
magnetic_field = 40e-6
layers = 1

all_results = {}

for face_name, dimensions in faces.items():
    board_width = dimensions[0]
    board_height = dimensions[1]

    max_turns = find_max_turns(board_width, board_height, trace_width, spacing, edge_margin)

    results = []

    for turns in range(1, max_turns + 1):
        result = simulate_coil(board_width, board_height, turns, trace_width, spacing, copper_thickness, edge_margin, drive_voltage, current_limit, magnetic_field, layers)
        results.append(result)
    
    all_results[face_name] = results

    print(face_name)
    print("Max number of turns: ", max_turns)
    print()





fig, axes = plt.subplots(3, 2, figsize=(12,12))

ax_moment = axes[0,0]
ax_current = axes[0,1]
ax_power = axes[1,0]
ax_resistance = axes[1,1]
ax_torque = axes[2,0]

axes[2,1].axis("off")

for face_name, results in all_results.items():
    turns = []
    moments = []
    currents = []
    powers = []
    resistances = []
    torques = []

    for result in results:
        turns.append(result["turns"])
        moments.append(result["magnetic_moment"])
        currents.append(result["current"])
        powers.append(result["power"])
        resistances.append(result["resistance"])
        torques.append(result["max_torque"])

    ax_moment.plot(turns, moments, label=face_name)
    ax_current.plot(turns, currents, label=face_name)
    ax_power.plot(turns, powers, label=face_name)
    ax_resistance.plot(turns, resistances, label=face_name)
    ax_torque.plot(turns, torques, label=face_name)

ax_moment.axhline(0.2, linestyle="--")
ax_moment.axhline(0.3, linestyle="--")
ax_moment.axhline(0.5, linestyle="--")

ax_moment.set_xlabel("Number of turns")
ax_moment.set_ylabel("Magnetic Moment (A m^2)")
ax_moment.set_title("Turns vs PCB Magnetic Moment")
ax_moment.grid()
ax_moment.legend()

ax_current.set_xlabel("Number of turns")
ax_current.set_ylabel("Current (A)")
ax_current.set_title("Turns vs Current")
ax_current.grid()
ax_current.legend()

ax_power.set_xlabel("Number of turns")
ax_power.set_ylabel("Power (W)")
ax_power.set_title("Turns vs Power")
ax_power.grid()
ax_power.legend()

ax_resistance.set_xlabel("Number of turns")
ax_resistance.set_ylabel("Resistance (Ohms)")
ax_resistance.set_title("Turns vs Resistance")
ax_resistance.grid()
ax_resistance.legend()

ax_torque.set_xlabel("Number of turns")
ax_torque.set_ylabel("Torque Max (N m)")
ax_torque.set_title("Turns vs Max Torque (B = 40 uT)")
ax_torque.grid()
ax_torque.legend()


plt.tight_layout()
plt.savefig("magnetorquer_test.png", dpi=300, bbox_inches="tight")
plt.show()

# plt.figure()

# for face_name, results in all_results.items():
#     turns = []
#     moments = []

#     for result in results:
#         turns.append(result["turns"])
#         moments.append(result["magnetic_moment"])
    
#     plt.plot(turns, moments, label=face_name)
# plt.axhline(0.2, linestyle="--")
# plt.axhline(0.3, linestyle="--")
# plt.axhline(0.5, linestyle="--")

# plt.xlabel("Number of turns")
# plt.ylabel("Magnetic Moment (Am^2)")
# plt.title("Turns vs PCB Magnetic Moment")
# plt.grid()
# plt.legend()

# plt.show()

# plt.figure()

# for face_name, results in all_results.items():
#     turns = []
#     currents = []

#     for result in results:
#         turns.append(result["turns"])
#         currents.append(result["current"])
    
#     plt.plot(turns, currents, label=face_name)

# plt.xlabel("Number of turns")
# plt.ylabel("Current (A)")
# plt.title("Turns vs Current")
# plt.grid()
# plt.legend()

# plt.show()

# plt.figure()

# for face_name, results in all_results.items():
#     turns = []
#     powers = []

#     for result in results:
#         turns.append(result["turns"])
#         powers.append(result["power"])
    
#     plt.plot(turns, powers, label=face_name)

# plt.xlabel("Number of turns")
# plt.ylabel("Power (W)")
# plt.title("Turns vs Power")
# plt.grid()
# plt.legend()

# plt.show()


# plt.figure()

# for face_name, results in all_results.items():
#     turns = []
#     resistances = []

#     for result in results:
#         turns.append(result["turns"])
#         resistances.append(result["resistance"])
    
#     plt.plot(turns, resistances, label=face_name)

# plt.xlabel("Number of turns")
# plt.ylabel("Resistance (Ohms))")
# plt.title("Turns vs Resistance")
# plt.grid()
# plt.legend()

# plt.show()


# plt.figure()

# for face_name, results in all_results.items():
#     turns = []
#     torques = []

#     for result in results:
#         turns.append(result["turns"])
#         torques.append(result["torque"])
    
#     plt.plot(turns, torques, label=face_name)

# plt.xlabel("Number of turns")
# plt.ylabel("Torque Max (uNm)")
# plt.title("Turns vs MaxTorque (B = 40 uT)")
# plt.grid()
# plt.legend()

# plt.show()