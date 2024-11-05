import matplotlib.animation as animation

from functions import *

if __name__ == "__main__":
    # Создание анимации
    ani = animation.FuncAnimation(fig, animate, frames=frames, interval=50)

    plt.show()
