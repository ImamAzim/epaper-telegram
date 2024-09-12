import logging


from epaper_telegram.models.img_creators import DrawTool
from epaper_telegram.models.display import Displayer


def draw_tool():
    logging.basicConfig(level=logging.INFO)
    with Displayer(mock_mode=True) as displayer:
        with DrawTool(displayer) as draw_tool:
            input()
            draw_tool.point_to(60, 30)
            input()


if __name__ == "__main__":
    draw_tool()
