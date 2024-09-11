from epaper_telegram.models.img_creators import DrawTool
from epaper_telegram.models.display import Displayer


def draw_tool():
    with Displayer() as displayer:
        drawtool = DrawTool(displayer)
        drawtool.clear_img()


if __name__ == "__main__":
    draw_tool()
