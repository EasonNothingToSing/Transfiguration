import pytest
import ast
import sys
sys.path.append(r'E:\APP\python_project\Transfiguration\Transfiguration')
from Transpell.expression_transformer import ExpressionTransformer


# Fixture: Create ExpressionTransformer instance
@pytest.fixture
def transformer(tmp_path):
    transformer = ExpressionTransformer(database=str(tmp_path))
    return transformer


def test_list2dict_basic(transformer):
    """Test basic conversion of list of lists to list of dictionaries"""
    data = [[1, 10], [2, 20], [3, 30]]
    keys = ["key1", "key2"]
    result = transformer.List2Dict(data, keys)
    expected = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 20},
        {"key1": 3, "key2": 30}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_list2dict_single_sublist(transformer):
    """Test single sublist input"""
    data = [[1, 10]]
    keys = ["key1", "key2"]
    result = transformer.List2Dict(data, keys)
    expected = [{"key1": 1, "key2": 10}]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_list2dict_empty_data(transformer):
    """Test empty data input"""
    data = []
    keys = ["key1", "key2"]
    result = transformer.List2Dict(data, keys)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_list2dict_single_element_sublist(transformer):
    """Test single-element sublists"""
    data = [[1], [2], [3]]
    keys = ["key1"]
    result = transformer.List2Dict(data, keys)
    expected = [{"key1": 1}, {"key1": 2}, {"key1": 3}]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_list2dict_mixed_types(transformer):
    """Test mixed type data"""
    data = [[1, "a", True], [2, "b", False]]
    keys = ["num", "str", "bool"]
    result = transformer.List2Dict(data, keys)
    expected = [
        {"num": 1, "str": "a", "bool": True},
        {"num": 2, "str": "b", "bool": False}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_list2dict_length_mismatch(transformer):
    """Test data length mismatch with keys"""
    data = [[1, 10, 100], [2, 20, 200]]
    keys = ["key1", "key2"]  # Fewer keys than data columns
    with pytest.raises(ValueError, match="Data length mismatch: 3 != 2"):
        transformer.List2Dict(data, keys)


def test_list2dict_invalid_data_type(transformer):
    """Test invalid data type (non-list data)"""
    data = "not a list"  # Invalid input
    keys = ["key1", "key2"]
    with pytest.raises(TypeError):  # Expect TypeError due to len(data)
        transformer.List2Dict(data, keys)


def test_list2dict_invalid_keys_type(transformer):
    """Test invalid keys type (non-list keys)"""
    data = [[1, 10], [2, 20]]
    keys = "not a list"  # Invalid input
    with pytest.raises(TypeError):  # Expect TypeError due to len(keys)
        transformer.List2Dict(data, keys)


def test_list2dict_with_ast(transformer):
    """Test List2Dict via AST call"""
    # Simulate AST call
    node = ast.Call(
        func=ast.Name(id="List2Dict", ctx=ast.Load()),
        args=[
            ast.Constant(value=[[1, 10], [2, 20]]),
            ast.Constant(value=["key1", "key2"])
        ],
        keywords=[]
    )
    result_node = transformer.visit_Call(node)
    result = result_node.value
    expected = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 20}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


# def test_list2dict_with_readexcel(transformer, setup_excel_file):
#     """Test List2Dict with ReadExcel output"""
#     # Use ReadExcel to get data
#     data = transformer.ReadExcel("test.xlsx", "Sheet1", ["A", "B"])
#     keys = ["A_col", "B_col"]
#     result = transformer.List2Dict(data, keys)
#     expected = [
#         {"A_col": 1, "B_col": 10},
#         {"A_col": 2, "B_col": 20},
#         {"A_col": 3, "B_col": 30},
#         {"A_col": 5, "B_col": 50}
#     ]
#     assert result == expected, f"Expected {expected}, but got {result}"
