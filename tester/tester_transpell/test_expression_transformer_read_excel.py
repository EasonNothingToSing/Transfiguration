import pytest
import pandas as pd
import os
import sys
sys.path.append(r'E:\APP\python_project\Transfiguration\Transfiguration')
from Transpell.expression_transformer import ExpressionTransformer


@pytest.fixture
def setup_excel_file(tmp_path):
    # 创建测试数据
    data = {
        "Sheet1": pd.DataFrame({
            "A": [1, 2, 3, None, 5],
            "B": [10, 20, 30, 40, 50],
            "C": ["x", "y", "z", "w", None]
        }),
        "Sheet2": pd.DataFrame({
            "X": [100, 200],
            "Y": [300, 400]
        })
    }
    
    # 保存到临时 Excel 文件
    excel_path = tmp_path / "test.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return str(excel_path)


@pytest.fixture
def transformer(tmp_path):
    # 使用临时目录作为 database 路径
    return ExpressionTransformer(database=str(tmp_path))


def test_read_excel_single_column(transformer, setup_excel_file):
    """测试读取单列数据"""
    result = transformer.ReadExcel("test.xlsx", "Sheet1", "A")
    
    # 预期结果：A 列非空值 [1, 2, 3, 5]
    expected = [[1.0], [2.0], [3.0], [5.0]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_read_excel_multiple_columns(transformer, setup_excel_file):
    """测试读取多列数据并验证排序"""
    result = transformer.ReadExcel("test.xlsx", "Sheet1", ["A", "B"])

    # 预期结果：按 A, B 顺序返回非空值 [[1, 10], [2, 20], [3, 30], [5, 50]]
    expected = [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0], [5.0, 50.0]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_read_excel_missing_values(transformer, setup_excel_file):
    """测试缺失值处理"""
    result = transformer.ReadExcel("test.xlsx", "Sheet1", ["A", "C"])
    
    # 预期结果：A 和 C 列非空且匹配的行 [[1, "x"], [2, "y"], [3, "z"]]
    expected = [[1.0, "x"], [2.0, "y"], [3.0, "z"]]
    assert result == expected, f"Expected {expected}, but got {result}"


def test_read_excel_invalid_column(transformer, setup_excel_file):
    """测试无效列名"""
    with pytest.raises(ValueError, match="None of the specified columns found"):
        transformer.ReadExcel("test.xlsx", "Sheet1", "InvalidColumn")


def test_read_excel_invalid_sheet(transformer, setup_excel_file):
    """测试无效 sheet 名"""
    with pytest.raises(ValueError, match="No sheet named"):
        transformer.ReadExcel("test.xlsx", "InvalidSheet", "A")


def test_read_excel_invalid_file(transformer):
    """测试文件不存在"""
    with pytest.raises(FileNotFoundError):
        transformer.ReadExcel("nonexistent.xlsx", "Sheet1", "A")


def test_read_excel_empty_colnames(transformer, setup_excel_file):
    """测试空列名列表"""
    with pytest.raises(ValueError, match="Column names must be provided"):
        transformer.ReadExcel("test.xlsx", "Sheet1", [])
