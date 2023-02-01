import io
import unittest

import plugin


class TestPlugin(unittest.TestCase):
    def test_print_menu_item(self) -> None:
        with io.StringIO() as buf:
            plugin.print_menu_item("test", out=buf, color="red", font="Arial", size=14)
            self.assertEqual(buf.getvalue(), "test | color=red font=Arial size=14\n")

    def test_print_menu_action(self) -> None:
        with io.StringIO() as buf:
            plugin.print_menu_action("test", ["ps", "aux"], out=buf)
            self.assertEqual(buf.getvalue(), "test | shell=ps param0=aux terminal=False\n")

    def test_print_menu_separator(self) -> None:
        with io.StringIO() as buf:
            plugin.print_menu_separator(out=buf)
            self.assertEqual(buf.getvalue(), "---\n")


if __name__ == "__main__":
    unittest.main()
