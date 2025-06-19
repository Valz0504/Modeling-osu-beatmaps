import math
import networkx as nx
import matplotlib.pyplot as plt

# parse hit objects
def parse_hit_objects(osu_file_path):
    hit_objects = []
    parsing = False
    with open(osu_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[HitObjects]"):
                parsing = True
                continue
            if parsing:
                if line == "" or line.startswith("["):
                    break
                parts = line.split(",")
                if len(parts) >= 5:
                    x = int(parts[0])
                    y = int(parts[1])
                    time = int(parts[2])
                    type_flag = int(parts[3])
                    
                    if type_flag & 1:
                        obj_type = "circle"
                    elif type_flag & 2:
                        obj_type = "slider"
                    elif type_flag & 8:
                        obj_type = "spinner"
                    else:
                        obj_type = "other"

                    hit_objects.append({
                        "x": x,
                        "y": y,
                        "time": time,
                        "type": obj_type
                    })
    return hit_objects

# weight formula
def calculate_difficulty(obj0, obj1, obj2, burst_bonus=100):
    dx = obj2["x"] - obj1["x"]
    dy = obj2["y"] - obj1["y"]
    spatial_dist = math.sqrt(dx**2 + dy**2)

    prev_dx = obj1["x"] - obj0["x"]
    prev_dy = obj1["y"] - obj0["y"]
    prev_dist = math.sqrt(prev_dx**2 + prev_dy**2)
    delta_spatial = abs(spatial_dist - prev_dist)

    delta_time = abs(obj2["time"] - obj1["time"])
    if delta_time == 0:
        delta_time = 1

    scale_factor = 5
    stream_factor = 1
    if (delta_time <= 100 and delta_spatial <= 1.5):
        stream_factor = 3
        scale_factor = 6
    if spatial_dist == 0:
        return (burst_bonus / delta_time)*(scale_factor*stream_factor)
    else:
        return (spatial_dist / delta_time)*(scale_factor*stream_factor)

# construct the graph
def build_graph(hit_objects):
    G = nx.DiGraph()
    for i, obj in enumerate(hit_objects):
        G.add_node(i, **obj)
    for i in range(len(hit_objects) - 1):
        obj0 = hit_objects[i - 1]
        obj1 = hit_objects[i]
        obj2 = hit_objects[i + 1]
        w = calculate_difficulty(obj0, obj1, obj2)
        print(f"Edge from {i} to {i+1}, weight = {w:.2f}")
        G.add_edge(i, i + 1, weight=w)
    return G

# visualization
def visualize_graph(G):
    pos = {node: (G.nodes[node]['x'], -G.nodes[node]['y']) for node in G.nodes}

    node_colors = []
    for n in G.nodes:
        obj_type = G.nodes[n]['type']
        if obj_type == "circle":
            node_colors.append("blue")
        elif obj_type == "slider":
            node_colors.append("green")
        else:
            node_colors.append("gray")

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=300,
            font_size=8, edge_color='gray', arrows=True)

    # edge weight
    for u, v, data in G.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        label_x = (x1 + x2) / 2
        label_y = (y1 + y2) / 2
        weight = data['weight']
        plt.text(label_x, label_y, f"{weight:.1f}", fontsize=6, color='red', ha='center', va='center')

    plt.show()

# estimate difficulty
def average_weight(G):
    if len(G.edges) == 0 or len(G.nodes) == 0:
        return 0.0
    total_weight = sum(data['weight'] for _, _, data in G.edges(data=True))
    avg_weight = total_weight / len(G.nodes)
    avg = avg_weight
    return avg

# driver
if __name__ == "__main__":

    # this path is adjustable
    osu_file = "beatmaps/TRUE - Soundscape (SkyFlame) [Easy].osu"
    
    hit_objects = parse_hit_objects(osu_file)
    print(f"Parsed {len(hit_objects)} hit objects.")

    G = build_graph(hit_objects)
    print(f"Graph: {len(G.nodes)} nodes, {len(G.edges)} edges.")

    average = average_weight(G)
    print(f"Average weight: {average:.2f}")

    if (average < 3):
        print("This map is Easyyyy!")
    elif (average >= 3 and average < 5):
        print("This map is quite challenging")
    elif (average >= 5 and average < 6.5):
        print("This map is medium well")
    else:
        print("This map is hard, you are cooked bro")

    visualize_graph(G)
