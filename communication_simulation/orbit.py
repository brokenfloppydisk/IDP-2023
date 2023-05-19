import matplotlib.pyplot as plt
from matplotlib import animation

# Constants
G = 6.67e-11 # Gravity (m^3/(kg*s^2))
C = 299_792_458 # Speed of Light (m/s)
AU = 1.5e11 # Astronomical Unit (m)
DaySeconds = 24*60*60 # 1 day in seconds

# Globals
t: float = 0
# 1 day (in seconds)
dt: float = DaySeconds
# Simulate 5 years
t_end = 5 * 365 * DaySeconds

fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()

def sign(num: float) -> int:
    if num == 0:
        return 0
    elif num > 1:
        return 1
    else:
        return -1

class Body:
    # List of all celestial bodies
    BodyList: list['Body'] = []

    def __init__(self, name: str, mass: float,
                x0: float=0, y0: float=0,
                vx0: float=0, vy0: float=0,
                color: str="blue", linewidth: float=1, 
                markersize: float=4) -> 'Body':
        self.name = name
        self.mass: float = mass

        self.x: float = x0
        self.y: float = y0

        self.xpositions: list[float] = [x0]
        self.ypositions: list[float] = [y0]

        self.vx: float = vx0
        self.vy: float = vy0

        self.line, = ax.plot([], [], lw=linewidth, c=color)

        self.point, = ax.plot([x0], [y0], marker="o", markersize=markersize, markeredgecolor=color, markerfacecolor=color)
        self.text: plt.text = ax.text(x0, y0, name)

        # Add to the list of celestial bodies
        Body.BodyList.append(self)

        # Gravity constants compared to all of the other bodies
        self.gravityDict: dict(str, float) = {}

    def update_pos(self) -> None:
        """
        Update the position and velocity of the body.
        
        F = G(m_1)(m_2)/d^2
        https://towardsdatascience.com/simulate-a-tiny-solar-system-with-python-fbbb68d8207b
        """
        for body in Body.BodyList:
            if (self == body):
                continue
            
            if (body.name not in self.gravityDict):
                self.gravityDict[body.name] = G * body.mass * self.mass 
            
            gravity_constant = self.gravityDict[body.name]

            x_dist = self.x - body.x
            y_dist = self.y - body.y

            # |sqrt(x^2 + y^2)|^3 = (x^2 + y^2)^1.5
            r3: float = ((x_dist)**2 + (y_dist)**2)**1.5

            fx = -gravity_constant*x_dist/r3
            fy = -gravity_constant*y_dist/r3

            self.vx += fx * dt / self.mass
            self.vy += fy * dt / self.mass
            
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.xpositions.append(self.x)
        self.ypositions.append(self.y)
        pass

    def __eq__(self, other):
        if (isinstance(other, Body)):
            return self.name == other.name
        return False


def simulate():
    global t
    # 5 years of time (in seconds)
    while t < 5 * 365 * DaySeconds:
        for body in Body.BodyList:
            body.update_pos()
        t += dt

# Runner code

sun = Body("The Sun", 2.0e30, 0, 0, 0, 0, "yellow", 1, 7)
earth = Body("Earth", 5.972e24, 1.0167*AU, 0, 0, 29290, "blue", 1, 4)
mars = Body("Mars", 6.39e23, 1.666*AU, 0, 0, 21970, "red", 1, 4)

earth_mars_distance, = plt.plot([], [], linestyle="--")
earth_mars_text = plt.text(0, 0, f"Distance: {0:.2f} AU")

def get_mars_distance(i):
    return ((mars.xpositions[i] - earth.xpositions[i])**2 + (mars.ypositions[i] - earth.ypositions[i])**2)**0.5


def update_animation(i):
    output_list = []

    earth_x = earth.xpositions[i]
    earth_y = earth.ypositions[i]
    mars_x = mars.xpositions[i]
    mars_y = mars.ypositions[i]

    earth_mars_distance.set_data([earth_x, mars_x], [earth_y, mars_y])
    output_list.append(earth_mars_distance)

    earth_mars_text_x = (2*earth_x + mars_x)/3
    earth_mars_text_y = (2*earth_y + mars_y)/3

    distance = get_mars_distance(i)

    earth_mars_text.set_text(
        f"Distance:{(distance / AU):.2f} AU\nTime to transmit:{((distance / C)/60):.0f} minutes")

    earth_mars_text.set_position((earth_mars_text_x, earth_mars_text_y))

    output_list.append(earth_mars_text)

    for body in Body.BodyList:
        body.line.set_data(body.xpositions[0:i], body.ypositions[0:i])
        body.point.set_data(body.xpositions[i], body.ypositions[i])
        body.text.set_position((body.xpositions[i], body.ypositions[i]))

        output_list.append(body.line)
        output_list.append(body.point)
        output_list.append(body.text)

    ax.axis('equal')
    ax.set_xlim(-3 * AU, 3 * AU)
    ax.set_ylim(-3 * AU, 3 * AU)

    return tuple(output_list)


simulate()

anim = animation.FuncAnimation(
    fig,
    func=update_animation,
    frames=int(t_end / dt),
    interval=1,
    blit=True
)

plt.show()