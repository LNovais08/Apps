import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agenda import _gerar_dias_do_mes


def test_gerar_dias_do_mes_inclui_todos_os_dias_do_mes():
    dias = _gerar_dias_do_mes(2026, 7)

    assert len(dias) == 42
    assert dias[0]["is_current_month"] is False
    assert dias[1]["is_current_month"] is False
    assert any(item["day"] == 1 and item["is_current_month"] for item in dias)
    assert any(item["day"] == 31 and item["is_current_month"] for item in dias)
