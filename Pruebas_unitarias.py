import pytest
from Clase_vector_3D import Vector3D
import math

def test_vector3d_init():
    v = Vector3D(1, 2, 3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3

def test_vector3d_add():
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    v_sum = v1 + v2
    assert v_sum.x == 5
    assert v_sum.y == 7
    assert v_sum.z == 9

def test_vector3d_sub():
    v1 = Vector3D(5, 5, 5)
    v2 = Vector3D(1, 2, 3)
    v_sub = v1 - v2
    assert v_sub.x == 4
    assert v_sub.y == 3
    assert v_sub.z == 2

def test_vector3d_mul_scalar():
    v = Vector3D(1, 2, 3)
    v_mul = v * 2
    assert v_mul.x == 2
    assert v_mul.y == 4
    assert v_mul.z == 6

def test_vector3d_rmul_scalar():
    v = Vector3D(1, 2, 3)
    v_mul = 2 * v
    assert v_mul.x == 2
    assert v_mul.y == 4
    assert v_mul.z == 6

def test_vector3d_magnitude():
    v = Vector3D(3, 4, 0)
    assert v.magnitude() == 5.0
    v_zero = Vector3D(0, 0, 0)
    assert v_zero.magnitude() == 0.0
    v_neg = Vector3D(-1, -2, -2)
    assert v_neg.magnitude() == 3.0

def test_vector3d_normalize():
    v = Vector3D(3, 4, 0)
    normalized_v = v.normalize()
    assert normalized_v.x == 0.6
    assert normalized_v.y == 0.8
    assert normalized_v.z == 0.0
    assert abs(normalized_v.magnitude() - 1.0) < 1e-9

def test_vector3d_normalize_zero_vector():
    v_zero = Vector3D(0, 0, 0)
    normalized_v = v_zero.normalize()
    assert normalized_v.x == 0
    assert normalized_v.y == 0
    assert normalized_v.z == 0

def test_vector3d_str_repr():
    v = Vector3D(1.2345, 6.789, 10.1112)
    assert str(v) == "(1.23e+00, 6.79e+00, 1.01e+01)"
    assert repr(v) == "Vector3D(1.2345, 6.789, 10.1112)"

def test_vector3d_to_list():
    v = Vector3D(1, 2, 3)
    assert v.to_list() == [1, 2, 3]

def test_vector3d_from_list():
    v_list = [10.0, 20.0, 30.0]
    v = Vector3D.from_list(v_list)
    assert v.x == 10.0
    assert v.y == 20.0
    assert v.z == 30.0

def test_vector3d_from_list_invalid_length():
    with pytest.raises(ValueError, match="La lista debe contener 3 elementos para un Vector3D."):
        Vector3D.from_list([1, 2])
    with pytest.raises(ValueError, match="La lista debe contener 3 elementos para un Vector3D."):
        Vector3D.from_list([1, 2, 3, 4])