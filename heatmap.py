import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------- MIDPOINT CIRCLE ALGORITHM --------
def midpoint_circle(r):
    x, y, p = 0, r, 1 - r
    points = set()
    while x <= y:
        points.update([
            ( x,  y), ( y,  x), (-x,  y), (-y,  x),
            (-x, -y), (-y, -x), ( x, -y), ( y, -x)
        ])
        if p < 0:
            p = p + 2*x + 1
        else:
            p = p + 2*x - 2*y + 1
            y -= 1
        x += 1
    return list(points)

# -------- SCALING TRANSFORMATION --------
def scale(points, s):
    return [(x*s, y*s) for x, y in points]

# -------- USER INPUT --------
r = int(input("Enter base radius: "))
max_scale = float(input("Enter max scale: "))
step = float(input("Enter scale step: "))

base_circle = midpoint_circle(r)

# -------- PLOTTING SETUP --------
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal") # Ensures the circle stays round

limit = r * max_scale + 10
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# The Expanding Ring
scatter = ax.scatter([], [], s=10) 

# The Heat Source (Changed to a dot)
ax.scatter(0, 0, color="black", s=30, marker='.') 
ax.text(2, 2, "HEAT SOURCE", fontsize=9, fontweight='bold') # Label near center

# Status Label (Top Left)
label_text = ax.text(-limit + 5, limit - 10, "", fontsize=12, fontweight='bold')

ax.set_title("Circular Heat Map using Midpoint Circle Drawing Algorithm ")

# -------- ANIMATION LOGIC --------
scales = [1.0 + i*step for i in range(int((max_scale-1)/step) + 1)]

def update(frame):
    s = scales[frame]
    scaled_pts = scale(base_circle, s)
    
    x_vals = [p[0] for p in scaled_pts]
    y_vals = [p[1] for p in scaled_pts]

    # Update ring positions
    scatter.set_offsets(list(zip(x_vals, y_vals)))
    
    # Keeping the circle solid: increase point size as scale grows
    scatter.set_sizes([s * 5 for _ in range(len(x_vals))])
    
    # Heat color logic
    if s < (1 + max_scale) / 3:
        color, label = "red", "HIGH HEAT"
    elif s < 2 * (1 + max_scale) / 3:
        color, label = "orange", "MEDIUM HEAT"
    else:
        color, label = "yellow", "LOW HEAT"

    scatter.set_color(color)
    label_text.set_text(label)
    label_text.set_color(color)

    return scatter, label_text

ani = animation.FuncAnimation(fig, update, frames=len(scales), interval=50, blit=True)

plt.show()