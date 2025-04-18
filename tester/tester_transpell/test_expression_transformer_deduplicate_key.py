import pytest
import pandas as pd
import ast
import os
import sys
sys.path.append(r'E:\APP\python_project\Transfiguration\Transfiguration')
from Transpell.expression_transformer import ExpressionTransformer


# Fixture: Create ExpressionTransformer instance
@pytest.fixture
def transformer(tmp_path):
    transformer = ExpressionTransformer(database=str(tmp_path))
    return transformer


# Fixture: Create test Excel file for ReadExcel integration
@pytest.fixture
def setup_excel_file(tmp_path):
    data = {
        "Sheet1": pd.DataFrame({
            "A": [1, 1, 2, 3, 1],
            "B": [10, 10, 20, 30, 40],
            "C": ["x", "y", "z", "w", "v"]
        })
    }
    excel_path = tmp_path / "test.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return str(excel_path)


def test_deduplicate_key_single_key(transformer):
    """Test deduplication based on a single key"""
    data = [
        {"key1": 1, "key2": 10},
        {"key1": 1, "key2": 20},
        {"key1": 2, "key2": 30}
    ]
    keys = ["key1"]
    result = transformer.DeduplicateKey(data, keys)
    expected = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 30}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_multiple_keys(transformer):
    """Test deduplication based on multiple keys"""
    data = [
        {"key1": 1, "key2": 10, "key3": "x"},
        {"key1": 1, "key2": 10, "key3": "y"},
        {"key1": 2, "key2": 20, "key3": "z"}
    ]
    keys = ["key1", "key2"]
    result = transformer.DeduplicateKey(data, keys)
    expected = [
        {"key1": 1, "key2": 10, "key3": "x"},
        {"key1": 2, "key2": 20, "key3": "z"}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_no_duplicates(transformer):
    """Test data with no duplicates"""
    data = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 20},
        {"key1": 3, "key2": 30}
    ]
    keys = ["key1"]
    result = transformer.DeduplicateKey(data, keys)
    expected = data
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_empty_data(transformer):
    """Test empty data input"""
    data = []
    keys = ["key1"]
    result = transformer.DeduplicateKey(data, keys)
    expected = []
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_single_dict(transformer):
    """Test single dictionary input"""
    data = [{"key1": 1, "key2": 10}]
    keys = ["key1"]
    result = transformer.DeduplicateKey(data, keys)
    expected = [{"key1": 1, "key2": 10}]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_empty_keys(transformer):
    """Test empty keys list (no deduplication)"""
    data = [
        {"key1": 1, "key2": 10},
        {"key1": 1, "key2": 10}
    ]
    keys = []
    result = transformer.DeduplicateKey(data, keys)
    expected = [{"key1": 1, "key2": 10}]  # Only first dict kept
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_invalid_data_type(transformer):
    """Test invalid data type (non-list)"""
    data = "not a list"
    keys = ["key1"]
    with pytest.raises(TypeError, match="Data must be a list"):
        transformer.DeduplicateKey(data, keys)


def test_deduplicate_key_invalid_dict_type(transformer):
    """Test invalid data elements (non-dictionary)"""
    data = [[1, 10], [2, 20]]
    keys = ["key1"]
    with pytest.raises(TypeError, match="Data must be a list of dictionaries"):
        transformer.DeduplicateKey(data, keys)


def test_deduplicate_key_invalid_keys_type(transformer):
    """Test invalid keys type (non-list)"""
    data = [{"key1": 1, "key2": 10}]
    keys = "not a list"
    with pytest.raises(TypeError, match="Keys must be a list"):
        transformer.DeduplicateKey(data, keys)


def test_deduplicate_key_missing_key(transformer):
    """Test missing key in dictionaries"""
    data = [
        {"key1": 1, "key2": 10},
        {"key1": 1}  # Missing key2
    ]
    keys = ["key1", "key2"]
    with pytest.raises(KeyError, match="'key2'"):
        transformer.DeduplicateKey(data, keys)


def test_deduplicate_key_with_list2dict(transformer):
    """Test integration with List2Dict"""
    data = [[1, 10], [1, 20], [2, 30]]
    keys = ["key1", "key2"]
    dict_data = transformer.List2Dict(data, keys)
    dedup_keys = ["key1"]
    result = transformer.DeduplicateKey(dict_data, dedup_keys)
    expected = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 30}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_with_readexcel(transformer, setup_excel_file):
    """Test integration with ReadExcel and List2Dict"""
    data = transformer.ReadExcel("test.xlsx", "Sheet1", ["A", "B"])
    dict_data = transformer.List2Dict(data, ["A_col", "B_col"])
    dedup_keys = ["A_col"]
    result = transformer.DeduplicateKey(dict_data, dedup_keys)
    expected = [
        {"A_col": 1, "B_col": 10},
        {"A_col": 2, "B_col": 20},
        {"A_col": 3, "B_col": 30}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_deduplicate_key_with_ast(transformer):
    """Test DeduplicateKey via AST call"""
    node = ast.Call(
        func=ast.Name(id="DeduplicateKey", ctx=ast.Load()),
        args=[
            ast.Constant(value=[
                {"key1": 1, "key2": 10},
                {"key1": 1, "key2": 20},
                {"key1": 2, "key2": 30}
            ]),
            ast.Constant(value=["key1"])
        ],
        keywords=[]
    )
    transformer._global_namepsace["DeduplicateKey"] = transformer.DeduplicateKey
    result_node = transformer.visit_Call(node)
    result = result_node.value
    expected = [
        {"key1": 1, "key2": 10},
        {"key1": 2, "key2": 30}
    ]
    assert result == expected, f"Expected {expected}, but got {result}"