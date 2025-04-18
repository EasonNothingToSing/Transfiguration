import pytest
import ast
import sys
sys.path.append(r'E:\APP\python_project\Transfiguration\Transfiguration')
from Transpell.expression_transformer import ExpressionTransformer


# 夹具：创建 ExpressionTransformer 实例
@pytest.fixture
def transformer(tmp_path):
    transformer = ExpressionTransformer(database=str(tmp_path))
    return transformer


def test_data_extend_single_data(transformer):
    """测试单一数据输入"""
    data = [[1, 10], [2, 20], [3, 30]]
    result = transformer.DataExtend(data)
    expected = data
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_multiple_data(transformer):
    """测试多个等长数据合并"""
    data1 = [[1, 10], [2, 20], [3, 30]]
    data2 = [[100, 200], [300, 400], [500, 600]]
    result = transformer.DataExtend(data1, data2)
    expected = [[1, 10, 100, 200], [2, 20, 300, 400], [3, 30, 500, 600]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_three_data(transformer):
    """测试三个等长数据合并"""
    data1 = [[1], [2], [3]]
    data2 = [[10], [20], [30]]
    data3 = [[100], [200], [300]]
    result = transformer.DataExtend(data1, data2, data3)
    expected = [[1, 10, 100], [2, 20, 200], [3, 30, 300]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_empty_lists(transformer):
    """测试空列表输入（非空参数）"""
    data1 = []
    data2 = []
    result = transformer.DataExtend(data1, data2)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_single_element(transformer):
    """测试单一元素数据"""
    data1 = [[1]]
    data2 = [[10]]
    result = transformer.DataExtend(data1, data2)
    expected = [[1, 10]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_no_data(transformer):
    """测试没有输入数据"""
    with pytest.raises(ValueError, match="No data provided"):
        transformer.DataExtend()


def test_data_extend_length_mismatch(transformer):
    """测试数据长度不一致"""
    data1 = [[1, 10], [2, 20]]
    data2 = [[100, 200], [300, 400], [500, 600]]
    with pytest.raises(ValueError, match="Data length mismatch: 3 != 2"):
        transformer.DataExtend(data1, data2)


def test_data_extend_mixed_types(transformer):
    """测试混合类型数据"""
    data1 = [[1, "a"], [2, "b"]]
    data2 = [[True, 10.0], [False, 20.0]]
    result = transformer.DataExtend(data1, data2)
    expected = [[1, "a", True, 10.0], [2, "b", False, 20.0]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_data_extend_with_ast(transformer):
    """测试通过 AST 调用 DataExtend"""
    # 模拟 AST 调用
    node = ast.Call(
        func=ast.Name(id="DataExtend", ctx=ast.Load()),
        args=[
            ast.Constant(value=[[1, 10], [2, 20]]),
            ast.Constant(value=[[100, 200], [300, 400]])
        ],
        keywords=[]
    )
    result_node = transformer.visit_Call(node)
    result = result_node.value
    expected = [[1, 10, 100, 200], [2, 20, 300, 400]]
    assert result == expected, f"Expected {expected}, but got {result}"