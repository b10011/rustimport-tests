// rustimport:pyo3
//: [dependencies]
//: numpy = "0.21.0"

// Random test functions and classes

use std::thread;
use std::thread::JoinHandle;

use numpy::PyUntypedArrayMethods;
use pyo3::prelude::*;

#[pyfunction]
fn say_hello() {
    println!("Hello from testcrate, implemented in Rust!")
}

#[pyfunction]
fn multiply(a: i64, b: i64) -> i64 {
    return a * b;
}

#[pyfunction]
fn sum_vec(vec: numpy::PyReadwriteArray1<i64>) -> i64 {
    let dims = vec.shape();
    let mut result: i64 = 0;
    for i in 0 .. dims[0] {
        if let Some(val) = vec.get(i) {
            result += val;
        }
    }
    return result;
}

#[pyfunction]
fn sum_mat(mat: numpy::PyReadwriteArray2<u8>) -> u64 {
    let dims = mat.shape();
    let mut result: u64 = 0;
    for i in 0 .. dims[0] {
        for j in 0 .. dims[1] {
            if let Some(&val) = mat.get([i, j]) {
                result = result + u64::from(val);
            }
        }
    }
    return result;
}

#[pyclass]
struct TestClass {
    val: i64,
    handle: Option<JoinHandle<()>>
}

#[pymethods]
impl TestClass {
    #[new]
    fn new(value: i64) -> Self {
        let result = TestClass {
            val: value,
            handle: Some(thread::spawn(|| { println!("hello from thread") }))
        };

        return result;
    }

    fn add(self_: PyRef<'_, Self>, value: i64) -> i64 {
        self_.val + value
    }

    fn join(mut self_: PyRefMut<'_, Self>) -> Result<(), PyErr> {
        if let Some(handle) = self_.handle.take() {
            handle.join().unwrap();
        }

        Ok(())
    }
}
